from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class Command:
    fn: Callable | None = None
    aliases: list[str] = field(default_factory=list)
    help: str = ""
    setup: Callable[[argparse.ArgumentParser], None] | None = None
    subcommands: dict[str, Command] = field(default_factory=dict)


def _register(sub: argparse._SubParsersAction, name: str, cmd: Command) -> None:
    p = sub.add_parser(name, aliases=cmd.aliases, help=cmd.help)
    if cmd.setup:
        cmd.setup(p)
    if cmd.subcommands:
        nested = p.add_subparsers(required=True)
        for sub_name, sub_cmd in cmd.subcommands.items():
            _register(nested, sub_name, sub_cmd)
    elif cmd.fn:
        p.set_defaults(_fn=cmd.fn)


def build_cli(
    commands: dict[str, Command], *, prog: str, version: str
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    sub = parser.add_subparsers(required=True)
    for name, cmd in commands.items():
        _register(sub, name, cmd)
    return parser


def run(parser: argparse.ArgumentParser) -> None:
    ns = vars(parser.parse_args())
    fn = ns.pop("_fn")
    fn(**{k: v for k, v in ns.items() if not k.startswith("_")})
