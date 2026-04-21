import sys
import tomllib
from pathlib import Path
from subprocess import CalledProcessError

from backpack.cli.toolchain import get_tc_path
from backpack.cmd import cmd


def _read_toolchain_from_toml(input: str | None) -> str:
    project_dir = Path(input) if input else Path()
    toml_path = project_dir / "goboscript.toml"
    try:
        with toml_path.open("rb") as f:
            data = tomllib.load(f)
        return data.get("toolchain", "latest")
    except FileNotFoundError:
        return "latest"


def build(input: str | None, output: str | None, toolchain: str | None) -> None:
    if toolchain is None:
        toolchain = _read_toolchain_from_toml(input)
    tc_path = get_tc_path(toolchain)
    try:
        cmd(tc_path).args("build", input).opt("--output", output).run()
    except CalledProcessError as err:
        sys.exit(err.returncode)
