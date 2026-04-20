import logging
import sys
from typing import TYPE_CHECKING

from rich import print

from .requirements import bkpk_requirement

if TYPE_CHECKING:
    from .requirements.base_requirement import BaseRequirement

log = logging.getLogger(__name__)


def _check_tree(
    requirement: BaseRequirement,
    out: list[BaseRequirement],
    visited: set[BaseRequirement] | None = None,
) -> None:
    if visited is None:
        visited = set()
    if requirement in visited:
        return
    visited.add(requirement)
    out.append(requirement)
    for dependency in requirement.dependencies:
        _check_tree(dependency, out, visited)


def _fix_tree(
    requirement: BaseRequirement,
    ok: set[BaseRequirement],
    out: list[BaseRequirement],
    visited: set[BaseRequirement] | None = None,
) -> None:
    if visited is None:
        visited = set()

    # 1. Skip if already healthy or already slated for a fix
    if requirement in ok or requirement in visited:
        return

    # 2. Mark as visited immediately to catch circular dependencies
    visited.add(requirement)

    # 3. Process dependencies first (Depth-First)
    for dependency in requirement.dependencies:
        _fix_tree(dependency, ok, out, visited)

    # 4. Finally, add the current requirement to the fix list
    # Because of the recursion above, this only happens AFTER
    # all its dependencies are already in 'out' or 'ok'.
    if requirement not in out:
        out.append(requirement)


def doctor(fix: str | bool) -> None:

    check_tree = []
    _check_tree(bkpk_requirement, check_tree)
    if isinstance(fix, str):
        fix = fix.lower()
        for requirement in check_tree:
            if requirement.id == fix:
                is_ok, _msg = requirement.check()
                if is_ok:
                    log.error("requirement '%s' is already satisfied", fix)
                    sys.exit(1)
                requirement.fix()
                return
        log.error("requirement '%s' not found", fix)
        sys.exit(1)
    ok = set()
    error = set()
    warning = set()
    for requirement in check_tree:
        is_ok, message = requirement.check()
        if is_ok:
            print("   [green]OK[/green]", message)
            ok.add(requirement)
        elif requirement.is_optional:
            print(" [yellow]WARN[/yellow]", message)
            warning.add(requirement)
        else:
            print("[red]ERROR[/red]", message)
            error.add(requirement)
    if fix:
        fix_tree = []
        _fix_tree(bkpk_requirement, ok, fix_tree)
        for requirement in fix_tree:
            requirement.fix()
    elif len(error) > 0:
        print("\nRun [blue]bkpk doctor --fix[/] to attempt to fix the issues.")
