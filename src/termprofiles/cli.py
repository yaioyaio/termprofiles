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
        a.add_argument("--isolate-cli", default=os.environ.get("TP_ISOLATE_CLI",""),
                       help="Comma-separated CLI names to wrap with isolated HOME/XDG dirs")
        so = sub.add_parser("setopt", help="adjust zsh setopt flags for this project profile")
        so.add_argument("--dir", default=None, help="Target directory (defaults to cwd)")
        so.add_argument("--slug", default=None, help="Override slug name")
        so.add_argument("--enable", default="", help="Comma-separated setopts to enable (non-interactive)")
        so.add_argument("--disable", default="", help="Comma-separated setopts to disable (non-interactive)")
        so.add_argument("--interactive", action="store_true", help="Force interactive picker even when enable/disable provided")

        pr = sub.add_parser("prompt", help="enable/disable the built-in prompt override")
        pr.add_argument("state", choices=["on", "off", "toggle"], help="Desired state")
        pr.add_argument("--dir", default=None, help="Target directory (defaults to cwd)")
        pr.add_argument("--slug", default=None, help="Override slug name")

        nw = sub.add_parser("new", help="open a new iTerm window/tab with this project profile")
        nw.add_argument("--dir", default=None, help="Target directory (defaults to cwd)")
        nw.add_argument("--slug", default=None, help="Override slug name")
        nw.add_argument("--tab", action="store_true", help="Open as a new tab in the current window")
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
            isolated = [s.strip() for s in (args.isolate_cli.split(",") if args.isolate_cli else []) if s.strip()]
            for d in args.dirs:
                results.append(backend.add(d, parent_guid=parent_guid, isolated_clis=isolated))
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

    if is_mac() and args.cmd == "setopt":
        enable = [s.strip() for s in args.enable.split(",") if s.strip()]
        disable = [s.strip() for s in args.disable.split(",") if s.strip()]
        print(backend.configure_setopts(
            dirpath=args.dir,
            slug_hint=args.slug,
            enable=enable,
            disable=disable,
            force_interactive=args.interactive,
        )); return

    if is_mac() and args.cmd == "prompt":
        print(backend.configure_prompt(args.state, dirpath=args.dir, slug_hint=args.slug)); return

    if is_mac() and args.cmd == "new":
        print(backend.open_new_session(dirpath=args.dir, slug_hint=args.slug, tab=args.tab)); return
