import sys

from rich import print
from rich.prompt import Confirm

from backpack.cmd import cmd

from .base_requirement import BaseRequirement
from .command_requirement import CommandRequirement


def _install_cargo_unix() -> None:
    cmd("sh").echo().args("-c", "wget -qO- https://sh.rustup.rs | sh").run()


class NightlyRequirement(BaseRequirement):
    def __init__(self) -> None:
        super().__init__(dependencies=[RustupRequirement()])
        self.id = "nightly"

    def check(self) -> tuple[bool, str]:
        try:
            toolchains = cmd("rustup").args("toolchain", "list").output()
        except ValueError:
            return (
                False,
                "rust nightly toolchain [dim white]not found, rustup not found[/]",
            )
        if "nightly-" in toolchains:
            return True, "rust nightly toolchain [dim white]found[/]"
        return False, "rust nightly toolchain [dim white]not found[/]"

    def fix(self) -> None:
        cmd("rustup").echo().args("toolchain", "install", "nightly").run()


class RustupRequirement(CommandRequirement):
    def __init__(self) -> None:
        super().__init__(
            "rustup", check_version=True, dependencies=[CommandRequirement("wget")]
        )

    def fix(self) -> None:
        if sys.platform == "win32":
            print(
                "follow instructions at https://rustup.rs/ to install rustup and cargo"
            )
            raise NotImplementedError
        q = "do you want to install rustup (and cargo) using the official installer script?"
        if not Confirm.ask(q):
            _install_cargo_unix()
