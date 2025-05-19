import math # Import the math module for calculations
import datetime # Get the current date and time
tire_prices = {
    (185, 50, 14): 350.00,
    (205, 60, 15): 450.00,
    (225, 55, 16): 550.00,
    (245, 40, 18): 750.00,
}
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
# Convert to liters
print(f'The approximate volume is: {volume_liters:.2f} liters')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
# Append the results to a file
with open('volumes.txt', 'a') as volume_file:
    volume_file.write(f'{current_date}, {int(width)}, {int(aspect_ratio)}, {int(diameter)}, {volume_liters:.2f}\n')
# Read the last line from the file    
with open('volumes.txt', 'rt') as volume_file:
    lines = volume_file.readlines()
    if lines:
        print(lines[-1].strip())

# Verify if there is a price for the tire
tire_size = (int(width), int(aspect_ratio), int(diameter))
if tire_size in tire_prices:
    print(f'The price of tires with these dimensions is: ${tire_prices[tire_size]:.2f}')

    # Ask the the user if he witchs to buy the tire
    buy = input('Do you want to buy these tires? (yes/no): ') # If the user wants to buy the tire
    # Yes or no condition
    if buy == 'yes':
        phone_number = input('Please enter your phone number: ')
        with open('volumes.txt', 'a') as volume_file:
            volume_file.write(f',{phone_number}\n')
        print('Your request has been saved. A representative will contact you soon.')
else:
    print('Sorry we do not have a price for these tires.') # If the tire size is not in the dictionary, print a message