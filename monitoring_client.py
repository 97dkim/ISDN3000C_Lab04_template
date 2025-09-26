import socket
import time
import json

# --- TODO: Configure these values --- #
SERVER_IP = '192.168.50.54'  # The IP address of your RDK-X5
SERVER_PORT = 9999
REQUEST_MESSAGE = "GET_DATA" # The message your server expects
# --- END OF TODO --- #

def run_client():
    while True:
        print("-" * 30)
        print(f"Attempting to connect to {SERVER_IP}:{SERVER_PORT}...")
        try:
            # Create a socket object and use 'with' statement for automatic cleanup
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Connect to the server
                client_socket.connect((SERVER_IP, SERVER_PORT))
                print("Connected to the server.")
                
                # Send the request message, encoded to bytes
                client_socket.sendall(REQUEST_MESSAGE.encode('utf-8'))
                print(f"Sent request: {REQUEST_MESSAGE}")
                
                # Receive the response from the server
                response_bytes = client_socket.recv(4096)
                
                # Decode the response from bytes to string
                response_string = response_bytes.decode('utf-8')
                
                # Parse the JSON response into a dictionary
                try:
                    data = json.loads(response_string)
                    
                    # Print the received data in a user-friendly format
                    print("\n=== SYSTEM INFORMATION ===")
                    print(f"Current Server Time: {data.get('message', 'N/A')}")
                    print(f"Current Minute: {data.get('current_minute', 'N/A')}")
                    print()
                    print(data.get('character_message', 'N/A'))
                    print()
                    print(data.get('character_art', 'N/A'))
                    print()
                    print(f"Device MAC Address: {data.get('device_mac_address', 'N/A')}")
                    print(f"Timestamp (UTC): {data.get('timestamp_utc', 'N/A')}")
                    print(f"System Uptime: {data.get('system_uptime', 'N/A')}")
                    print("=========================")
                    
                except json.JSONDecodeError:
                    print(f"Received non-JSON response: {response_string}")
                
            # Connection is automatically closed when exiting the 'with' block
            print("Connection closed.")

        except ConnectionRefusedError:
            print("Connection failed. Is the server running?")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for 60 seconds before the next request
        print("\nWaiting for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    run_client()
