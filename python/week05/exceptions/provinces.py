with open('provinces.txt', 'r') as file:
    provinces = [line.strip() for line in file]

print(provinces)

provinces.pop(0)

provinces.pop(-1)

provinces = [line.replace('AB', 'Alberta') for line in provinces]

num_alberta = provinces.count('Alberta')

print(f'Alberta occurs {num_alberta} times in the modified list.')