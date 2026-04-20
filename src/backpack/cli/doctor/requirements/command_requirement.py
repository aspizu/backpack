from backpack.cmd import cmd

from .base_requirement import BaseRequirement


class CommandRequirement(BaseRequirement):
    command: str
    check_version: bool

    def __init__(
        self,
        command: str,
        check_version: bool = False,
        dependencies: list[BaseRequirement] | None = None,
    ) -> None:
        super().__init__(dependencies)
        self.id = command
        self.command = command
        self.check_version = check_version

    def check(self) -> tuple[bool, str]:
        try:
            c = cmd(self.command)
        except ValueError:
            return False, f"{self.command} not found"
        if self.check_version:
            version = (
                c.args("--version")
                .output()
                .removeprefix(self.command)
                .removeprefix(" version ")
                .removeprefix(" v")
                .strip()
            )
            return (
                True,
                f"{self.command} [dim white]{version} found at[/] {c.program}",
            )
        return True, f"{self.command} [dim white]found at[/] {c.program}"

    def fix(self) -> None:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.command)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CommandRequirement) and self.command == other.command
