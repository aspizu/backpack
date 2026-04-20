import importlib.resources
import logging
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from backpack.cmd import cmd

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

log = logging.getLogger(__name__)
res = importlib.resources.files("backpack.res")


def _copy_files(src: Traversable, dst: Path) -> None:
    for path in src.iterdir():
        if path.is_dir():
            dst.joinpath(path.name).mkdir(parents=True, exist_ok=True)
            _copy_files(path, dst.joinpath(path.name))
        else:
            shutil.copyfileobj(path.open("rb"), dst.joinpath(path.name).open("wb"))


def new(name: Path) -> None:
    outdir = name.absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    if len(list(outdir.iterdir())) > 0:
        log.error("directory '%s' is not empty", outdir.relative_to(Path().absolute()))
        sys.exit(1)
    _copy_files(res.joinpath("template"), outdir)
    cmd("git").args("init").run(cwd=outdir)
