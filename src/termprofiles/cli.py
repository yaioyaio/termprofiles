import os, sys, argparse

def is_mac() -> bool: return sys.platform == "darwin"
def is_win() -> bool: return os.name == "nt"

def main():
    if not (is_mac() or is_win()):
        print("Supported on macOS (iTerm2) and Windows (Windows Terminal)."); sys.exit(1)

    if is_mac():
        from . import mac as backend
    else:
        from . import win as backend

    ap = argparse.ArgumentParser(prog="termprofiles",
        description="Per-project terminal profiles for iTerm2 (macOS) / Windows Terminal (Windows).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add profiles for dir(s)")
    if is_mac():
        a.add_argument("--parent-guid", default=os.environ.get("TP_PARENT_GUID",""),
                       help="iTerm2 parent profile GUID to inherit UI from")
        a.add_argument("--parent-name", default=os.environ.get("TP_PARENT_NAME",""),
                       help="iTerm2 parent profile NAME (case-insensitive)")
    else:
        a.add_argument("--color-scheme", default=os.environ.get("TP_COLOR_SCHEME",""),
                       help="Windows Terminal colorScheme name to apply")
        a.add_argument("--shell", default=os.environ.get("TP_SHELL","powershell"),
                       help="Shell: powershell|cmd|git-bash|wsl")
        a.add_argument("--wsl-distro", default=os.environ.get("TP_WSL_DISTRO",""),
                       help="WSL distro name (e.g., Ubuntu)")
        a.add_argument("--wsl-zdotdir", default=os.environ.get("TP_WSL_ZDOTDIR",""),
                       help="(optional) WSL-side ZDOTDIR path for zsh")

    a.add_argument("dirs", nargs="+", help="project directories")

    r = sub.add_parser("remove", help="remove profile by dir or slug")
    if is_mac():
        r.add_argument("--keep-zdotdir", action="store_true", help="do not delete ~/.zsh-profiles/<slug>")
    r.add_argument("targets", nargs="+")
    l = sub.add_parser("list", help="list profiles")

    if is_mac():
        p = sub.add_parser("parents", help="list iTerm2 profiles (name + GUID) detected by this tool")

    args = ap.parse_args()

    if args.cmd == "add":
        results = []
        if is_mac():
            parent_guid = args.parent_guid or None
            if not parent_guid and args.parent_name:
                from .mac import resolve_parent_guid_by_name
                parent_guid = resolve_parent_guid_by_name(args.parent_name)
                if parent_guid:
                    print(f"Resolved parent '{args.parent_name}' -> {parent_guid}")
                else:
                    print(f"WARNING: parent '{args.parent_name}' not found; continuing without parent.")
            for d in args.dirs:
                results.append(backend.add(d, parent_guid=parent_guid))
        else:
            for d in args.dirs:
                results.append(backend.add(
                    d, color_scheme=(args.color_scheme or None),
                    shell=args.shell, wsl_distro=(args.wsl_distro or None),
                    wsl_zdotdir=(args.wsl_zdotdir or None)
                ))
        print("\n".join(results)); return

    if args.cmd == "remove":
        results = []
        for t in args.targets:
            if is_mac():
                results.append(backend.remove(t, keep_zdotdir=args.keep_zdotdir))
            else:
                results.append(backend.remove(t))
        print("\n".join(results)); return

    if args.cmd == "list":
        rows = backend.list_profiles()
        if not rows:
            print("(no dynamic profiles)")
        else:
            w = max(len(n) for n,_ in rows) if rows else 10
            for n,p in rows:
                print(f"{n:<{w}}  {p}")
        return

    if is_mac() and args.cmd == "parents":
        from .mac import list_parents
        rows = list_parents()
        if not rows:
            print("(no bookmarks)"); return
        w = max(len(n) for n,_ in rows)
        for n,g in rows:
            print(f"{n:<{w}}  {g}")
        return
