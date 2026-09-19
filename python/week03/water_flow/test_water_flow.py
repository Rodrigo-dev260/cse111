import pytest
from water_flow import (
    pressure_loss_from_fittings,
    reynolds_number,
    pressure_loss_from_pipe_reduction,
    pressure_loss_from_pipe,
    water_column_height,
    pressure_gain_from_water_height,
)

# Test for water column height
def test_water_column_height():
    assert water_column_height(0.0, 0.0) == pytest.approx(0.0, 0.001)
    assert water_column_height(0.0, 10.0) == pytest.approx(7.5, 0.001)
    assert water_column_height(25.0, 0.0) == pytest.approx(25.0, 0.001)
    assert water_column_height(48.3, 12.8) == pytest.approx(57.9, 0.001)

# Test for pressure gain from water height
def test_pressure_gain_from_water_height():
    assert pressure_gain_from_water_height(0.0) == pytest.approx(0.0, abs=0.001)
    assert pressure_gain_from_water_height(30.2) == pytest.approx(295.628, abs=0.001)
    assert pressure_gain_from_water_height(50.0) == pytest.approx(489.450, abs=0.001)

# Test for pressure loss from pipe friction
def test_pressure_loss_from_pipe():
    assert pressure_loss_from_pipe(0.048692, 0.0, 0.018, 1.75) == pytest.approx(0.0, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.0, 1.75) == pytest.approx(0.0, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 0.0) == pytest.approx(0.0, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.75) == pytest.approx(-113.008, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.65) == pytest.approx(-100.462, abs=0.001)
    assert pressure_loss_from_pipe(0.286870, 1000.0, 0.013, 1.65) == pytest.approx(-61.576, abs=0.001)
    assert pressure_loss_from_pipe(0.286870, 1800.75, 0.013, 1.65) == pytest.approx(-110.884, abs=0.001)

# Test for pressure loss from fittings
def test_pressure_loss_from_fittings():
    assert pressure_loss_from_fittings(0.00, 3) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 0) == pytest.approx(0.000, abs=0.001) 
    assert pressure_loss_from_fittings(1.65, 2) == pytest.approx(-0.109, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 2) == pytest.approx(-0.122, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 5) == pytest.approx(-0.306, abs=0.001)

# Test for Reynolds number
def test_reynolds_number():
    assert reynolds_number(0.048692, 0.0) == pytest.approx(0, abs=1)
    assert reynolds_number(0.048692, 1.65) == pytest.approx(80069, abs=1)
    assert reynolds_number(0.048692, 1.75) == pytest.approx(84922, abs=1)
    assert reynolds_number(0.286870, 1.65) == pytest.approx(471729, abs=1)
    assert reynolds_number(0.286870, 1.75) == pytest.approx(500318, abs=1)

# Test for pressure loss from pipe reduction
def test_pressure_loss_from_pipe_reduction():
    reynolds = reynolds_number(0.28687, 1.65)
    assert pressure_loss_from_pipe_reduction(0.28687, 0.0, 1, 0.048692) == pytest.approx(0.0, abs=0.001)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.65, 471729, 0.048692) == pytest.approx(-163.744, abs=0.001)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.75, 500318, 0.048692) == pytest.approx(-184.182, abs=0.001)

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])

