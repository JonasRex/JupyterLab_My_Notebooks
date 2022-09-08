import csv
from my_modules.ex3.assignment1 import *

def write_students_to_csv_file(output_file, lst):            
    with open(f'data/{output_file}', 'w') as stream:
        writer = csv.writer(stream)
        writer.writerows(lst)
    print(f'{output_file} been added to data folder')
    
    
def read_students_from_csv_file(input_file):
    with open(input_file) as stream:
        reader = csv.reader(stream)
        return [Student(*row) for row in reader]
        