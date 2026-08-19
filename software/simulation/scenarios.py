from __future__ import annotations
from typing import Any, Dict
from simulation.vehicle import SimulatedVehicle
from simulation.simulator import VehicleSimulator

from communication.message_schema import (
    build_obstacle_alert,
    build_emergency_brake,
)

from intelligence.safety import (
    evaluate_message_safety,
)


# ==========================================================
# HELPER
# ==========================================================
def create_vehicle(
    vehicle_id: str,
    lane_id: int,
    position: float,
    speed: float,
    heading: float = 0.0,
) -> SimulatedVehicle:

    return SimulatedVehicle(
        vehicle_id=vehicle_id,
        lane_id=lane_id,
        position=position,
        speed=speed,
        heading=heading,
    )


# ==========================================================
# SCENARIO 1
# SAME LANE HAZARD
# ==========================================================

def scenario_same_lane_hazard() -> Dict[str, Any]:
    """
    A detects an obstacle.

    B is behind A in the same lane.

    Expected:
        B -> RELEVANT
        B -> WARNING / CRITICAL
        B -> SLOW_DOWN / BRAKE
    """

    simulator = VehicleSimulator()
    vehicle_a = create_vehicle(
        vehicle_id="A",
        lane_id=1,
        position=100.0,
        speed=10.0,
    )

    vehicle_b = create_vehicle(
        vehicle_id="B",
        lane_id=1,
        position=80.0,
        speed=15.0,
    )

    simulator.add_vehicle(vehicle_a)
    simulator.add_vehicle(vehicle_b)

    # A detects obstacle
    vehicle_a.set_obstacle(
        detected=True,
        distance=20.0,
    )

    message = build_obstacle_alert(
        vehicle_state=vehicle_a.get_state(),
        sequence=1,
    )

    relevance, safety = evaluate_message_safety(
        message=message,
        receiver=vehicle_b.get_state().to_dict(),
        max_relevant_distance=30.0,
        obstacle_critical_distance=50.0,
        obstacle_warning_distance=100.0,
    )

    return {
        "scenario": "Same Lane Hazard",
        "sender": vehicle_a.get_state(),
        "receiver": vehicle_b.get_state(),
        "message": message,
        "relevance": relevance,
        "safety": safety,
    }


# ==========================================================
# SCENARIO 2
# ADJACENT LANE
# ==========================================================
def scenario_adjacent_lane() -> Dict[str, Any]:
    """
    A detects an obstacle.

    C is in an adjacent lane.

    Expected:
        C -> NOT RELEVANT
        C -> IGNORE
    """

    simulator = VehicleSimulator()
    vehicle_a = create_vehicle(
        vehicle_id="A",
        lane_id=1,
        position=100.0,
        speed=10.0,
    )

    vehicle_c = create_vehicle(
        vehicle_id="C",
        lane_id=2,
        position=80.0,
        speed=15.0,
    )

    simulator.add_vehicle(vehicle_a)
    simulator.add_vehicle(vehicle_c)

    vehicle_a.set_obstacle(
        detected=True,
        distance=20.0,
    )

    message = build_obstacle_alert(
        vehicle_state=vehicle_a.get_state(),
        sequence=1,
    )

    relevance, safety = evaluate_message_safety(
        message=message,
        receiver=vehicle_c.get_state().to_dict(),
        max_relevant_distance=30.0,
        obstacle_critical_distance=50.0,
        obstacle_warning_distance=100.0,
    )

    return {
        "scenario": "Adjacent Lane",
        "sender": vehicle_a.get_state(),
        "receiver": vehicle_c.get_state(),
        "message": message,
        "relevance": relevance,
        "safety": safety,
    }


# ==========================================================
# SCENARIO 3
# DIFFERENT SPEED / TTC
# ==========================================================

def scenario_different_speed(
    receiver_speed: float,
) -> Dict[str, Any]:
    """
    Same lane and same distance, but receiver speed
    changes.

    This demonstrates that TTC depends on relative speed.

    Example:
        Receiver = 15 m/s
        Sender   = 10 m/s

        TTC = 20 / 5
            = 4 seconds

    Increasing receiver speed should reduce TTC.
    """

    simulator = VehicleSimulator()
    vehicle_a = create_vehicle(
        vehicle_id="A",
        lane_id=1,
        position=100.0,
        speed=10.0,
    )

    vehicle_b = create_vehicle(
        vehicle_id="B",
        lane_id=1,
        position=80.0,
        speed=receiver_speed,
    )

    simulator.add_vehicle(vehicle_a)
    simulator.add_vehicle(vehicle_b)

    vehicle_a.set_obstacle(
        detected=True,
        distance=20.0,
    )

    message = build_obstacle_alert(
        vehicle_state=vehicle_a.get_state(),
        sequence=1,
    )

    relevance, safety = evaluate_message_safety(
        message=message,
        receiver=vehicle_b.get_state().to_dict(),
        max_relevant_distance=30.0,
        obstacle_critical_distance=50.0,
        obstacle_warning_distance=100.0,
    )

    return {
        "scenario": f"Different Speed ({receiver_speed} m/s)",
        "sender": vehicle_a.get_state(),
        "receiver": vehicle_b.get_state(),
        "message": message,
        "relevance": relevance,
        "safety": safety,
    }


# ==========================================================
# SCENARIO 4
# EMERGENCY BRAKE
# ==========================================================
def scenario_emergency_brake() -> Dict[str, Any]:
    """
    A suddenly performs emergency braking.
    B is behind A in the same lane.

    Expected:
        B -> RELEVANT
        B -> CRITICAL
        B -> BRAKE
    """

    simulator = VehicleSimulator()
    vehicle_a = create_vehicle(
        vehicle_id="A",
        lane_id=1,
        position=100.0,
        speed=10.0,
    )

    vehicle_b = create_vehicle(
        vehicle_id="B",
        lane_id=1,
        position=80.0,
        speed=15.0,
    )

    simulator.add_vehicle(vehicle_a)
    simulator.add_vehicle(vehicle_b)

    # A applies emergency brake
    vehicle_a.apply_brake()

    message = build_emergency_brake(
        vehicle_state=vehicle_a.get_state(),
        sequence=1,
    )

    relevance, safety = evaluate_message_safety(
        message=message,
        receiver=vehicle_b.get_state().to_dict(),
        max_relevant_distance=30.0,
        obstacle_critical_distance=50.0,
        obstacle_warning_distance=100.0,
    )

    return {
        "scenario": "Emergency Brake",
        "sender": vehicle_a.get_state(),
        "receiver": vehicle_b.get_state(),
        "message": message,
        "relevance": relevance,
        "safety": safety,
    }


# ==========================================================
# OUTPUT FUNCTION
# ==========================================================
def print_result(result: Dict[str, Any]):
    print("\n" + "=" * 65)
    print(f"SCENARIO: {result['scenario']}")
    print("=" * 65)

    sender = result["sender"]
    receiver = result["receiver"]

    relevance = result["relevance"]
    safety = result["safety"]

    print(f"Sender   : {sender.vehicle_id}")
    print(f"Receiver : {receiver.vehicle_id}")
    print(f"Lane     : {receiver.lane_id}")
    print(f"Distance : {abs(sender.position - receiver.position):.2f} m")
    print(f"Sender speed   : {sender.speed:.2f} m/s")
    print(f"Receiver speed : {receiver.speed:.2f} m/s")
    print(f"Message  : {result['message'].message_type.value}")

    print("\nRELEVANCE")
    print("-" * 65)

    print(f"Relevant : {relevance.relevant}")
    print(f"Score    : {relevance.score}")
    print(f"Reason   : {relevance.reason}")

    print("\nSAFETY")
    print("-" * 65)

    if safety is None:
        print("Risk     : N/A")
        print("Action   : IGNORE")

    else:
        print(f"Risk     : {safety.risk.value}")
        print(f"Action   : {safety.action.value}")
        print(f"Reason   : {safety.reason}")

# ==========================================================
# RUN ALL SCENARIOS
# ==========================================================

if __name__ == "__main__":
    print("\n")
    print("#" * 65)
    print("#              SIH V2V SCENARIO TEST SUITE")
    print("#" * 65)

    # Scenario 1
    result_1 = scenario_same_lane_hazard()
    print_result(result_1)

    # Scenario 2
    result_2 = scenario_adjacent_lane()
    print_result(result_2)

    # Scenario 3 — Warning case
    result_3 = scenario_different_speed(receiver_speed=15.0)
    print_result(result_3)

    # Scenario 3 — Critical case
    result_4 = scenario_different_speed(receiver_speed=22.0)
    print_result(result_4)

    # Scenario 4
    result_5 = scenario_emergency_brake()
    print_result(result_5)

    print("\n")
    print("#" * 65)
    print("#              SCENARIOS COMPLETE")
    print("#" * 65)