from formula import parse_formula


def make_periodic_table():
    periodic_table_dict = {
        "Ac": ["Actinium", 227],
        "Ag": ["Silver", 107.8682],
        "Al": ["Aluminum", 26.9815386],
        "Ar": ["Argon", 39.948],
        "As": ["Arsenic", 74.9216],
        "At": ["Astatine", 210],
        "Au": ["Gold", 196.966569],
        "B": ["Boron", 10.811],
        "Ba": ["Barium", 137.327],
        "Be": ["Beryllium", 9.012182],
        "Bi": ["Bismuth", 208.9804],
        "Br": ["Bromine", 79.904],
        "C": ["Carbon", 12.0107],
        "Ca": ["Calcium", 40.078],
        "Cd": ["Cadmium", 112.411],
        "Ce": ["Cerium", 140.116],
        "Cl": ["Chlorine", 35.453],
        "Co": ["Cobalt", 58.933195],
        "Cr": ["Chromium", 51.9961],
        "Cs": ["Cesium", 132.9054519],
        "Cu": ["Copper", 63.546],
        "Dy": ["Dysprosium", 162.5],
        "Er": ["Erbium", 167.259],
        "Eu": ["Europium", 151.964],
        "F": ["Fluorine", 18.9984032],
        "Fe": ["Iron", 55.845],
        "Fr": ["Francium", 223],
        "Ga": ["Gallium", 69.723],
        "Gd": ["Gadolinium", 157.25],
        "Ge": ["Germanium", 72.64],
        "H": ["Hydrogen", 1.00794],
        "He": ["Helium", 4.002602],
        "Hf": ["Hafnium", 178.49],
        "Hg": ["Mercury", 200.59],
        "Ho": ["Holmium", 164.93032],
        "I": ["Iodine", 126.90447],
        "In": ["Indium", 114.818],
        "Ir": ["Iridium", 192.217],
        "K": ["Potassium", 39.0983],
        "Kr": ["Krypton", 83.798],
        "La": ["Lanthanum", 138.90547],
        "Li": ["Lithium", 6.941],
        "Lu": ["Lutetium", 174.9668],
        "Mg": ["Magnesium", 24.305],
        "Mn": ["Manganese", 54.938045],
        "Mo": ["Molybdenum", 95.96],
        "N": ["Nitrogen", 14.0067],
        "Na": ["Sodium", 22.98976928],
        "Nb": ["Niobium", 92.90638],
        "Nd": ["Neodymium", 144.242],
        "Ne": ["Neon", 20.1797],
        "Ni": ["Nickel", 58.6934],
        "Np": ["Neptunium", 237],
        "O": ["Oxygen", 15.9994],
        "Os": ["Osmium", 190.23],
        "P": ["Phosphorus", 30.973762],
        "Pa": ["Protactinium", 231.03588],
        "Pb": ["Lead", 207.2],
        "Pd": ["Palladium", 106.42],
        "Pm": ["Promethium", 145],
        "Po": ["Polonium", 209],
        "Pr": ["Praseodymium", 140.90765],
        "Pt": ["Platinum", 195.084],
        "Pu": ["Plutonium", 244],
        "Ra": ["Radium", 226],
        "Rb": ["Rubidium", 85.4678],
        "Re": ["Rhenium", 186.207],
        "Rh": ["Rhodium", 102.9055],
        "Rn": ["Radon", 222],
        "Ru": ["Ruthenium", 101.07],
        "S": ["Sulfur", 32.065],
        "Sb": ["Antimony", 121.76],
        "Sc": ["Scandium", 44.955912],
        "Se": ["Selenium", 78.96],
        "Si": ["Silicon", 28.0855],
        "Sm": ["Samarium", 150.36],
        "Sn": ["Tin", 118.71],
        "Sr": ["Strontium", 87.62],
        "Ta": ["Tantalum", 180.94788],
        "Tb": ["Terbium", 158.92535],
        "Tc": ["Technetium", 98],
        "Te": ["Tellurium", 127.6],
        "Th": ["Thorium", 232.03806],
        "Ti": ["Titanium", 47.867],
        "Tl": ["Thallium", 204.3833],
        "Tm": ["Thulium", 168.93421],
        "U": ["Uranium", 238.02891],
        "V": ["Vanadium", 50.9415],
        "W": ["Tungsten", 183.84],
        "Xe": ["Xenon", 131.293],
        "Y": ["Yttrium", 88.90585],
        "Yb": ["Ytterbium", 173.054],
        "Zn": ["Zinc", 65.38],
        "Zr": ["Zirconium", 91.224]
    }
    
    return periodic_table_dict

def compute_molar_mass(formula, periodic_table_dict):
    """
    Compute the molar mass of a compound given its formula.
    Parameters:
        formula: string with the molecular formula (e.g., "H2O")
        periodic_table_dict: dictionary of elements and atomic masses
    Return:
        total molar mass in grams/mole (float)
    """
    parsed = parse_formula(formula, periodic_table_dict)
    total_mass = 0
    for element, count in parsed:
        atomic_mass = periodic_table_dict[element][1]
        total_mass += atomic_mass * count
    return total_mass


def compute_sample_mass(moles, molar_mass):
    """
    Compute the mass of a chemical sample in grams.
    Parameters:
        moles: number of moles (float)
        molar_mass: molar mass in grams/mole (float)
    Return:
        mass of the sample in grams (float)
    """
    return moles * molar_mass


def compute_percent_composition(element_masses, sample_mass):
    """
    Compute the percent composition of each element in the sample.
    Parameters:
        element_masses: dictionary {element: mass in grams}
        sample_mass: total mass of the sample in grams (float)
    Return:
        dictionary {element: percent composition}
    """
    percent_comp = {}
    for element, mass in element_masses.items():
        percent = (mass / sample_mass) * 100
        percent_comp[element] = percent
    return percent_comp


def compute_element_masses(formula, periodic_table_dict, moles):
    """
    Compute the mass of each element in the sample.
    Parameters:
        formula: molecular formula (string)
        periodic_table_dict: dictionary of elements and atomic masses
        moles: number of moles (float)
    Return:
        dictionary {element: mass in grams}
    """
    parsed = parse_formula(formula, periodic_table_dict)
    element_masses = {}
    for element, count in parsed:
        atomic_mass = periodic_table_dict[element][1]
        mass = atomic_mass * count * moles
        element_masses[element] = mass
    return element_masses


def main():
    """
    Main program execution:
    - Ask user for molecular formula
    - Compute molar mass
    - Ask user for sample mass in grams
    - Compute number of moles
    - Compute mass of each element
    - Compute percent composition of each element
    - Print results
    """
    formula = input("Enter the molecular formula of the sample: ")
    periodic_table_dict = make_periodic_table()
    molar_mass = compute_molar_mass(formula, periodic_table_dict)
    print(f"{molar_mass:.5f} grams/mole")

    grams = float(input("Enter the mass in grams of the sample: "))
    moles = grams / molar_mass
    print(f"{moles:.5f} moles.")

    element_masses = compute_element_masses(formula, periodic_table_dict, moles)
    print("\nMass of each element in the sample:")
    for element, mass in element_masses.items():
        print(f"{element}: {mass:.3f} g")

    percent_comp = compute_percent_composition(element_masses, grams)
    print("\nPercent composition of each element:")
    for element, percent in percent_comp.items():
        print(f"{element}: {percent:.2f}%")


if __name__ == "__main__":
    main()
