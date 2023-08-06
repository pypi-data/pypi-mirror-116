import asyncio
import socket


class Reader:
    """
    Wraps asyncio.StreamReader
    """
    def __init__(self, reader):
        self.__reader = reader

    async def read(self) -> bytes:
        """
        Read frame from stream
        """
        header = await self.__reader.readexactly(4)
        length = int.from_bytes(header, byteorder='big', signed=False)
        return await self.__reader.readexactly(length)


class Writer:
    """
    Wraps asyncio.StreamWriter
    """
    def __init__(self, writer):
        self.__writer = writer

    def write(self, payload: bytes):
        """
        Write payload to stream
        """
        header = len(payload).to_bytes(4, byteorder='big')
        self.__writer.write(header)
        self.__writer.write(payload)

    async def drain(self):
        """
        Flush the write buffer.
        """
        await self.__writer.drain()

    async def close(self):
        """
        Close stream with confirmation
        """
        self.__writer.close()
        await self.__writer.wait_closed()

    def close_nowait(self):
        """
        Close stream without confirmation
        """
        self.__writer.close()

    def is_closing(self):
        """
        Check if stream closed
        """
        return self.__writer.is_closing()


class Server:
    """
    Wraps TCP server
    """
    def __init__(self, handle, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__handle = handle

    async def __my_handle(self, reader, writer):
        await self.__handle(Reader(reader), Writer(writer))

    async def run(self, loop=None):
        """
        Run server
        """
        server = await asyncio.start_server(self.__my_handle, self.__host, self.__port, loop=loop)
        async with server:
            await server.serve_forever()


async def connect(host: str, port: int, loop=None) -> (Reader, Writer):
    """
    Connect to SFP over TCP server
    Returns socket reader and writer objects
    """
    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    return Reader(reader), Writer(writer)

if hasattr(socket, 'AF_UNIX'):
    class ServerUnix:
        """
        Wraps unix domain socket server
        """
        def __init__(self, handle, path: str):
            self.__path = path
            self.__handle = handle

        async def __my_handle(self, reader, writer):
            await self.__handle(Reader(reader), Writer(writer))

        async def run(self, loop=None):
            """
            Run server
            """
            server = await asyncio.start_unix_server(self.__my_handle, self.__path, loop=loop)
            async with server:
                await server.serve_forever()


    async def connect_unix(path: str, loop=None) -> (Reader, Writer):
        """
        Connect to SFP over unix domain socket server
        Returns socket reader and writer objects
        """
        reader, writer = await asyncio.open_unix_connection(path, loop=loop)
        return Reader(reader), Writer(writer)
