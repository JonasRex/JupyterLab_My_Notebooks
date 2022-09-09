class Student():
       
    def __init__(self, name, gender, data_sheet, image_url):
        self.name = name
        self.gender = gender
        self.data_sheet = DataSheet(data_sheet)
        self.image_url = image_url
        
        
    def __repr__(self) -> str:
        return 'Student(%r, %r, %r, %r)' % (self.name, self.gender, self.data_sheet, self.image_url)
    
    def __str__(self) -> str:
        return '{name}, {gender}, {ds}, {url}'.format(
            name=self.name,
            gender=self.gender,
            ds=self.data_sheet,
            url=self.image_url
            )
    def __iter__(self):
        return iter([self.name, self.gender, self.data_sheet, self.image_url])
    
    def get_avg_grade(self):
        grades = self.data_sheet.get_grades_as_list()
        
        return sum(grades) / len(grades)
    
    def get_avg_grade_by_list(self, grades):
        
        return sum(grades) / len(grades)
        

class DataSheet():
    
    def __init__(self, courses=[]):
        #self.courses = courses
        self.courses = []
        for course in courses:
            new_course = Course(course.name, course.classroom, course.teacher, course.ETCS, course.grade)
            self.courses.append(new_course)
    
    def __repr__(self) -> str:
        return 'DataSheet(%r)' % (self.courses)   
    
    def __str__(self) -> str:
        return '{courses}'.format(
            courses=self.courses)
        
    def __iter__(self):
        return iter(self.courses)
        
    def get_grades_as_list(self):
        return list([course.grade for course in self.courses])

class Course():
    
    def __init__(self, name, classroom, teacher, ETCS, grade):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher
        self.ETCS = ETCS
        self.grade = grade

    def __repr__(self) -> str:
        return 'Course(%r, %r, %r, %r, %r)' % (self.name, self.classroom, self.teacher, self.ETCS, self.grade)
    
    def __str__(self) -> str:
        return '{name}, {classroom}, {teacher}, {ETCS}, {grade}'.format(
            name=self.name,
            classroom=self.classroom,
            teacher=self.teacher,
            ETCS=self.ETCS,
            grade=self.grade
            )
        
    def __iter__(self):
        return iter([self.name, self.classroom, self.teacher, self.ETCS, self.grade])