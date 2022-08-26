import retirement_calculator_service.calculator_service as cs
import pytest

def test_future_value():
    assert int(cs.future_value(100, 12, 1)) == 112
    assert int(cs.future_value(100, 10, 2)) == 121
    with pytest.raises(TypeError):
        cs.future_value("hey there", 10, 30)