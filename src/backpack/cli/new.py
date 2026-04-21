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


def _build_gstoml_lines(  # noqa: PLR0913
    toolchain: str | None,
    std: str | None,
    bitmap_resolution: int | None,
    frame_rate: int | None,
    max_clones: float | None,
    no_miscellaneous_limits: bool,
    no_sprite_fencing: bool,
    frame_interpolation: bool,
    high_quality_pen: bool,
    stage_width: int | None,
    stage_height: int | None,
) -> list[str]:
    str_opts: list[tuple[str, str | None]] = [
        ("toolchain", toolchain),
        ("std", std),
    ]
    val_opts: list[tuple[str, int | float | None]] = [
        ("bitmap_resolution", bitmap_resolution),
        ("frame_rate", frame_rate),
        ("max_clones", max_clones),
        ("stage_width", stage_width),
        ("stage_height", stage_height),
    ]
    bool_opts: list[tuple[str, bool]] = [
        ("no_miscellaneous_limits", no_miscellaneous_limits),
        ("no_sprite_fencing", no_sprite_fencing),
        ("frame_interpolation", frame_interpolation),
        ("high_quality_pen", high_quality_pen),
    ]
    return [
        *[f'{k} = "{v}"' for k, v in str_opts if v is not None],
        *[f"{k} = {v}" for k, v in val_opts if v is not None],
        *[f"{k} = true" for k, v in bool_opts if v],
    ]


def new(  # noqa: PLR0913
    name: Path,
    toolchain: str | None,
    no_git: bool,
    std: str | None,
    bitmap_resolution: int | None,
    frame_rate: int | None,
    max_clones: float | None,
    no_miscellaneous_limits: bool,
    no_sprite_fencing: bool,
    frame_interpolation: bool,
    high_quality_pen: bool,
    stage_width: int | None,
    stage_height: int | None,
    no_makefile: bool,
) -> None:
    outdir = name.absolute()
    outdir.mkdir(parents=True, exist_ok=True)

    if any(outdir.iterdir()):
        log.error("directory '%s' is not empty", outdir.relative_to(Path().absolute()))
        sys.exit(1)

    _copy_files(res.joinpath("template"), outdir)

    if not no_git:
        cmd("git").args("init").run(cwd=outdir)
    if no_makefile:
        (outdir / "Makefile").unlink()
    if no_git:
        (outdir / ".gitignore").unlink()

    lines = _build_gstoml_lines(
        toolchain,
        std,
        bitmap_resolution,
        frame_rate,
        max_clones,
        no_miscellaneous_limits,
        no_sprite_fencing,
        frame_interpolation,
        high_quality_pen,
        stage_width,
        stage_height,
    )
    if lines:
        with (outdir / "goboscript.toml").open("a") as f:
            f.write("\n".join(lines) + "\n")
