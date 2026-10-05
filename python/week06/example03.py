# Example 3
from functools import reduce
def main():
    numbers = [
        87, 95, 72, 92, 95, 88, 84
        ]
    func_add = lambda a, b: a + b
    total = reduce(func_add, numbers)
    average = total / len(numbers)
    print(f'Average: {average:.2f}')
# Call main to start the program
if __name__ == '__main__':
    main()
