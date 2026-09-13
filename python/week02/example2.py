# Exemple 2
import math
# Define a function named print_cylinder_volume.
def print_cylinder_volume(radius, height):
    """ Compute and print the volume of a cylinder.
    Parameters
    radius: the radius of the cylinder
    height: the height od the cylinder
    Return: nothing
    """
    # Compute the volume of the cylinder.
    volume = math.pi * radius**2 * height
    # Print the volume of the cylinder.
    print(volume)

print_cylinder_volume(2.4, 4.1)