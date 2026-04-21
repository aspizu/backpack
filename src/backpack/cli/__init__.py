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
        default=None,
        help="The version of the toolchain (goboscript compiler) to use.",
    )


def _setup_new(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "name",
        help=(
            "Name of directory to create new project, if not given, "
            "the current directory is used. If this is a path to an existing directory,"
            " it must be empty."
        ),
        type=Path,
        default=Path(),
        nargs="?",
    )
    p.add_argument(
        "-t",
        "--toolchain",
        default=None,
        help=(
            "The version of the toolchain (goboscript compiler) to use,"
            " defaults to 'latest'"
        ),
    )
    p.add_argument(
        "-G", "--no-git", action="store_true", help="Do not initialize a Git repository"
    )
    p.add_argument(
        "-s",
        "--std",
        default=None,
        help="Version of the standard library to use. Defaults to bleeding-edge",
    )
    p.add_argument("-b", "--bitmap-resolution", type=int, default=None)
    p.add_argument(
        "-f",
        "--frame-rate",
        "--fps",
        type=int,
        default=None,
        help="Custom frame rate, used by TurboWarp",
    )
    p.add_argument(
        "-c",
        "--max-clones",
        "--clones",
        type=float,
        default=None,
        help=(
            "Custom maximum number of clones allowed, used by TurboWarp."
            " Use `--max-clones inf` for infinite clones"
        ),
    )
    p.add_argument(
        "-l",
        "--no-miscellaneous-limits",
        "--limitless",
        action="store_true",
        help="Disable miscellaneous limits, used by TurboWarp",
    )
    p.add_argument(
        "-o",
        "--no-sprite-fencing",
        "--offscreen",
        action="store_true",
        help="Disable sprite fencing, used by TurboWarp",
    )
    p.add_argument(
        "-i",
        "--frame-interpolation",
        "--interpolate",
        action="store_true",
        help="Enable frame interpolation, used by TurboWarp",
    )
    p.add_argument(
        "-q",
        "--high-quality-pen",
        "--hqpen",
        action="store_true",
        help="Enable high quality pen, used by TurboWarp",
    )
    p.add_argument(
        "-W",
        "--stage-width",
        "--width",
        type=int,
        default=None,
        help="Custom stage width, used by TurboWarp",
    )
    p.add_argument(
        "-H",
        "--stage-height",
        "--height",
        type=int,
        default=None,
        help="Custom stage height, used by TurboWarp",
    )
    p.add_argument(
        "-M",
        "--no-makefile",
        action="store_true",
        help="Do not generate a Makefile for building the project",
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
        setup=lambda p: p.add_argument("--fix", nargs="?", const=True, default=False),
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
