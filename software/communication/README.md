# V2V Communication

## Purpose

This folder contains the communication layer responsible for exchanging structured information between vehicle nodes.

The physical communication channel currently uses ESP32 and LoRa.

## Main Responsibilities

The communication layer handles:

1. Message types
2. Message structure
3. Encoding
4. Decoding
5. Validation
6. Transmission
7. Reception

## Message Types

Initial message types:

### STATE_UPDATE

Shares the current state of a vehicle.

Example:

{
    "type": "STATE_UPDATE",
    "vehicle_id": "A",
    "speed": 0.72,
    "lane_id": 1
}

### OBSTACLE_ALERT

Indicates that a vehicle has detected an obstacle.

Example:

{
    "type": "OBSTACLE_ALERT",
    "vehicle_id": "A",
    "obstacle_distance": 42,
    "timestamp": 123456
}

### EMERGENCY_BRAKE

Indicates an emergency braking event.

### HEARTBEAT

Used to indicate that a vehicle is still active and reachable.

## Files

### message_schema.py

Defines valid message structures and message types.

### encoder.py

Converts software objects/messages into a format suitable for transmission.

### decoder.py

Converts received data back into software objects.

### transport.py

Provides the communication interface to the ESP32/LoRa transport layer.

The rest of the software should not need to know the low-level LoRa implementation details.

## Development Rule

The communication layer should be independent of the intelligence layer.

Communication answers:

"WHAT MESSAGE WAS RECEIVED?"

Intelligence answers:

"WHAT SHOULD I DO ABOUT IT?"

Do not place collision or safety decisions inside this folder.

## Hardware Integration

The hardware team is responsible for providing the working ESP32/LoRa transmission interface.

Software should interact with that interface through transport.py.

## Testing Requirements

The communication layer should eventually support testing for:

- Valid message transmission
- Valid message reception
- Invalid message detection
- Unknown message types
- Missing fields
- Corrupted/incomplete messages