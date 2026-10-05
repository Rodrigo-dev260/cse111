import csv
from datetime import datetime

def read_dictionary(filename):
    prod_dictionary = {}
    with open('products.csv', 'r', newline='')as pfile:
        reader = csv.reader(pfile)
        next(reader)
        for row in reader:
            product_id = row[0]  #product cod
            name = row[1]        # product name
            price =float(row[2]) # product price
            prod_dictionary[product_id] = {'name': name, 'price': price}
    return prod_dictionary

try:        
    products_dict = read_dictionary("products.csv")

    print("=== ARAUJO MARKET ===")
    print("Order Receipt\n")

    total_items = 0
    subtotal = 0.0

    with open("request.csv", newline="") as request_file:
        request_reader = csv.reader(request_file)
        next(request_reader)  # jump the header

        for row in request_reader:
            product_id = row[0]
            quantity = int(row[1])

            product = products_dict[product_id]   # busca no catálogo
            name = product["name"]
            price = product["price"]
            line_total = price * quantity

            print(f"{name}: {quantity} x ${price:.2f} = ${line_total:.2f}")

            total_items += quantity
            subtotal += line_total

    # calculate total and tax
    print("\nNumber of items:", total_items)
    print("Subtotal: $",f"{subtotal:.2f}")

    tax = subtotal * 0.06
    total = subtotal + tax

    print("sale tax (6%): $", f"{tax:.2f}")
    print("Total due: $", f"{total:.2f}")

    print("\nThanks for your purchase!")
    current_time = datetime.now()
    print("Date and time:", current_time.strftime("%d/%m/%Y %H:%M:%S"))

except FileNotFoundError:
    print("Erro: One of the CSV files wasn't found.")
except PermissionError:
    print("Erro: Permission denied when accessing the file.")
except KeyError as e:
    print(f"Erro: Product with ID {e} doesn't exist in the catalog.")



