from datetime import datetime
DISCOUN_RATE = .1
TAX_RATE = .06
today = datetime.now()
dow = today.weekday()
subtotal = float(input('Enter the subtotal: '))
print(f'Total order {subtotal}')
discount = 0
if dow == 2 or dow == 3 or dow == 0:
    if subtotal > 50:
        discount = subtotal * DISCOUN_RATE
print(f'Discount {discount}')
subtotal -= discount
tax=subtotal * TAX_RATE
total = subtotal + tax

print(f'Tax {tax}')
print(f'Total Due {total}')