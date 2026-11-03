#!/usr/bin/env python3
"""Acquire selected stock photos, validate dimensions, then crop to local WebP.
Runs on GitHub Actions before any deployment. No stock API account/key required.
Missing photos fail the build; unrelated or synthetic photos are NEVER substituted.
"""
from __future__ import annotations
import argparse, hashlib, io, json, os, shutil, sys, tempfile, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from PIL import Image, ImageOps, UnidentifiedImageError
from photo_library import ROOT,SITE,records
MAX_BYTES=35*1024*1024
CACHE=ROOT/'.photo-cache'

def digest(b): return hashlib.sha256(b).hexdigest()

def fetch(url):
    request=Request(url,headers={'User-Agent':'Mozilla/5.0 Y2C-Website-Asset-Build/22','Accept':'image/jpeg,image/png,image/webp;q=0.9,*/*;q=0.5'})
    with urlopen(request,timeout=45) as r:
        if urlparse(r.url).hostname not in {'images.pexels.com','images.unsplash.com','unsplash.com'}:
            raise ValueError('Unexpected download destination')
        if not r.headers.get('Content-Type','').lower().startswith('image/'):
            raise ValueError('Source returned non-image data')
        b=r.read(MAX_BYTES+1)
    if len(b)>MAX_BYTES: raise ValueError('Source file exceeds 35 MB')
    return b

def raw_for(p,source_dir=None):
    CACHE.mkdir(exist_ok=True)
    cache=CACHE/(p['photo_id']+'.bin')
    if source_dir:
        for ext in ('.jpg','.jpeg','.png','.webp'):
            f=Path(source_dir)/(p['photo_id']+ext)
            if f.exists(): return f.read_bytes()
        raise ValueError('Original missing in supplied directory: '+p['photo_id'])
    if cache.exists(): return cache.read_bytes()
    urls=[p['download_url']]
    if p.get('preview_url'): urls.append(p['preview_url'])
    else: urls.append(p['download_url'].split('?')[0])
    error=None
    for attempt in range(3):
        for url in urls:
            try:
                b=fetch(url)
                with Image.open(io.BytesIO(b)) as im: im.verify()
                cache.write_bytes(b);return b
            except Exception as e: error=e
        if attempt<2: time.sleep(2**(attempt+1))
    raise RuntimeError(f'{p["key"]}: could not download selected original: {error}')

def convert(p,raw,dest):
    with Image.open(io.BytesIO(raw)) as original:
        im=ImageOps.exif_transpose(original).convert('RGB')
        ow,oh=im.size
        if min(ow,oh)<900: raise ValueError('Source resolution too low: '+p['key'])
        l,t,r,b=p['crop'];crop=(round(l*ow),round(t*oh),round(r*ow),round(b*oh))
        im=im.crop(crop)
        tw,th=p['target'];scale=min(1,im.width/tw,im.height/th)
        target=(round(tw*scale),round(th*scale))
        if target[0]<760 or target[1]<450: raise ValueError('Crop resolution too low: '+p['key'])
        im=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(.5,.5))
        im.save(dest,'WEBP',quality=87,method=6)
    return {'key':p['key'],'photo_id':p['photo_id'],'file':'assets/images/'+p['file'],
            'original_size':[ow,oh],'output_size':list(target),'source_sha256':digest(raw),
            'sha256':digest(dest.read_bytes()),'source_url':p['source_url']}

def verify():
    receipt=SITE/'data/photo-build.json'
    if not receipt.exists(): raise ValueError('No completed photo acquisition receipt. Run prepare_photos.py first.')
    result=json.loads(receipt.read_text())
    r={p['key']:p for p in result['photos']}
    for p in records():
        f=SITE/'assets/images'/p['file'];row=r.get(p['key'],{})
        if not f.is_file() or row.get('photo_id')!=p['photo_id'] or digest(f.read_bytes())!=row.get('sha256'):
            raise ValueError('Missing or changed photo: '+p['key'])
        with Image.open(f) as im: im.verify()
    print(f'OK: {len(r)} acquired and verified local photographs')
    return result

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');ap.add_argument('--source-dir')
    args=ap.parse_args(argv)
    if args.verify_only: verify();return
    stage=Path(tempfile.mkdtemp(prefix='y2c-photo-'))
    try:
        rows=[]
        for p in records():
            print('Preparing '+p['key'],flush=True)
            rows.append(convert(p,raw_for(p,args.source_dir),stage/p['file']))
        out=SITE/'assets/images';out.mkdir(parents=True,exist_ok=True)
        allowed={p['file'] for p in records()}
        for f in out.iterdir():
            if f.is_file() and f.name not in allowed and f.name!='README.md': f.unlink()
        for p in records(): os.replace(stage/p['file'],out/p['file'])
        (SITE/'data/photo-build.json').write_text(json.dumps({'version':22,'photos':rows},ensure_ascii=False,indent=2),encoding='utf-8')
        verify()
    finally: shutil.rmtree(stage,ignore_errors=True)
if __name__=='__main__':
    try: main()
    except Exception as e:
        print('PHOTO BUILD FAILED: '+str(e),file=sys.stderr)
        print('The previous deployed site is unchanged. Check the selected source URL; no unrelated replacement was used.',file=sys.stderr)
        sys.exit(1)
