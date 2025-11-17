# 📘 Mini Trading System

A simplified end-to-end electronic trading system used to demonstrate core concepts in order handling, FIX parsing, risk checks, state machines, and logging.

This project contains 4 main components:

```
FIX → Parser → Order → RiskEngine → Logger → events.json
```

Modules included:

| Module | Description |
|--------|-------------|
| `fix_parser.py` | Converts FIX messages into Python dictionaries with validation. |
| `order.py` | Implements order state machine (NEW → ACKED → FILLED, etc.). |
| `risk_engine.py` | Performs max order size & position limit checks. |
| `logger.py` | Singleton logger that records events to JSON. |
| `main.py` | Integrates all modules to process trading messages. |

---

# 🧩 1. FIX Message Parser (`fix_parser.py`)

### ✔ Features
- Parses raw FIX strings such as:  
  `8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2`
- Converts into a Python dictionary
- Validates required tags:
  - `35` (MsgType)  
  - `55` (Symbol)  
  - `54` (Side: 1=Buy, 2=Sell)  
  - `38` (Quantity)

### ✔ Example
```python
from fix_parser import FixParser

msg = FixParser().parse("8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2")
print(msg)
```

---

# 🧩 2. Order Lifecycle Simulator (`order.py`)

### ✔ State Machine

Valid state transitions:

```
NEW → ACKED → FILLED
NEW → REJECTED
ACKED → CANCELED
```

### ✔ Example
```python
from order import Order, OrderState

order = Order("AAPL", 100, "1")
order.transition(OrderState.ACKED)
order.transition(OrderState.FILLED)
```

Invalid transitions print warnings, but do not terminate the program.

---

# 🧩 3. Risk Check Engine (`risk_engine.py`)

### ✔ Rules Implemented
- **Maximum Order Size** (default: 1000 shares)
- **Maximum Position Limit per Symbol** (default: ±2000 shares)
- Long orders (`side="1"`) increase position; short orders (`side="2"`) decrease position

### ✔ Example
```python
risk = RiskEngine()
risk.check(order)
risk.update_position(order)
```

The `check()` method raises `ValueError` if limits are violated.

---

# 🧩 4. Event Logger (`logger.py`)

### ✔ Features
- Implemented as a **singleton**, ensuring only one logger exists
- Logs all events in the system:
  - Order creation  
  - Risk check failures  
  - State transitions  
  - Fills  
  - Rejections  
- Saves event history to `events.json`

### ✔ Example
```python
log = Logger()
log.log("OrderCreated", {"symbol": "AAPL"})
log.save()
```

---

# ⚙️ Integration (`main.py`)

### ✔ Workflow

1. Receive raw FIX message  
2. Parse FIX  
3. Create Order object  
4. Perform risk checks  
5. Acknowledge order  
6. Update position on fill  
7. Log all events  
8. Save to JSON

### ✔ Running

```bash
python main.py
```

### ✔ Sample Output
```
[LOG] OrderCreated → {...}
Order AAPL is now ACKED
Order AAPL is now FILLED
[LOG] OrderFilled → {'symbol': 'AAPL', 'qty': 500}
[LOG] Saved to events.json
```

---

# 🧪 Unit Tests

Tests included in:

```
tests/
  test_fix_parser.py
  test_order.py
  test_risk_engine.py
  test_logger.py
  test_main_flow.py
```

Run all tests:

```bash
pytest -q
```

Generate coverage report:

```bash
pytest --cov=. --cov-report=term-missing
```

A sample `coverage_report.md` is provided in the project.

---

# 📁 Project Structure

```
mini-trading-system/
├── fix_parser.py
├── order.py
├── risk_engine.py
├── logger.py
├── main.py
├── tests/
│   ├── test_fix_parser.py
│   ├── test_order.py
│   ├── test_risk_engine.py
│   ├── test_logger.py
│   └── test_main_flow.py
├── coverage_report.md
├── events.json
└── README.md
```


