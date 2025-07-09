from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Self, override

from .package import Package

REQUIREMENT_RE = re.compile(r"(.*?)/(.*?)==(\d+)\.\*\.\*")


@dataclass(slots=True, frozen=True)
class Requirement:
    package: Package
    major_version: int

    @override
    def __str__(self) -> str:
        return (
            f"{self.package.username}/{self.package.reponame}=={self.major_version}.*.*"
        )

    @classmethod
    def parse(cls, text: str) -> Self:
        match = REQUIREMENT_RE.fullmatch(text)
        if match is None:
            msg = "Malformed requirement string."
            raise ValueError(msg)
        return cls(Package(match.group(1), match.group(2)), int(match.group(3)))
