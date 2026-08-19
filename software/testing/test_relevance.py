from simulation.scenarios import (
    scenario_same_lane_hazard,
    scenario_adjacent_lane,
)
from intelligence.relevance import evaluate_relevance

def test_same_lane_vehicle_is_relevant():
    result = scenario_same_lane_hazard()
    relevance = result["relevance"]
    assert relevance.relevant is True
    assert relevance.score == 100


def test_adjacent_lane_vehicle_is_not_relevant():
    result = scenario_adjacent_lane()
    relevance = result["relevance"]
    assert relevance.relevant is False


def test_vehicle_behind_sender_is_relevant():
    sender = {
        "vehicle_id": "A",
        "lane_id": 1,
        "position": 100.0,
        "speed": 10.0,
        "heading": 0.0,
    }

    receiver = {
        "vehicle_id": "B",
        "lane_id": 1,
        "position": 80.0,
        "speed": 15.0,
        "heading": 0.0,
    }

    result = evaluate_relevance(
        receiver=receiver,
        sender=sender,
        max_relevant_distance=30.0,
    )
    assert result.relevant is True


def test_vehicle_ahead_is_not_relevant():
    sender = {
        "vehicle_id": "A",
        "lane_id": 1,
        "position": 80.0,
        "speed": 10.0,
        "heading": 0.0,
    }

    receiver = {
        "vehicle_id": "B",
        "lane_id": 1,
        "position": 100.0,
        "speed": 15.0,
        "heading": 0.0,
    }

    result = evaluate_relevance(
        receiver=receiver,
        sender=sender,
        max_relevant_distance=30.0,
    )
    assert result.relevant is False


def test_far_vehicle_is_not_relevant():
    sender = {
        "vehicle_id": "A",
        "lane_id": 1,
        "position": 150.0,
        "speed": 10.0,
        "heading": 0.0,
    }

    receiver = {
        "vehicle_id": "B",
        "lane_id": 1,
        "position": 50.0,
        "speed": 15.0,
        "heading": 0.0,
    }

    result = evaluate_relevance(
        receiver=receiver,
        sender=sender,
        max_relevant_distance=30.0,
    )

    assert result.relevant is False


def test_different_direction_is_not_relevant():
    sender = {
        "vehicle_id": "A",
        "lane_id": 1,
        "position": 100.0,
        "speed": 10.0,
        "heading": 0.0,
    }

    receiver = {
        "vehicle_id": "B",
        "lane_id": 1,
        "position": 80.0,
        "speed": 15.0,
        "heading": 180.0,
    }

    result = evaluate_relevance(
        receiver=receiver,
        sender=sender,
        max_relevant_distance=30.0,
    )
    assert result.relevant is False