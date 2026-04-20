import logging
import os

from rich.logging import RichHandler

from .misc import CACHE_DIR


class NoTracebackFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if os.getenv("TRACE") in ["1", "true"]:
            return super().format(record)
        record = logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=record.msg,
            args=record.args,
            exc_info=None,
            func=record.funcName,
            sinfo=record.stack_info,
        )
        record.exc_info = None
        return super().format(record)


def setup_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
    file_handler = logging.FileHandler(CACHE_DIR.joinpath("log.txt"), encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter(
            "[%(levelname)s] %(asctime)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    rich_handler = RichHandler(
        rich_tracebacks=False,
        enable_link_path=False,
        show_time=False,
    )
    rich_handler.setFormatter(NoTracebackFormatter("%(message)s"))
    rich_handler.setLevel(log_level)
    logging.basicConfig(level=log_level, handlers=[rich_handler, file_handler])
