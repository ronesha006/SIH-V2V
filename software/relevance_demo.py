from models.vehicle_state import VehicleState

from communication.message_schema import (
    build_obstacle_alert,
)

from intelligence.relevance import (
    evaluate_message_relevance,
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
# VEHICLE C — DIFFERENT LANE
# ==========================================

vehicle_c = VehicleState.create(
    vehicle_id="C",
    lane_id=2,
    position=80,
    speed=10,
    heading=0,
)


# ==========================================
# A CREATES V2V MESSAGE
# ==========================================

message = build_obstacle_alert(
    vehicle_a,
    sequence=1,
)


print("\n==============================")
print("V2V MESSAGE")
print("==============================")

print(message)


# ==========================================
# B RECEIVES MESSAGE
# ==========================================

result_b = evaluate_message_relevance(
    message=message,
    receiver=vehicle_b.to_dict(),
)


print("\n==============================")
print("VEHICLE B")
print("==============================")

print("Relevant :", result_b.relevant)
print("Score    :", result_b.score)
print("Reason   :", result_b.reason)


# ==========================================
# C RECEIVES SAME MESSAGE
# ==========================================

result_c = evaluate_message_relevance(
    message=message,
    receiver=vehicle_c.to_dict(),
)


print("\n==============================")
print("VEHICLE C")
print("==============================")

print("Relevant :", result_c.relevant)
print("Score    :", result_c.score)
print("Reason   :", result_c.reason)


# ==========================================
# VERIFY
# ==========================================

assert result_b.relevant is True

assert result_c.relevant is False

assert message.sender_id == "A"

assert message.sequence == 1


print("\n==============================")
print("TEST RESULT")
print("==============================")

print("V2V MESSAGE → RELEVANCE TEST PASSED!")