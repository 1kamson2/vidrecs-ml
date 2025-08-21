from model.model import VRModel
from utils.config.argument_parsing import Config
from utils.listener import server_main
import threading
import asyncio


def main() -> None:
    config = Config() 
    # WARNING: This might not work, backtrack there if fails.
    model = VRModel(**config.content)
    # model.run()
    server_thread = threading.Thread(
        target=lambda: asyncio.run(server_main(config.content["listener"], model))
    )
    server_thread.start()


if __name__ == "__main__":
    main()
