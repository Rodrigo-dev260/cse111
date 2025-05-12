DISCOUNT_RATE=.1
TAX_RATE=.06
subtotal=float(input('Enter the subtotal'))
print(f'Total order {subtotal}')
discount=subtotal * DISCOUNT_RATE
print(f'Discount {discount}')
subtotal -=discount
tax=subtotal * TAX_RATE
total=subtotal + tax
print(f'Subtotal {subtotal}')
print(f'tax {tax}')
print(f'Total Due {total}')