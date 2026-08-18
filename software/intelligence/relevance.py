from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
from communication.message_schema import V2VMessage

@dataclass
class RelevanceResult:
    """
    Result returned by the relevance engine.
    """

    relevant: bool
    score: int
    reason: str


def same_direction(
    heading_a: float,
    heading_b: float,
    tolerance: float = 30.0,
) -> bool:
    """
    Check whether two vehicles are travelling
    approximately in the same direction.

    Heading is measured in degrees.
    """

    difference = abs(
        (heading_a - heading_b + 180.0) % 360.0 - 180.0
    )

    return difference <= tolerance


def evaluate_relevance(
    receiver: Dict[str, Any],
    sender: Dict[str, Any],
    max_relevant_distance: float = 30.0,
) -> RelevanceResult:
    """
    Determine whether an event from the sender
    is relevant to the receiving vehicle.

    Current MVP checks:

    1. Same lane
    2. Same direction
    3. Receiver is behind sender
    4. Vehicles are within relevant distance
    """

    score = 0
    reasons = []

    # -----------------------------------------
    # 1. SAME LANE
    # -----------------------------------------

    same_lane = (
        int(receiver["lane_id"])
        ==
        int(sender["lane_id"])
    )

    if same_lane:

        score += 40
        reasons.append("same lane")

    else:

        reasons.append("different lane")

    # -----------------------------------------
    # 2. SAME DIRECTION
    # -----------------------------------------

    direction_match = same_direction(
        float(receiver["heading"]),
        float(sender["heading"]),
    )

    if direction_match:

        score += 20
        reasons.append("same direction")

    else:

        reasons.append("different direction")

    # -----------------------------------------
    # 3. RELATIVE POSITION
    # -----------------------------------------

    distance_between = (
        float(sender["position"])
        -
        float(receiver["position"])
    )

    receiver_behind = distance_between > 0

    if receiver_behind:

        score += 20
        reasons.append("receiver is behind sender")

    else:

        reasons.append("receiver is not behind sender")

    # -----------------------------------------
    # 4. DISTANCE
    # -----------------------------------------

    close_enough = (
        abs(distance_between)
        <=
        max_relevant_distance
    )

    if close_enough:

        score += 20
        reasons.append("within relevance distance")

    else:

        reasons.append("outside relevance distance")

    # -----------------------------------------
    # FINAL DECISION
    # -----------------------------------------

    relevant = (
        same_lane
        and
        direction_match
        and
        receiver_behind
        and
        close_enough
    )

    return RelevanceResult(
        relevant=relevant,
        score=score,
        reason=", ".join(reasons),
    )

def evaluate_message_relevance(
    message: V2VMessage,
    receiver: Dict[str, Any],
    max_relevant_distance: float = 30.0,
) -> RelevanceResult:
    """
    Evaluate whether a received V2V message is relevant
    to the receiving vehicle.

    The sender information is extracted from the V2VMessage
    before being passed to the relevance engine.
    """

    sender = message.payload.copy()

    # The payload of an OBSTACLE_ALERT does not currently
    # contain vehicle_id, so use the message sender ID.
    sender["vehicle_id"] = message.sender_id

    return evaluate_relevance(
        receiver=receiver,
        sender=sender,
        max_relevant_distance=max_relevant_distance,
    )