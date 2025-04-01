import logging
from pathlib import Path


def logger_builder(name: str, path: Path) -> logging.Logger:
    """
    Parameters:
        - name: this should be the name of file ('__name__'), filename will be
          used but stripped of '_'
    Function:
        This function builds the logger.
    """
    filename = Path(name.strip("_") + ".log")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        filename=path.joinpath(filename), level=logging.INFO, format=format
    )
    logger = logging.getLogger(name)
    print(f"[INFO] Logs for '{name}' will be saved in '{path}'")
    return logger
