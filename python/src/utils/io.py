import pickle
from pathlib import Path
from typing import Any


def pkl_save(obj: Any, filename: str, path: Path) -> None:
    filename = filename + ".pkl" if filename[-4:] != ".pkl" else filename
    try:
        file2path: Path = Path(filename)
        with open(path.joinpath(file2path), "wb") as pkl:
            pickle.dump(obj, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        print("[ERROR] pkl_save(): File saved.")
    except (TypeError, FileNotFoundError, RuntimeError) as e:
        print(e)
        exit(1)


def pkl_load(filename: str, path: Path) -> Any:
    filename = filename + ".pkl" if filename[-4:] != ".pkl" else filename
    try:
        file2path: Path = Path(filename)
        with open(path.joinpath(file2path), "rb") as pkl:
            obj: Any = pickle.load(pkl)
        print("[ERROR] pkl_save(): File loaded.")
        return obj
    except (TypeError, FileNotFoundError, RuntimeError) as e:
        print(e)
        exit(1)
