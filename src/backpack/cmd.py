import functools
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from rich import print

if TYPE_CHECKING:
    from collections.abc import Iterator


def _quote_command(program: str, args: list[str]) -> str:
    return "$ " + Path(program).name + " " + " ".join(shlex.quote(arg) for arg in args)


@dataclass
class Cmd:
    program: str
    _args: list[str]
    _echo: bool

    def echo(self) -> Cmd:
        return Cmd(self.program, self._args, _echo=True)

    def args(self, *args: object) -> Cmd:
        return Cmd(
            self.program,
            [*self._args, *(str(arg) for arg in args if arg is not None)],
            self._echo,
        )

    def opt(self, key: str, value: object | None) -> Cmd:
        if value is None:
            return self
        return self.args(key, value)

    def __iter__(self) -> Iterator[str]:
        yield self.program
        yield from self._args

    def output(self) -> str:
        if self._echo:
            print(_quote_command(self.program, self._args))
        return (
            subprocess.check_output(iter(self), stderr=subprocess.DEVNULL)
            .decode()
            .rstrip("\n")
        )

    def run(self, cwd: str | Path | None = None) -> subprocess.CompletedProcess:
        if self._echo:
            print(_quote_command(self.program, self._args))
        return subprocess.run(iter(self), check=True, cwd=cwd)


_extra_path = [
    Path("~/.cargo/bin").expanduser().as_posix(),
    Path("~/.local/bin").expanduser().as_posix(),
]
if sys.platform == "win32":
    p = Path(os.environ["LOCALAPPDATA"]).joinpath("Microsoft/WinGet/Links").as_posix()
    _extra_path.append(p)
EXTRA_PATH = ":".join(_extra_path)


@functools.cache
def cmd(name: str) -> Cmd:
    program = shutil.which(name)
    if program is None:
        program = shutil.which(name, path=EXTRA_PATH)
    if program is None:
        msg = f"{name} not found"
        raise ValueError(msg)
    return Cmd(program, _args=[], _echo=False)
