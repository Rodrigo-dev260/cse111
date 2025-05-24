"""assert temperature < 0, "Temperature is below absolute zero!"
assert len(given_name) > 0, "Name cannot be empty!"
assert balance == 0, "Balance cannot be zero!"
assert school_year > 0, "School year must be a positive integer!"
"""

def test_min():
    assert min(7, -3, 0, 2)  == 3

