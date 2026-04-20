import importlib.resources
import logging
import shutil
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)
res = importlib.resources.files("backpack.res")


def new(name: Path) -> None:
    outdir = name.absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    if len(list(outdir.iterdir())) > 0:
        log.error("directory '%s' is not empty", outdir)
        sys.exit(1)
    for path in res.joinpath("template").iterdir():
        shutil.copyfileobj(path.open("rb"), outdir.joinpath(path.name).open("wb"))
