import logging
from pathlib import Path


def logger_builder(name: str, path: Path) -> logging.Logger:
    """
        Builder for loggers.

        Arguments:
            name: filename that will be used in logging.

        Returns:
            Logger.
    """
    filename = Path(name.strip("_") + ".log")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        filename=path.joinpath(filename), level=logging.INFO, format=format
    )
    logger = logging.getLogger(name)
    logger.info(f"[INFO] Logs for '{name}' will be saved in '{path}'")
    return logger
