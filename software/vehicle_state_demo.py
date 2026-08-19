from models.vehicle_state import VehicleState

from communication.message_schema import (
    build_state_message,
    build_obstacle_alert,
    build_emergency_brake,
)

from communication.encoder import encode_message

from communication.decoder import decode_message


# ==========================================================
# CREATE VEHICLE
# ==========================================================

vehicle = VehicleState.create(

    vehicle_id="A",

    lane_id=1,

    position=100,

    speed=10,

    heading=0,

    obstacle_distance=30,

    obstacle_detected=True,

    brake_status=False,
)


print("\n==============================")
print("VEHICLE STATE")
print("==============================")

print(vehicle)


# ==========================================================
# STATE → DICTIONARY
# ==========================================================

print("\n==============================")
print("VEHICLE DICTIONARY")
print("==============================")

print(vehicle.to_dict())


# ==========================================================
# STATE UPDATE MESSAGE
# ==========================================================

state_message = build_state_message(

    vehicle,

    sequence=1,
)


print("\n==============================")
print("STATE UPDATE")
print("==============================")

print(state_message)


# ==========================================================
# OBSTACLE ALERT
# ==========================================================

obstacle_message = build_obstacle_alert(

    vehicle,

    sequence=2,
)


print("\n==============================")
print("OBSTACLE ALERT")
print("==============================")

print(obstacle_message)


# ==========================================================
# EMERGENCY BRAKE
# ==========================================================

brake_message = build_emergency_brake(

    vehicle,

    sequence=3,
)


print("\n==============================")
print("EMERGENCY BRAKE")
print("==============================")

print(brake_message)


# ==========================================================
# ENCODE MESSAGE
# ==========================================================

encoded = encode_message(
    obstacle_message
)


print("\n==============================")
print("ENCODED MESSAGE")
print("==============================")

print(encoded)


# ==========================================================
# DECODE MESSAGE
# ==========================================================

decoded = decode_message(
    encoded
)


print("\n==============================")
print("DECODED MESSAGE")
print("==============================")

print(decoded)


# ==========================================================
# VERIFY
# ==========================================================

assert decoded.message_type == obstacle_message.message_type

assert decoded.sender_id == "A"

assert decoded.sequence == 2

assert decoded.payload["lane_id"] == 1

assert decoded.payload["obstacle_distance"] == 30


print("\n==============================")
print("TEST RESULT")
print("==============================")

print("ALL VEHICLE + MESSAGE TESTS PASSED!")