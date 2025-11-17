
import json
import os
import tempfile
from logger import Logger


def test_logger_is_singleton():
    log1 = Logger()
    log2 = Logger()
    assert log1 is log2  # same instance


def test_log_adds_event():
    logger = Logger()
    logger.events = []  # reset for testing

    logger.log("TestEvent", {"value": 123})

    assert len(logger.events) == 1
    entry = logger.events[0]

    assert entry["type"] == "TestEvent"
    assert entry["data"] == {"value": 123}
    assert "timestamp" in entry  # auto-added


def test_log_multiple_events():
    logger = Logger()
    logger.events = []  # reset

    logger.log("A", {})
    logger.log("B", {})

    assert len(logger.events) == 2


def test_save_writes_file_correctly():
    # create a temporary file to avoid writing real events.json
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name

    try:
        logger = Logger(path=path)
        logger.events = []  # reset
        logger.log("SavedEvent", {"x": 1})

        logger.save()

        # Read file content
        with open(path, "r") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["type"] == "SavedEvent"
        assert data[0]["data"] == {"x": 1}

    finally:
        os.remove(path)  # cleanup tmp file
