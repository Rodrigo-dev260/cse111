def water_column_height(tower_height, tank_height):
    # A altura da coluna de água é a soma da altura da torre
    # com metade da altura do tanque (considerando que está cheio).
    height = tower_height + (tank_height / 2)
    return height

