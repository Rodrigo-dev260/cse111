# Example 4
# The variable e and f can be any floating-
# point number from any calculation.
e = 7.135
f = 7.128
if abs(e - f) < 0.01:
    print(f'{e} and {f} are close enough so')
    print("We'll consider them to")
else:
    print(f'{e} and {f} are not close and')
    print('therefor not equal')

