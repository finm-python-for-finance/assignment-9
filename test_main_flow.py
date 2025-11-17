import json
import tempfile
import os
import pytest

from main import process_message, fix, risk, log
from order import OrderState
from logger import Logger


@pytest.fixture
def temp_logger():
    """Create a temporary logger instance isolated from the real events.json."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name

    # Create a new Logger instance for testing
    logger = Logger(path=path)
    logger.events = []  # clear events
    
    yield logger, path

    # cleanup
    os.remove(path)


def test_process_message_success(monkeypatch, temp_logger):
    logger, path = temp_logger

    # monkeypatch global logger in main.py
    monkeypatch.setattr("main.log", logger)

    # Valid FIX message
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"

    process_message(raw)

    # The message should generate 2 events:
    # - OrderCreated
    # - OrderFilled
    assert len(logger.events) == 2

    assert logger.events[0]["type"] == "OrderCreated"
    assert logger.events[1]["type"] == "OrderFilled"

    # Check order was filled
    # It is difficult to capture the actual order instance here,
    # but we can check RiskEngine updated the position:
    assert risk.positions.get("AAPL") == 500


def test_process_message_rejected(monkeypatch, temp_logger):
    logger, path = temp_logger

    # monkeypatch global logger
    monkeypatch.setattr("main.log", logger)

    # This order qty exceeds max_order_size=1000 → should be rejected
    raw = "8=FIX.4.2|35=D|55=MSFT|54=1|38=5000|40=2|10=128"

    process_message(raw)

    # Should generate 2 logs:
    # - OrderCreated
    # - OrderRejected
    assert len(logger.events) == 2
    assert logger.events[1]["type"] == "OrderRejected"
    assert "exceeds" in logger.events[1]["data"]["reason"]

    # RiskEngine should NOT update the position
    assert risk.positions.get("MSFT", 0) == 0


def test_logger_save_writes_json(monkeypatch, temp_logger):
    logger, path = temp_logger

    monkeypatch.setattr("main.log", logger)

    # produce two events
    process_message("8=FIX.4.2|35=D|55=IBM|54=1|38=100|40=2|10=128")
    process_message("8=FIX.4.2|35=D|55=TSLA|54=1|38=200|40=2|10=128")

    # Now save to file
    logger.save()

    # Verify file content
    with open(path, "r") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["type"] == "OrderCreated"
    assert data[1]["type"] in ("OrderFilled", "OrderRejected")
