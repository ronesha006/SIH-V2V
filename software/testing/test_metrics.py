from monitoring.event_logger import EventLogger
from monitoring.metrics import Metrics


def create_test_logger():
    logger = EventLogger()

    logger.log_event(
        sender="A",
        receiver="B",
        message_type="OBSTACLE_ALERT",
        relevant=True,
        relevance_score=100,
        ttc=1.67,
        risk="CRITICAL",
        action="BRAKE",
        latency=None,
    )

    logger.log_event(
        sender="A",
        receiver="C",
        message_type="OBSTACLE_ALERT",
        relevant=False,
        relevance_score=40,
        ttc=None,
        risk=None,
        action=None,
        latency=None,
    )

    logger.log_event(
        sender="B",
        receiver="A",
        message_type="OBSTACLE_ALERT",
        relevant=True,
        relevance_score=100,
        ttc=4.0,
        risk="WARNING",
        action="SLOW_DOWN",
        latency=None,
    )

    return logger


def test_basic_metrics():

    logger = create_test_logger()

    metrics = Metrics()
    metrics.update(logger.get_events())

    assert metrics.messages_sent() == 3
    assert metrics.messages_received() == 3

    assert metrics.packet_loss_percentage() == 0.0

    assert metrics.relevant_events() == 2
    assert metrics.ignored_events() == 1

    assert metrics.warning_events() == 1
    assert metrics.critical_events() == 1

    assert metrics.brake_actions() == 1
    assert metrics.slow_down_actions() == 1


def test_no_latency_during_simulation():

    logger = create_test_logger()

    metrics = Metrics()
    metrics.update(logger.get_events())

    assert metrics.average_latency() is None
    assert metrics.minimum_latency() is None
    assert metrics.maximum_latency() is None


def test_real_latency_values():

    logger = EventLogger()

    logger.log_event(
        sender="A",
        receiver="B",
        message_type="OBSTACLE_ALERT",
        relevant=True,
        relevance_score=100,
        ttc=1.5,
        risk="CRITICAL",
        action="BRAKE",
        latency=0.020,
    )

    logger.log_event(
        sender="A",
        receiver="C",
        message_type="OBSTACLE_ALERT",
        relevant=True,
        relevance_score=100,
        ttc=3.0,
        risk="WARNING",
        action="SLOW_DOWN",
        latency=0.040,
    )

    metrics = Metrics()
    metrics.update(logger.get_events())

    assert metrics.average_latency() == 0.030
    assert metrics.minimum_latency() == 0.020
    assert metrics.maximum_latency() == 0.040