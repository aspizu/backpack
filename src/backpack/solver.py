from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING

from backpack.package import Package, fetch_package, fetch_versions

from .requirement import Requirement

if TYPE_CHECKING:
    from pathlib import Path

    from .version import Version


def load_requirements(path: Path) -> dict[str, Requirement]:
    with path.joinpath("goboscript.toml").open("rb") as f:
        config = tomllib.load(f)
    requirements: dict[str, Requirement] = {}
    for key, value in config.get("requirements", {}):
        requirements[key] = Requirement.parse(value)
    return requirements


type Solution = dict[Package, Version]


# AI generated
async def solve(
    initial_requirements: dict[str, Requirement],
) -> Solution:
    solution: Solution = {}
    visited: set[Package] = set()

    async def resolve(requirement: Requirement) -> None:
        key = requirement.package

        if key in visited:
            return  # Prevent cycles

        visited.add(key)

        # Fetch all versions and pick the latest that matches major_version
        versions = await fetch_versions(requirement.package)
        compatible_versions = [
            v for v in versions if v.major == requirement.major_version
        ]
        if not compatible_versions:
            msg = f"No compatible versions found for {key} with major version {
                requirement.major_version
            }"
            raise ValueError(msg)

        latest_version = max(compatible_versions)

        # If not already added or if this version is newer, update solution
        if key not in solution or solution[key] < latest_version:
            solution[key] = latest_version

            # Fetch package and load its requirements recursively
            package_path = await fetch_package(requirement.package, latest_version)
            new_requirements = load_requirements(package_path)

            for new_req in new_requirements.values():
                await resolve(new_req)

    # Start resolving for all initial requirements
    for req in initial_requirements.values():
        await resolve(req)

    return solution
