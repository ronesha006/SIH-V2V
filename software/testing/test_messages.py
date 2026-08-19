from models.vehicle_state import VehicleState
from communication.message_schema import (
    MessageType,
    build_state_message,
    build_obstacle_alert,
    build_emergency_brake,
    build_heartbeat,
)
from communication.encoder import encode_message 
from communication.decoder import decode_message

def create_test_vehicle():
    return VehicleState.create(
        vehicle_id="A",
        lane_id=1,
        position=100.0,
        speed=10.0,
        heading=0.0,
        obstacle_distance=20.0,
        obstacle_detected=True,
        brake_status=False,
    )


def test_state_message_creation():
    vehicle = create_test_vehicle()
    message = build_state_message(
        vehicle_state=vehicle,
        sequence=1,
    )

    assert message.message_type == MessageType.STATE_UPDATE
    assert message.sender_id == "A"
    assert message.sequence == 1
    assert message.payload["vehicle_id"] == "A"


def test_obstacle_message_creation():
    vehicle = create_test_vehicle()
    message = build_obstacle_alert(
        vehicle_state=vehicle,
        sequence=1,
    )

    assert (message.message_type== MessageType.OBSTACLE_ALERT)
    assert message.sender_id == "A"
    assert message.payload["lane_id"] == 1
    assert message.payload["position"] == 100.0
    assert message.payload["obstacle_distance"] == 20.0


def test_emergency_brake_message_creation():
    vehicle = create_test_vehicle()
    message = build_emergency_brake(
        vehicle_state=vehicle,
        sequence=5,
    )
    assert (message.message_type== MessageType.EMERGENCY_BRAKE)
    assert message.sender_id == "A"
    assert message.sequence == 5


def test_heartbeat_creation():
    message = build_heartbeat(
        sender_id="A",
        sequence=10,
        timestamp=12345.0,
    )

    assert (message.message_type== MessageType.HEARTBEAT)
    assert message.sender_id == "A"
    assert message.sequence == 10
    assert message.timestamp == 12345.0

def test_message_encode_decode():
    vehicle = create_test_vehicle()
    original = build_obstacle_alert(
        vehicle_state=vehicle,
        sequence=7,
    )
    encoded = encode_message(original)
    decoded = decode_message(encoded)

    assert (decoded.message_type == original.message_type)
    assert decoded.sender_id == original.sender_id
    assert decoded.sequence == original.sequence
    assert (decoded.payload == original.payload)


def test_invalid_empty_message():
    try:
        decode_message("")
        assert False

    except ValueError:
        assert True