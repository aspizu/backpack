from __future__ import annotations

import asyncio

from .sync import sync

asyncio.run(sync())
