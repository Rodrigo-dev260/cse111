import math
def main():
    name = '#1 Picnic'
    radius = 6.83
    height = 10.16
    volume = can_vol(radius, height)
    print(f'{name} volume={volume}')

def can_vol(radius, height):
    vol = math.pi * radius ** 2 * height
    return vol

main()
