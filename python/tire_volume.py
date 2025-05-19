import math # Import the math module for calculations
# Ask the user for tire dimensions
# Get the width, aspect ratio, and diameter of the tire
width = float(input('Enter the width of the tire in mm (ex 205): '))
aspect_ratio = float(input('Enter the aspect ratio of the tire (ex 60): '))
diameter = float(input('Enter the diameter of the wheel in inches (ex 15): '))
#calculate the volume of tire
wheel_diameter_mm = diameter * 25.4
# Convert diameter from inches to mm
sidewall_height_mm = (aspect_ratio / 100) * width
# Calculate the sidewall height in mm
total_diameter_mm = wheel_diameter_mm + 2 * sidewall_height_mm
# Calculate the total diameter in mm
outer_radius_m = (total_diameter_mm / 2) / 1000
# Convert to meters
inner_radius_m = (wheel_diameter_mm / 2) / 1000
width_m = width / 1000
volume = math.pi * (outer_radius_m**2 - inner_radius_m**2) * width_m
# Convert to liters
volume_liters = volume * 1000
# Print the result to the user
print(f'The approximate volume is: {volume_liters:.2f} liters')





