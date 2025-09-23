import os

from termprofiles.doctor import _CmdResult, check_git, check_pypi


class FakeRunner:
    def __init__(self, mapping):
        self.mapping = {tuple(k): v for k, v in mapping.items()}
        self.calls = []

    def __call__(self, cmd):
        key = tuple(cmd)
        self.calls.append(key)
        return self.mapping.get(key, _CmdResult(returncode=1, stdout="", stderr=""))


def test_check_git_with_upstream(tmp_path, monkeypatch):
    runner = FakeRunner({
        ("git", "rev-parse", "--is-inside-work-tree"): _CmdResult(0, "true", ""),
        ("git", "rev-parse", "--abbrev-ref", "HEAD"): _CmdResult(0, "develop", ""),
        ("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"): _CmdResult(0, "origin/develop", ""),
        ("git", "remote", "get-url", "--push", "origin"): _CmdResult(0, "git@github.com:yaioyaio/termprofiles.git", ""),
    })

    lines = check_git(runner=runner)

    assert any("현재 브랜치" in line for line in lines)
    assert any("업스트림" in line and "OK" in line for line in lines)
    assert any("SSH" in line for line in lines)


def test_check_git_without_upstream(monkeypatch):
    runner = FakeRunner({
        ("git", "rev-parse", "--is-inside-work-tree"): _CmdResult(0, "true", ""),
        ("git", "rev-parse", "--abbrev-ref", "HEAD"): _CmdResult(0, "feature", ""),
        ("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"): _CmdResult(1, "", ""),
        ("git", "remote", "get-url", "--push", "origin"): _CmdResult(0, "https://github.com/yaioyaio/termprofiles.git", ""),
    })

    lines = check_git(runner=runner)

    assert any("WARN" in line and "업스트림 브랜치" in line for line in lines)
    assert any("HTTPS" in line for line in lines)


def test_check_pypi(tmp_path, monkeypatch):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "dummy.whl").write_text("placeholder")

    env = {
        "TWINE_USERNAME": "__token__",
        "TWINE_PASSWORD": "pypi-xxx",
    }

    # ensure which() finds a fake twine path
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ.get('PATH', '')}")
    fake_twine = tmp_path / "twine"
    fake_twine.write_text("#!/bin/sh\n")
    fake_twine.chmod(0o755)

    monkeypatch.chdir(tmp_path)

    lines = check_pypi(env=env, home=tmp_path)

    assert any("twine" in line for line in lines)
    assert any("환경 변수" in line for line in lines)
    assert any("~/.pypirc" in line and "WARN" in line for line in lines)
    assert any("dist/" in line for line in lines)
