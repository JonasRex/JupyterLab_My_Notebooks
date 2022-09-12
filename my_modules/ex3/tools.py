from random import randint
import argparse



def get_rand(lst):
    """Return random item from attached list"""
    return lst[randint(1, len(lst)) - 1]


def get_rand_datasheet():
    """Generates a datasheet with minimum 3 courses (max 5)"""
    courses = []
    # Finding 4 - 7 unique courses
    while len(courses) <= randint(4, 7) - 1:
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
        name = f'{get_rand(MALE_NAMES)} {get_rand(LAST_NAMES)}'
        datasheet = get_rand_datasheet()
        student = Student(name, "male", datasheet, get_rand(PIC_URLS_MALES))
        students.append(student)
    return students


def assign_random_grades():
    # Made it less likely to return failing grades. If 2 or lower do a reroll once. Can technically still roll a failing grade again
    grade = get_rand(GRADES)
    if grade <= 2:
        return get_rand(GRADES)
    return grade


class NotEnoughStudentsException(Exception):
    def __init__(self, top, limit):
        self.top = top
        self.limit = limit
        self.message = f'Not enough students found in top: {top}, with a ETCS score higher than: {limit}!'
        super().__init__(self.message)
   

def closest_to_finishing(students, top=3, limit=120):
    sorted_by_ETCS = sorted(students, key=lambda x: x.data_sheet.get_total_ETCS(), reverse=True)
    closest_to_finish = [student for student in sorted_by_ETCS if student.data_sheet.get_total_ETCS() >= limit ]
    try:
        # Checks if the final candidate qualifies or not. 
        if len(closest_to_finish) >= top:
            return closest_to_finish[:top]
        else:
            raise NotEnoughStudentsException(top, limit)
    except (NotEnoughStudentsException) as e:
        print(e)
    
        
if __name__ == '__main__':
    from ex3_data import *
    from assignment1 import *
    
    parser = argparse.ArgumentParser(description='A program that creates n amount of students with a datasheet')
    parser.add_argument('amount', help='Input number of students to create')
    
    args = parser.parse_args()
    
    
    print(create_n_number_of_students(int(args.amount)))
else:
    from my_modules.ex3.ex3_data import *
    from my_modules.ex3.assignment1 import *




