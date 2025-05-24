def main_sum():
    """ This is the main function that calculates the sum
        of two numbers and print the result
    """
    num1 = float(input('Enter the first number: '))
    num2 = float(input('Enter the second number: '))
    sum = num1 + num2
    print(f'The sum of {num1} and {num2} is: {sum:.2f}')
    return sum

main_sum()