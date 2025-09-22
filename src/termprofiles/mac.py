import os, uuid, plistlib, shutil, re
from .util import slugify, atomic_write_json

ITERM_DP_DIR = os.path.expanduser("~/Library/Application Support/iTerm2/DynamicProfiles")
ZROOT        = os.path.expanduser("~/.zsh-profiles")
ITERM_PREFS  = os.path.expanduser("~/Library/Preferences/com.googlecode.iterm2.plist")

def ensure_dirs():
    os.makedirs(ITERM_DP_DIR, exist_ok=True)
    os.makedirs(ZROOT, exist_ok=True)

def _ensure_project_zsh(slug: str):
    proj_dir = os.path.join(ZROOT, slug)
    os.makedirs(proj_dir, exist_ok=True)
    hist = os.path.join(proj_dir, ".zsh_history")
    zrc  = os.path.join(proj_dir, ".zshrc")
    if not os.path.exists(zrc):
        with open(zrc, "w", encoding="utf-8") as f:
            f.write(f"""# per-project zshrc (auto)
export HISTFILE="{hist}"; export HISTSIZE=50000; export SAVEHIST=50000
setopt NO_SHARE_HISTORY HIST_IGNORE_ALL_DUPS HIST_REDUCE_BLANKS EXTENDED_HISTORY
[ -f "$HOME/.zshrc.common" ] && source "$HOME/.zshrc.common"
# PROMPT="[%F{{cyan}}{slug}%f] %n@%m %~ %# "  # 부모 테마 그대로 쓰려면 주석 유지
""")
    return proj_dir, hist, zrc

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().casefold()

def resolve_parent_guid_by_name(name: str) -> str | None:
    """Find parent GUID by NAME (case-insensitive, normalized spaces).
       If exact (normalized) match not found, try unique 'contains' match."""
    target = _norm(name)
    try:
        with open(ITERM_PREFS, "rb") as f:
            p = plistlib.load(f)
        choices = p.get("New Bookmarks", [])
        # exact normalized match
        for b in choices:
            if _norm(b.get("Name", "")) == target:
                guid = b.get("Guid")
                return str(guid) if guid else None
        # unique contains match
        cands = [b for b in choices if target and target in _norm(b.get("Name", ""))]
        if len(cands) == 1:
            guid = cands[0].get("Guid")
            return str(guid) if guid else None
    except Exception:
        pass
    return None

def list_parents():
    """Return [(Name, GUID), ...] from iTerm2 preferences."""
    try:
        with open(ITERM_PREFS, "rb") as f:
            p = plistlib.load(f)
        rows = []
        for b in p.get("New Bookmarks", []):
            rows.append((str(b.get("Name", "")), str(b.get("Guid", ""))))
        return rows
    except Exception as e:
        return [("!error reading prefs", str(e))]

def add(dirpath: str, parent_guid: str | None = None) -> str:
    ensure_dirs()
    d = os.path.expanduser(dirpath)
    if not os.path.isdir(d):
        return f"Skip (not a dir): {dirpath}"
    slug = slugify(d)
    name = f"proj-{slug}"
    json_path = os.path.join(ITERM_DP_DIR, f"dp-{slug}.json")
    if os.path.exists(json_path):
        return f"Skip (exists): {name}"
    proj_dir, _, _ = _ensure_project_zsh(slug)
    prof = {
        "Name": name,
        "Guid": str(uuid.uuid4()),
        "Custom Directory": "Yes",
        "Working Directory": d,
        "Custom Command": "Yes",
        "Command": f"/usr/bin/env ZDOTDIR=\"{proj_dir}\" /bin/zsh -l",
        # "Rewritable": True,  # 원하면 주석 해제
    }
    if parent_guid:
        prof["Dynamic Profile Parent GUID"] = parent_guid
    data = {"Profiles": [prof]}
    atomic_write_json(json_path, data)
    return f"Added: {name}"

def remove(target: str, keep_zdotdir: bool = False) -> str:
    slug = slugify(target)
    name = f"proj-{slug}"
    json_path = os.path.join(ITERM_DP_DIR, f"dp-{slug}.json")
    msg = []
    if os.path.exists(json_path):
        os.remove(json_path); msg.append(f"Removed JSON: {json_path}")
    else:
        msg.append(f"No JSON: {json_path}")
    proj_dir = os.path.join(ZROOT, slug)
    if os.path.isdir(proj_dir) and not keep_zdotdir:
        shutil.rmtree(proj_dir); msg.append(f"Removed ZDOTDIR: {proj_dir}")
    else:
        msg.append(f"Keep/No ZDOTDIR: {proj_dir}")
    return " | ".join(msg)

def list_profiles() -> list[tuple[str, str]]:
    out = []
    import json
    for fn in sorted(os.listdir(ITERM_DP_DIR)):
        if not (fn.startswith("dp-") and fn.endswith(".json")):
            continue
        path = os.path.join(ITERM_DP_DIR, fn)
        try:
            d = json.load(open(path, encoding="utf-8"))
            for p in d.get("Profiles", []):
                out.append((p.get("Name", "?"), p.get("Working Directory", "?")))
        except Exception as e:
            out.append((f"! invalid: {fn}", str(e)))
    return out
