# water_flow.py

# Constantes globais
PVC_SCHED80_INNER_DIAMETER = 0.28687  # metros
PVC_SCHED80_FRICTION_FACTOR = 0.013  # adimensional
SUPPLY_VELOCITY = 1.65  # m/s

HDPE_SDR11_INNER_DIAMETER = 0.048692  # metros
HDPE_SDR11_FRICTION_FACTOR = 0.018  # adimensional
HOUSEHOLD_VELOCITY = 1.75  # m/s

# Função: perda de pressão por conexões
def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calcula a perda de pressão devido a conexões."""
    WATER_DENSITY = 998.2  # kg/m³
    return (-0.04 * 2 * WATER_DENSITY * fluid_velocity * quantity_fittings) / 2000

# Função: cálculo do número de Reynolds
def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calcula o número de Reynolds do fluido em um tubo."""
    WATER_DENSITY = 998.2  # kg/m³
    DYNAMIC_VISCOSITY = 0.0010016  # Pa·s
    return (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / DYNAMIC_VISCOSITY

# Função: perda de pressão por redução de diâmetro
def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calcula a perda de pressão devido à redução do diâmetro do tubo."""
    WATER_DENSITY = 998.2  # kg/m³

    k = 0.1 + ((50 / reynolds_number) * (((larger_diameter / smaller_diameter) ** 4) - 1))

    return (-2 * k * WATER_DENSITY * fluid_velocity) / 1000  # Correção aplicada!

# Função: perda de pressão por atrito no tubo
def pressure_loss_from_pipe(diameter, length, friction_factor, velocity):
    """Calcula a perda de pressão devido ao atrito no tubo."""
    WATER_DENSITY = 998.2  # kg/m³

    return (-friction_factor * length * WATER_DENSITY * (velocity**2)) / (2 * diameter * 1000)

# Função: altura da coluna de água
def water_column_height(tower_height, tank_height):
    """Calcula a altura total da coluna de água."""
    return tower_height + ((3 * tank_height) / 4)  # Correção aplicada

# Função: ganho de pressão devido à altura da coluna de água
def pressure_gain_from_water_height(height):
    """Calcula o ganho de pressão devido à altura da água."""
    WATER_DENSITY = 998.2  # kg/m³
    GRAVITY = 9.80665  # m/s²

    return (WATER_DENSITY * GRAVITY * height) / 1000  # Correção na ordem das operações

# Função principal
def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    # Cálculo inicial
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    # Primeira tubulação
    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    
    pressure -= pressure_loss_from_pipe(diameter, length1, friction, velocity)  # Correção: subtração
    pressure -= pressure_loss_from_fittings(velocity, quantity_angles)  # Correção: subtração
    pressure -= pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)  # Correção: subtração

    # Segunda tubulação
    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    
    pressure -= pressure_loss_from_pipe(diameter, length2, friction, velocity)  # Correção: subtração

    print(f"Pressure at house: {pressure:.1f} kilopascals")

if __name__ == "__main__":
    main()
