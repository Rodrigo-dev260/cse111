# Example 2
import math
def print_cylinder_volume(radius, height):
    """ Compute and print the volume of a cylinder.
    Parameters
    radius: the radius of a cylinder
    height: the height of a cylinder
    Return: nothing
    """
    # Compute the volume of the cylinder.
    volume = math.pi * radius**2 * height
    # Print the volume of the cylinder.
    print(volume)