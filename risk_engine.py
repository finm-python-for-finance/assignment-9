# risk_engine.py
class RiskEngine:
    def __init__(self, max_order_size=1000, max_position=2000):
        self.max_order_size = max_order_size
        self.max_position = max_position
        self.positions = {}  # symbol → net qty

    def check(self, order) -> bool:
        """Validate an order. Raise ValueError on failure."""

        # Order size limit
        if order.qty > self.max_order_size:
            raise ValueError(f"Order size {order.qty} exceeds max {self.max_order_size}")

        # Position limit
        current_pos = self.positions.get(order.symbol, 0)
        new_pos = current_pos + (order.qty if order.side == "1" else -order.qty)

        if abs(new_pos) > self.max_position:
            raise ValueError(
                f"Position {new_pos} exceeds limit {self.max_position}"
            )

        return True

    def update_position(self, order):
        """Update symbol position after a fill."""
        delta = order.qty if order.side == "1" else -order.qty
        self.positions[order.symbol] = self.positions.get(order.symbol, 0) + delta
