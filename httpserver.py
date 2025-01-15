from fastapi import FastAPI
import socket
import json

app = FastAPI()

# Connect to a TCP server that calculates the distance


def get_distance_from_tcp_server(rssi):
    # Connection to the TCP server
    server_ip = '127.0.0.1'  # IP address of the TCP server (if using the same machine)
    server_port = 12345       # TCP server port

    # Connect to the TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))  # Connects to the TCP server
        client_socket.sendall(str(rssi).encode('utf-8'))  # Sends the RSSI

        # Receives the response from the server
        data = client_socket.recv(1024)
        return data.decode('utf-8')


@app.post("/send-rssi/")
async def receive_rssi(rssi: float):
    """Function that receives the RSSI and returns the distance status"""
    distance_status = get_distance_from_tcp_server(rssi)  # Sends the RSSI to the TCP server
    return {"rssi": rssi, "distance_status": distance_status}

@app.get("/health")
async def health_check():
    return {"status": "Server is running!"}
