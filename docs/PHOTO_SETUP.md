# V22 사진 자동 포함과 운영

## 왜 사진 파일이 바로 보이지 않나요?

제작 환경에서 외부 원본을 파일로 다운로드할 수 없었습니다. 따라서 배포용 소스에는 **정확한 원본 주소와 자동 취득 코드**를 넣었습니다. 원본의 화면을 확인해 선별했지만, 최종 다운로드 바이트와 크롭 결과를 이 환경에서 직접 검증한 것은 아닙니다.

빌드 전 HTML에는 같은 사진의 외부 URL이 연결되어 있습니다. GitHub Actions에서 다운로드가 성공한 뒤 HTML은 `assets/images/*.webp` 로컬 경로로 바뀝니다. 게시된 사이트는 성공 배포본의 로컬 사진을 사용합니다.

## 자동 작업

1. `data/photo_sources.json`의 11개 고유 사진 ID와 URL을 검증합니다.
2. HTTPS로 원본을 읽고 허용된 제공업체 호스트, 이미지 MIME, 최대 35MB, 실제 이미지 디코딩을 검사합니다.
3. 원본 짧은 변 900px 미만이면 거부합니다. 지정한 범위만 잘라 WebP로 저장하며 작은 원본을 확대하지 않습니다.
4. 11개가 모두 변환된 경우에만 사이트 이미지 폴더를 교체합니다. 기존 생성 이미지가 저장소에 남았더라도 새 배포물에서는 제거됩니다.
5. 출처 ID·해시·출력 크기를 `site/data/photo-build.json`에 기록합니다.
6. 각 페이지를 다시 만들고, 모든 사진이 사이트 내부에 있으며 해시가 맞는지 검사한 후 배포합니다.

자동 기술 검사는 사진이 무엇을 나타내는지 또는 법적 사용권을 독립적으로 판정하지 않습니다. 주제·카테고리 대응은 원본 선별 검토에 근거하며, 실제 필름·소재·상품 성능을 사진으로 확정하지 않습니다.

## 다운로드가 실패하면

Actions의 **Acquire and verify category photographs** 단계를 펼쳐 실패한 사진 키를 확인하세요. 같은 사진 URL을 재시도한 뒤에도 실패하면 새 배포를 멈춥니다. 소스가 없는데 아무 사진이나 대체하는 동작은 없습니다.

`PHOTO_REVIEW.html` 또는 `docs/IMAGE_MAP.md`의 원본 페이지를 확인하고, 해당 원본을 직접 저장한 뒤 아래 오프라인 취득 방법을 사용할 수 있습니다. 제공업체 주소가 변경됐다면 `data/photo_sources.json`의 동일 사진 URL을 수정합니다.

## 원본을 직접 보유한 경우

원본 파일명을 `photo_id.jpg` 또는 `.jpeg/.png/.webp`로 맞춰 별도 폴더에 보관합니다. 예: manifest에 적힌 photo_id를 그대로 사용합니다.

```sh
python -m pip install -r requirements.txt
python scripts/prepare_photos.py --source-dir /path/to/originals
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/build_seo_pages.py --excel data/website_content.xlsx --site site
python scripts/build_home.py
python scripts/build_photo_credits.py
python scripts/site_shell.py
python scripts/prepare_photos.py --verify-only
python scripts/package_release.py --output Y2C_V22_READY.zip
```

## 업데이트·보관

가격·본문 수정은 기존처럼 `data/website_content.xlsx`를 변경하면 됩니다. 사진 자체를 변경할 때는 `data/photo_sources.json`과 Excel의 `이미지맵`·`사진출처_V22`도 일치시켜야 합니다. 원본 사진·라이선스·실제 출처를 확인하지 않고 임의 URL을 넣지 마세요.

성공한 Actions의 **Y2C-V22-source-with-photos** 아티팩트는 사진 포함 소스입니다. 현재는 3일 보관하므로 별도로 다운로드해 보관하세요. 공개 DB 보고서는 이 소스 아카이브에 포함되지 않습니다.
