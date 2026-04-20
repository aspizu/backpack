from backpack._logging import setup_logging

from .cli import cli


def main() -> None:
    setup_logging()
    cli()
