from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict

from models.vehicle_state import VehicleState


class MessageType(str, Enum):

    STATE_UPDATE = "STATE_UPDATE"

    OBSTACLE_ALERT = "OBSTACLE_ALERT"

    EMERGENCY_BRAKE = "EMERGENCY_BRAKE"

    HEARTBEAT = "HEARTBEAT"


@dataclass
class V2VMessage:
    """
    Represents a message exchanged between vehicles.
    """

    message_type: MessageType

    sender_id: str

    sequence: int

    timestamp: float

    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert V2VMessage into a dictionary.
        """

        data = asdict(self)

        data["message_type"] = self.message_type.value

        return data

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any]
    ) -> "V2VMessage":
        """
        Reconstruct a V2VMessage from a dictionary.
        """

        required = {
            "message_type",
            "sender_id",
            "sequence",
            "timestamp",
            "payload",
        }

        missing = required - data.keys()

        if missing:
            raise ValueError(
                f"Missing V2V message fields: {sorted(missing)}"
            )

        try:
            message_type = MessageType(
                data["message_type"]
            )

        except ValueError as exc:

            raise ValueError(
                f"Unknown message type: "
                f"{data['message_type']}"
            ) from exc

        if not isinstance(data["payload"], dict):

            raise ValueError(
                "payload must be a dictionary"
            )

        return cls(
            message_type=message_type,

            sender_id=str(
                data["sender_id"]
            ),

            sequence=int(
                data["sequence"]
            ),

            timestamp=float(
                data["timestamp"]
            ),

            payload=data["payload"],
        )


# ==========================================================
# MESSAGE BUILDERS
# ==========================================================


def build_state_message(
    vehicle_state: VehicleState,
    sequence: int,
) -> V2VMessage:
    """
    Create a message containing the vehicle's
    current state.
    """

    return V2VMessage(

        message_type=MessageType.STATE_UPDATE,

        sender_id=vehicle_state.vehicle_id,

        sequence=sequence,

        timestamp=vehicle_state.timestamp,

        payload=vehicle_state.to_dict(),
    )


def build_obstacle_alert(
    vehicle_state: VehicleState,
    sequence: int,
) -> V2VMessage:
    """
    Create an obstacle warning message.
    """

    return V2VMessage(

        message_type=MessageType.OBSTACLE_ALERT,

        sender_id=vehicle_state.vehicle_id,

        sequence=sequence,

        timestamp=vehicle_state.timestamp,

        payload={

            "lane_id":
                vehicle_state.lane_id,

            "position":
                vehicle_state.position,

            "speed":
                vehicle_state.speed,

            "heading":
                vehicle_state.heading,

            "obstacle_distance":
                vehicle_state.obstacle_distance,
        },
    )


def build_emergency_brake(
    vehicle_state: VehicleState,
    sequence: int,
) -> V2VMessage:
    """
    Create an emergency braking message.
    """

    return V2VMessage(

        message_type=MessageType.EMERGENCY_BRAKE,

        sender_id=vehicle_state.vehicle_id,

        sequence=sequence,

        timestamp=vehicle_state.timestamp,

        payload={

            "lane_id":
                vehicle_state.lane_id,

            "position":
                vehicle_state.position,

            "speed":
                vehicle_state.speed,

            "heading":
                vehicle_state.heading,
        },
    )


def build_heartbeat(
    sender_id: str,
    sequence: int,
    timestamp: float,
) -> V2VMessage:
    """
    Create a heartbeat message indicating
    that a vehicle is active.
    """

    return V2VMessage(

        message_type=MessageType.HEARTBEAT,

        sender_id=sender_id,

        sequence=sequence,

        timestamp=timestamp,

        payload={},
    )