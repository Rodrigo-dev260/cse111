# example 5
import math 
# Define a funtcion amed main.
def main():
    # Get the radius and height from the user.
    radius = float(input('Enter the radius of the cylinder: '))
    height = float(input('Enter the height of the cylinder: '))
    # Compute the volume of the cylinder.
    volume = math.pi * radius**2 * height
    # Print the volume of the cylinder.
    print(f'Volume: {volume:.2f}')
    # Start this program by
    # calling the mais fuhnction.
main()