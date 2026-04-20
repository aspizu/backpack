from abc import ABC, abstractmethod


class BaseRequirement(ABC):
    id: str
    dependencies: list[BaseRequirement]
    is_optional: bool

    def __init__(
        self,
        dependencies: list[BaseRequirement] | None = None,
        is_optional: bool = False,
    ) -> None:
        self.dependencies = dependencies or []
        self.is_optional = is_optional

    @abstractmethod
    def check(self) -> tuple[bool, str]: ...

    @abstractmethod
    def fix(self) -> None: ...
