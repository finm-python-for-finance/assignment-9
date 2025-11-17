# order.py
from enum import Enum, auto

class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()


class Order:
    def __init__(self, symbol, qty, side):
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.state = OrderState.NEW

    def transition(self, new_state):
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        }

        current = self.state

        # If state not allowed, ignore
        if current in allowed and new_state in allowed[current]:
            self.state = new_state
            print(f"Order {self.symbol} is now {new_state.name}")
        else:
            print(f"[WARN] Transition {current.name} → {new_state.name} not allowed")
