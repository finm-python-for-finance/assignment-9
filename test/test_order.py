import pytest
from order import Order, OrderState


def test_initial_state_is_new():
    order = Order("AAPL", 100, "1")
    assert order.state == OrderState.NEW


def test_new_to_acked_transition():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.ACKED)
    assert order.state == OrderState.ACKED


def test_new_to_rejected_transition():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.REJECTED)
    assert order.state == OrderState.REJECTED


def test_acked_to_filled_transition():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.ACKED)
    order.transition(OrderState.FILLED)
    assert order.state == OrderState.FILLED


def test_acked_to_canceled_transition():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.ACKED)
    order.transition(OrderState.CANCELED)
    assert order.state == OrderState.CANCELED


def test_invalid_transition_is_ignored():
    order = Order("AAPL", 100, "1")
    # NEW → FILLED is not allowed
    order.transition(OrderState.FILLED)
    assert order.state == OrderState.NEW  # should stay unchanged


def test_no_transition_allowed_after_filled():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.ACKED)
    order.transition(OrderState.FILLED)

    order.transition(OrderState.CANCELED)  # should be ignored
    assert order.state == OrderState.FILLED


def test_no_transition_allowed_after_rejected():
    order = Order("AAPL", 100, "1")
    order.transition(OrderState.REJECTED)

    order.transition(OrderState.ACKED)  # invalid
    assert order.state == OrderState.REJECTED
