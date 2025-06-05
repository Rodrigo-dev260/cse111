import pytest
from water_flow import (
    pressure_loss_from_fittings,
    reynolds_number,
    pressure_loss_from_pipe_reduction,
    pressure_loss_from_pipe,
    water_column_height,
    pressure_gain_from_water_height,
)

# Teste da altura da coluna de água
def test_water_column_height():
    assert water_column_height(36.6, 9.1) == pytest.approx(43.425, 0.001)

# Teste do ganho de pressão pela altura da água
def test_pressure_gain_from_water_height():
    assert pressure_gain_from_water_height(43.425) == pytest.approx(212.54, 0.01)

# Teste do número de Reynolds
def test_reynolds_number():
    assert reynolds_number(0.28687, 1.65) == pytest.approx(471728.73, 0.1)

# Teste da perda de pressão por atrito no tubo
def test_pressure_loss_from_pipe():
    assert pressure_loss_from_pipe(0.28687, 1524.0, 0.013, 1.65) == pytest.approx(-46.92, 0.01)

# Teste da perda de pressão por conexões
def test_pressure_loss_from_fittings():
    assert pressure_loss_from_fittings(1.65, 3) == pytest.approx(-0.20, 0.01)

# Teste da perda de pressão por redução de diâmetro
def test_pressure_loss_from_pipe_reduction():
    reynolds = reynolds_number(0.28687, 1.65)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.65, reynolds, 0.048692) == pytest.approx(-0.75, 0.01)

# Teste da perda de pressão por atrito no segundo tubo
def test_pressure_loss_from_pipe_second():
    assert pressure_loss_from_pipe(0.048692, 15.2, 0.018, 1.75) == pytest.approx(-4.29, 0.01)

