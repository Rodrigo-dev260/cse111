import datetime
import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name('inventory.csv')
inventory = []
CATEGORIES = ['Shelf-Stable', 'Frozen']


def load_inventory():
    global inventory
    inventory = []
    try:
        with open(DATA_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['quantity'] = int(row['quantity'])
                inventory.append(row)
    except FileNotFoundError:
        inventory = []


def save_inventory():
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'category', 'quantity', 'expiration_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in inventory:
            writer.writerow(product)


def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def choose_category():
    print('\nAvailable categories:')
    for index, category in enumerate(CATEGORIES, start=1):
        print(f'{index}. {category}')
    choice = input('Choose a category (number): ')
    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        return CATEGORIES[int(choice) - 1]
    else:
        print("❌ Invalid category. Using 'Shelf-Stable' by default.")
        return 'Shelf-Stable'


def register_product():
    name = input('Product name: ')
    category = choose_category()
    quantity = int(input('Quantity: '))
    expiration_date = input('Expiration date (dd/mm/yyyy): ')

    if quantity < 0:
        print('❌ Invalid quantity. It must be non-negative.')
        return
    if not validate_date(expiration_date):
        print('❌ Invalid date. Use the format dd/mm/yyyy.')
        return

    product = {
        'name': name,
        'category': category,
        'quantity': quantity,
        'expiration_date': expiration_date,
    }
    inventory.append(product)
    save_inventory()
    print(f"\n✅ Product '{name}' successfully registered in the '{category}' category!\n")


def list_inventory():
    if not inventory:
        print('\n⚠️ No products registered.\n')
        return

    print('\n📦 Full inventory report:')
    for index, product in enumerate(inventory, start=1):
        print(f"{index}. {product['name']} | Category: {product['category']} | "
              f"Qty: {product['quantity']} | Expiration: {product['expiration_date']}")
    print()


def record_stock_in():
    list_inventory()
    index = int(input('Enter the product number for stock in: ')) - 1
    if 0 <= index < len(inventory):
        quantity = int(input('Quantity to add: '))
        if quantity > 0:
            inventory[index]['quantity'] += quantity
            save_inventory()
            print(f"\n✅ Stock in recorded! New stock for {inventory[index]['name']}: {inventory[index]['quantity']}\n")
        else:
            print('❌ Invalid quantity.')
    else:
        print('\n❌ Invalid product.')


def record_stock_out():
    list_inventory()
    index = int(input('Enter the product number for stock out: ')) - 1
    if 0 <= index < len(inventory):
        quantity = int(input('Quantity to remove: '))
        if 0 < quantity <= inventory[index]['quantity']:
            inventory[index]['quantity'] -= quantity
            save_inventory()
            print(f"\n✅ Stock out recorded! New stock for {inventory[index]['name']}: {inventory[index]['quantity']}\n")
        else:
            print('\n❌ Invalid or insufficient quantity.\n')
    else:
        print('\n❌ Invalid product.\n')


def check_alerts():
    today = datetime.datetime.today()
    print('\n🚨 Inventory alerts:')
    alerts_found = False

    for product in inventory:
        if product['quantity'] < 5:
            print(f"⚠️ Low stock: {product['name']} (Qty: {product['quantity']})")
            alerts_found = True

        try:
            expiration_date = datetime.datetime.strptime(product['expiration_date'], '%d/%m/%Y')
            days_remaining = (expiration_date - today).days
            if days_remaining <= 5:
                status = 'EXPIRED' if days_remaining < 0 else f'expires in {days_remaining} days'
                print(f"⚠️ Expiration alert: {product['name']} ({status})")
                alerts_found = True
        except ValueError:
            print(f"❌ Invalid date for {product['name']}")

    if not alerts_found:
        print('✅ No alerts at this time.\n')


def report_by_category():
    print('\nAvailable report categories:')
    for index, category in enumerate(CATEGORIES, start=1):
        print(f'{index}. {category}')
    choice = input('Choose a category (number): ')

    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        selected_category = CATEGORIES[int(choice) - 1]
        print(f'\n📊 Product report for category: {selected_category}')
        print('-' * 48)
        found = False
        for product in inventory:
            if product['category'] == selected_category:
                print(f"- {product['name']} | Qty: {product['quantity']} | Expiration: {product['expiration_date']}")
                found = True
        if not found:
            print(f"⚠️ No products registered in the '{selected_category}' category.\n")
    else:
        print('❌ Invalid category.\n')


def main_menu():
    load_inventory()
    options = {
        '1': register_product,
        '2': list_inventory,
        '3': check_alerts,
        '4': record_stock_in,
        '5': record_stock_out,
        '6': report_by_category,
    }

    while True:
        print('-' * 38)
        print('=== Inventory Control System ===')
        print('-' * 38)
        print('1. Register product')
        print('2. Full inventory report')
        print('3. Check alerts')
        print('4. Record stock in')
        print('5. Record stock out')
        print('6. Report by category (Shelf-Stable or Frozen)')
        print('7. Exit')

        option = input('Choose an option: ')
        if option == '7':
            print('\nClosing the system. Goodbye!')
            break
        elif option in options:
            options[option]()
        else:
            print('\n❌ Invalid option. Please try again.')


if __name__ == '__main__':
    main_menu()
