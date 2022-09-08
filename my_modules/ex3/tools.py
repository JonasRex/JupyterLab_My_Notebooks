from random import randint
from my_modules.ex3.ex3_data import *
from my_modules.ex3.assignment1 import *


def get_rand(lst):
    """Return random item from attached list"""
    return lst[randint(1, len(lst)) - 1]


def get_rand_datasheet():
    """Generates a datasheet with minimum 3 courses (max 5)"""
    courses = []
    # Finding 3 - 5 unique courses
    while len(courses) <= randint(3, 5) - 1:
        c = get_rand(COURSES)
        # Check if course already has been selected
        if not c in courses:
            courses.append(c)
            
    # Convert to Course objects and apply random grade for each.    
    courses = [Course(c[0], c[1], c[2], c[3], assign_random_grades()) for c in courses]
    # Convert to DataSheet object 
    new_ds = DataSheet(courses)    
    return new_ds


def create_n_number_of_students(n):
    students = []
    for i in range(n):
        name = f'{get_rand(MALE_NAMES)} {get_rand(MALE_NAMES)}'
        datasheet = get_rand_datasheet()
        student = Student(name, "male", datasheet, get_rand(PIC_URLS_MALES))
        students.append(student)
    return students


def assign_random_grades():
    # TODO: Make it less likely to return failing grades
    return get_rand(GRADES)