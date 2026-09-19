# Constantes
PVC_SCHED80_INNER_DIAMETER = 0.28687   # metros
PVC_SCHED80_FRICTION_FACTOR = 0.013    # adimensional
SUPPLY_VELOCITY = 1.65                 # m/s

HDPE_SDR11_INNER_DIAMETER = 0.048692   # metros
HDPE_SDR11_FRICTION_FACTOR = 0.018     # adimensional
HOUSEHOLD_VELOCITY = 1.75              # m/s

WATER_DENSITY = 998.2                  # kg/m³
GRAVITY = 9.80665                      # m/s²
WATER_DYNAMIC_VISCOSITY = 0.0010016    # Pa·s


def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    loss = pressure_loss_from_pipe(
        PVC_SCHED80_INNER_DIAMETER, length1, PVC_SCHED80_FRICTION_FACTOR, SUPPLY_VELOCITY
    )
    pressure += loss

    loss = pressure_loss_from_fittings(SUPPLY_VELOCITY, quantity_angles)
    pressure += loss

    reynolds = reynolds_number(PVC_SCHED80_INNER_DIAMETER, SUPPLY_VELOCITY)
    loss = pressure_loss_from_pipe_reduction(
        PVC_SCHED80_INNER_DIAMETER, SUPPLY_VELOCITY, reynolds, HDPE_SDR11_INNER_DIAMETER
    )
    pressure += loss

    loss = pressure_loss_from_pipe(
        HDPE_SDR11_INNER_DIAMETER, length2, HDPE_SDR11_FRICTION_FACTOR, HOUSEHOLD_VELOCITY
    )
    pressure += loss

    print(f"Pressure at house: {pressure:.1f} kilopascals")


def water_column_height(tower_height, tank_height):
    return tower_height + (3 * tank_height / 4)


def pressure_gain_from_water_height(height):
    return (WATER_DENSITY * GRAVITY * height) / 1000


def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    # O denominador correto para converter diretamente de Pa para kPa é 2000
    numerator = -friction_factor * pipe_length * WATER_DENSITY * (fluid_velocity ** 2)
    denominator = 2000 * pipe_diameter
    return numerator / denominator


def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calcula a perda de pressão em kPa devido a conexões (curvas de 90°)."""
    return (-0.04 * WATER_DENSITY * (fluid_velocity ** 2) * quantity_fittings) / 2000


def reynolds_number(hydraulic_diameter, fluid_velocity):
    return (WATER_DENSITY * fluid_velocity * hydraulic_diameter) / WATER_DYNAMIC_VISCOSITY


def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    k = (0.1 + (50 / reynolds_number)) * (((larger_diameter / smaller_diameter) ** 4) - 1)
    return (-k * WATER_DENSITY * (fluid_velocity ** 2)) / 2000


if __name__ == "__main__":
    main()