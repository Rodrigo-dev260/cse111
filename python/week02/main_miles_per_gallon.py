start_hodometer = float(input('Enter the starting odometer reading in miles: '))
end_hodometer = float(input('Enter the ending odometer reading in milles: '))
amont_gallons = float(input('Enter the amount of fuel used in gallons: '))

mpg = (end_hodometer - start_hodometer) / amont_gallons
lp100k = 235.215 / mpg
print(f'Fuel efficiency in milles per gallon is: {mpg:.2f}')