import math
from pytest import approx
# Exemple 5
def tes_sqrt():
    assert math.sqrt(5) == approx(2.24, rel=0.01)
