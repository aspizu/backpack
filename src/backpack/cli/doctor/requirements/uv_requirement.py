import sys
from typing import override

from rich.prompt import Confirm

from backpack.cmd import cmd

from .command_requirement import CommandRequirement


def _install_uv_windows() -> None:
    cmd("pwsh.exe").echo().args(
        "-ExecutionPolicy",
        "ByPass",
        "-c",
        "irm https://astral.sh/uv/install.ps1 | iex",
    ).run()


def _install_uv_unix() -> None:
    cmd("sh").echo().args("-c", "wget -qO- https://astral.sh/uv/install.sh | sh").run()


class UvRequirement(CommandRequirement):
    def __init__(self) -> None:
        super().__init__(
            "uv", check_version=True, dependencies=[CommandRequirement("wget")]
        )

    @override
    def fix(self) -> None:
        q = "do you want to install uv using the official installer script?"
        if Confirm.ask(q):
            if sys.platform == "win32":
                _install_uv_windows()
            else:
                _install_uv_unix()
