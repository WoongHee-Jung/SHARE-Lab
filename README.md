# SHARE Lab 홈페이지 운영·관리 전체 안내서


> **대상:** 홈페이지를 GitHub Pages로 공개하고 GitHub 웹에서 직접 수정하는 관리자  
> **홈페이지 구성:** Home · People · Research · Publications · News · Contact

---

## 1. 먼저 알아둘 핵심 원리

SHARE Lab 홈페이지는 **정적 웹사이트**입니다. 화면의 내용은 여러 원본 파일을 `build.py`가 모아서 `docs/` 폴더의 완성된 HTML로 생성합니다.

```text
content.yml             연구실 정보, 교수·학생·연구분야·뉴스
publications_*.yml      논문 목록
       +
templates/*.html        각 페이지의 문구와 화면 구성
       +
assets/styles.css       색상, 글꼴, 크기, 간격, 모바일 레이아웃
assets/*.webp           사진과 연구 그림
       |
       v
python build.py         홈페이지 생성
       |
       v
docs/*.html             완성된 공개용 웹페이지
       |
       v
GitHub Actions          GitHub Pages에 자동 게시
```

**가장 중요한 원칙:** `docs/index.html`, `docs/people.html` 같은 결과물을 직접 고치지 마세요. 다음 자동 빌드에서 덮어써집니다. **원본**인 `content.yml`, `templates/`, `assets/`, 논문 YAML 파일을 수정하세요.

### 주요 파일 한눈에 보기

| 수정하려는 내용 | 수정 파일 | 비고 |
|---|---|---|
| 홈페이지 첫 화면 문구·카드 제목 | `templates/home.html` | `[01] HERO` ~ `[06] NEWS` 주석으로 구분 |
| 연구실 소개 본문·연구분야 설명 | `content.yml` | `lab.about`, `research` 등 |
| 교수 이름·직급·사진 경로 | `content.yml` | `professor` 아래 항목 |
| 학생·졸업생 정보, News | `content.yml` | `people`, `news` 아래 항목 |
| 전체 글씨 색상·글꼴·크기·버튼 | `assets/styles.css` | **맨 아래 ‘사용자 설정’**만 수정 |
| 메인/연구분야/프로필 그림 | `assets/` + 필요한 경우 참조 경로 | 아래 5장 참고 |
| People·Research 등 세부 페이지 레이아웃 | `templates/people.html`, `templates/research.html` 등 | HTML 수정 필요 |
| 상단 메뉴 순서·Footer 공통 레이아웃 | `build.py`의 `menu` / `templates/shell.html` | 메뉴명·구성 변경 시 |
| 직접 관리하는 논문 | `publications_curated.yml` | 검증된 논문 |
| OpenAlex가 추가한 논문 | `publications_auto.yml` | 자동 갱신 결과, 가급적 직접 수정하지 않기 |
| Contact 주소의 **본문** | `templates/contact.html` | 현재 코드는 주소가 직접 입력되어 있음 |
| Footer 주소 | `content.yml`의 `lab.address` | Contact와 별도이므로 두 곳 모두 확인 |

---

## 2. GitHub에서 내용을 수정하고 게시하는 기본 절차

SHARE Lab 저장소: <https://github.com/WoongHee-Jung/SHARE-Lab>

1. GitHub 로그인 → 해당 저장소의 **Code** 탭으로 이동합니다.
2. 수정할 파일(예: `content.yml`)을 클릭합니다.
3. 연필 아이콘 **Edit this file**을 클릭하고 내용을 수정합니다.
4. **Commit changes**를 눌러 `main` 브랜치에 저장합니다.
5. **Actions → Publish SHARE Lab Website**에서 실행 상태를 확인합니다.
6. 초록색 체크가 표시되면 공개 사이트 <https://woonghee-jung.github.io/SHARE-Lab/>을 새로고침해 확인합니다. 브라우저 캐시가 남으면 Windows에서 **Ctrl+F5**를 사용합니다.

**정상적인 자동 게시 조건:** `.github/workflows/pages.yml` 파일이 존재하고, **Settings → Pages → Build and deployment → Source가 `GitHub Actions`**로 설정되어 있어야 합니다. 이 조건이 충족되면 **Commit 후 Actions의 `Run workflow`를 매번 누를 필요가 없습니다.**

> GitHub Pages를 `Deploy from a branch` 방식으로 운영한다면 `content.yml`만 수정해서는 자동으로 HTML이 재생성되지 않습니다. 이 안내서의 자동 갱신은 `GitHub Actions` 방식을 기준으로 합니다.

---

## 3. 자주 바꾸는 문구·연구실 정보

### 3-1. Home의 큰 문구

`templates/home.html`을 열고 주석으로 구분된 부분을 찾습니다.

- `[01] HERO` — 맨 위 메인 문구·Research/People 버튼
- `[02] ABOUT` — *Building resilient systems under uncertainty.* 제목
- `[03] RESEARCH` — 연구분야 카드 영역 제목과 배열 구조
- `[04] PEOPLE` — *Research is a team endeavor.* 문구
- `[05] PUBLICATIONS` — *New ideas. Shared knowledge.* 문구
- `[06] NEWS` — News 제목·빈 상태의 안내문

예를 들어 About 제목은 다음처럼 작성되어 있습니다.

```html
<h2 id="about-title" class="about-title">
  Building <span>resilient systems</span><br>
  under <span>uncertainty</span>.
</h2>
```

- `<span>...</span>`으로 감싼 단어만 강조색으로 표시됩니다.
- `<br>`은 줄바꿈입니다.
- 글씨 색상·크기를 바꾸려면 HTML이 아니라 `assets/styles.css` 맨 아래 설정을 수정하세요.

### 3-2. 연구실 소개 본문

`content.yml`의 `lab.about`을 수정합니다.

```yaml
lab:
  about: >-
    SHARE Lab explores the behavior and performance of built infrastructure
    under uncertain environmental loads and natural hazards.
```

`templates/home.html`에 있는 `{{ lab.about }}`가 이 값을 가져와 표시합니다. 반면 Hero에 직접 적혀 있는 제목과 About의 키워드 태그는 **현재 `templates/home.html`에서 수정**해야 합니다. 모든 텍스트가 `content.yml`로 연결되어 있지는 않습니다.

### 3-3. 교수 이름·직급·프로필 사진

`content.yml`의 `professor` 부분을 수정합니다.

```yaml
professor:
  name: WoongHee Jung
  title: Assistant Professor
  role: Professor
  photo: assets/professor.jpg
```

- `title`: 이름 위에 표시되는 `ASSISTANT PROFESSOR` 등 직급
- `role`: 관리용 정보이며 위의 작은 직급 표시를 바꾸는 항목은 **`title`**입니다.
- `photo`: 업로드한 파일의 상대경로. 사진이 없으면 빈 문자열 `''`로 둘 수 있습니다.
- **People 페이지의 큰 ‘Professor’ 섹션 제목**은 `templates/people.html`에 별도로 적혀 있어 `title`을 바꿔도 그대로 유지됩니다.

YAML은 들여쓰기에 민감하므로 **탭 대신 공백**을 사용하고, 기존 항목의 계층과 들여쓰기를 유지하세요.

### 3-4. Research 분야 추가·수정

`content.yml`의 `research` 아래에 항목을 수정합니다.

```yaml
research:
  - slug: uq
    title: Uncertainty Quantification
    summary: Quantifying uncertainties in hazards and structural performance.
    topics:
      - Probabilistic modeling and uncertainty propagation
      - Structural reliability and risk assessment
```

- `title`과 `summary`: Home 카드와 Research 상세 페이지에 모두 사용됩니다.
- `topics`: Research 상세 페이지의 목록입니다.
- `slug`: 이미지 파일명(`research-uq.webp`)과 페이지 내 링크(`research.html#uq`)에도 사용되므로 **기존 값은 함부로 변경하지 않는 편이 안전**합니다.
- `detail_image`가 있다면 Research **상세 페이지**에서 해당 이미지 파일을 우선 사용합니다(아래 5장 참고).

### 3-5. 연구실 구성원 추가

먼저 인물 사진을 `assets/`에 업로드합니다. 그런 다음 `content.yml`의 적절한 그룹에 정보를 추가합니다.

```yaml
people:
  graduate_students:
    - name: Student Name
      role: M.S. Student
      research: Structural Reliability
      photo: assets/student-name.jpg
      initials: SN
  undergraduate_researchers: []
  alumni: []
```

위 이름은 **예시**입니다. 학생이 늘어나면 목록 안에 같은 형식의 항목을 추가하면 됩니다. 아직 학생이 없다면 `[]`로 둡니다. 학생 공개 프로필은 당사자 동의를 받은 뒤 올리는 것이 좋습니다.

### 3-6. News 추가

`content.yml`의 `news`에 다음처럼 추가합니다.

```yaml
news:
  - date: '2026-10-22'
    title: New research announcement
    summary: A short description of the laboratory update.
    url: https://example.com
```

- `url`은 실제 연결할 소식이 없으면 `''`로 설정할 수 있습니다.
- Home에는 **앞의 최대 3개**가 표시됩니다. 현재 코드는 날짜를 기준으로 자동 정렬하지 않으므로 **최신 소식을 맨 위에 입력**하세요.

### 3-7. Contact와 Footer

- 연구실 이메일·전화번호의 표시 내용: `content.yml` → `lab.email`, `lab.phone`
- **Footer**의 주소: `content.yml` → `lab.address`
- **Contact 본문**의 주소: 현재 `templates/contact.html`에 직접 적힌 Office 문구
- 전화번호 자체를 변경한다면 화면에 보이는 `lab.phone`뿐 아니라 `templates/contact.html`과 `templates/shell.html`의 **`tel:` 링크**도 새 번호로 바꿔야 합니다.

**예시 권장 주소**: `Room 214, College of Engineering - Building 2, 152 Jukjeon-ro, Suji-gu, Yongin-si, Gyeonggi-do, 16890, Republic of Korea`. 공개 전 단국대학교 공식 표기를 확인하세요.

---

## 4. 색상·글씨체·간격 수정 (`styles.css`)

`assets/styles.css` 파일을 열고 **맨 아래**에 있는 아래 주석을 찾습니다.

```css
/* 사용자 설정 (직접 수정하는 곳) — FONT / TEXT COLOR / BUTTON / BACKGROUND */
```

이 영역에서 다음 설정값을 수정할 수 있습니다.

| 수정 항목 | 변수 이름 | 예시 |
|---|---|---|
| 제목 색상 | `--color-heading` | `#153758` |
| 기본 본문 색상 | `--color-body` | `#172C3C` |
| 보조 설명 색상 | `--color-muted` | `#687988` |
| 파란 강조·링크 | `--color-accent` | `#206A9E` |
| 상단 메뉴 색상 | `--color-nav` | `#536676` |
| 배경 색상 | `--color-background` | `#FFFFFF` |
| 버튼 배경·글씨 | `--color-button`, `--color-button-text` | HEX 색상 |
| 일반/제목 글꼴 | `--font-body`, `--font-heading` | `DM Sans`, `Manrope` |
| About 제목 크기 | `--font-about-title-size` | `clamp(1.8rem, 2.65vw, 2.4rem)` |
| About 좌우 간격 | `--about-column-gap` | `32px` |
| 카드 모서리 | `--card-radius` | `12px` |

**예시:** 강조 색을 바꾸려면 `--color-accent: #206A9E;`의 HEX 코드만 바꾸고 Commit합니다.

**중요:** Version 7~8에서는 원래 `styles.css`와 `theme.css`를 **`styles.css` 한 파일로 통합**했습니다. 현재 `build.py`의 `<head>`에는 `assets/styles.css`만 연결되어 있어야 하며, `theme.css` 연결이 남아 있다면 이전 스타일이 덮어쓸 수 있으니 확인하세요.

글꼴 이름을 변경할 때는 변경할 폰트가 브라우저에서 로드될 수 있어야 합니다. 현재 Google Fonts에서 `DM Sans`와 `Manrope`를 가져오는 설정은 `styles.css` 맨 위에 있습니다.

---

## 5. 사진·연구 그림 교체하기

### 5-1. 새 이미지 올리기

1. 저장소 **Code → assets** 폴더를 엽니다.
2. **Add file → Upload files**로 새 이미지(`.jpg`, `.png`, `.webp` 등)를 올립니다.
3. **Commit changes**를 누릅니다.
4. 이미지 파일명을 바꾸었다면 **해당 이미지를 참조하는 원본 파일의 경로**도 수정합니다.

**권장:** 기존 이미지를 무리하게 덮어쓰기보다 이름이 다른 파일로 올려 참조 경로를 바꾸면 작업 전후를 비교하기 쉽습니다. GitHub의 파일명은 대소문자를 구분합니다.

### 5-2. 이미지별 경로

| 이미지 | 기본 파일 | 경로 변경 시 수정 위치 |
|---|---|---|
| 메인 Hero 일러스트 | `assets/hero-illustration.webp` | `templates/home.html`의 `src` |
| UQ 카드 | `assets/research-uq.webp` | 파일명 규칙은 `templates/home.html`의 `research-{{ item.slug }}.webp` |
| Natural Hazards 카드 | `assets/research-hazards.webp` | 동일 |
| Wind Engineering 카드 | `assets/research-wind.webp` | 동일 |
| Structural Engineering 카드 | `assets/research-structural.webp` | 동일 |
| Infrastructure Resilience 카드 | `assets/research-resilience.webp` | 동일 |
| Natural Hazards 상세 이미지 | `assets/research-detail-hazards.webp` | `content.yml`의 해당 `detail_image` |
| Infrastructure Resilience 상세 이미지 | `assets/research-detail-resilience.webp` | `content.yml`의 해당 `detail_image` |
| 교수 사진 | 예: `assets/professor.jpg` | `content.yml`의 `professor.photo` |

**카드 이미지와 상세 이미지가 서로 다를 수 있습니다.** 예를 들어 상세 페이지의 그림만 바꾸고 싶다면 Research 항목의 `detail_image`를 수정하면 됩니다.

### 5-3. 모바일에서 교수 사진이 잘리는 경우

Version 6 이후 CSS에는 `.people-panel > .person-visual img`의 `object-fit: contain` 및 모바일 크기 조절 규칙이 포함되어 있습니다. `cover`가 아니라 **`contain`**을 쓰면 사진 전체가 보이되 여백이 남을 수 있습니다. 사진 원본 비율이 특이할 경우 이미지 자체의 여백을 조정하세요.

### 5-4. 이미지 공개 시 주의

저장소가 **Public**이면 `assets`에 올린 원본 파일도 누구나 볼 수 있습니다. 공개 홈페이지에 표시되는 사진은 방문자가 저장할 수도 있습니다. 교수·학생의 공개용 사진만 올리고, 고해상도 원본, 비공개 연구 데이터, 개인 문서, API 키 등은 저장소에 올리지 마세요. 사진의 위치정보(EXIF)도 제거하는 편이 좋습니다.

---

## 6. Publications와 Google Scholar 관리

Google Scholar 버튼은 `content.yml`의 `professor.scholar_url`을 엽니다. **Google Scholar 논문 목록을 직접 복제하는 기능은 아닙니다.** 홈페이지의 논문 목록은 다음 두 파일을 바탕으로 생성됩니다.

- `publications_curated.yml`: 직접 확인해 등록한 논문(제목, 저자, 저널, 발행연도, DOI). 주요 논문은 여기에서 관리합니다.
- `publications_auto.yml`: OpenAlex 동기화 결과. 가능하면 자동 관리 상태로 유지합니다.

`build.py`는 두 목록과 `content.yml`의 `publications` 항목을 합쳐 DOI(없으면 제목)를 기준으로 중복을 제거하고 연도 순으로 표시합니다.

### 6-1. 논문 직접 추가하기

`publications_curated.yml`의 `publications:` 아래에 항목을 추가합니다.

```yaml
publications:
  - year: 2026
    title: 'Example research paper title'
    authors: 'WoongHee Jung, Coauthor Name'
    venue: 'Example Journal'
    doi: 10.xxxx/example
```

위 예시는 실제 논문이 아닙니다. DOI는 `https://doi.org/`를 붙이지 않은 값으로 적는 편이 일관적입니다.

### 6-2. OpenAlex 반자동 갱신 활성화

현재 `.github/workflows/pages.yml`은 매주 **월요일 오전 11:15(한국시간)**경 갱신을 시도하도록 설정되어 있습니다(실제 실행은 지연될 수 있음).

1. OpenAlex에서 API 키를 발급받습니다.
2. GitHub 저장소 → **Settings → Secrets and variables → Actions → Secrets → New repository secret**에서 이름을 `OPENALEX_API_KEY`로 등록합니다.
3. **Actions → Publish SHARE Lab Website → Run workflow**를 누르면 수동으로 논문 갱신을 시도할 수 있습니다.
4. 스크립트는 확인된 DOI 논문을 이용해 저자 ID를 식별하고 새로운 저널 논문 메타데이터를 추가합니다. 저자 판별이나 API 호출이 실패하면 기존 논문 목록을 유지합니다.
5. 잘못 수집된 논문은 `publications_exclude.txt`에 DOI를 추가해 제외할 수 있습니다.

**참고:** 일반적인 `content.yml` 수정으로 실행되는 배포는 홈페이지를 다시 만드는 작업이고, OpenAlex 조회는 예약 실행 또는 `Run workflow`에서만 수행됩니다. Google Scholar 인용 수는 이 사이트에 동기화되지 않습니다.

---

## 7. 자동 배포 설정과 확인

필요한 파일: `.github/workflows/pages.yml`

1. **Settings → Pages → Build and deployment → Source = GitHub Actions**로 설정합니다.
2. GitHub 저장소에 위 워크플로 파일이 있고 `main` 브랜치에 수정 내용이 Commit되면 자동 실행됩니다.
3. 워크플로에서 `pyyaml`, `jinja2`를 설치한 뒤 `python build.py`를 실행합니다.
4. 완성된 `docs/` 폴더를 GitHub Pages로 배포합니다.
5. **Actions → Publish SHARE Lab Website**에서 마지막 실행의 상태를 확인합니다.

정상적으로 설정했다면 Home·People·Research·Publications·News·Contact 중 어느 페이지의 원본 파일을 수정하더라도 **별도의 HTML 업로드 없이 업데이트됩니다.**

### 수동 실행이 필요한 때

- OpenAlex 논문 목록을 지금 확인하고 싶을 때
- 오류 수정 후 자동 실행을 다시 시도하고 싶을 때
- GitHub Actions에서 직접 재배포를 시작하고 싶을 때

**평소에는 `Commit changes`만으로 충분합니다.**

---

## 8. 로컬 PC에서 미리보기·생성하기 (선택)

GitHub 웹에서만 편집한다면 이 단계는 생략해도 됩니다. PC에서 ZIP 파일의 원본을 직접 수정하는 경우:

```bash
python -m pip install pyyaml jinja2
python build.py
```

그다음 `docs/index.html`을 브라우저에서 엽니다. 이 버전은 `build.py`에서 정적 HTML과 Quarto 호환 `.qmd`를 함께 생성하지만, **실제 GitHub Pages 게시에는 Quarto 설치가 필수는 아닙니다.**

로컬에서 수정한 내용은 GitHub 저장소에 Commit해야 온라인 홈페이지에 반영됩니다.

---

## 9. 자주 발생하는 오류와 해결

| 증상 | 확인할 것 |
|---|---|
| Commit했지만 홈페이지가 바뀌지 않음 | Actions 실행·성공 여부, Pages Source 설정, `main` 브랜치 확인. 캐시 새로고침(Ctrl+F5) |
| About 문구를 바꿨는데 반영 안 됨 | `templates/home.html`을 수정했는지 확인. `docs/index.html`을 직접 수정하지 않았는지 확인 |
| 색상이 예상과 다름 | `assets/styles.css` 맨 아래 사용자 설정 및 `build.py`에 `theme.css` 연결이 남아 있는지 확인 |
| 사진이 안 나옴 | 파일이 `assets/`에 있는지, `content.yml`의 `photo` 경로와 대소문자가 맞는지 확인 |
| 모바일 사진 위아래가 잘림 | `object-fit: contain` 규칙이 적용되었는지 확인. 원본 사진 비율 확인 |
| Research 카드와 상세 이미지가 다름 | `detail_image`가 설정돼 있는지 확인(설정됐다면 의도된 차이일 수 있음) |
| Contact 주소만 예전 주소 | `content.yml` 외에 `templates/contact.html`의 Office 문구 수정 필요 |
| Footer 주소만 예전 주소 | `content.yml`의 `lab.address` 확인 |
| 논문이 새로 추가되지 않음 | OpenAlex API 키, 예약·수동 실행 여부, Actions 로그, curated 항목 검토 |
| YAML을 수정한 뒤 빌드 오류 | 공백 들여쓰기·따옴표·콜론(`:`) 위치 확인 |
| 버튼을 눌러도 엉뚱한 곳으로 이동 | `templates/*.html`의 `href` 값 확인 |

**문제가 생겼다면:** `Actions` 탭 → 실패한 실행(빨간 X) → 실패 단계의 메시지를 확인하고, 마지막으로 정상 작동했던 Commit과 비교해 수정하세요.

---

## 10. 관리 권장사항과 체크리스트

- **GitHub의 최신 파일을 기준으로 작업:** 과거 ZIP으로 전체 덮어쓰기를 하지 않기
- **Commit 메시지 간단히 쓰기:** 예: `Update professor photo`, `Revise homepage intro`, `Change theme colors`
- **큰 변경 전 백업:** 특히 `styles.css`, `templates/home.html`, `content.yml`
- **공개 자료만 업로드:** 초상권·외부 이미지 재사용 권한·미공개 연구자료 확인
- **연구실 학생 증가 시:** `people`에 프로필만 추가하고 공개 동의 받기
- **논문 관리:** 중요한 신규 논문은 DOI·저널명·게재연도를 확인하여 수동 보완
- **로고 확정 시:** 현재의 `SHARE Lab.` 텍스트 워드마크는 `templates/shell.html`에서 관리

### 일상 작업 최소 절차

**문구 수정:** `content.yml` 또는 `templates/home.html` → Commit → Actions 성공 확인  
**디자인 수정:** `assets/styles.css` 맨 아래 사용자 설정 → Commit → 새로고침  
**사진 추가:** `assets/` 업로드 → 필요시 `content.yml` 경로 입력 → Commit  
**새 논문:** `publications_curated.yml` 추가 → Commit  
**공통 메뉴·Footer 변경:** `templates/shell.html` 또는 `build.py` → Commit

---

## 11. 이번 안내서에 대한 참고

- 이 안내서는 **Version 8에 포함된 실제 원본 코드**(`build.py`, `content.yml`, `templates/`, `styles.css`, `pages.yml`, 논문 갱신 스크립트)를 확인해 작성했습니다.
- GitHub에 별도로 수정해 둔 **가장 최신** 사진, 직급, 연락처, 문구가 ZIP과 다를 수 있습니다. 따라서 **실제 GitHub 저장소의 최신 상태를 우선**하세요.
- 안내서 파일 자체(`README_KO.md`)는 홈페이지 동작을 결정하지 않습니다. **원하면 저장소 최상위에 올려서 팀의 운영 문서로 보관**하면 됩니다.
