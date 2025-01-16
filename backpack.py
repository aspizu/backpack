import argparse
import shutil
import subprocess
from pathlib import Path

import toml


class Backpack:
    def __init__(self, backpack: Path):
        self.backpack = backpack
        self.fetched = set()

    def fetch_dependency(self, name: str, dependency: str):
        if name in self.fetched:
            return
        self.fetched.add(name)
        url, version = dependency.rsplit("@", 1)
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                version,
                url,
                self.backpack.joinpath(name),
            ],
            check=False,
        ).check_returncode()

    def fetch_dependencies(self, dependencies: dict[str, str]):
        for name, dependency in dependencies.items():
            self.fetch_dependency(name, dependency)
            submanifest = backpack.joinpath(name).joinpath("goboscript.toml")
            if submanifest.exists():
                submanifest = toml.load(submanifest.open())
                self.fetch_dependencies(submanifest["dependencies"])


parser = argparse.ArgumentParser()
parser.add_argument("input", type=Path)
args = parser.parse_args()
input: Path = args.input.absolute()
manifest = toml.load(input.joinpath("goboscript.toml").open())
dependencies = manifest["dependencies"]
backpack = input.joinpath("backpack")
shutil.rmtree(backpack, ignore_errors=True)
backpack.mkdir()
backpack.joinpath(".gitignore").write_text("*")
Backpack(backpack).fetch_dependencies(dependencies)
