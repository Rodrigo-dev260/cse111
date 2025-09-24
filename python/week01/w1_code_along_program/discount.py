DSCOUNT_RATE=.1
TAX_RATE=.06
subtotal=input('Enter thesubtotal: ')
tax=subtotal * TAX_RATE
total=subtotal + tax
print(f'Subtotal {subtotal}')
print(f'Tax {tax}')
