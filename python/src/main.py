import argparse
import json
from pathlib import Path
from typing import Any, Dict
from utils.listener import server_main
import asyncio
import threading

# [WARNING]: DO NOT REUSE THOSE VARIABLES, THOSE ARE MADE TO USE ONLY IN THIS
# FILE
__MODE_CHOICES = ["train", "validation", "test", "inference"]
__CONFIG_FILE_PATH = Path("resource/cfg/config.json")


def args_validation(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Parameters:
        - args: This parameter should contain user's passed parameters.
    This function validates what user passed, also does some config's
    variables normalization, that wasn't possible on JSON's level.
    """
    with open(__CONFIG_FILE_PATH, "r") as config_file:
        config = json.load(config_file)

    # Check if the variables are correct
    if len(args.name) > 0:
        config["db"]["name"] = args.name
    elif len(config["db"]["name"]) <= 0:
        print(f"[ERROR] '{config['db']['name']}' is not a correct variable")
        exit(1)

    if len(args.user) > 0:
        config["db"]["user"] = args.user
    elif len(config["db"]["user"]) <= 0:
        print(f"[ERROR] '{config['db']['user']}' is not a correct variable")
        exit(1)

    if len(args.mode) > 0 and args.mode in __MODE_CHOICES:
        config["model"]["mode"] = args.mode
    elif config["model"]["mode"] not in __MODE_CHOICES:
        print(f"[ERROR] '{config['model']['mode']}' is not a correct variable")
        exit(1)

    # Normalize all variables
    try:
        config["paths"]["resource"] = Path(config["paths"]["resource"])
        config["paths"]["source"] = Path(config["paths"]["source"])
        config["paths"]["utils"] = Path(config["paths"]["utils"])
        config["paths"]["links"] = Path(config["paths"]["links"])
        config["paths"]["movies"] = Path(config["paths"]["movies"])
        config["paths"]["ratings"] = Path(config["paths"]["ratings"])
        config["paths"]["tags"] = Path(config["paths"]["tags"])
        config["paths"]["queries"] = Path(config["paths"]["queries"])
        config["paths"]["cfg"] = Path(config["paths"]["cfg"])
    except ValueError as e:
        print(e)
        exit(1)
    return config


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Video Recommendation Model",
        description="Show user the best recommendations of movies, "
        "using Reinforcement Learning method.",
        epilog="Arguments passed through, have the higher priority, "
        "than those specified in the config.",
    )

    parser.add_argument("name", help="Specify the database name.", type=str)
    parser.add_argument("user", help="Specify the database username.", type=str)
    parser.add_argument(
        "mode", help="Specify in what mode should the model run.", type=str
    )
    args = parser.parse_args()
    full_config = args_validation(args)
    # model = VRModel(**full_config)
    # model.run()
    server_thread = threading.Thread(
        target=lambda: asyncio.run(server_main(full_config["listener"]))
    )
    server_thread.start()


if __name__ == "__main__":
    main()
