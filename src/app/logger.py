"""
Logging configuration tập trung.
Import logger này thay vì dùng print() ở bất kỳ đâu trong project.

Usage:
    from app.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened")
    logger.error("Something failed", exc_info=True)
"""

import logging
import sys
from typing import Optional


LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO") -> None:
    """
    Gọi một lần duy nhất ở startup (trong lifespan).
    level: "DEBUG" | "INFO" | "WARNING" | "ERROR"
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),   # in ra console
        ],
    )

    # Giảm noise từ các thư viện bên thứ 3
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("passlib").setLevel(logging.ERROR)


def get_logger(name: str) -> logging.Logger:
    """
    Trả về logger với tên module.
    Dùng: logger = get_logger(__name__)
    """
    return logging.getLogger(name)