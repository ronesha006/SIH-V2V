from simulation.scenarios import (
    scenario_same_lane_hazard,
    scenario_adjacent_lane,
    scenario_different_speed,
    scenario_emergency_brake,
)
from intelligence.safety import (
    RiskLevel,
    VehicleAction,
)


def test_same_lane_hazard_produces_safety_decision():
    result = scenario_same_lane_hazard()
    assert result["relevance"].relevant is True
    assert result["safety"] is not None

    assert result["safety"].risk in (
        RiskLevel.WARNING,
        RiskLevel.CRITICAL,
    )

    assert result["safety"].action in (
        VehicleAction.SLOW_DOWN,
        VehicleAction.BRAKE,
    )


def test_adjacent_lane_is_ignored():
    result = scenario_adjacent_lane()
    assert result["relevance"].relevant is False
    assert result["safety"] is None


def test_ttc_warning_case():
    result = scenario_different_speed(receiver_speed=15.0)
    assert result["relevance"].relevant is True
    assert result["safety"] is not None
    assert (result["safety"].risk == RiskLevel.WARNING)
    assert (result["safety"].action == VehicleAction.SLOW_DOWN)


def test_ttc_critical_case():
    result = scenario_different_speed(receiver_speed=22.0)
    assert result["relevance"].relevant is True
    assert result["safety"] is not None
    assert (result["safety"].risk == RiskLevel.CRITICAL)
    assert (result["safety"].action == VehicleAction.BRAKE)


def test_emergency_brake():
    result = scenario_emergency_brake()
    assert result["relevance"].relevant is True
    assert result["safety"] is not None
    assert (result["safety"].risk == RiskLevel.CRITICAL)
    assert (result["safety"].action == VehicleAction.BRAKE)