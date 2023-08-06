# PySFP
Python implementation of [Simple Frame Protocol](https://github.com/xenocorn/SFP/blob/master/README.md)
over TCP and unix domain sockets
## Instalation
    $ pip install sfp
## Usage
### Client
```Python
from asyncio import get_event_loop
from sfp import sfp

# Use tcp socket on non unix OS
URI = "tcp://localhost"

# Or use unix domain socket
if 'unix' in sfp.AVAILABLE_SCHEMES:
    URI = "unix:///tmp/example.sock"
    
async def main():
    reader, writer = await sfp.connect_to_uri(URI)
    try:
        async with writer:
            writer.write("SOME DATA".encode())
            data = await reader.read()
            print(data.decode())
    except:
        pass # Connection closed unexpectedly

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
```     
## Server
```Python
from asyncio import get_event_loop
from sfp import sfp

# Use tcp socket on non unix OS
URI = "tcp://localhost"

# Or use unix domain socket
if 'unix' in sfp.AVAILABLE_SCHEMES:
    URI = "unix:///tmp/example.sock"

async def handle(reader: sfp.Reader, writer: sfp.Writer):
    # Connection accepted
    try:
        async with writer:
            data = await reader.read()
            print(data.decode())
            writer.write("SOME DATA".encode())
            await writer.drain()
    except:
        pass # Connection closed unexpectedly

async def main():
    reader, writer = await sfp.connect_to_uri(URI)
    writer.write("SOME DATA".encode())
    data = await reader.read()
    print(data.decode())
    await writer.close()

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
```     
Also see [examples](https://github.com/xenocorn/PySFP/tree/master/examples)
