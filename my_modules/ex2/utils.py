from os import listdir
from os.path import isfile, join
import argparse

def get_file_names(folderpath,out='output.txt', write_or_abend='w'):
    """ takes a path to a folder and writes all filenames in the folder to a specified output file"""
    # Make a list of files & dirs and then remove everything that is not a file
    files_and_dir = listdir(folderpath)
    lst = [file for file in files_and_dir if isfile(join(folderpath, file))]
    print(f'Files in {folderpath}: ', lst)

    # Convert list to string and write to new file.
    list_as_string = f'/{folderpath}/: ' + ' '.join(lst)
    with open(f'data/{out}', write_or_abend) as file_object:
        # Make line break if its a sub folder being abended
        if write_or_abend == 'a':
            file_object.write('\n')
        file_object.write(list_as_string)

    # Makes sure it doesn't print this msg out if its a sub folder
    if write_or_abend == 'w':    
        print(f'{out} has been created with the file names in the data folder.')

def get_all_file_names(folderpath,out='output.txt'):
    """takes a path to a folder and write all filenames recursively (files of all sub folders to)"""
    # First run the other function
    get_file_names(folderpath, out)

    # Now find the sub folders
    files_and_dir = listdir(folderpath)
    sub_folders = [file for file in files_and_dir if not isfile(join(folderpath, file))]
    for sub in sub_folders:
        fp = f'{folderpath}/{sub}'
        get_file_names(fp, out, 'a')

def print_line_one(file_names):
    """takes a list of filenames and print the first line of each"""
    # Using idx and enumerate just for the readability and for practicing.
    for idx, file in enumerate(file_names):
        with open(file) as data:
            for line in data:
                print(idx, line)
                # Breaking after 1 line
                break

def print_emails(file_names):
    """takes a list of filenames and print each line that contains an email (just look for @)"""
    for file in file_names:
        print(f'Lines with email adresses in {file}: ')
        print('-----------------------------------------------------------')
        with open(file) as data:
            for idx, line in enumerate(data):
                if '@' in line:
                    print(f'{idx}:', line)
                

def write_headlines(md_files, out='output.txt'):
    """takes a list of md files and writes all headlines (lines starting with #) to a file"""
    for file in md_files:
        with open(file) as data:
            for line in data:
                if '#' in line[0]:
                    print(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that creates a txt files with all the files in the path folder, including the subfolders')
    parser.add_argument('path', help='File path for the csv file')
    parser.add_argument('--out', help='The name of the output file. Default output.txt')

    args = parser.parse_args()

    get_all_file_names(args.path, f'{args.out}.txt')