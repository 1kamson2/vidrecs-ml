import asyncio
from typing import Any, Dict
from model.model import VRModel
from utils.io import json2dict, obs2json
from utils.enums import Actions


async def server_handle_request(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, model: VRModel
) -> None:
    data = await reader.read()
    message: str = data.decode()
    # content: str is VERY UNSAFE (no sanitization) use wisely and get rid of
    # ASAP
    print(message)
    content: str = message.split("\n")[-1]
    content_tgt: Dict = json2dict(content)
    action: Actions = (
        Actions.UPVOTE if content_tgt["action"] == "like" else Actions.DOWNVOTE
    )
    obs = model.run_user_choice(action)
    addr: Any = writer.get_extra_info("peername")
    print(
        f"[INFO] Server received the following content: {content}\n       From: {addr!r}."
    )

    json2send = obs2json(obs)
    print(json2send)
    writer.write(json2send.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def server_main(config: Dict, model: VRModel) -> None:
    req_handler = lambda reader, writer: server_handle_request(reader, writer, model)
    server = await asyncio.start_server(req_handler, config["host"], config["port"])
    addrs = ":".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[INFO] Working on: {addrs}")

    async with server:
        await server.serve_forever()
