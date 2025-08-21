import pickle
from pathlib import Path
from typing import Any

# TODO: Switch prints to logging

def serialize(obj: Any, filename: str, path: Path) -> None:
    if not filename.find(".pkl"):
        print(f"[ERROR] serialize(): {filename} doesn't contain pickle extension.")
    try:
        file_path: Path = Path(filename)
        with open(path.joinpath(file_path), "wb") as pkl:
            pickle.dump(obj, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        print("[INFO] serialize(): File saved.")
    except (TypeError, FileNotFoundError, RuntimeError) as e:
        print(e)
        exit(1)


def deserialize(filename: str, path: Path) -> Any:
    if not filename.find(".pkl"):
        print(f"[ERROR] deserialize(): {filename} doesn't contain pickle extension.")
    try:
        file_path: Path = Path(filename)
        with open(path.joinpath(file_path), "rb") as pkl:
            obj: Any = pickle.load(pkl)
        print("[INFO] pkl_save(): File loaded.")
        return obj
    except (TypeError, FileNotFoundError, RuntimeError) as e:
        print(e)
        exit(1)



