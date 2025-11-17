import pytest
from fix_parser import FixParser


def test_parse_valid_fix_message():
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2"

    result = parser.parse(msg)

    assert result["35"] == "D"
    assert result["55"] == "AAPL"
    assert result["54"] == "1"
    assert result["38"] == "100"
    assert result["8"] == "FIX.4.2"
    assert result["40"] == "2"
    assert isinstance(result, dict)


def test_missing_required_field_should_raise():
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1"  # missing tag 38 (qty)

    with pytest.raises(ValueError) as exc:
        parser.parse(msg)

    assert "Missing required FIX fields" in str(exc.value)
    assert "38" in str(exc.value)


def test_empty_message_should_raise():
    parser = FixParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_message_with_invalid_parts_should_ignore_invalid():
    parser = FixParser()
    msg = "8=FIX.4.2|INVALID|35=D|55=AAPL|54=1|38=50"

    result = parser.parse(msg)

    # Still valid because invalid segment is skipped
    assert result["55"] == "AAPL"
    assert result["38"] == "50"
