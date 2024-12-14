# README

## Overview
This project is a FastAPI-based agent system that allows you to:
1. **Create new servers** by sending a GET request to the agent.
2. **Communicate with specific servers** by their UUID(client request to agent->to server, response: server-> agent->client).
3. **Retrieve server interaction data** from the database.

The system tracks the number of requests each client sends to a specific server and stores this information in a SQLite database.

---

## Installation Instructions

### 1. Clone the Repository
```bash
# Clone the project repository
$ git clone <repository_url>

# Navigate to the project directory
$ cd <repository_directory>
```

### 2. Create a Virtual Environment (Optional, but Recommended)
```bash
# Create a virtual environment
$ python3 -m venv venv

# Activate the virtual environment
# On Windows:
$ venv\Scripts\activate
# On macOS/Linux:
$ source venv/bin/activate
```

### 3. Install Dependencies
The project dependencies are listed in the `requirements.txt` file. Install them using:
```bash
$ pip install -r requirements.txt
```

---

## Running the Agent

1. Open a terminal and navigate to the project directory.

2. Run the agent using the following command:
```bash
$ python agent.py
```

3. Once the server starts, the terminal will display the IP address where you can access the Swagger documentation. For example:
```
You can see the server swagger by inserting <IP_ADDRESS>:8000/docs into your browser
```
Replace `<IP_ADDRESS>` with the actual IP shown in the terminal output.

---

## API Endpoints

### 1. Create a New Server
**Endpoint:** `/`

**Method:** `GET`

**Description:** Creates a new server instance and returns its UUID.

**Example Request (Using cURL):**
```bash
curl -X GET http://<IP_ADDRESS>:8000/
```

**Example Response:**
```json
{
    "uuid": "56d28b89-2377-4d08-a84b-65f88968285f"
}
```

---

### 2. Communicate with a Specific Server
**Endpoint:** `/{id}`

**Method:** `GET`

**Description:** Sends a request to the server identified by the UUID and retrieves its response. The system also updates the database to increment the request count for the client-server pair.

**Parameters:**
- `id`: UUID of the server.

**Example Request (Using cURL):**
```bash
curl -X GET http://<IP_ADDRESS>:8000/56d28b89-2377-4d08-a84b-65f88968285f
```

**Example Response:**
```json
{
    "message": "Or Barak"
}
```

---

### 3. Retrieve Database Records
**Endpoint:** `/database`

**Method:** `GET`

**Description:** Returns all rows from the `server_table` database. Each row includes the `client_ip`, `server_id`, and `request_count`.

**Example Request (Using cURL):**
```bash
curl -X GET http://<IP_ADDRESS>:8000/database
```

**Example Response:**
```json
[
    {
        "client_ip": "127.0.0.1",
        "server_id": "56d28b89-2377-4d08-a84b-65f88968285f",
        "request_count": 3
    },
    {
        "client_ip": "192.168.1.1",
        "server_id": "c8a45623-84b7-4e8b-9af9-38372a32d6b5",
        "request_count": 1
    }
]
```

---

## Additional Notes

- The **Swagger Documentation** is available at `http://<IP_ADDRESS>:8000/docs`. It provides an interactive UI to test all the endpoints.

- The SQLite database file (`servers.db`) is automatically created in the project directory. If the file exists when the server starts, it will be deleted and recreated.

- To reset the system, stop the agent, delete the `servers.db` file manually (if necessary), and restart the agent.

---

## Troubleshooting

1. **Database Not Found**:
   If you see the error `Database file not found`, ensure that the agent is started without any conflicting processes and that the working directory is correct.

2. **Dependencies Missing**:
   Run the following to ensure all dependencies are installed:
   ```bash
   $ pip install -r requirements.txt
   ```

3. **Port Already in Use**:
   If port `8000` is already in use, you can modify the port in the `uvicorn.run()` call in `agent.py`:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=<NEW_PORT>)
   ```

