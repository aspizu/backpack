from .command_requirement import CommandRequirement
from .rustup_requirement import NightlyRequirement
from .uv_requirement import UvRequirement

git_requirement = CommandRequirement("git")
wget_requirement = CommandRequirement("wget")
uv_requirement = UvRequirement()
nightly_requirement = NightlyRequirement()
bkpk_requirement = CommandRequirement(
    "bkpk",
    check_version=True,
    dependencies=[
        uv_requirement,
        git_requirement,
        wget_requirement,
        nightly_requirement,
    ],
)
