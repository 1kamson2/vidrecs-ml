import argparse
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict
import numpy as np
from json_parsing import deserialize

class Config:
    __prog: str = "Game Recommendation Model." 
    __desc: str = "Reinforcement Learning (RL) game recommendation system."
    __epil: str = """Arguments passed here have the higher priority than those
    specified in the configuration file.""" 
    __MODE_CHOICES = np.array(
        ["train", "validation", "test", "inference"],
        dtype=str
    ) 
    __CONFIG_FILE_PATH = Path("resource/cfg/config.json")

    def __init__(self):
        """
            Handling for the application's config and arguments.

            Attributes:
                parser: Parser which handles arguments.
                content: Final config.
        """
        self.parser: ArgumentParser = self.__set_parser()
        args = self.parser.parse_args()
        self.content: Dict = self.__finalize(args)

    def __set_parser(self) -> ArgumentParser:
        """
            Initialize parser for handling arguments.

            Returns:
                Parser.
        """
        parser = argparse.ArgumentParser(
            prog=self.__prog,
            description=self.__desc,
            epilog=self.__epil,
        )
        parser.add_argument(
            "name", 
            help="Specify the database name.", 
            type=str
        )
        parser.add_argument(
            "user", 
            help="Specify the database username.", 
            type=str
        )
        parser.add_argument(
            "mode", 
            help="Specify in what mode should the model run.", 
            type=str
        )
        return parser

    def __finalize(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
            Validate JSON config and arguments from a parser and normalize
            config.

            Arguments:
                args: Parser arguments.

            Returns:
                Config object.
        """
        config = deserialize(self.__CONFIG_FILE_PATH)

        assert len(config["db"]["name"]) > 0, (
            f"[ERROR] '{config['db']['name']}' is not a correct variable."
        ) 
        config["db"]["name"] = args.name

        assert len(args.user) > 0, (
            f"[ERROR] '{config['db']['user']}' is not a correct variable."
        ) 
        config["db"]["user"] = args.user

        assert len(args.mode) > 0 and args.mode in self.__MODE_CHOICES,(
            f"[ERROR] '{config['model']['mode']}' is not a correct variable."
        ) 
        config["model"]["mode"] = args.mode
        return config

    def __getitem__(self, key: str) -> Any:
        if key in self.content.keys():
            return self.content[key]
        else:
            raise KeyError(f"'{key}' doesn't exist.")
