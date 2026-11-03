#!/usr/bin/env python3
"""Create a short-path complete source archive, excluding caches and credentials."""
import argparse,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED_DIRS={'.git','.photo-cache','__pycache__','qa','.pytest_cache','node_modules'}
EXCLUDED_SUFFIX={'.pyc','.woff','.woff2','.ttf','.otf','.ttc','.zip','.y2cbackup'}
def package(output):
 output=Path(output).resolve()
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for p in sorted(ROOT.rglob('*')):
   rel=p.relative_to(ROOT)
   if not p.is_file() or p.resolve()==output or any(x in EXCLUDED_DIRS for x in rel.parts) or p.suffix.lower() in EXCLUDED_SUFFIX or p.name.startswith('.env'): continue
   z.write(p,str(rel))
 print('Created '+str(output))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='Y2C_V22_READY.zip');args=ap.parse_args();package(args.output)
