from models.vehicle_state import VehicleState

from communication.message_schema import (
    build_obstacle_alert,
)

from intelligence.safety import (
    evaluate_message_safety,
    RiskLevel,
    VehicleAction,
)


# ==========================================
# TEST 1 — LOW TTC
# ==========================================

vehicle_a = VehicleState.create(
    vehicle_id="A",
    lane_id=1,
    position=100,
    speed=10,
    heading=0,
    obstacle_distance=80,
    obstacle_detected=True,
)


vehicle_b = VehicleState.create(
    vehicle_id="B",
    lane_id=1,
    position=80,
    speed=15,
    heading=0,
)


message = build_obstacle_alert(
    vehicle_a,
    sequence=1,
)


relevance, decision = evaluate_message_safety(
    message=message,
    receiver=vehicle_b.to_dict(),
)


print("\n==============================")
print("TEST 1 — TTC WARNING")
print("==============================")

print("TTC-based decision:")
print("Risk   :", decision.risk.value)
print("Action :", decision.action.value)
print("Reason :", decision.reason)


assert relevance.relevant is True

assert decision.risk == RiskLevel.WARNING

assert decision.action == VehicleAction.SLOW_DOWN


# ==========================================
# TEST 2 — VERY LOW TTC
# ==========================================

vehicle_b_fast = VehicleState.create(
    vehicle_id="B",
    lane_id=1,
    position=80,
    speed=22,
    heading=0,
)


relevance, decision = evaluate_message_safety(
    message=message,
    receiver=vehicle_b_fast.to_dict(),
)


print("\n==============================")
print("TEST 2 — TTC CRITICAL")
print("==============================")

print("TTC-based decision:")
print("Risk   :", decision.risk.value)
print("Action :", decision.action.value)
print("Reason :", decision.reason)


assert relevance.relevant is True

assert decision.risk == RiskLevel.CRITICAL

assert decision.action == VehicleAction.BRAKE


print("\n==============================")
print("TEST RESULT")
print("==============================")

print("TTC SAFETY INTEGRATION PASSED!")