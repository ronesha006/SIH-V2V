from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TTCResult:
    """
    Result of a Time-to-Collision calculation.
    """

    ttc: float | None
    closing: bool
    relative_speed: float


def calculate_ttc(
    receiver_position: float,
    receiver_speed: float,
    sender_position: float,
    sender_speed: float,
) -> TTCResult:
    """
    Calculate approximate Time-to-Collision.

    Assumption for MVP:
    - Position is a 1-D longitudinal road coordinate.
    - Both vehicles are travelling in the same direction.
    - Positive relative speed means the receiver
      is closing the gap with the sender.

    TTC = distance / closing_speed
    """

    distance = sender_position - receiver_position

    relative_speed = receiver_speed - sender_speed

    # Receiver is not closing the gap.
    if relative_speed <= 0:

        return TTCResult(
            ttc=None,
            closing=False,
            relative_speed=relative_speed,
        )

    # Invalid/non-positive distance.
    if distance <= 0:

        return TTCResult(
            ttc=0.0,
            closing=True,
            relative_speed=relative_speed,
        )

    ttc = distance / relative_speed

    return TTCResult(
        ttc=ttc,
        closing=True,
        relative_speed=relative_speed,
    )