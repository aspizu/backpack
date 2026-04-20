import logging
import shutil
import sys
from typing import TYPE_CHECKING

from rich import print

from backpack.cmd import cmd
from backpack.misc import CACHE_DIR

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


def get_tc_path(version: str) -> Path:
    return CACHE_DIR.joinpath("bin", version.replace("/", "-"), "goboscript")


def install(version: str) -> None:
    goboscript_dir = CACHE_DIR.joinpath("goboscript")
    if not goboscript_dir.exists():
        cmd("git").echo().args(
            "clone", "https://github.com/aspizu/goboscript", goboscript_dir
        ).run()
    cmd("git").echo().args("checkout", "main" if version == "latest" else version).run(
        cwd=goboscript_dir
    )
    cmd("cargo").echo().args("build", "--release").run(cwd=goboscript_dir)
    tc_path = get_tc_path(version)
    tc_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(goboscript_dir.joinpath("target/release/goboscript"), tc_path)
    print(f"toolchain '{version}' [dim]installed at[/] {tc_path}")


def remove(version: str) -> None:
    try:
        shutil.rmtree(get_tc_path(version))
    except FileNotFoundError:
        log.exception("version '%s' not found", version)
        sys.exit(1)


def list_() -> None:
    for version in sorted(CACHE_DIR.joinpath("bin").iterdir()):
        print(f"{version.name} [dim]at[/] {version}/goboscript")
