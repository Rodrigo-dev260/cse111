# Example 3
import math
# Define a funtcion named computer_cylinder_volume.
def computer_cylinder_volume(radius, height):
    """ Compute and return the volume of a cylinder.
    Parameters
    radius: the radius of the cylinder
    height: the height of the cylinder
    Return: the volume of the cylinder
    """
    # Compute the volume of the cylinder.
    volume = math.pi * radius**2 * height
    # Retur the volume of the cylinder so that the 
    # volume can be used somewhere else in the program.
    return volume