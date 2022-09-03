import argparse

def print_file_content(file):
    with open(file) as data:
        for line in data:
            print(line)
        

def write_list_to_file(output_file, lst):
    list_as_string = ' '.join(lst)
    with open(output_file, 'w') as file_object:
        file_object.write(list_as_string)
    print(f'{output_file} been added to data folder')

def read_csv(input_file):
    with open(input_file) as data:
        lst = []
        for line in data:
            lst.append(line)
        return lst

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that handles csv files')
    parser.add_argument('path', help='File path for the csv file')
    parser.add_argument('--file', help='The name of the file')

    args = parser.parse_args()

    print_file_content(f'{args.path}/{args.file}')
