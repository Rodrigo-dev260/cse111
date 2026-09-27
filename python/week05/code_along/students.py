import csv
def read_dictionary(filename, key_column_index):
    s_dictionary = {}
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            key_value = row[key_column_index]
            s_dictionary[key_value] = row
    return s_dictionary

def main():
    KEY_INDEX = 0
    NAME_INDEX = 1
    students = read_dictionary('studants.csv', KEY_INDEX)
    print(students)

if __name__ == '__main__':
    main()