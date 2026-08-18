# Decentralized V2V Communication Platform

A prototype Vehicle-to-Vehicle (V2V) communication and cooperative safety system designed for real-time exchange of vehicle state and safety information without cloud dependency.

## Problem

Vehicles travelling near each other may encounter hazards that are detected by one vehicle before the others become aware of them.

A conventional approach may require each vehicle to independently detect the same hazard. Our system explores a decentralized V2V approach where vehicles exchange contextual information directly and locally determine whether a received event is relevant to them.

## Core Idea

The system follows the pipeline:

Vehicle Sensors
        ↓
Vehicle State
        ↓
V2V Communication
        ↓
Message Relevance
        ↓
Safety Decision
        ↓
Vehicle Action

The prototype uses ESP32-based vehicle nodes and LoRa for direct wireless communication.

## Current Prototype

The initial hardware setup consists of two nodes representing two vehicles:

Vehicle A
ESP32 + LoRa
      ↕
  Wireless V2V
      ↕
Vehicle B
ESP32 + LoRa

The hardware team has already established basic communication between the two nodes.

The software team is responsible for converting this communication channel into a structured V2V safety system.

## Software Modules

### 1. Models

Defines common data structures used across the software system.

Primary object:

VehicleState

### 2. Communication

Defines the V2V message protocol, encoding/decoding and communication interface.

Responsibilities include:

- Message types
- Vehicle state transmission
- Safety event transmission
- Message validation
- ESP32/LoRa communication interface

### 3. Intelligence

Contains the decision-making logic.

Responsibilities include:

- Message relevance evaluation
- Context-aware vehicle filtering
- Safety/risk classification
- Action generation

Example:

RELEVANT → evaluate safety
NOT_RELEVANT → ignore

### 4. Simulation

Provides simulated vehicle states and scenarios so that the software can be developed and tested without depending on physical hardware.

### 5. Monitoring

Provides logging, communication metrics and a basic interface for observing the V2V system.

Metrics may include:

- Packet count
- Packet loss
- Latency
- Vehicle status
- Message type
- Relevance
- Safety state
- Generated action

### 6. Testing

Contains automated tests for the software modules.

## Hardware Interface

The hardware layer is expected to provide vehicle information such as:

- Vehicle ID
- Speed
- Position
- Heading
- Lane/context information
- Obstacle distance
- Obstacle detection status
- Brake status

The software layer produces high-level vehicle actions such as:

- CONTINUE
- SLOW_DOWN
- BRAKE

Hardware is responsible for converting these actions into physical motor behaviour.

## Development Philosophy

The project is being developed in independent modules so that software can be tested using simulated data before being integrated with physical vehicles.

The software should not depend directly on hardware-specific implementation wherever possible.

## Development Workflow

Each contributor should work on a separate Git branch.

Example:

feature/protocol
feature/safety-engine
feature/simulation
feature/monitoring

Changes should be tested before merging into the main branch.

## Project Status

Current stage:

- ESP32 communication: Working
- LoRa communication: Working
- V2V software protocol: In development
- Vehicle state model: In development
- Relevance engine: Planned
- Safety engine: Planned
- Monitoring: Planned
- Hardware integration: In progress

## Important Scope Rule

The first milestone is not a complete autonomous vehicle.

The first milestone is:

Vehicle A detects/represents a safety event
        ↓
Structured V2V message
        ↓
Vehicle B receives message
        ↓
Vehicle B evaluates relevance
        ↓
Vehicle B determines safety response

Advanced features such as trajectory prediction, dynamic lane estimation, computer vision and machine learning are considered future extensions.