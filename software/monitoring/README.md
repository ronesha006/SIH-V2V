# SIH-V2V
# Monitoring and Metrics

## Purpose
This folder provides visibility into the V2V system during development and demonstration.

The monitoring layer should make the system's internal behaviour visible to developers and judges.

## Information to Display
### Vehicle Information
- Vehicle ID
- Lane
- Position
- Speed
- Heading
- Vehicle status

### Communication Information
- Last received message
- Sender
- Receiver
- Message type
- Timestamp
- Latency
- Packet count
- Packet loss

### Intelligence Information
- Relevance result
- Safety state
- Generated action

## Example
V2V EVENT

Sender: Vehicle A
Receiver: Vehicle B
Message: OBSTACLE_ALERT
Relevance: HIGH
Risk: CRITICAL
Action: BRAKE
Latency: 28 ms

## Files
### logger.py
Records system events.

Example events:
- Message sent
- Message received
- Relevance evaluated
- Safety decision
- Action generated
- Communication timeout

### metrics.py
Calculates communication and system metrics.

Initial metrics:
- Packets sent
- Packets received
- Packet loss
- Average latency
- Minimum latency
- Maximum latency
- Message response time

### dashboard.py
Provides a basic visual/terminal representation of system status.

## Development Priority
The dashboard is NOT the priority.
The priority is:
1. Correct data
2. Correct decisions
3. Correct metrics
4. Visualization
