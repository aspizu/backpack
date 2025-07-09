from __future__ import annotations

import shutil
from pathlib import Path

import msgspec

from backpack.package import Package, fetch_package
from backpack.solver import Solution, load_requirements, solve
from backpack.version import Version


def load_lockfile(path: Path) -> Solution:
    entries = msgspec.json.decode(path.joinpath("backpack-lock.json").read_bytes())
    solution: Solution = {}
    for entry in entries:
        version = Version.parse(entry["version"])
        solution[Package(entry["username"], entry["reponame"])] = version
    return solution


async def sync() -> None:
    path = Path()
    backpack_path = path.joinpath("backpack")
    shutil.rmtree(backpack_path, ignore_errors=True)
    backpack_path.mkdir(parents=True)
    backpack_path.joinpath(".gitignore").write_text("*\n")
    requirements = load_requirements(path)
    try:
        solution = load_lockfile(path)
    except FileNotFoundError:
        solution = await solve(requirements)
    for package, version in solution.items():
        package_path = await fetch_package(package, version)
        link_path = backpack_path.joinpath(package.username, package.reponame)
        link_path.parent.mkdir()
        link_path.symlink_to(package_path, target_is_directory=True)
