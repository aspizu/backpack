import contextlib

from backpack.cli.doctor.requirements.uv_requirement import UvRequirement
from backpack.cmd import cmd

from .base_requirement import BaseRequirement


class OptionalToolRequirement(BaseRequirement):
    _package: str
    _git: str | None

    def __init__(self, package: str, git: str | None = None) -> None:
        super().__init__(dependencies=[UvRequirement()], is_optional=True)
        self.id = package
        self._package = package
        self._git = git

    def check(self) -> tuple[bool, str]:
        c = None
        with contextlib.suppress(ValueError):
            c = cmd(self._package)
        try:
            version = next(
                (
                    line
                    for line in cmd("uv").args("tool", "list").output().splitlines()
                    if self._package in line
                ),
                None,
            )
            version = version and version.strip().removeprefix(self._package + " ")
        except ValueError:
            return False, f"{self._package} not found, uv not found"
        if c:
            if version:
                return (
                    True,
                    f"{self._package} [white dim]{version} found at[/] {c.program}",
                )
            return True, f"{self._package} [white dim]found at[/] {c.program}"
        if version:
            msg = (
                f"{self._package} [white dim]{version} "
                f"installed but binary not found[/]"
            )
            return (False, msg)
        return False, f"{self._package} [white dim]not installed[/]"

    def fix(self) -> None:
        cmd("uv").echo().args(
            "tool", "install", f"git+{self._git}" if self._git else self._package
        ).run()
