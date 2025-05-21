import math
def main():
    name = '#1 Picnic'
    radius = 6.83
    height = 10.16
    volume = can_vol(radius, height)
    area = can_area(radius, height)
    eff = volume / area
    print(f'{name} volume={volume:.2f} area={area:.2f} efficiency={eff:.2f}')

def can_vol(radius, height):
    volume = math.pi * radius ** 2 * height
    return volume

def can_area(radius, height):
    area = 2 * math.pi * radius * (radius + height)
    return area
main()