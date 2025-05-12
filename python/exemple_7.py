# Exemple 7
import math
# Get a number from the user
number = float(input('Enter a number: '))
# Call the math.sqrt fution and 
#immediately print its return value
print(math.sqrt(number))
# Call the math.sqrt function againn and 
#use its return value in an if statement.
if math.sqrt(number) < 100:
    print(f'The square root is less than 100.')
elif math.sqrt(number) > 100:
    print(f'The square root is more then 100.')
else:
    print(f'The square root is exactly 100.') 
