from __future__ import annotations

from dataclasses import dataclass
from typing import Self, override


@dataclass(slots=True, frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, text: str) -> Self:
        parts = text.split(".")
        if len(parts) != 3:
            msg = "Malformed version number."
            raise ValueError(msg)
        nums = [int(part) for part in parts]
        if any(num < 0 for num in nums):
            msg = "Malformed version number."
            raise ValueError(msg)
        return cls(*nums)

    @override
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
