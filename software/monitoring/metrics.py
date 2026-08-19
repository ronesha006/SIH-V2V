from __future__ import annotations

from typing import Any, Dict, List

from monitoring.event_logger import V2VEvent


class Metrics:
    """
    Calculates communication and safety metrics
    from recorded V2V events.
    """

    def __init__(self) -> None:
        self.events: List[V2VEvent] = []

    def update(self, events: List[V2VEvent]) -> None:
        """
        Replace the current event list with the latest events.
        """
        self.events = events

    # ==========================================
    # COMMUNICATION METRICS
    # ==========================================

    def messages_sent(self) -> int:
        """
        Number of messages recorded.
        """
        return len(self.events)

    def messages_received(self) -> int:
        """
        Number of received messages.

        For the simulation, every logged event represents
        a successfully received message.
        """
        return len(self.events)

    def packet_loss_percentage(self) -> float:
        """
        Calculate packet loss percentage.

        During simulation, packet loss is 0 because
        there is no unreliable communication layer yet.
        """

        sent = self.messages_sent()
        received = self.messages_received()

        if sent == 0:
            return 0.0

        return ((sent - received) / sent) * 100.0

    # ==========================================
    # LATENCY METRICS
    # ==========================================

    def latency_values(self) -> List[float]:
        """
        Return only events that contain real latency values.

        Simulation events have latency=None and are ignored.
        """
        return [
            event.latency
            for event in self.events
            if event.latency is not None
        ]

    def average_latency(self) -> float | None:
        """
        Calculate average communication latency.

        Returns None when no real latency measurements
        are available.
        """

        values = self.latency_values()

        if not values:
            return None

        return sum(values) / len(values)

    def minimum_latency(self) -> float | None:
        """
        Return minimum measured latency.
        """

        values = self.latency_values()

        if not values:
            return None

        return min(values)

    def maximum_latency(self) -> float | None:
        """
        Return maximum measured latency.
        """

        values = self.latency_values()

        if not values:
            return None

        return max(values)

    # ==========================================
    # SAFETY METRICS
    # ==========================================

    def relevant_events(self) -> int:
        """
        Number of events considered relevant.
        """

        return sum(
            1
            for event in self.events
            if event.relevant
        )

    def ignored_events(self) -> int:
        """
        Number of events considered irrelevant.
        """

        return sum(
            1
            for event in self.events
            if not event.relevant
        )

    def warning_events(self) -> int:
        """
        Number of WARNING decisions.
        """

        return sum(
            1
            for event in self.events
            if event.risk == "WARNING"
        )

    def critical_events(self) -> int:
        """
        Number of CRITICAL decisions.
        """

        return sum(
            1
            for event in self.events
            if event.risk == "CRITICAL"
        )

    def brake_actions(self) -> int:
        """
        Number of BRAKE actions.
        """

        return sum(
            1
            for event in self.events
            if event.action == "BRAKE"
        )

    def slow_down_actions(self) -> int:
        """
        Number of SLOW_DOWN actions.
        """

        return sum(
            1
            for event in self.events
            if event.action == "SLOW_DOWN"
        )

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self) -> Dict[str, Any]:
        """
        Return all important metrics as a dictionary.
        """

        return {
            "messages_sent": self.messages_sent(),
            "messages_received": self.messages_received(),
            "packet_loss_percentage":
                self.packet_loss_percentage(),

            "average_latency":
                self.average_latency(),

            "minimum_latency":
                self.minimum_latency(),

            "maximum_latency":
                self.maximum_latency(),

            "relevant_events":
                self.relevant_events(),

            "ignored_events":
                self.ignored_events(),

            "warning_events":
                self.warning_events(),

            "critical_events":
                self.critical_events(),

            "brake_actions":
                self.brake_actions(),

            "slow_down_actions":
                self.slow_down_actions(),
        }