from __future__ import annotations

from dataclasses import dataclass, asdict
from time import time
from typing import Any, Dict, List, Optional


@dataclass
class V2VEvent:
    """
    Represents one event in the V2V system.

    During simulation, latency may be None.
    During real hardware testing, it will contain
    the measured communication latency in seconds.
    """

    timestamp: float
    sender: str
    receiver: str
    message_type: str

    relevant: bool
    relevance_score: int

    ttc: Optional[float]

    risk: Optional[str]
    action: Optional[str]

    latency: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event into a dictionary."""
        return asdict(self)


class EventLogger:
    """
    Stores V2V events during simulation and execution.

    Events are kept in memory for the MVP.
    """

    def __init__(self) -> None:
        self.events: List[V2VEvent] = []

    def log_event(
        self,
        sender: str,
        receiver: str,
        message_type: str,
        relevant: bool,
        relevance_score: int,
        ttc: Optional[float],
        risk: Optional[str],
        action: Optional[str],
        latency: Optional[float] = None,
    ) -> V2VEvent:
        """
        Create and store a V2V event.
        """

        event = V2VEvent(
            timestamp=time(),
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            relevant=relevant,
            relevance_score=relevance_score,
            ttc=ttc,
            risk=risk,
            action=action,
            latency=latency,
        )

        self.events.append(event)

        return event

    def get_events(self) -> List[V2VEvent]:
        """
        Return all recorded events.
        """
        return self.events

    def get_latest(self) -> Optional[V2VEvent]:
        """
        Return the most recent event.

        Returns None if no events exist.
        """

        if not self.events:
            return None

        return self.events[-1]

    def clear(self) -> None:
        """
        Remove all recorded events.
        """
        self.events.clear()

    def count(self) -> int:
        """
        Return the number of recorded events.
        """
        return len(self.events)