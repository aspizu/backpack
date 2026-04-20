import importlib.metadata
from pathlib import Path
from typing import TYPE_CHECKING

from . import toolchain
from .build import build
from .cli_builder import Command, build_cli, run
from .doctor import doctor
from .install import install
from .new import new
from .remove import remove

if TYPE_CHECKING:
    import argparse


def _setup_build(p: argparse.ArgumentParser) -> None:
    p.add_argument("input", nargs="?", help="Project directory, defaults to cwd.")
    p.add_argument("-o", "--output")
    p.add_argument(
        "-t",
        "--toolchain",
        default="latest",
        help="The version of the toolchain (goboscript compiler) to use.",
    )


def _setup_new(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "name", help="Name of the project.", type=Path, default=Path(), nargs="?"
    )


_commands = {
    "install": Command(
        install,
        ["i"],
        setup=lambda p: p.add_argument("package", nargs="?"),
    ),
    "remove": Command(
        remove,
        ["r"],
        setup=lambda p: p.add_argument("package"),
    ),
    "build": Command(
        build,
        ["b"],
        help="Compile a goboscript project to `.sb3`",
        setup=_setup_build,
    ),
    "doctor": Command(
        doctor,
        ["d"],
        help="Check (and optionally fix) issues with your setup.",
        setup=lambda p: p.add_argument("--fix", action="store_true"),
    ),
    "new": Command(
        new,
        ["n"],
        help="Create a new goboscript project.",
        setup=_setup_new,
    ),
    "toolchain": Command(
        aliases=["tc"],
        help="Manage goboscript compiler versions.",
        subcommands={
            "install": Command(
                toolchain.install,
                ["i"],
                help="Install or upgrade a toolchain.",
                setup=lambda p: p.add_argument(
                    "version",
                    default="latest",
                    nargs="?",
                    help="Branch name or commit hash, defaults to 'latest'",
                ),
            ),
            "remove": Command(
                toolchain.remove,
                ["r"],
                help="Remove a toolchain.",
                setup=lambda p: p.add_argument(
                    "version",
                    default="latest",
                    nargs="?",
                    help="Branch name or commit hash, defaults to 'latest'",
                ),
            ),
            "list": Command(
                toolchain.list_,
                ["l"],
                help="List installed toolchains and their paths.",
            ),
        },
    ),
}


def cli() -> None:
    run(
        build_cli(
            _commands, prog="backpack", version=importlib.metadata.version("backpack")
        )
    )
