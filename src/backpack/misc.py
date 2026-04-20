from pathlib import Path

CACHE_DIR = Path("~/.local/share/backpack").expanduser()
CACHE_DIR.mkdir(parents=True, exist_ok=True)
