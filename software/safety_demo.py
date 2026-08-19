from models.vehicle_state import VehicleState

from communication.message_schema import (
    build_obstacle_alert,
    build_emergency_brake,
)

from intelligence.safety import (
    evaluate_message_safety,
    RiskLevel,
    VehicleAction,
)


# ==========================================
# VEHICLE A — SENDER
# ==========================================

vehicle_a = VehicleState.create(

    vehicle_id="A",

    lane_id=1,

    position=100,

    speed=10,

    heading=0,

    obstacle_distance=30,

    obstacle_detected=True,

    brake_status=False,
)


# ==========================================
# VEHICLE B — SAME LANE
# ==========================================

vehicle_b = VehicleState.create(

    vehicle_id="B",

    lane_id=1,

    position=80,

    speed=10,

    heading=0,
)


# ==========================================
# CREATE OBSTACLE MESSAGE
# ==========================================

obstacle_message = build_obstacle_alert(

    vehicle_a,

    sequence=1,
)


print("\n==============================")
print("OBSTACLE ALERT → VEHICLE B")
print("==============================")


relevance, decision = evaluate_message_safety(

    message=obstacle_message,

    receiver=vehicle_b.to_dict(),
)


print("Relevant :", relevance.relevant)

print("Score    :", relevance.score)

print("Reason   :", relevance.reason)

print()


if decision:

    print("Risk     :", decision.risk.value)

    print("Action   :", decision.action.value)

    print("Safety   :", decision.reason)


# ==========================================
# VERIFY OBSTACLE CASE
# ==========================================

assert relevance.relevant is True

assert decision is not None

assert decision.risk == RiskLevel.CRITICAL

assert decision.action == VehicleAction.BRAKE


# ==========================================
# EMERGENCY BRAKE
# ==========================================

emergency_message = build_emergency_brake(

    vehicle_a,

    sequence=2,
)


print("\n==============================")
print("EMERGENCY BRAKE → VEHICLE B")
print("==============================")


relevance, decision = evaluate_message_safety(

    message=emergency_message,

    receiver=vehicle_b.to_dict(),
)


print("Relevant :", relevance.relevant)

print("Score    :", relevance.score)

print("Reason   :", relevance.reason)

print()

print("Risk     :", decision.risk.value)

print("Action   :", decision.action.value)

print("Safety   :", decision.reason)


# ==========================================
# VERIFY EMERGENCY CASE
# ==========================================

assert relevance.relevant is True

assert decision.risk == RiskLevel.CRITICAL

assert decision.action == VehicleAction.BRAKE


print("\n==============================")
print("TEST RESULT")
print("==============================")

print("SAFETY ENGINE TESTS PASSED!")