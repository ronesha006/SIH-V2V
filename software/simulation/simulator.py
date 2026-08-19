from __future__ import annotations
from typing import Dict, List
from simulation.vehicle import SimulatedVehicle
from models.vehicle_state import VehicleState


class VehicleSimulator:
    """
    Manages multiple simulated vehicles.
    """

    def __init__(self):
        self.vehicles: Dict[str, SimulatedVehicle] = {}

    def add_vehicle(
        self,
        vehicle: SimulatedVehicle,
    ) -> None:
        """Add a simulated vehicle."""

        vehicle_id = vehicle.get_state().vehicle_id
        self.vehicles[vehicle_id] = vehicle

    def get_vehicle(
        self,
        vehicle_id: str,
    ) -> SimulatedVehicle:
        """Return a vehicle using its ID."""

        if vehicle_id not in self.vehicles:
            raise ValueError(
                f"Vehicle '{vehicle_id}' does not exist."
            )

        return self.vehicles[vehicle_id]

    def get_all_states(self) -> List[VehicleState]:
        """Return the current state of all vehicles."""

        return [vehicle.get_state() for vehicle in self.vehicles.values()]

    def update(
        self,
        time_delta: float,
    ) -> List[VehicleState]:
        """
        Move every vehicle forward by time_delta seconds.
        """
        for vehicle in self.vehicles.values():
            vehicle.update(time_delta)

        return self.get_all_states()

    def vehicle_count(self) -> int:
        """Return the number of simulated vehicles."""

        return len(self.vehicles)