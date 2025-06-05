def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    WATER_DENSITY = 998.2  # kg/m³
    perda = (-0.04 * 2 * WATER_DENSITY * fluid_velocity * quantity_fittings) / 2000
    print(f"Perda de pressão por conexões: {perda:.2f} kPa")
    return perda

def reynolds_number(hydraulic_diameter, fluid_velocity):
    WATER_DENSITY = 998.2  # kg/m³
    DYNAMIC_VISCOSITY = 0.0010016  # Pa·s
    reynolds = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / DYNAMIC_VISCOSITY
    print(f"Número de Reynolds: {reynolds:.2f}")
    return reynolds

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    WATER_DENSITY = 998.2  # kg/m³
    k = 0.1 + ((50 / reynolds_number) * (((larger_diameter / smaller_diameter) ** 4) - 1))
    perda = (-2 * k * WATER_DENSITY * fluid_velocity) / 1000
    print(f"Perda de pressão por redução de diâmetro: {perda:.2f} kPa")
    return perda

def pressure_loss_from_pipe(diameter, length, friction_factor, velocity):
    WATER_DENSITY = 998.2  # kg/m³
    perda = (-friction_factor * length * WATER_DENSITY * (velocity**2)) / (2 * diameter * 2000)
    print(f"Perda de pressão por atrito no tubo: {perda:.2f} kPa")
    return perda

def water_column_height(tower_height, tank_height):
    altura = tower_height + ((3 * tank_height) / 4)
    print(f"Altura da coluna de água: {altura:.2f} metros")
    return altura

def pressure_gain_from_water_height(height):
    WATER_DENSITY = 998.2  # kg/m³
    GRAVITY = 9.80665  # m/s²
    ganho = (WATER_DENSITY * GRAVITY * height) / 2000
    print(f"Ganho de pressão pela altura da água: {ganho:.2f} kPa")
    return ganho

PVC_SCHED80_INNER_DIAMETER = 0.28687  # metros
PVC_SCHED80_FRICTION_FACTOR = 0.013  
SUPPLY_VELOCITY = 1.65
HDPE_SDR11_INNER_DIAMETER = 0.048692  # metros
HDPE_SDR11_FRICTION_FACTOR = 0.018  
HOUSEHOLD_VELOCITY = 1.75

def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)

    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss

    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss

    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss

    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY

    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss

    print(f"Pressão final na casa: {pressure:.1f} kPa")

if __name__ == "__main__":
    main()
