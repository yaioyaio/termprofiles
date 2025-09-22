import os, json, re, tempfile

APP_NAME = "TermProfiles"

def slugify(x: str) -> str:
    s = os.path.basename(x).lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_.-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "proj"

def atomic_write_json(path: str, data: dict) -> None:
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    # ensure UTF-8 (Windows Terminal fragments require UTF-8, not UTF-16) :contentReference[oaicite:3]{index=3}
    with tempfile.NamedTemporaryFile("w", delete=False, dir=d, encoding="utf-8") as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name
    os.replace(tmp_path, path)
