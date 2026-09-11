import math
n1 = int(input('Enter the number of items: '))
iperbox = int(input('Enter the number of items per box: '))
number_of_box = math.ceil(n1 / iperbox)
# display a blank line
print()
# display he results for the user o see.
print(f'For {n1} items, packing {iperbox} items in each box, you will need {number_of_box} boxes')