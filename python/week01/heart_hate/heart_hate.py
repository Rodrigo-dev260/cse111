# Exemple 2
# The input function always a string.
k = input("Please enter a number: ")
m = input("Please enter another number: ")
n = k + m  # string plus string makes string
print(f"k: {type (k)} {k}")
print(f"m: {type (m)} {m}")
print(f"n: {type (n)} {n}")
print()
# The int and float functions convert a string to a number.
p = int(input("Please enter a number: "))
q = float(input("Please enter another number: ")) # float
r = p + q  # int plus float makes float
print(f"p: {type(p)} {p}")
print(f"q: {type(q)} {q}")
print(f"r: {type(r)} {r}")
