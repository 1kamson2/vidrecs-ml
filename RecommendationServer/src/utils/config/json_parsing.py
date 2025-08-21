from pathlib import Path
from typing import Dict
import json

def deserialize(json_: Path | str) -> Dict:
    """
        Deserialize JSON as a file or string to a Dictionary.

        Arguments:
            json_: Either string or file.

        Returns:
            The representation of JSON as dictionary.
    """
    try:

        if isinstance(json_, Path):
            with open(json_, "r") as json_obj:
                deser_dict = json.load(json_obj)
            return deser_dict

        if isinstance(json_, str):
            deser_dict = json.loads(json_)
            return deser_dict

    except (FileNotFoundError, TypeError) as e:
        print(e)
        exit(1)


def serialize(**kwargs) -> str:
    """
        Serialize (key: value) arguments to a JSON.

        Arguments:
            **kwargs: (key: value) arguments. 

        Returns:
            JSON representation of (key: value) arguments
    """
    return json.dumps(kwargs)
