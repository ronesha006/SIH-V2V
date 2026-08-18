from __future__ import annotations

from dataclasses import dataclass, asdict
from time import time
from typing import Any, Dict


@dataclass
class VehicleState:
    """
    Represents the current state of one vehicle.
    """

    vehicle_id: str
    lane_id: int
    position: float
    speed: float
    heading: float
    obstacle_distance: float
    obstacle_detected: bool
    brake_status: bool
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert VehicleState object into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any]
    ) -> "VehicleState":
        """
        Reconstruct a VehicleState object from a dictionary.
        """

        required = {
            "vehicle_id",
            "lane_id",
            "position",
            "speed",
            "heading",
            "obstacle_distance",
            "obstacle_detected",
            "brake_status",
            "timestamp",
        }

        missing = required - data.keys()

        if missing:
            raise ValueError(
                f"Missing VehicleState fields: {sorted(missing)}"
            )

        return cls(
            vehicle_id=str(data["vehicle_id"]),
            lane_id=int(data["lane_id"]),
            position=float(data["position"]),
            speed=float(data["speed"]),
            heading=float(data["heading"]),
            obstacle_distance=float(
                data["obstacle_distance"]
            ),
            obstacle_detected=bool(
                data["obstacle_detected"]
            ),
            brake_status=bool(
                data["brake_status"]
            ),
            timestamp=float(data["timestamp"]),
        )

    @classmethod
    def create(
        cls,
        vehicle_id: str,
        lane_id: int = 1,
        position: float = 0.0,
        speed: float = 0.0,
        heading: float = 0.0,
        obstacle_distance: float = 999.0,
        obstacle_detected: bool = False,
        brake_status: bool = False,
    ) -> "VehicleState":
        """
        Convenient constructor that automatically
        generates the timestamp.
        """

        return cls(
            vehicle_id=vehicle_id,
            lane_id=lane_id,
            position=position,
            speed=speed,
            heading=heading,
            obstacle_distance=obstacle_distance,
            obstacle_detected=obstacle_detected,
            brake_status=brake_status,
            timestamp=time(),
        )