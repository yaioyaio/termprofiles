"""Release environment diagnostics for termprofiles CLI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import subprocess
from typing import Callable, Dict, Iterable, List, Optional


@dataclass
class _CmdResult:
    returncode: int
    stdout: str
    stderr: str


Runner = Callable[[Iterable[str]], _CmdResult]


def _default_runner(cmd: Iterable[str]) -> _CmdResult:
    try:
        completed = subprocess.run(
            list(cmd),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:  # git or other tool missing
        return _CmdResult(returncode=127, stdout="", stderr=str(exc))
    return _CmdResult(completed.returncode, completed.stdout.strip(), completed.stderr.strip())


def _status(tag: str, message: str) -> str:
    return f"[{tag}] {message}"


def check_git(runner: Optional[Runner] = None) -> List[str]:
    runner = runner or _default_runner
    lines: List[str] = []

    inside = runner(["git", "rev-parse", "--is-inside-work-tree"])
    if inside.returncode != 0:
        lines.append(_status("WARN", "Git repository가 아니어서 깃 관련 검사를 건너뜁니다."))
        return lines

    branch = runner(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch.returncode == 0 and branch.stdout:
        lines.append(_status("OK", f"현재 브랜치: {branch.stdout}"))
    else:
        lines.append(_status("WARN", "현재 브랜치를 확인할 수 없습니다."))

    upstream = runner(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if upstream.returncode == 0 and upstream.stdout:
        lines.append(_status("OK", f"업스트림 브랜치 추적 중: {upstream.stdout}"))
    else:
        lines.append(_status("WARN", "업스트림 브랜치가 설정되지 않았습니다. `git push --set-upstream origin <branch>`를 실행하세요."))

    remote = runner(["git", "remote", "get-url", "--push", "origin"])
    if remote.returncode == 0 and remote.stdout:
        if remote.stdout.startswith("git@"):
            lines.append(_status("OK", f"origin push URL이 SSH입니다: {remote.stdout}"))
        else:
            lines.append(_status("WARN", f"origin push URL이 HTTPS입니다: {remote.stdout}. SSH로 전환하려면 `git remote set-url origin git@...`을 참고하세요."))
    else:
        lines.append(_status("WARN", "origin push URL을 확인할 수 없습니다."))

    return lines


def check_pypi(env: Optional[Dict[str, str]] = None, home: Optional[Path] = None) -> List[str]:
    env = env or os.environ
    home = home or Path.home()
    lines: List[str] = []

    twine_path = shutil.which("twine")
    if twine_path:
        lines.append(_status("OK", f"twine 감지됨: {twine_path}"))
    else:
        lines.append(_status("WARN", "twine이 PATH에서 발견되지 않았습니다. `python -m pip install --upgrade twine`으로 설치하세요."))

    has_env_token = any(env.get(k) for k in ("TWINE_PASSWORD", "TWINE_API_KEY", "PYPI_TOKEN"))
    if env.get("TWINE_USERNAME") or has_env_token:
        lines.append(_status("OK", "PyPI 환경 변수 자격 증명이 설정되어 있습니다."))
    else:
        lines.append(_status("WARN", "PyPI 환경 변수 자격 증명이 없습니다 (예: TWINE_USERNAME/TWINE_PASSWORD)."))

    pypirc = home / ".pypirc"
    if pypirc.exists():
        lines.append(_status("OK", f"~/.pypirc 발견: {pypirc}"))
    else:
        lines.append(_status("WARN", "~/.pypirc 파일이 없습니다."))

    dist_dir = Path.cwd() / "dist"
    if dist_dir.exists() and any(dist_dir.iterdir()):
        lines.append(_status("OK", "dist/ 디렉터리에 배포 아티팩트가 있습니다."))
    else:
        lines.append(_status("WARN", "dist/ 디렉터리에 빌드 결과가 없습니다. `python -m build`를 먼저 실행하세요."))

    return lines


def run_doctor(
    runner: Optional[Runner] = None,
    env: Optional[Dict[str, str]] = None,
    home: Optional[Path] = None,
) -> str:
    sections = []
    sections.append("## Git 상태")
    sections.extend(check_git(runner=runner))
    sections.append("")
    sections.append("## PyPI 배포")
    sections.extend(check_pypi(env=env, home=home))
    return "\n".join(sections)
