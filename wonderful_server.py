import random
import socket
import threading
from uuid import uuid4
import uvicorn
from fastapi import FastAPI



class WonderfulServer(threading.Thread):
    """
    The server instance that the Agent creating
    All the attributes with '_' because no one need to change them
    The property give the agent the ability to use the port and the id
    """
    def __init__(self, response: str) -> None:
        self._id: str = str(uuid4())
        self._port: int = random.randint(8001, 9999)
        self._server = FastAPI()
        self._response = response

        threading.Thread.__init__(self)

        @self._server.get("/")
        async def name_it():
            return {"message": self._response}


    def run(self):
        print(f"You can see the server swagger by insrt {socket.gethostbyname(socket.gethostname())}:{self._port}/docs into your browser")
        uvicorn.run(self._server, host=socket.gethostbyname(socket.gethostname()), port=self._port)


    @property
    def id(self) -> str:
        return self._id

    @property
    def port(self) -> int:
        return self._port
