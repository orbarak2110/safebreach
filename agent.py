import json
import os
from http.client import HTTPConnection
import names
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import threading
from sqlalchemy.orm import sessionmaker, close_all_sessions
from server_table import ServerTable, engine
from wonderful_server import WonderfulServer
import socket


app = FastAPI()
# list to store UUID
servers: list[WonderfulServer] = []
_update_lock = threading.Lock()


@app.get("/")
async def initialize_server(request: Request):
    """
    Create a new server only when a GET request is received,
    and communicate with it from the agent.
    """

    server = WonderfulServer(names.get_full_name()) # Creating server instance with data(a random name)
    server.start() # Start the server(the start will call the run method)
    servers.append(server) # store the new server inside the list for the agent
    return JSONResponse(content={"uuid": server.id}) # response to the client with the uuid of the new server


@app.get("/database")
async def get_database_table():
    """
    Getting the table from db. for every server and client ip there is a counter.
    Example: a client sent 3 request to specific server:
    {'client_ip': '127.0.0.1', 'request_count': 3, 'server_id': '56d28b89-2377-4d08-a84b-65f88968285f'}
    """
    with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as db:
        # Query all rows in the server_table
        records = db.query(ServerTable).all()

        # Convert rows to list[dict]
        result = [
            {

                "client_ip": record.client_ip,
                "server_id": record.server_id,
                "request_count": record.request_count,
            }
            for record in records
        ]

    return JSONResponse(content=result)

@app.api_route("/{id}", methods=["GET"])
async def communicate_with_server(id: str, request: Request):
    """
    The ability of the agent to talk with each server.
    """
    try:
        server = next(ser for ser in servers if ser.id == id) #The agent will verify the uuid that came from the client
    except StopIteration:
        raise HTTPException(status_code=404, detail=f"Server with UUID, {id} does not exist")

    with _update_lock: # Using lock to wait the counter will do ++1
        with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as db:
            record = db.query(ServerTable).filter(ServerTable.server_id == id).filter(ServerTable.client_ip == request.client.host).first() # If the row with the server id and the client ip exist the counter will do ++1
            if not record:
                record = ServerTable(server_id=id, client_ip=request.client.host, request_count=1) # If not exist will store with 1(the first request to the server id(uuid)
            else:
                record.request_count += 1
            db.add(record)
            db.commit()

    connection = HTTPConnection("localhost", port=server.port)
    connection.request("GET", "/") # Here the server will send a request to the server
    data = connection.getresponse().read() # Agent getting the response from the server(bytes)
    return json.loads(data) # Convert to dict






if __name__ == "__main__":
    print(f"You can see the server swagger by insrt {socket.gethostbyname(socket.gethostname())}:8000/docs into your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    database_file = "servers.db"  # Path to the database file
    if os.path.exists(database_file):
        # Close all active sessions for the db
        close_all_sessions()

        # Delete the file(db file)
        os.remove(database_file)
    else:
        raise HTTPException(status_code=404, detail="Database file not found.")
