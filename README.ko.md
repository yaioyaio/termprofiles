# termprofiles

[![PyPI](https://img.shields.io/pypi/v/termprofiles?label=PyPI)](https://pypi.org/project/termprofiles/)
![Python](https://img.shields.io/pypi/pyversions/termprofiles)
![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-blue)
![Terminal](https://img.shields.io/badge/for-iTerm2%20%7C%20Windows%20Terminal-8A2BE2)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- GitHub Actions 배지는 repo 경로 바꿔서 사용하세요 -->
<!-- [![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml) -->

> macOS(iTerm2)와 Windows(Windows Terminal)에서 JSON을 손으로 수정할 필요 없이 프로젝트별 터미널 프로필을 만들어 줍니다.

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

### `termprofiles parents` _(macOS 전용)_

`~/Library/Preferences/com.googlecode.iterm2.plist`에서 감지한 iTerm2 프로필과 GUID를 나열합니다.

## 프로필 구조

- **슬러그 생성:** 디렉터리 이름을 소문자로 변환하고, 공백은 `-`, 영문/숫자/`_.-` 이외 문자는 제거합니다. (예: `/Users/Alex/My App` → `my-app`)
- **파일 이름:**
  - macOS: `~/Library/Application Support/iTerm2/DynamicProfiles/dp-<slug>.json`
  - Windows: `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles\proj-<slug>.json`
- **멱등성:** JSON 파일이 이미 존재하면 `Skip (exists)`를 출력하고 기존 설정을 유지합니다.

## macOS 상세 정보

- 각 프로젝트마다 `~/.zsh-profiles/<slug>/` 디렉터리가 생성되고, 그 안에 `.zshrc`와 `.zsh_history`가 포함됩니다.
- `.zshrc`는 `~/.zshrc.common`이 존재할 경우 자동으로 소스하여 공통 설정을 공유할 수 있습니다.
- 히스토리 크기는 `HISTSIZE` 및 `SAVEHIST` 50,000으로 넉넉하게 설정됩니다.
- 실행 명령어: `/usr/bin/env ZDOTDIR="<project_zdotdir>" /bin/zsh -l`
- 부모 프로필을 설정하면 색상, 폰트 등 UI 구성을 그대로 상속 받을 수 있습니다.

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

커맨드라인 인자가 환경 변수보다 우선합니다. 원하는 기본값을 설정하려면 셸 프로파일에 다음과 같이 추가하세요.

```bash
export TP_PARENT_NAME="Solarized Dark"
export TP_COLOR_SCHEME="One Half Dark"
```

## 활용 예시

- **프로필 일괄 생성:** `find ~/Code -maxdepth 1 -type d -not -path '*/.*' -print0 | xargs -0 termprofiles add`
- **일관된 테마 유지:** macOS에선 `TP_PARENT_NAME`, Windows에선 `TP_COLOR_SCHEME`을 설정해 색상과 UI를 맞춰보세요.
- **WSL 개발 환경:** `termprofiles add "/mnt/c/dev/app" --shell wsl --wsl-distro Ubuntu-22.04 --wsl-zdotdir "/home/user/.config/zsh/app"` 명령으로 프로젝트 전용 설정이 적용된 WSL zsh를 즉시 실행합니다.
- **깔끔한 제거:** `termprofiles remove ~/dev/sample-app --keep-zdotdir`는 동적 프로필만 제거하고 히스토리를 보존합니다.

## 문제 해결 & FAQ

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
