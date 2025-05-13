from datetime import datetime
DISCOUNT_DAYS=[2,3]
DISCOUNT_RATE=.1
TAX_RATE=.06
today=datetime.now()
dow=today.weekday()
subtotal=0
quantity=1
while quantity !=0:
    quantity=int(input(f'Enter the quantity:'))
    if quantity !=0:
        price=float(input('Enter the price: '))
        subtotal+=quantity * price   
print(f'Total order {subtotal:.2f}')
discount=0
if dow in DISCOUNT_DAYS:
    if subtotal > 50:
        discount=round(subtotal * DISCOUNT_RATE,2)
        print(f'Discount {discount:.2f}')
    else:
        short=50-subtotal
        print(f'You can get a discount by ordering {short:.2f} more.')
subtotal -=discount
tax=round(subtotal * TAX_RATE,2)
total=subtotal + tax

print(f'tax {tax:.2f}')
print(f'Total Due {total:.2f}')