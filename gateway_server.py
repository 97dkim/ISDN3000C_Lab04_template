import socket
import threading
import subprocess
import json
from datetime import datetime

HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 9999       # Port for our gateway service

def pixel_to_char(pixel_value, char_ramp='.:-=+*#%@'):
    """
    Takes a grayscale pixel value (0-255) and maps it to a character from the ramp.
    """
    # Ensure pixel value is within bounds
    pixel_value = max(0, min(255, pixel_value))
    # Map to character index
    char_index = int((pixel_value / 255) * (len(char_ramp) - 1))
    return char_ramp[char_index]

def create_irene_art():
    """
    Creates ASCII art of Irene using symbols - devil horns, skull, white face, devil tail
    """
    irene = [
        "    @@#       #@@      ",
        "   @@@#       #@@@     ",
        "  @@@@  %###%  @@@@    ",
        " @@@@@  %***%  @@@@@   ",
        "@@@@@@@@@@@@@@@@@@@@@@  ",
        "@@@                @@@  ",
        "@@  ***       ***  @@  ",
        "@@     @@@@@@@     @@  ",
        "@@     @  =  @     @@  ",
        "@@       ---       @@  ",
        " @@@             @@@   ",
        "  @@@@         @@@@    ",
        "    @@@@@@@@@@@@@      ",
    ]
    return "\n".join(irene)

def create_maeko_art():
    """
    Creates ASCII art of Maeko using symbols - pink bow, whiskers, yellow nose, pink outfit
    """
    maeko = [
        "        @@@@@@@@        ",
        "      @@@%%%%%%@@@      ",
        "     @@%%%%%%%%%@@      ",
        "   @@@             @@@  ",
        "  @@  ---   ---     @@  ",
        " @@   ---   ---      @@ ",
        " @@      ***         @@ ",
        " @@       o          @@ ",
        " @@                  @@ ",
        "  @@               @@   ",
        "   @@@           @@@    ",
        "     @@@@@@@@@@@@@      ",
        "     @@%%%%%%%%%@@      ",
        "    @@%%%%%%%%%%%@@     ",
        "   @@%%%%%%%%%%%%%@@    ",
        "   @@             @@    ",
        "   @@             @@    "
    ]
    return "\n".join(maeko)

def get_system_info():
    """
    This function gathers the required system information.
    This is a suggested implementation. You can modify it if you wish.
    """
    # Get MAC Address for eth0 (a unique identifier for your device)
    try:
        mac_addr_output = subprocess.run(
            ['cat', '/sys/class/net/eth0/address'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        mac_addr_output = "MAC_NOT_FOUND"

    # Get system uptime
    try:
        uptime_output = subprocess.run(
            ['uptime', '-p'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        uptime_output = "UPTIME_NOT_FOUND"

    # Get current timestamp
    timestamp = datetime.now().isoformat()
    
    # Get current time and check if minute is odd or even
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    current_minute = current_datetime.minute
    
    # Determine character and message based on odd/even minute
    if current_minute % 2 == 1:  # Odd minute
        character_art = create_irene_art()
        character_message = "The minute is odd! Irene is odd!"
    else:  # Even minute
        character_art = create_maeko_art()
        character_message = "The minute is even! Maeko is going to get even!"

    # Structure the data
    info = {
        "message": current_time,
        "character_art": character_art,
        "character_message": character_message,
        "current_minute": current_minute,
        "device_mac_address": mac_addr_output,
        "timestamp_utc": timestamp,
        "system_uptime": uptime_output
    }
    return info

def handle_client(conn, addr):
    """
    This function is executed in a separate thread for each client.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            # Wait for a request from the client
            request = conn.recv(1024).decode('utf-8')
            if not request:
                # If client closes connection, break the loop
                break

            print(f"Received request from {addr}: {request}")

            # Check if the client's request is valid
            if request.strip() == "GET_DATA":
                # Request is valid, get system information
                system_data = get_system_info()
                
                # Serialize the data to JSON format
                json_response = json.dumps(system_data)
                
                # Encode and send the response back to the client
                conn.sendall(json_response.encode('utf-8'))
                print(f"Sent system data to {addr}")
            else:
                # Request is not valid, send error message
                error_message = json.dumps({"error": "Invalid request. Expected 'GET_DATA'."})
                conn.sendall(error_message.encode('utf-8'))
                print(f"Sent error message to {addr} for invalid request: {request}")
            
            ## --- END OF TODO --- ##

    print(f"[CONNECTION CLOSED] {addr} disconnected.")

def start_server():
    """
    Starts the main server loop to listen for incoming connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        # Create a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
