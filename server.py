import socket


# Function that converts RSSI to distance
def classify_distance(rssi):
    """Function that determines if the computer is close or far based on RSSI"""
    if rssi > -30:
        return "Very Close"
    elif rssi > -50:
        return "Close"
    else:
        return "Far"


def start_server(host='0.0.0.0', port=12345):
    """Function that starts the server and waits for a connection"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is waiting for connection on {host}:{port}...")

    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    return client_socket


def handle_client(client_socket):
    """Function that handles client messages and calculates the distance"""
    while True:
        try:
            data = client_socket.recv(1024)  # Receives data from the client
            if not data:
                break  # If no data, exit the loop
            rssi = float(data.decode('utf-8'))  # Converts the data to RSSI
            distance_status = classify_distance(rssi)  # Determines if the computer is close or far
            print(f"Received RSSI: {rssi} dB - {distance_status}")
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()


if __name__ == "__main__":
    while True:
        client_socket = start_server()  # Starts the server and waits for a connection
        handle_client(client_socket)  # Handles the client
