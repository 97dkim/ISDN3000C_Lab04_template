# ISDN3000C Lab04 - Maeko & Irene Monitoring System

A TCP-based monitoring system that displays ASCII art characters based on the current time, featuring **Maeko** and **Irene**.

## Features

- **Real-time System Monitoring**: Displays MAC address, system uptime, and timestamps
- **Character-based Time Display**: Shows different characters based on odd/even minutes
- **ASCII Art**: Character representations using symbols
- **JSON Communication**: Structured data exchange between client and server
- **Multi-threaded Server**: Handles multiple client connections simultaneously

## Characters

### Maeko (Even Minutes) 
*"The minute is even! Maeko is going to get even!"*
- Features: Pink bow, whiskers, yellow nose, pink outfit
- Appears when the current minute is even (0, 2, 4, 6, 8...)

### Irene (Odd Minutes)
*"The minute is odd! Irene is odd!"*
- Features: Devil horns, skull decoration, white face, devil tail
- Appears when the current minute is odd (1, 3, 5, 7, 9...)

## Project Structure

```
ISDN3000C_Lab04_template-master/
├── gateway_server.py      # TCP server with character logic
├── monitoring_client.py   # Client that connects every 60 seconds
└── readme.md             # This file
```

## Getting Started

### Prerequisites
- Python 3.x
- Network connectivity between client and server

### Configuration

1. **Update Server IP** in `monitoring_client.py`:
   ```python
   SERVER_IP = '192.168.50.54'  # Change to your server's IP
   ```

2. **Server Settings** in `gateway_server.py`:
   ```python
   HOST = '0.0.0.0'  # Listens on all interfaces
   PORT = 9999       # Default port
   ```

### Running the System

1. **Start the Gateway Server**:
   ```bash
   python gateway_server.py
   ```

2. **Run the Monitoring Client**:
   ```bash
   python monitoring_client.py
   ```

## Communication Protocol

### Request Format
The client sends a simple text request:
```
GET_DATA
```

### Response Format
The server responds with JSON data:
```json
{
    "message": "14:30:25",
    "character_art": "ASCII art here...",
    "character_message": "The minute is even! Maeko is going to get even!",
    "current_minute": 30,
    "device_mac_address": "aa:bb:cc:dd:ee:ff",
    "timestamp_utc": "2025-09-26T14:30:25.123456",
    "system_uptime": "up 2 days, 4 hours, 30 minutes"
}
```

## ASCII Art Examples

### Maeko (Even Minutes)
```
        @@@@@@@@        
      @@@%%%%%%@@@      
     @@%%%%%%%%%@@      
   @@@             @@@  
  @@  ---   ---     @@  
 @@   ---   ---      @@ 
 @@      ***         @@ 
 @@       o          @@ 
 @@                  @@ 
  @@               @@   
   @@@           @@@    
     @@@@@@@@@@@@@      
     @@%%%%%%%%%@@      
    @@%%%%%%%%%%%@@     
   @@%%%%%%%%%%%%%@@    
   @@             @@    
   @@             @@    
```

### Irene (Odd Minutes)
```
    @@#       #@@      
   @@@#       #@@@     
  @@@@  %###%  @@@@    
 @@@@@  %***%  @@@@@   
@@@@@@@@@@@@@@@@@@@@@@  
@@@                @@@  
@@  ***       ***  @@  
@@     @@@@@@@     @@  
@@     @  =  @     @@  
@@       ---       @@  
 @@@             @@@   
  @@@@         @@@@    
    @@@@@@@@@@@@@      
```

## Technical Details

### Server Architecture
- **Multi-threaded**: Uses `threading.Thread` for concurrent client handling
- **Socket-based**: TCP connections on port 9999
- **JSON serialization**: Uses `json.dumps()` for data formatting
- **System information**: Gathers MAC address and uptime via subprocess

### Client Architecture
- **Connection cycle**: Connects every 60 seconds
- **Error handling**: Graceful handling of connection failures
- **JSON parsing**: Uses `json.loads()` for data deserialization
- **Clean display**: Formatted output with character art

### Character Logic
```python
if current_minute % 2 == 1:  # Odd minute
    character_art = create_irene_art()
    character_message = "The minute is odd! Irene is odd!"
else:  # Even minute
    character_art = create_maeko_art()
    character_message = "The minute is even! Maeko is going to get even!"
```

## Customization

### Adding New Characters
1. Create new ASCII art function:
   ```python
   def create_new_character_art():
       # Your ASCII art here
       return "\n".join(art_lines)
   ```

2. Update the character logic in `get_system_info()`

### Changing Update Frequency
Modify the sleep duration in `monitoring_client.py`:
```python
time.sleep(60)  # Change to desired seconds
```

### Character Mapping
The `pixel_to_char()` function maps grayscale values to characters:
```python
char_ramp = '.:-=+*#%@'  # Customize this ramp
```

## Troubleshooting

### Connection Issues
- Verify server IP address in client configuration
- Check if server is running and listening on correct port
- Ensure firewall allows connections on port 9999

### ASCII Art Display
- Use monospace fonts for proper character alignment
- Adjust terminal width if art appears distorted

### System Information
- MAC address requires `/sys/class/net/eth0/address` (Linux/Unix)
- Uptime command requires `uptime -p` availability

## Dependencies

- `socket` - TCP networking
- `threading` - Multi-client support
- `subprocess` - System information gathering
- `json` - Data serialization
- `datetime` - Timestamp generation
- `time` - Client timing control

## Learning Objectives

This project demonstrates:
- TCP socket programming
- Client-server architecture
- JSON data exchange
- Multi-threading concepts
- System monitoring techniques
- ASCII art generation
- Time-based conditional logic

## Character Credits

Inspired by Sanrio characters but reimagined as Maeko and Irene for this monitoring system.

---
*Built for ISDN3000C Lab04*
