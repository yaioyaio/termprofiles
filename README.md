# termprofiles
[![PyPI version](https://img.shields.io/pypi/v/termprofiles.svg)](https://pypi.org/project/termprofiles/)

[![PyPI](https://img.shields.io/pypi/v/termprofiles?label=PyPI)](https://pypi.org/project/termprofiles/)
![Python](https://img.shields.io/pypi/pyversions/termprofiles)
![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-blue)
![Terminal](https://img.shields.io/badge/for-iTerm2%20%7C%20Windows%20Terminal-8A2BE2)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- GitHub Actions 배지는 repo 경로 바꿔서 사용하세요 -->
<!-- [![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml) -->

> Per-project terminal profiles that feel native on macOS (iTerm2) and Windows (Windows Terminal), without hand-editing JSON.
>
> Keywords: iTerm2 dynamic profiles, Windows Terminal fragments, per-project ZDOTDIR, developer automation CLI.

TermProfiles creates one JSON file per project so you can add or remove profiles safely. On macOS, each project gets its own `ZDOTDIR` (history + `.zshrc`), while Windows users receive tidy Windows Terminal fragments. Everything lives inside your home directory.

## Contents

- [Overview](#overview)
- [Supported Platforms & Requirements](#supported-platforms--requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [How Profiles Are Structured](#how-profiles-are-structured)
- [macOS Details](#macos-details)
- [Windows Details](#windows-details)
- [Configuration & Environment Variables](#configuration--environment-variables)
- [Example Workflows](#example-workflows)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Uninstalling](#uninstalling)
- [Contributing](#contributing)
- [License](#license)

## Overview

- **Per-project profiles:** Generates one dynamic profile (macOS) or fragment (Windows) per directory.
- **Safe JSON handling:** Files are written atomically with UTF-8 encoding to avoid corruption.
- **No tmux required:** Launch directly into the project directory with your preferred shell.
- **Easy cleanup:** `termprofiles remove` deletes the generated JSON (and optional macOS ZDOTDIR).
- **Discoverable:** `termprofiles list` shows exactly what was created.

## Supported Platforms & Requirements

**macOS**

- macOS 11 or newer recommended.
- iTerm2 with Dynamic Profiles enabled.
- Shell: `/bin/zsh` is used, but you can customize via the generated `.zshrc`.

**Windows**

- Windows 10 19041+ or Windows 11 with Windows Terminal 1.16 or newer.
- PowerShell installed (default). Optional: Git Bash, Command Prompt, or WSL.

## Installation
TermProfiles is published on [PyPI](https://pypi.org/project/termprofiles/); choose one of the installation methods below.

### Using pipx (recommended)

`pipx` installs packages in isolated virtual environments and adds entry points to your shell.

```bash
# macOS (optional helper if Homebrew is available)
brew install pipx
pipx ensurepath
exec $SHELL

# macOS or Windows
pipx install termprofiles
# Upgrade later
pipx upgrade termprofiles
```

Verify the installation:

```bash
termprofiles --help
```

### Using pip

If you prefer a virtual environment or user-site install:

```bash
python -m venv .venv  # optional virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install termprofiles
```

### From source

```bash
git clone https://github.com/yaioyaio/termprofiles.git
cd termprofiles
pipx install .  # or: python -m pip install .
```

## Quick Start

### macOS (iTerm2)

1. Run `termprofiles add /path/to/project`.
2. Reopen iTerm2 (or `Profiles → Other Actions → Reload All Profiles`).
3. Launch the new profile named `proj-<slug>`.
4. Enjoy an isolated `.zshrc` and history backed by `~/.zsh-profiles/<slug>/`.

Example:

```bash
termprofiles add ~/dev/sample-app
```

Outputs something like `Added: proj-sample-app` and creates `dp-sample-app.json` in iTerm2's DynamicProfiles directory.

### Windows (Windows Terminal)

1. Run PowerShell **as the user** (no admin needed).
2. Execute `termprofiles add "C:\\src\\sample-app"`.
3. Close and reopen Windows Terminal (or run `wt.exe` again).
4. Select the new profile `proj-sample-app` from the dropdown.

By default the profile uses PowerShell and opens in your project directory.

## Command Reference

### `termprofiles add <dir> [<dir> ...]`

Create profiles for one or more project directories.

macOS options:

- `--parent-guid GUID` — inherit UI from an existing iTerm2 profile.
- `--parent-name NAME` — locate a profile by name (case-insensitive) and use its GUID.

Windows options:

- `--color-scheme NAME` — apply an existing Windows Terminal color scheme.
- `--shell TYPE` — `powershell` (default), `cmd`, `git-bash`, `wsl`, `wsl:<alias>`.
- `--wsl-distro NAME` — WSL distribution to launch (default `Ubuntu`).
- `--wsl-zdotdir PATH` — export `ZDOTDIR` before starting `zsh` in WSL.

### `termprofiles remove <target> [<target> ...]`

Delete generated profiles. Each `target` can be the original directory or its slug.

- macOS: add `--keep-zdotdir` to preserve `~/.zsh-profiles/<slug>`.
- Windows: only the fragment JSON is removed.

### `termprofiles list`

Show profiles discovered via the generated JSON files. Helpful for auditing or scripting.

### `termprofiles parents` _(macOS only)_

Enumerate iTerm2 profiles detected in `~/Library/Preferences/com.googlecode.iterm2.plist` with their GUIDs.

## How Profiles Are Structured

- **Slug generation:** The directory name is lowercased, spaces become `-`, and non-alphanumeric characters are stripped (e.g., `/Users/Alex/My App` → `my-app`).
- **File naming:**
  - macOS: `~/Library/Application Support/iTerm2/DynamicProfiles/dp-<slug>.json`
  - Windows: `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles\proj-<slug>.json`
- **Idempotent:** If a JSON file already exists, the command prints `Skip (exists)` and leaves your configuration untouched.

## macOS Details

- Each project gets `~/.zsh-profiles/<slug>/` containing `.zshrc` and `.zsh_history`.
- `.zshrc` sources `~/.zshrc.common` if present, so you can share aliases across projects.
- History is unlimited up to 50k entries (`HISTSIZE` + `SAVEHIST`).
- Launch command: `/usr/bin/env ZDOTDIR="<project_zdotdir>" /bin/zsh -l`.
- If you set a parent profile, the generated dynamic profile inherits colors, fonts, and other UI settings from it.

## Windows Details

- Fragment JSON conforms to the Windows Terminal fragment spec and is auto-discovered on launch.
- `--shell wsl` runs `wsl.exe -d <distro>`; combine with `--wsl-zdotdir` to export `ZDOTDIR` and spawn `zsh` via `bash -lc`.
- `--shell git-bash` points to the default Git for Windows install path (`"C:\\Program Files\\Git\\bin\\bash.exe" -li`). Adjust manually if you installed Git elsewhere.
- `startingDirectory` is set to the project path; Windows Terminal respects it for local shells and translates for WSL.

## Configuration & Environment Variables

Every CLI flag has an environment variable equivalent (useful for shell rc files or CI scripts):

| Purpose              | Flag             | Environment Variable | Default      |
| -------------------- | ---------------- | -------------------- | ------------ |
| iTerm2 parent GUID   | `--parent-guid`  | `TP_PARENT_GUID`     | None         |
| iTerm2 parent name   | `--parent-name`  | `TP_PARENT_NAME`     | None         |
| Windows color scheme | `--color-scheme` | `TP_COLOR_SCHEME`    | None         |
| Windows shell        | `--shell`        | `TP_SHELL`           | `powershell` |
| WSL distro           | `--wsl-distro`   | `TP_WSL_DISTRO`      | `Ubuntu`     |
| WSL ZDOTDIR export   | `--wsl-zdotdir`  | `TP_WSL_ZDOTDIR`     | None         |

Command-line arguments take precedence over environment variables. Set them in your shell profile to create customized defaults, e.g.:

```bash
export TP_PARENT_NAME="Solarized Dark"
export TP_COLOR_SCHEME="One Half Dark"
```

## Example Workflows

- **Automate profile creation:** `find ~/Code -maxdepth 1 -type d -not -path '*/.*' -print0 | xargs -0 termprofiles add`.
- **Shared look & feel:** on macOS set `TP_PARENT_NAME` to your favorite theme; on Windows set `TP_COLOR_SCHEME` to keep colors consistent.
- **WSL development:** `termprofiles add "/mnt/c/dev/app" --shell wsl --wsl-distro Ubuntu-22.04 --wsl-zdotdir "/home/user/.config/zsh/app"` launches straight into WSL zsh with project-specific config.
- **Clean removal:** `termprofiles remove ~/dev/sample-app --keep-zdotdir` keeps historical context while removing the dynamic profile.

## Troubleshooting & FAQ

- **Profiles are missing.** Restart iTerm2/Windows Terminal so it reloads dynamic profiles/fragments.
- **iTerm2 cannot read the JSON.** Ensure Dynamic Profiles are enabled (`Preferences → Profiles → Other Actions → Import JSON Profiles`).
- **Windows Terminal ignores the profile.** Confirm fragments are enabled (`Settings → Open JSON file` should list `TermProfiles`). Check `%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\TermProfiles` for the created JSON.
- **Parent profile not found (macOS).** Use `termprofiles parents` to list available names and GUIDs. Remember that matching is case-insensitive and trims whitespace.
- **Custom shells.** For Windows Git Bash installs in a different location, copy the generated fragment, edit `commandline`, or pass a custom path by editing the JSON after creation.
- **Unrecognized directory.** `termprofiles add` skips paths that are not directories and prints `Skip (not a dir)`.

## Uninstalling

- Remove generated JSON: run `termprofiles remove <targets>` (and optionally delete `~/.zsh-profiles/<slug>`).
- Delete the package:
  - pipx: `pipx uninstall termprofiles`
  - pip/virtualenv: `python -m pip uninstall termprofiles`
- Clean up leftover directories if desired: `rm -rf ~/Library/Application Support/iTerm2/DynamicProfiles/dp-*.json` (macOS) or delete the fragments folder on Windows.

## Contributing

- Issues and pull requests welcome at **[GitHub](https://github.com/yaioyaio/termprofiles)**.
- Local setup:
  ```bash
  git clone https://github.com/yaioyaio/termprofiles.git
  cd termprofiles
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -e .
  termprofiles --help
  ```
- Run formatting and packaging checks as needed (`python -m build`).
- Follow conventional Python best practices and keep documentation updated.

## License

MIT © yaioyaio