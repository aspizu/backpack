import sys
from subprocess import CalledProcessError

from backpack.cli.toolchain import get_tc_path
from backpack.cmd import cmd


def build(input: str | None, output: str | None, toolchain: str) -> None:
    tc_path = get_tc_path(toolchain)
    try:
        cmd(tc_path).args("build", input).opt("--output", output).run()
    except CalledProcessError as err:
        sys.exit(err.returncode)
