# fix_parser.py
class FixParser:
    REQUIRED_FIELDS = ["35", "55", "54", "38"]  # MsgType, Symbol, Side, Qty

    def parse(self, raw: str) -> dict:
        """
        Convert FIX message string to dict.
        Example: "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2"
        """
        if not raw:
            raise ValueError("Empty FIX message")

        parts = raw.split("|")
        msg = {}

        for p in parts:
            if "=" not in p:
                continue
            k, v = p.split("=", 1)
            msg[k] = v

        # Validate required fields
        missing = [tag for tag in self.REQUIRED_FIELDS if tag not in msg]
        if missing:
            raise ValueError(f"Missing required FIX fields: {missing}")

        return msg


if __name__ == "__main__":
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
    print(FixParser().parse(msg))
