import pickle
from pathlib import Path
from typing import Any, Dict, Tuple
import json


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


def json2dict(json_info: Path | str) -> Dict:
    try:
        if isinstance(json_info, Path):
            with open(json_info, "r") as _json:
                _dict = json.load(_json)
            return _dict
        if isinstance(json_info, str):
            _dict = json.loads(json_info)
            return _dict

    except (FileNotFoundError, TypeError) as e:
        print(e)
        exit(1)


def obs2json(obs: Tuple) -> str:
    if len(obs) != 6:
        print("[ERROR] Your observation is incomplete or has incorrect dimensions.")
        return ""
    id, imdbid, title, genres, nratings, nusers = obs
    dict2json = {
        "id": id,
        "imdbid": imdbid,
        "title": title,
        "genres": genres,
        "nratings": nratings,
        "nusers": nusers,
    }
    return json.dumps(dict2json)
