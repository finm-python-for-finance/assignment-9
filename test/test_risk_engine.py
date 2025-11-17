import pytest
from risk_engine import RiskEngine
from order import Order


def test_order_passes_risk_checks():
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order("AAPL", 500, "1")  # buy 500

    assert risk.check(order) is True


def test_order_size_exceeds_limit():
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order("AAPL", 1500, "1")  # too large

    with pytest.raises(ValueError) as exc:
        risk.check(order)

    assert "exceeds max" in str(exc.value)


def test_position_limit_exceeded():
    risk = RiskEngine(max_order_size=1000, max_position=2000)

    # first order, valid size
    order1 = Order("AAPL", 900, "1")
    risk.check(order1)
    risk.update_position(order1)

    # second order, still valid size, but pushes position over limit
    order2 = Order("AAPL", 1200, "1")  # 900 + 1200 = 2100 > 2000

    with pytest.raises(ValueError):
        risk.check(order2)


def test_update_position_buy():
    risk = RiskEngine()
    order = Order("AAPL", 300, "1")

    risk.update_position(order)
    assert risk.positions["AAPL"] == 300


def test_update_position_sell():
    risk = RiskEngine()
    order = Order("AAPL", 300, "2")  # sell

    risk.update_position(order)
    assert risk.positions["AAPL"] == -300


def test_multiple_updates_accumulate():
    risk = RiskEngine()
    o1 = Order("MSFT", 100, "1")  # buy 100
    o2 = Order("MSFT", 50, "2")   # sell 50

    risk.update_position(o1)
    risk.update_position(o2)

    assert risk.positions["MSFT"] == 50
