from __future__ import annotations

import contextlib
from dataclasses import dataclass
from email.message import Message
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import async_lru
import msgspec
from httpx import AsyncClient as HTTPXAsyncClient

from .version import Version

CACHE_PATH = Path("~/.cache/backpack").expanduser()
CACHE_PATH.mkdir(parents=True, exist_ok=True)

httpx = HTTPXAsyncClient(follow_redirects=True)


@dataclass(slots=True, frozen=True)
class Package:
    username: str
    reponame: str


@async_lru.alru_cache(maxsize=None)
async def fetch_package(package: Package, version: Version) -> Path:
    path = CACHE_PATH.joinpath(package.username, package.reponame, str(version))
    if path.exists():
        return path
    path.parent.mkdir(parents=True)
    url = f"https://api.github.com/repos/{package.username}/{package.reponame}/zipball/refs/tags/v{version}"
    response = await httpx.get(url)
    msg = Message()
    msg["content-disposition"] = response.headers["content-disposition"]
    filename = msg.get_filename()
    assert filename is not None
    body = await response.aread()
    with ZipFile(BytesIO(body)) as f:
        f.extractall(path.parent)
    path.parent.joinpath(filename).rename(path)
    return path


@async_lru.alru_cache(maxsize=None)
async def fetch_versions(package: Package) -> list[Version]:
    url = f"https://api.github.com/repos/{package.username}/{package.reponame}/tags"
    response = await httpx.get(url)
    body = msgspec.json.decode(await response.aread())
    versions = []
    for tag in body:
        with contextlib.suppress(ValueError):
            version = Version.parse(tag["name"].removeprefix("v"))
            versions.append(version)
    versions.sort()
    return versions
