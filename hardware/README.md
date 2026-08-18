# Hardware Interface

## Purpose
This folder documents the physical hardware system and the interface expected between hardware and software.

## Current Hardware
The current prototype includes:
- ESP32
- LoRa communication modules
- Vehicle platform
- Motors
- Motor driver
- Sensors as available

## Current Status
Two ESP32 + LoRa nodes have been configured as two vehicle communication nodes.

Basic wireless communication between the nodes has been demonstrated.

## Hardware → Software
Hardware should provide software with meaningful vehicle information.

Expected information:
- Vehicle ID
- Speed
- Position
- Heading
- Lane/context information
- Obstacle distance
- Obstacle detection
- Brake status
- Timestamp

Some values may initially be simulated or predefined.

## Software → Hardware
Software produces high-level actions:
CONTINUE
SLOW_DOWN
BRAKE

Hardware converts these actions into motor-control commands.

## Interface Principle
Hardware should handle:
Sensor reading
Motor control
LoRa physical communication

Software should handle:
Message interpretation
Context evaluation
Safety decisions
Action selection

## Important
Hardware-specific implementation details should remain isolated from the software intelligence layer wherever possible.