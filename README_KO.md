# SHARE Lab 공식 홈페이지 — Version 5 (화이트 테마)

**현 상태:** 공개 전 미리보기용 사이트. 로고는 확정 전이므로 텍스트 `SHARE Lab.` 워드마크만 사용합니다. 전체 배경은 화이트이며, PPT의 연구 시각자료를 선정해 구성했습니다.

## 1. 홈페이지 살펴보기
ZIP을 해제한 뒤 `docs/index.html`을 브라우저에서 열어주세요. Home / People / Research / Publications / News / Contact 메뉴로 이동할 수 있습니다.

## 2. 현재 반영 사항 (Version 5)
- 학과: **Department of Civil and Environmental Engineering**, Dankook University
- 교수: WoongHee Jung / **Professor**
- Scholar: https://scholar.google.com/citations?user=pqIQHbcAAAAJ&hl=en
- Publications: 출판사/DOI 자료로 확인한 9개 논문을 `publications_curated.yml`에 등록했습니다. **전체 논문 목록을 완전히 검증한 것은 아니며**, 추가된 자동 항목은 OpenAlex 인덱스를 기준으로 합니다.
- PPT 연구 이미지: `assets/hero-*.webp`, `assets/research-*.webp`. 원본 출처 대응 관계는 `IMAGE_SOURCES.md`에 있습니다.
- 학생/뉴스/교수 사진은 예시나 빈칸으로 두었으며, 이메일 및 전화번호는 등록되어 있습니다.

## 3. 텍스트·구성원·뉴스 수정
- `content.yml` 에서 연구분야, 자기소개, People/News 변경
- `publications_curated.yml` 에서 직접 검증한 논문 추가/수정
- `python -m pip install pyyaml jinja2` 와 `python build.py` 로 `docs/*.html` 재생성
- `publications_auto.yml`은 OpenAlex 갱신 결과라 직접 편집하지 않는 편이 좋습니다. 잘못된 DOI는 `publications_exclude.txt`에 등록해 제외할 수 있습니다.

## 4. Google Scholar + 반자동 Publications 동기화
Google Scholar는 프로필 링크 버튼입니다. 논문 메타데이터는 **Google Scholar 직접 수집이 아니라 OpenAlex API**에서 받아옵니다.

1. https://openalex.org/settings/api 에 무료 회원가입 및 API 키 발급 후 이메일 인증
2. GitHub 저장소 **Settings → Secrets and variables → Actions → New repository secret**에서 이름 `OPENALEX_API_KEY`로 비밀 키 등록
3. GitHub Pages 배포 시 매주 월요일 오전 11:15 (한국시간) 논문을 확인하며, `Actions → Publish SHARE Lab Website → Run workflow`로 수동 갱신할 수도 있습니다.
4. 자동 스크립트는 확인된 논문 2편 이상의 DOI를 대조해 OpenAlex 저자 ID를 식별한 뒤 해당 저자 논문 목록을 받아옵니다. 확인 가능한 DOI가 있는 저널 논문만 추가하며 중복을 제거합니다.
5. Google Scholar와 OpenAlex의 등재 범위가 다르므로 일부 논문이 빠지거나 발행연도가 다를 수 있습니다. 중요한 논문은 `publications_curated.yml`에서 직접 관리하세요.

**중요:** GitHub Actions가 정기 실행돼도 OpenAlex 키가 등록되지 않았다면 자동 갱신은 실행되지 않습니다. 단, 홈페이지 자체는 기존 논문 목록으로 계속 배포됩니다.

## 5. GitHub Pages에 무료 공개
1. GitHub에 공용(Public) 저장소 `share-lab`을 만듭니다.
2. ZIP의 `SHARE_Lab_Website` 폴더 **안의 모든 내용**을 저장소 루트에 업로드합니다 (`.github` 포함).
3. **Settings → Pages → Build and deployment → Source: GitHub Actions** 설정.
4. **Actions → Publish SHARE Lab Website** 에서 워크플로를 실행하면 웹사이트가 배포됩니다.
5. 공식 로고를 결정하면 header/footer 영역의 텍스트 워드마크를 해당 SVG로 바꾸면 됩니다.

## 6. 공개 전에 확인할 것
- PPT 일부 그림은 외부 논문/기관 이미지일 수 있으므로 온라인 재사용 권한 및 출처 표기 확인
- 교수 사진, CV, News 추가 (이메일과 전화번호는 반영됨)
- 부서/건물 주소의 공식 영문 표기 확인
- DOI 목록의 누락 및 일부 게재연도 검토 (온라인 선공개/권호 발행연도 차이)

사이트는 완전히 정적이므로 GitHub Pages에서 무료로 호스팅할 수 있습니다. Python/Quarto가 웹 서버에 설치될 필요는 없습니다.

## Version 5 디자인 업데이트
- 전체 화이트 배경과 SHARE Lab 텍스트 워드마크 유지 (공식 로고 미확정)
- Home의 메인 비주얼과 Research Area 아이콘은 사용자가 선택한 파스텔 아이콘형 일러스트 시안을 바탕으로 재구성
- 자연재난 상세 페이지: 이전 메인에 있던 허리케인 이미지
- Infrastructure Resilience 상세 페이지: 제공 PPT `중앙대_심화심사_정웅희.pptx` 8번째 슬라이드의 산불/인프라 이미지
- 모든 링크/버튼의 화살표 제거, 홈 버튼명 Research / People
- Contact의 OUR FOCUS 영역 제거, Office 아래 wjung@dankook.ac.kr 및 031-8005-3483 추가

## 7. GitHub 웹사이트에서 직접 수정 (초보자용)
1. GitHub 저장소 화면에서 `content.yml` 파일을 선택합니다.
2. 오른쪽의 연필(Edit) 아이콘으로 내용을 수정합니다. 예: `professor.name`, 연구 설명, `people`, `news`.
3. `Commit changes`를 눌러 저장합니다. `main` 브랜치에 저장했다면 GitHub Actions가 사이트를 다시 만듭니다.
4. 이미지 교체: `assets/` 폴더에서 같은 파일명을 사용하는 `.webp`를 새 파일로 업로드합니다. 직접 만든 이미지에 저작권 문제가 없는지 확인하세요.
5. 색상 변경: `assets/styles.css`의 `:root`에 있는 색상 변수(예: `--navy`, `--blue`)를 수정하면 사이트 전체에 적용됩니다.
6. 변경 확인: `Actions → Publish SHARE Lab Website`가 성공한 뒤 실제 사이트를 새로고침합니다. CDN/브라우저 캐시 때문에 반영이 조금 늦을 수 있습니다.

**주의:** `docs/*.html`을 직접 수정하지 마세요. 이 파일들은 `build.py`가 매번 다시 생성하므로 나중에 덮어써집니다. 배포 초기 설정이 완료되어야 GitHub 편집만으로 자동 반영됩니다.
