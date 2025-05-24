import math
nitems = int(input('Enter the number of items: '))
items_per_box = int(input('Enter the number of items per box: '))

# Calculate the number of boxes needed to pack the items
boxes = math.ceil(nitems / items_per_box)
#print the results
print(f'For {nitems} items, packing {items_per_box} items in each box, you will need {boxes} boxes')