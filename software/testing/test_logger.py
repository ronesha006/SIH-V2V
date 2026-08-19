from monitoring.event_logger import EventLogger


def test_log_event():

    logger = EventLogger()

    event = logger.log_event(
        sender="A",
        receiver="B",
        message_type="OBSTACLE_ALERT",
        relevant=True,
        relevance_score=100,
        ttc=1.67,
        risk="CRITICAL",
        action="BRAKE",
    )

    assert logger.count() == 1

    assert event.sender == "A"
    assert event.receiver == "B"
    assert event.message_type == "OBSTACLE_ALERT"

    assert event.relevant is True
    assert event.relevance_score == 100

    assert event.ttc == 1.67
    assert event.risk == "CRITICAL"
    assert event.action == "BRAKE"

    # Simulation has no real communication latency yet.
    assert event.latency is None


def test_latest_event():

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
    )

    latest = logger.get_latest()

    assert latest is not None
    assert latest.receiver == "C"


def test_clear_events():

    logger = EventLogger()

    logger.log_event(
        sender="A",
        receiver="B",
        message_type="EMERGENCY_BRAKE",
        relevant=True,
        relevance_score=100,
        ttc=0.5,
        risk="CRITICAL",
        action="BRAKE",
    )

    assert logger.count() == 1

    logger.clear()

    assert logger.count() == 0
    assert logger.get_latest() is None