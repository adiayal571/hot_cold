import socket
import time
import sounddevice as sd
import numpy as np
import requests

# Function to calculate RSSI
def calculate_rssi(data):
    rms = np.sqrt(np.mean(np.square(data)))  # Calculate RMS
    rssi = 20 * np.log10(rms)  # Convert RMS to RSSI (in decibels)
    return rssi

# Function to record sound using sounddevice
def record_sound(duration=1.0):
    sample_rate = 18000  # Sample rate (Hz)
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to finish
    return recording.flatten()  # Return the recording as a one-dimensional array

# Connect to the server and send RSSI
def connect_to_server(host='172.30.149.72', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # Connect to the server
    print(f"Connected to server at {host}:{port}")
    return client_socket

# Continuously send RSSI to the server
def send_rssi_to_server(client_socket):
    while True:
        sound_data = record_sound()  # Record the sound
        rssi = calculate_rssi(sound_data)  # Calculate the RSSI
        print(f"Sending RSSI: {rssi} dBm")
        requests.get(url = f"http://127.0.0.1:8000/setLast/{rssi}")
        client_socket.sendall(str(rssi).encode('utf-8'))  # Send the RSSI to the server
        time.sleep(1)  # Send every second

if __name__ == "__main__":
    client_socket = connect_to_server()  # Connect to the server
    send_rssi_to_server(client_socket)  # Continuously send the RSSI
