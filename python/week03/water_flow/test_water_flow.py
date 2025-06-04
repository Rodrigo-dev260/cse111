import pytest
from water_flow import pressure_loss_from_fittings

def test_typical_values():
    result = pressure_loss_from_fittings(2.0, 5)
    expected = -(0.04 * 2 * 998.2 * 2.0 * 5) / 2000
    assert result == pytest.approx(expected, rel=1e-5)

def test_zero_fittings():
    result = pressure_loss_from_fittings(2.0, 0)
    assert result == 0

def test_zero_velocity():
    result = pressure_loss_from_fittings(0, 10)
    assert result == 0

def test_large_values():
    result = pressure_loss_from_fittings(10.0, 100)
    expected = -(0.04 * 2 * 998.2 * 10.0 * 100) / 2000
    assert result == pytest.approx(expected, rel=1e-5)

def test_negative_velocity():
    # Testa caso estranho — não faz sentido fisicamente, mas vamos ver o comportamento.
    result = pressure_loss_from_fittings(-2.0, 5)
    expected = -(0.04 * 2 * 998.2 * -2.0 * 5) / 2000
    assert result == pytest.approx(expected, rel=1e-5)
