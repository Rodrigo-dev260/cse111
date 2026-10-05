def main():
  # Create and print a list named fruit.
  fruit_list = ["pear", "banana", "apple", "mango"]
  print(f"original: {fruit_list}")
  fruit_list.reverse()
  print(f'reversed: {fruit_list}')
  fruit_list.append('orange')
  print(f'append orange: {fruit_list}')
  apple_index = fruit_list.index('apple')
  fruit_list.insert(apple_index, 'cherry')
  print(f'insert cherry: {fruit_list}')
  fruit_list.remove('banana')
  print(f'remove banana: {fruit_list}')
  fruit_list.pop()
  print(f'pop orange: {fruit_list}')
  fruit_list.sort()
  print(f'sorted: {fruit_list}')
  fruit_list.clear()
  print(f'clear: {fruit_list}')

  

if __name__ == '__main__':
  main()