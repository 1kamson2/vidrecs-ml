import asyncio
from typing import Any, Dict


async def server_handle_request(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    data = await reader.read()
    message: str = data.decode()
    addr: Any = writer.get_extra_info("peername")
    print(f"[INFO] Server received: {message}\n       From: {addr!r}.")
    writer.close()
    await writer.wait_closed()


async def server_main(config: Dict) -> None:
    server = await asyncio.start_server(
        server_handle_request, config["host"], config["port"]
    )
    addrs = ":".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[INFO] Working on: {addrs}")

    async with server:
        await server.serve_forever()
