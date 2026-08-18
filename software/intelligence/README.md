# Vehicle Intelligence

## Purpose

This folder contains the decision-making logic of the V2V system.

The intelligence layer receives vehicle state and V2V messages and determines:

1. Whether a received event is relevant
2. How dangerous the situation is
3. What action should be taken

## Pipeline

Received V2V Message
        ↓
Context Evaluation
        ↓
Relevance Decision
        ↓
Safety Evaluation
        ↓
Vehicle Action

## 1. Relevance Engine

File:

relevance.py

The relevance engine determines whether a received message is relevant to the receiving vehicle.

Initial contextual factors:

- Lane
- Direction/heading
- Relative position
- Distance
- Speed

Example:

Vehicle A:
Lane = 1
Position = 100

Vehicle B:
Lane = 1
Position = 80

A sends an emergency event.

B:

Same lane → YES
Behind sender → YES
Close enough → YES

Result:

RELEVANT

Another vehicle in Lane 2 may receive the same message but determine:

NOT_RELEVANT

## Important Principle

Receiving a message does NOT automatically mean reacting to it.

The system must first determine whether the event affects the receiving vehicle.

## 2. Safety Engine

File:

safety.py

The safety engine evaluates relevant events and assigns a safety state.

Initial states:

SAFE
WARNING
CRITICAL

Possible outputs:

SAFE → CONTINUE

WARNING → SLOW_DOWN

CRITICAL → BRAKE

## Initial Implementation

The first implementation should use deterministic rules.

Machine learning is not required for the initial prototype.

The rules must be:

- Easy to test
- Easy to explain
- Deterministic
- Fast enough for real-time decisions

## Future Extensions

Possible future improvements include:

- Time-to-Collision estimation
- Relative velocity
- Trajectory prediction
- Dynamic lane estimation
- Sensor fusion
- Adaptive relevance scoring

These should not be implemented until the basic safety pipeline is stable.

## Files

### relevance.py

Contains message relevance logic.

### safety.py

Contains risk classification and action generation.

## Owner

Primary owner: Software Person 1

Integration/testing: Software Person 2