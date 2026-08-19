from __future__ import annotations
from time import time
from models.vehicle_state import VehicleState

class SimulatedVehicle:
    """
    Represents a simulated moving vehicle.
    VehicleState remains the common data structure used
    throughout the V2V system.
    """

    def __init__(
        self,
        vehicle_id: str,
        lane_id: int,
        position: float,
        speed: float,
        heading: float = 0.0,
        obstacle_distance: float = 999.0,
        obstacle_detected: bool = False,
        brake_status: bool = False,
    ):
        self.state = VehicleState.create(
            vehicle_id=vehicle_id,
            lane_id=lane_id,
            position=position,
            speed=speed,
            heading=heading,
            obstacle_distance=obstacle_distance,
            obstacle_detected=obstacle_detected,
            brake_status=brake_status,
        )

    def update(self, time_delta: float) -> VehicleState:
        """
        Move the vehicle according to:
        new_position = old_position + speed * time_delta
        """

        self.state.position += (self.state.speed * time_delta)
        self.state.timestamp = time()

        return self.state

    def set_speed(self, speed: float) -> None:
        """Change the vehicle's speed."""

        self.state.speed = speed
        self.state.timestamp = time()

    def set_obstacle(
        self,
        detected: bool,
        distance: float = 999.0,
    ) -> None:
        """Set the obstacle status of the vehicle."""

        self.state.obstacle_detected = detected
        self.state.obstacle_distance = distance
        self.state.timestamp = time()

    def apply_brake(self) -> None:
        """Apply the vehicle's simulated brakes."""

        self.state.brake_status = True
        self.state.timestamp = time()

    def release_brake(self) -> None:
        """Release the vehicle's simulated brakes."""

        self.state.brake_status = False
        self.state.timestamp = time()

    def get_state(self) -> VehicleState:
        """Return the current VehicleState."""
        return self.state