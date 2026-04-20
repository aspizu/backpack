from abc import ABC, abstractmethod


class BaseRequirement(ABC):
    dependencies: list[BaseRequirement]

    def __init__(self, dependencies: list[BaseRequirement] | None = None) -> None:
        self.dependencies = dependencies or []

    @abstractmethod
    def check(self) -> tuple[bool, str]: ...

    @abstractmethod
    def fix(self) -> None: ...
