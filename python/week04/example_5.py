# Example 5
def main():
    # create a list of colors names.
    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    # Use a for loop to print each element in the list.
    for color in colors:
        print(color)
    print()
    # User a different for loop to 
    # print each element from the list.
    for i in range(len(colors)):
        # Use the index i to retrieve
        # an element from the list.
        color = colors[i]
        print(color)
# Call main to start the program.
if __name__ == '__main__':
    main()