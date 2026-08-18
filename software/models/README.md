# Models

## Purpose

This folder contains the common data structures used throughout the V2V software system.

The goal is to ensure that all software modules use the same representation of a vehicle.

## Primary Model

### VehicleState

The VehicleState represents the current state of a vehicle.

Initial fields:

- vehicle_id
- lane_id
- position
- speed
- heading
- obstacle_distance
- obstacle_detected
- brake_status
- timestamp

Example conceptual state:

{
    "vehicle_id": "A",
    "lane_id": 1,
    "position": 100.0,
    "speed": 0.72,
    "heading": 0.0,
    "obstacle_distance": 42.0,
    "obstacle_detected": true,
    "brake_status": false,
    "timestamp": 123456789
}

## Responsibilities

This module should:

- Define the VehicleState structure
- Validate required fields
- Provide consistent data types
- Provide serialization-friendly data
- Act as the common interface between modules

## Important Rule

Other modules should use VehicleState instead of independently creating different vehicle-data formats.

For example:

Correct:

communication → VehicleState

simulation → VehicleState

intelligence → VehicleState

Incorrect:

simulation → custom dictionary

communication → different dictionary

intelligence → different object

## Current Scope

Initially, some fields may contain simulated or predefined values.

Hardware-derived values will be integrated later.

## Owner

Shared module.

Both software developers must agree before changing the VehicleState structure because multiple modules depend on it.