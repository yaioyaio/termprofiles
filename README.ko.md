# termprofiles

[![PyPI](https://img.shields.io/pypi/v/termprofiles?label=PyPI)](https://pypi.org/project/termprofiles/)
![Python](https://img.shields.io/pypi/pyversions/termprofiles)
![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-blue)
![Terminal](https://img.shields.io/badge/for-iTerm2%20%7C%20Windows%20Terminal-8A2BE2)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- GitHub Actions 배지는 repo 경로 바꿔서 사용하세요 -->
<!-- [![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml) -->

> macOS(iTerm2)와 Windows(Windows Terminal)에서 JSON을 손으로 수정할 필요 없이 프로젝트별 터미널 프로필을 만들어 줍니다.
>
> 키워드: iTerm2 동적 프로필, Windows Terminal 프래그먼트, 프로젝트별 ZDOTDIR, 개발 자동화 CLI

TermProfiles는 프로젝트마다 별도의 JSON 파일을 생성하여 안전하게 추가/삭제할 수 있게 해 줍니다. macOS에서는 각 프로젝트마다 전용 `ZDOTDIR`(히스토리 + `.zshrc`)가 만들어지고, Windows 사용자는 깔끔한 Windows Terminal 프래그먼트를 얻게 됩니다. 모든 파일은 홈 디렉터리 안에만 생성됩니다.

## 목차

- [개요](#개요)
- [지원 플랫폼 및 요구 사항](#지원-플랫폼-및-요구-사항)
- [설치](#설치)
- [빠른 시작](#빠른-시작)
- [명령어 안내](#명령어-안내)
- [프로필 구조](#프로필-구조)
- [macOS 상세 정보](#macos-상세-정보)
- [Windows 상세 정보](#windows-상세-정보)
- [설정 및 환경 변수](#설정-및-환경-변수)
- [활용 예시](#활용-예시)
- [문제 해결 & FAQ](#문제-해결--faq)
- [제거하기](#제거하기)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 개요

- **프로젝트 단위 프로필:** 디렉터리마다 macOS용 동적 프로필 또는 Windows용 프래그먼트를 생성합니다.
- **안전한 JSON 처리:** UTF-8로 원자적(atomic) 저장을 사용하여 파일 손상을 방지합니다.
- **tmux 불필요:** 원하는 셸로 프로젝트 디렉터리에 바로 진입합니다.
- **간단한 정리:** `termprofiles remove`로 생성된 JSON(및 macOS의 경우 ZDOTDIR)을 쉽게 삭제합니다.
- **확인 가능:** `termprofiles list`로 어떤 프로필이 생성되었는지 즉시 확인합니다.

## 지원 플랫폼 및 요구 사항

**macOS**

- macOS 11 이상 권장.
- iTerm2에서 Dynamic Profiles 활성화.
- 기본 셸은 `/bin/zsh`이며 생성된 `.zshrc`로 자유롭게 커스터마이즈할 수 있습니다.

**Windows**

- Windows 10 19041 이상 또는 Windows 11, Windows Terminal 1.16 이상 권장.
- 기본 PowerShell 설치 필요. 선택 사항: Git Bash, CMD, WSL.

## 설치

TermProfiles는 [PyPI](https://pypi.org/project/termprofiles/)에 게시되어 있으며 아래 방법 중 하나로 설치할 수 있습니다.

### pipx 사용(추천)

`pipx`는 패키지를 격리된 가상환경에 설치하고 실행 파일을 PATH에 추가합니다.

```bash
# macOS (Homebrew 사용 시)
brew install pipx
pipx ensurepath
exec $SHELL

# macOS 또는 Windows
pipx install termprofiles
# 업데이트
pipx upgrade termprofiles
```

설치 확인:

```bash
termprofiles --help
```

### pip 사용

가상환경 또는 사용자 사이트에 설치하고 싶다면:

```bash
python -m venv .venv  # 선택 사항
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install termprofiles
```

### 소스에서 설치

```bash
git clone https://github.com/yaioyaio/termprofiles.git
cd termprofiles
pipx install .  # 또는 python -m pip install .
```

## 빠른 시작

### macOS (iTerm2)

1. `termprofiles add /path/to/project` 실행
2. iTerm2를 다시 열거나 `Profiles → Other Actions → Reload All Profiles` 선택
3. `proj-<slug>` 이름의 새 프로필 실행
4. `~/.zsh-profiles/<slug>/` 기반의 독립된 `.zshrc`와 히스토리를 사용

예시:

```bash
termprofiles add ~/dev/sample-app
```

`Added: proj-sample-app` 출력과 함께 iTerm2 DynamicProfiles 디렉터리에 `dp-sample-app.json`이 생성됩니다.

### Windows (Windows Terminal)

1. 관리자 권한이 아닌 일반 PowerShell을 실행합니다.
2. `termprofiles add "C:\\src\\sample-app"` 명령 실행
3. Windows Terminal을 닫았다가 다시 실행하거나 `wt.exe`를 다시 실행
4. 드롭다운에서 `proj-sample-app` 프로필 선택

기본적으로 PowerShell을 사용하며 시작 디렉터리는 지정한 프로젝트 경로입니다.

## 명령어 안내

### `termprofiles add <dir> [<dir> ...]`

하나 이상의 프로젝트 디렉터리에 대한 프로필을 생성합니다.

macOS 옵션:

- `--parent-guid GUID` — 기존 iTerm2 프로필에서 UI 설정을 상속합니다.
- `--parent-name NAME` — 이름(대소문자 무시)으로 프로필을 찾아 GUID를 자동으로 사용합니다.

Windows 옵션:

- `--color-scheme NAME` — 기존 Windows Terminal 색상 테마를 적용합니다.
- `--shell TYPE` — `powershell`(기본), `cmd`, `git-bash`, `wsl`, `wsl:<alias>` 중 선택.
- `--wsl-distro NAME` — WSL 사용 시 실행할 배포판(기본 `Ubuntu`).
- `--wsl-zdotdir PATH` — WSL에서 `zsh` 실행 전에 `ZDOTDIR`을 내보냅니다.

### `termprofiles remove <target> [<target> ...]`

생성된 프로필을 삭제합니다. `target`은 원본 디렉터리나 슬러그 중 어느 것이든 가능합니다.

- macOS: `--keep-zdotdir`로 `~/.zsh-profiles/<slug>`를 유지할 수 있습니다.
- Windows: 프래그먼트 JSON만 삭제합니다.

### `termprofiles list`

생성된 JSON 파일을 읽어 프로필과 작업 디렉터리를 표시합니다.

### `termprofiles doctor`

배포 전에 필요한 항목을 점검합니다. 현재 Git 브랜치가 업스트림을 추적하는지, `origin` 원격이 SSH인지 확인하고 PyPI 업로드 준비(`twine`, 환경 변수, `~/.pypirc`, `dist/` 빌드 산출물)를 검사합니다.

### `termprofiles parents` _(macOS 전용)_

`~/Library/Preferences/com.googlecode.iterm2.plist`에서 감지한 iTerm2 프로필과 GUID를 나열합니다.

### `termprofiles setopt` _(macOS 전용)_

현재 프로젝트의 `.zshrc`에 적용할 추천 `setopt` 옵션(`NO_SHARE_HISTORY`, `SHARE_HISTORY`, `EXTENDED_HISTORY`, `INC_APPEND_HISTORY` 등)을 인터랙티브하게 켜고 끄거나, `--enable SHARE_HISTORY --disable NO_SHARE_HISTORY`와 같이 비대화식으로 적용할 수 있습니다. 변경 사항은 원자적으로 저장되며, 동일한 프로필을 사용하는 모든 iTerm 탭에서 즉시 `source` 됩니다.

### `termprofiles prompt on|off|toggle` _(macOS 전용)_

기본 제공 프롬프트(`[%F{cyan}<slug>%f] user@host path %#`)를 켜거나 끄거나 토글합니다. 켜면 부모 프로필에서 내려온 프롬프트 대신 프로젝트 전용 프롬프트가 적용되고, 실행 중인 탭에도 즉시 반영됩니다.

### `termprofiles new` _(macOS 전용)_

현재 프로젝트 프로필을 사용하는 iTerm 새 창을 엽니다 (`--tab`을 주면 같은 창에 새 탭으로 열 수 있습니다).

## 프로필 구조

- **슬러그 생성:** 디렉터리 이름을 소문자로 변환하고, 공백은 `-`, 영문/숫자/`_.-` 이외 문자는 제거합니다. (예: `/Users/Alex/My App` → `my-app`)
- **파일 이름:**
  - macOS: `~/Library/Application Support/iTerm2/DynamicProfiles/dp-<slug>.json`
  - Windows: `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles\proj-<slug>.json`
- **멱등성:** JSON 파일이 이미 존재하면 `Skip (exists)`를 출력하고 기존 설정을 유지합니다.

## macOS 상세 정보

- 각 프로젝트마다 `~/.zsh-profiles/<slug>/` 디렉터리가 생성되고, 그 안에 `.zshrc`와 `.zsh_history`가 포함됩니다.
- 슬러그 하나가 곧 세션의 범위이며, `ZDOTDIR=~/.zsh-profiles/<slug>`로 강제됩니다. 같은 슬러그를 쓰는 모든 터미널은 히스토리와 설정을 공유하지만 다른 슬러그와는 완전히 분리됩니다.
- `.zshrc`는 `~/.zshrc.common`이 존재할 경우 자동으로 소스하여 공통 설정을 공유할 수 있습니다.
- 히스토리 크기는 `HISTSIZE` 및 `SAVEHIST` 50,000으로 넉넉하게 설정됩니다. 기본적으로 `setopt NO_SHARE_HISTORY`가 적용되어 실시간 히스토리 동기화를 끄고, 다른 프로젝트에서 명령이 섞이지 않게 합니다. 실시간 공유가 필요하면 생성된 `.zshrc`에서 `NO_SHARE_HISTORY`를 제거하고 `setopt SHARE_HISTORY`로 바꾸면 됩니다.
- 실행 명령어: `/usr/bin/env ZDOTDIR="<project_zdotdir>" /bin/zsh -l`
- `--isolate-cli codex,my-cli`처럼 지정하면 `~/.zsh-profiles/<slug>/bin/`에 래퍼가 생성되고, 해당 CLI는 프로젝트 전용 HOME/XDG 디렉터리를 사용합니다.
- 부모 프로필을 설정하면 색상, 폰트 등 UI 구성을 그대로 상속 받을 수 있습니다.
- `termprofiles setopt` (또는 `termprofiles setopt --enable SHARE_HISTORY --disable NO_SHARE_HISTORY`)로 `NO_SHARE_HISTORY` ↔ `SHARE_HISTORY`, `HIST_IGNORE_SPACE` 같은 옵션을 간단히 토글하면 결과가 즉시 모든 탭에 적용됩니다.
- `termprofiles prompt on|off|toggle`로 프로젝트 전용 프롬프트를 손쉽게 켜고 끌 수 있습니다.

### codex 세션 공유 안내

- `termprofiles add <dir> --isolate-cli codex`로 래퍼를 만들면 프로젝트 슬러그별로 `~/.zsh-profiles/<slug>/cli-homes/codex` 디렉터리가 생성되고, 같은 프로파일을 사용하는 모든 터미널에서 동일한 codex 홈/히스토리를 바라봅니다.
- codex CLI는 프로세스가 종료될 때 히스토리 파일을 덮어쓰는 방식이라, 두 터미널에서 동시에 실행 중인 명령은 즉시 동기화되지 않습니다. 한쪽에서 `codex`를 종료하거나 저장을 트리거하는 명령(`codex history` 등)을 실행하면 다른 터미널에서도 최신 히스토리를 확인할 수 있습니다.
- codex 업데이트는 PATH에 있는 실제 실행 파일을 교체하는 것만으로 적용됩니다. `pipx upgrade codex`처럼 바이너리가 제자리에 교체되면 모든 프로파일이 자동으로 새 버전을 사용합니다. 래퍼가 가리키는 경로가 바뀌었을 때만 `termprofiles add <dir> --isolate-cli codex`를 다시 실행해 덮어쓰면 됩니다.

## Windows 상세 정보

- 프래그먼트 JSON은 Windows Terminal 프래그먼트 사양을 따르며 실행 시 자동으로 로드됩니다.
- `--shell wsl`은 `wsl.exe -d <distro>`를 실행하고, `--wsl-zdotdir`를 함께 사용하면 `bash -lc`로 `zsh -l`을 실행하기 전에 `ZDOTDIR`을 내보냅니다.
- `--shell git-bash`는 기본 Git for Windows 경로(`"C:\\Program Files\\Git\\bin\\bash.exe" -li`)를 사용합니다. 다른 경로에 설치했다면 JSON을 수정하거나 명령을 도구 실행 후 직접 변경하세요.
- `startingDirectory`는 프로젝트 경로로 설정되며, Windows Terminal이 로컬 셸과 WSL 모두에 맞게 처리합니다.

## 설정 및 환경 변수

모든 CLI 플래그는 환경 변수로도 제어할 수 있습니다(쉘 rc 파일이나 CI 스크립트에 유용).

| 용도              | 플래그           | 환경 변수         | 기본값       |
| ----------------- | ---------------- | ----------------- | ------------ |
| iTerm2 부모 GUID  | `--parent-guid`  | `TP_PARENT_GUID`  | 없음         |
| iTerm2 부모 이름  | `--parent-name`  | `TP_PARENT_NAME`  | 없음         |
| Windows 색상 테마 | `--color-scheme` | `TP_COLOR_SCHEME` | 없음         |
| Windows 셸        | `--shell`        | `TP_SHELL`        | `powershell` |
| WSL 배포판        | `--wsl-distro`   | `TP_WSL_DISTRO`   | `Ubuntu`     |
| WSL ZDOTDIR       | `--wsl-zdotdir`  | `TP_WSL_ZDOTDIR`  | 없음         |
| CLI 세션 분리     | `--isolate-cli`  | `TP_ISOLATE_CLI`  | 없음         |

커맨드라인 인자가 환경 변수보다 우선합니다. 원하는 기본값을 설정하려면 셸 프로파일에 다음과 같이 추가하세요. 반드시 자신의 환경에 실제로 존재하는 이름을 선택해야 합니다.

```bash
# macOS 예시 — `termprofiles parents` 목록 중 하나 사용
export TP_PARENT_NAME="DEFAULT"
# Windows 예시 — Windows Terminal `schemes` 이름 사용
export TP_COLOR_SCHEME="One Half Dark"
```

- macOS에서 사용할 부모 프로필 이름은 `termprofiles parents` 명령으로 확인할 수 있습니다. iTerm2 환경설정에서 감지된 이름과 GUID가 함께 출력됩니다.
- Windows에서는 `wt settings`로 설정 편집기를 열거나 `settings.json` 파일의 `schemes` 배열을 확인해 `TP_COLOR_SCHEME`에 사용할 색상 테마 이름을 복사하세요.

## 활용 예시

- **프로필 일괄 생성:** `find ~/Code -maxdepth 1 -type d -not -path '*/.*' -print0 | xargs -0 termprofiles add`
- **일관된 테마 유지:** macOS에선 `TP_PARENT_NAME`, Windows에선 `TP_COLOR_SCHEME`을 설정해 색상과 UI를 맞춰보세요.
- **CLI 세션 분리:** `termprofiles add ~/dev/sample-app --isolate-cli codex`로 Codex CLI의 `~/.codex` 데이터를 프로젝트 전용 경로(`~/.zsh-profiles/sample-app/cli-homes/codex`)에 격리합니다.
- **codex 공유 사용법:** `termprofiles add . --isolate-cli codex` → iTerm2에서 동일한 `proj-<slug>` 프로파일 창을 두 개 연다 → 각 창에서 `codex`를 실행해 명령을 남긴 뒤, 다른 창에서 `codex history --latest`로 히스토리가 공유되는지 확인합니다.
- **zsh 옵션 빠르게 조정:** `termprofiles setopt`로 원하는 `setopt` 조합을 고르고, `termprofiles prompt on/off`로 프롬프트를 전환하면 바뀐 설정이 즉시 모든 탭에 적용됩니다.
- **새 셸 열기:** `termprofiles new --tab`으로 같은 프로필의 새 탭을 바로 띄울 수 있어 변경 사항 확인이 편합니다.
- **WSL 개발 환경:** `termprofiles add "/mnt/c/dev/app" --shell wsl --wsl-distro Ubuntu-22.04 --wsl-zdotdir "/home/user/.config/zsh/app"` 명령으로 프로젝트 전용 설정이 적용된 WSL zsh를 즉시 실행합니다.
- **깔끔한 제거:** `termprofiles remove ~/dev/sample-app --keep-zdotdir`는 동적 프로필만 제거하고 히스토리를 보존합니다.

## 문제 해결 & FAQ

- **`git push` 실행 시 “no upstream branch” 오류가 나요.** `git push --set-upstream origin <branch>`(예: `git push --set-upstream origin develop`)을 한 번 실행해 원격 브랜치와 연결하세요.
- **깃이 매번 계정 정보를 요구해요.** SSH 키를 GitHub에 등록한 뒤 `git remote set-url origin git@github.com:yaioyaio/termprofiles.git`로 전환하거나, Personal Access Token을 `git config --global credential.helper`로 저장하세요.
- **PyPI 업로드에서 인증이 거절돼요.** 업로드 전에 `~/.pypirc`를 준비하거나 `TWINE_USERNAME=__token__`, `TWINE_PASSWORD=pypi-...` 환경변수를 설정한 상태에서 `python -m twine upload dist/*`를 실행하세요.
- **빌드는 성공하지만 라이선스 경고가 나와요.** `pyproject.toml`의 `project.license` 값을 SPDX 문자열(예: `"MIT"`)로 바꾸면 setuptools의 폐기 예정 경고를 없앨 수 있습니다.
- **자동으로 점검하고 싶어요.** `termprofiles doctor`를 실행하면 Git/PyPI 배포 준비 사항을 한 번에 확인할 수 있습니다.
- **프로필이 보이지 않아요.** iTerm2/Windows Terminal을 재시작하여 동적 프로필/프래그먼트를 다시 로드하세요.
- **iTerm2가 JSON을 읽지 못해요.** Dynamic Profiles가 활성화되어 있는지 확인합니다(`Preferences → Profiles → Other Actions → Import JSON Profiles`).
- **Windows Terminal에서 프로필이 적용되지 않아요.** 설정에서 프래그먼트가 활성화되어 있는지 확인하고, `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles`에 JSON이 생성되었는지 점검하세요.
- **macOS에서 부모 프로필을 찾지 못해요.** `termprofiles parents`로 사용 가능한 이름과 GUID를 확인하세요. 검색은 공백/대소문자를 무시합니다.
- **사용자 정의 셸.** Git Bash가 다른 경로에 설치되었다면 생성된 JSON의 `commandline`을 직접 수정하세요.
- **디렉터리를 못 찾았다고 나와요.** `termprofiles add`는 존재하지 않는 경로를 건너뛰고 `Skip (not a dir)`를 출력합니다.

## 제거하기

- 생성된 JSON은 `termprofiles remove <targets>`로 삭제하고, 필요하다면 `~/.zsh-profiles/<slug>`도 직접 지우세요.
- 패키지 제거 방법:
  - pipx: `pipx uninstall termprofiles`
  - pip/가상환경: `python -m pip uninstall termprofiles`
- 정리하고 싶다면 다음 폴더를 수동으로 삭제할 수 있습니다:
  - macOS: `~/Library/Application Support/iTerm2/DynamicProfiles/dp-*.json`
  - Windows: `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles`

## 기여하기

- 이슈와 PR은 **[GitHub](https://github.com/yaioyaio/termprofiles)**에서 환영합니다.
- 로컬 개발 환경 구성:
  ```bash
  git clone https://github.com/yaioyaio/termprofiles.git
  cd termprofiles
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -e .
  termprofiles --help
  ```
- 필요 시 포매터나 패키징 검사를 실행하세요(`python -m build`).
- 일반적인 파이썬 베스트 프랙티스를 따르고 문서를 최신 상태로 유지해주세요.

## 라이선스

MIT © yaioyaio
