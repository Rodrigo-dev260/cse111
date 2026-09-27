# Example 1
def main():
    # Create a list that contains strings.
    colors = ['yellow', 'red', 'green', 'yellow', 'blue']
    # Call the built-in len function
    # and print the lenght of the list.
    lenght = len(colors)
    print(f'Number of elements: {lenght}')
    # Print the element that is stored
    # at index 2 in the colors list.
    print(colors[2])
    # Change the element that is stored at 
    # index 3 from "yellow" to "purple".
    colors[3] = 'purple'
    # Print the entire colors list.
    print(colors)
    # Call main to start this program.
if  __name__== '__main__':
    main()