from math import isclose
from water_flow import pressure_loss_from_fittings

def test_pressure_loss_from_fittings():
    assert isclose(pressure_loss_from_fittings(0.00, 3), 0.000, abs_tol=0.001)
    assert isclose(pressure_loss_from_fittings(1.65, 0), 0.000, abs_tol=0.001)
    assert isclose(pressure_loss_from_fittings(1.65, 2), -0.109, abs_tol=0.001)
    assert isclose(pressure_loss_from_fittings(1.75, 2), -0.122, abs_tol=0.001)
    assert isclose(pressure_loss_from_fittings(1.75, 5), -0.306, abs_tol=0.001)
