import os, uuid
from .util import slugify, atomic_write_json, APP_NAME

# 사용자 범위 설치 경로(권장) – 없으면 생성
# C:\Users\<user>\AppData\Local\Microsoft\Windows Terminal\Fragments\<app-name>\*.json :contentReference[oaicite:4]{index=4}
WT_FRAG_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    "Microsoft", "Windows Terminal", "Fragments", APP_NAME
)

def ensure_dir():
    os.makedirs(WT_FRAG_DIR, exist_ok=True)

def _default_commandline(shell: str, wsl_distro: str | None, zdotdir: str | None) -> str:
    # 기본은 PowerShell. WSL을 쓰면 WSL 배포판 지정 가능
    if shell.lower().startswith("wsl"):
        distro = (wsl_distro or "Ubuntu").strip()
        # WSL에서 ZDOTDIR을 쓰고 싶으면 bash -lc로 zsh -l 실행 전에 export
        if zdotdir:
            return f'wsl.exe -d {distro} --cd ~ -e bash -lc "export ZDOTDIR=\\"{zdotdir}\\"; exec zsh -l"'
        return f"wsl.exe -d {distro}"
    elif shell.lower().startswith("git-bash"):
        return r'"C:\Program Files\Git\bin\bash.exe" -li'
    elif shell.lower().startswith("cmd"):
        return "cmd.exe"
    # default powershell
    return "powershell.exe"

def add(dirpath: str, color_scheme: str | None = None,
        shell: str = "powershell", wsl_distro: str | None = None,
        wsl_zdotdir: str | None = None) -> str:
    ensure_dir()
    d = os.path.expanduser(dirpath)
    if not os.path.isdir(d):
        return f"Skip (not a dir): {dirpath}"
    slug = slugify(d)
    name = f"proj-{slug}"
    json_path = os.path.join(WT_FRAG_DIR, f"{name}.json")
    if os.path.exists(json_path):
        return f"Skip (exists): {name}"

    prof = {
        "name": name,
        "guid": "{%s}" % uuid.uuid4(),   # WT는 중괄호 포함 문자열 권장
        "commandline": _default_commandline(shell, wsl_distro, wsl_zdotdir),
        "startingDirectory": d,          # WT가 자동 인식(WSL 등에서는 --cd 로 변환) :contentReference[oaicite:5]{index=5}
    }
    if color_scheme:
        prof["colorScheme"] = color_scheme

    data = {"profiles": [prof]}
    atomic_write_json(json_path, data)
    return f"Added: {name}"

def remove(target: str) -> str:
    slug = slugify(target)
    name = f"proj-{slug}"
    json_path = os.path.join(WT_FRAG_DIR, f"{name}.json")
    if os.path.exists(json_path):
        os.remove(json_path)
        return f"Removed JSON: {json_path}"
    return f"No JSON: {json_path}"

def list_profiles() -> list[tuple[str, str]]:
    out = []
    if not os.path.isdir(WT_FRAG_DIR):
        return out
    import json
    for fn in sorted(os.listdir(WT_FRAG_DIR)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(WT_FRAG_DIR, fn)
        try:
            d = json.load(open(path, encoding="utf-8"))
            for p in d.get("profiles", []):
                out.append((p.get("name", "?"), p.get("startingDirectory", "?")))
        except Exception as e:
            out.append((f"! invalid: {fn}", str(e)))
    return out
