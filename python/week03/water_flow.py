DENSITY_WATER = 998.2  # kg/m^3

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    return -0.04 * 2 * 998.2 * fluid_velocity * quantity_fittings / 2000
