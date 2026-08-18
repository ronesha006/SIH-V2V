# SIH-V2V
# Vehicle Simulation

## Purpose
This folder provides simulated vehicle data and test scenarios so that the software can be developed without requiring physical vehicles.

This is important because the software must be testable even when ESP32/LoRa hardware is unavailable.

## Main Goal
Simulate:
- Multiple vehicles
- Vehicle positions
- Lanes
- Speeds
- Headings
- Obstacles
- Braking events
- V2V messages

## Example Vehicles
Vehicle A:
Lane = 1
Position = 100
Speed = 50

Vehicle B:
Lane = 1
Position = 80
Speed = 48

Vehicle C:
Lane = 2
Position = 95
Speed = 51

## Example Scenarios
### Scenario 1 — Relevant Emergency Event
A detects an obstacle.
A sends an emergency message.
B is behind A in the same lane.

Expected:
B → RELEVANT
B → CRITICAL
B → BRAKE

### Scenario 2 — Different Lane
A sends an emergency message.
C is in another lane and is not affected.

Expected:
C → NOT_RELEVANT

### Scenario 3 — Far Vehicle
A sends an emergency message.
B is in the same lane but far away.

Expected:
B → LOW/NOT_RELEVANT depending on implemented threshold.

### Scenario 4 — Multiple Vehicles
Simulate several vehicles receiving the same event.
Each vehicle should independently determine whether the event affects it.

## Files
### vehicle_generator.py
Creates simulated vehicle states.

### scenario.py
Defines reproducible scenarios.

### test_data.py
Contains reusable test inputs and sample states.

## Development Rule
Simulation data must use the same VehicleState structure used by the real system.
Do not create a separate data format for simulation.
This allows simulation to be replaced by real ESP32 data later without rewriting the intelligence layer.