
from __future__ import annotations

from monitoring.event_logger import EventLogger
from monitoring.metrics import Metrics

from simulation.scenarios import (
    scenario_same_lane_hazard,
    scenario_adjacent_lane,
    scenario_different_speed,
    scenario_emergency_brake,
)

from intelligence.ttc import calculate_ttc


# ==========================================================
# DASHBOARD HELPERS
# ==========================================================

def divider(width: int = 65):
    print("─" * width)


def title():
    print("=" * 65)
    print("                V2V SAFETY COMMAND CENTER")
    print("              Decentralized Vehicle Network")
    print("=" * 65)


def road_view(sender, receiver):
    """
    Simple 1-D road visualization.
    """

    road_length = 40

    minimum = min(sender.position, receiver.position)
    maximum = max(sender.position, receiver.position)

    if maximum == minimum:
        maximum += 1

    sender_index = int(
        (sender.position - minimum)
        / (maximum - minimum)
        * (road_length - 1)
    )

    receiver_index = int(
        (receiver.position - minimum)
        / (maximum - minimum)
        * (road_length - 1)
    )

    lane = [" "] * road_length

    lane[sender_index] = "A"

    lane[receiver_index] = "B"

    print("LIVE ROAD VIEW")
    divider()

    print(f"Lane {sender.lane_id}")

    print("[" + "".join(lane) + "]")

    print(f"A = {sender.position:.0f} m")
    print(f"B = {receiver.position:.0f} m")
    print()


def vehicle_table(sender, receiver):
    print("VEHICLE NETWORK")
    divider()

    print(
        f"{'ID':<6}{'Lane':<8}{'Position':<12}{'Speed'}"
    )

    print(
        f"{sender.vehicle_id:<6}"
        f"{sender.lane_id:<8}"
        f"{sender.position:<12.1f}"
        f"{sender.speed:.1f}"
    )

    print(
        f"{receiver.vehicle_id:<6}"
        f"{receiver.lane_id:<8}"
        f"{receiver.position:<12.1f}"
        f"{receiver.speed:.1f}"
    )

    print()


def event_panel(event):
    print("LATEST V2V EVENT")
    divider()

    print(f"Sender      : {event.sender}")
    print(f"Receiver    : {event.receiver}")
    print(f"Message     : {event.message_type}")
    print()

    print(f"Relevant    : {event.relevant}")
    print(f"Score       : {event.relevance_score}")

    if event.ttc is None:
        print("TTC         : N/A")
    else:
        print(f"TTC         : {event.ttc:.2f} sec")

    print()

    print(f"Risk        : {event.risk}")
    print(f"Action      : {event.action}")

    if event.latency is None:
        print("Latency     : Simulation")
    else:
        print(
            f"Latency     : {event.latency*1000:.0f} ms"
        )

    print()


def metrics_panel(metrics):
    data = metrics.summary()

    print("V2V METRICS")
    divider()

    print(
        f"Messages Sent     : {data['messages_sent']}"
    )

    print(
        f"Messages Received : {data['messages_received']}"
    )

    print(
        f"Packet Loss       : "
        f"{data['packet_loss_percentage']:.1f}%"
    )

    print()

    latency = data["average_latency"]

    if latency is None:
        print("Average Latency   : Simulation")
    else:
        print(
            f"Average Latency   : {latency*1000:.1f} ms"
        )

    print()

    print(
        f"Relevant Events   : {data['relevant_events']}"
    )

    print(
        f"Ignored Events    : {data['ignored_events']}"
    )

    print(
        f"Warnings          : {data['warning_events']}"
    )

    print(
        f"Critical Events   : {data['critical_events']}"
    )

    print(
        f"Brake Actions     : {data['brake_actions']}"
    )

    print(
        f"Slow Down Actions : {data['slow_down_actions']}"
    )

    print()


# ==========================================================
# DASHBOARD ENGINE
# ==========================================================

class Dashboard:

    def __init__(self):
        self.logger = EventLogger()
        self.metrics = Metrics()

    def display(self, result):
        sender = result["sender"]
        receiver = result["receiver"]

        relevance = result["relevance"]
        safety = result["safety"]

        # TTC
        ttc_result = calculate_ttc(
            receiver_position=receiver.position,
            receiver_speed=receiver.speed,
            sender_position=sender.position,
            sender_speed=sender.speed,
        )

        event = self.logger.log_event(
            sender=sender.vehicle_id,
            receiver=receiver.vehicle_id,
            message_type=result["message"].message_type.value,
            relevant=relevance.relevant,
            relevance_score=relevance.score,
            ttc=ttc_result.ttc,
            risk=(
                safety.risk.value
                if safety
                else None
            ),
            action=(
                safety.action.value
                if safety
                else None
            ),
            latency=None,
        )

        self.metrics.update(
            self.logger.get_events()
        )

        print("\n" * 2)

        title()

        print(
            f"Scenario : {result['scenario']}\n"
        )

        vehicle_table(sender, receiver)

        road_view(sender, receiver)

        event_panel(event)

        metrics_panel(self.metrics)

        print("=" * 65)


# ==========================================================
# MENU
# ==========================================================

def menu():
    print("\nSelect Scenario\n")

    print("1. Same Lane Hazard")
    print("2. Adjacent Lane")
    print("3. TTC Warning")
    print("4. TTC Critical")
    print("5. Emergency Brake")
    print("0. Exit")


def main():
    dashboard = Dashboard()

    while True:

        menu()

        choice = input("\nChoice: ")

        if choice == "1":

            dashboard.display(
                scenario_same_lane_hazard()
            )

        elif choice == "2":

            dashboard.display(
                scenario_adjacent_lane()
            )

        elif choice == "3":

            dashboard.display(
                scenario_different_speed(
                    receiver_speed=15
                )
            )

        elif choice == "4":

            dashboard.display(
                scenario_different_speed(
                    receiver_speed=22
                )
            )

        elif choice == "5":

            dashboard.display(
                scenario_emergency_brake()
            )

        elif choice == "0":

            print("\nExiting dashboard...")
            break

        else:

            print("\nInvalid choice.")


if __name__ == "__main__":
    main()