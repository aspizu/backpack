from backpack.cli.doctor.requirements.optional_tool_requirement import (
    OptionalToolRequirement,
)

from .command_requirement import CommandRequirement
from .rustup_requirement import NightlyRequirement
from .uv_requirement import UvRequirement

git_requirement = CommandRequirement("git")
wget_requirement = CommandRequirement("wget")
uv_requirement = UvRequirement()
nightly_requirement = NightlyRequirement()
sb2gs_requirement = OptionalToolRequirement(
    "sb2gs", git="https://github.com/aspizu/sb2gs"
)
bkpk_requirement = CommandRequirement(
    "bkpk",
    check_version=True,
    dependencies=[
        uv_requirement,
        git_requirement,
        wget_requirement,
        nightly_requirement,
        sb2gs_requirement,
    ],
)
