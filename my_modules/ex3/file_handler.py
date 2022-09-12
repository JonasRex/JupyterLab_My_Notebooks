import csv


def write_students_to_csv_file(output_file, lst):            
    with open(f'data/{output_file}', 'w') as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerows(lst)
    print(f'{output_file} been added to data folder')
    
    
def read_students_from_csv_file(input_file):
    """Doesnt work.."""
    with open(input_file) as stream:
        reader = csv.reader(stream, delimiter=";")
        return [Student(*row[1:]) for row in reader]
                  
            
def write_students_to_csv_file_by_courses(output_file, student_list):
    """A line for each of the students courses. So one student have one line for each course"""
    with open(f'data/{output_file}', 'w') as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["name", "gender", "course", "classroom", "teacher", "ETCS", "grade", "pic_url"])
        for student in student_list:
            for course in student.data_sheet.courses:   
                writer.writerow([student.name, student.gender, course.name, course.classroom, course.teacher, course.ETCS, course.grade, student.image_url])
    print(f'{output_file} been added to data folder')
                
                

def read_students_from_csv_file_by_courses(input_file):
    """Handle a line for each of the students courses. So one student have one line for each course. Returns list of all the students in the input file"""
    with open(input_file) as stream:
        reader = csv.reader(stream, delimiter=";")
        student_objs = []
        names_already_created = set()
        
        rows = [rows for rows in reader]
        for row in rows[1:]:
            # First create the student, with empty datasheet. ONLY: if the student is not created already
            if not row[0] in names_already_created:
                student_objs.append(Student(row[0], row[1], [], row[7]))
                
            # Adds name to a set, so we dont create more than one of each.
            names_already_created.add(row[0])
                
            # Create the course
            new_course = Course(row[2], row[3], row[4], row[5], row[6])
                
            # Find the student and course
            for so in student_objs:
                if so.name == row[0]:
                    so.data_sheet.courses.append(new_course)
    
        return student_objs
    
    
    
def write_three_closest_to_finish(student_list, output_file='close_to_completion.csv'):
    with open(f'data/{output_file}', 'w') as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["name", "gender", "datasheet", "image_url"])
        for student in student_list:
            writer.writerow(student)
    print(f'{output_file} been added to data folder')
            
if __name__ == '__main__':
    from assignment1 import *
    print(read_students_from_csv_file_by_courses("data/students_courses.csv"))
else:
    from my_modules.ex3.assignment1 import *