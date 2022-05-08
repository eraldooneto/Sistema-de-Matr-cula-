from Subjects import *


class Student:
    def __init__(self, name, registration, semester, _type, approved):
        self.name = name
        self.registration = registration
        self.enrolled_classes = [] # list of Subject
        self.approved_classes = approved # list({'subject': grade}
        self.semester = semester
        self.coefficent = sum([float(i[1]) for i in self.approved_classes]) / len(self.approved_classes) if len(self.approved_classes) else None
        self.type = _type

    def __str__(self):
        return 'Name: %s\nSemester: %s\nCoeff: %s'%(self.name, self.semester, self.coefficent)
        

    def getEnrolledClasses(self):
        return ', '.join(str(i) for i in self.enrolled_classes)

    # Returns calendar for enrolled classes
    def getComprovant(self):
        return calendar(self.enrolled_classes)

    # Returns all past grades 
    def getGrades(self):
        return '\n'.join(str(i[0]) + '\t' + str(i[1]) for i in self.approved_classes)

    # Check if this students has the pre requisites for taking a given subject 
    def canTakeTheSubject(self, subject):
        if subject.pre_requisite:
            history = [i[0] for i in self.approved_classes]
            for pre in subject.pre_requisite:
                if not pre in history:
                    return 0
        return 1


    def formatStudentForDatabase(self):
        if self.approved_classes:
            student_history = '&'.join(str(i[0])+','+str(i[1]) for i in self.approved_classes)
        else:
            student_history = ''

        enrolled = '&'.join(i.code for i in self.enrolled_classes)
        return '%s; %s; %s; %s; %s; %s'%(self.name, self.registration, self.semester, self.type, student_history, enrolled)



# |-------------------------------| #
# |         More Functions        | #
# |-------------------------------| #


# !!!!!!!!!!!! # 
# Need to be replaced with the same function in "make_random_database.py"
# Right now it will fail at reading the database
def read_students():
    with open('students0.1.txt', 'r') as f:
        raw_data = f.read().split('\n')
   
    if raw_data[-1] == '':
        raw_data = raw_data[:-1]
    students = []
    for line in raw_data:
        name, registration, semester, _type, approved = line.split('; ')
        approved = [i.split(',') for i in approved.split('&')]
        if len(approved) >= 32:
            _type = 'Formando'
        students.append(Student(name, registration, semester, _type, approved))

    return students


# !!!!!!!!!!!! # 
# Needs to be modified based as the function make_new_entries in "make_random_database.py"
# It will use the new logic of random names and sequential registration number
def read_calouros():
    with open('calouros.txt', 'r') as f:
        raw_data = f.read().split('\n')

    if raw_data[-1] == '':
        raw_data = raw_data[:-1]
    new_students = []
    
    subjects[0].enrolled_sudents = len(raw_data)
    subjects[1].enrolled_sudents = len(raw_data)
    subjects[2].enrolled_sudents = len(raw_data)
    subjects[3].enrolled_sudents = len(raw_data)
    subjects[4].enrolled_sudents = len(raw_data)
    
    for line in raw_data:
        name, registration = line.split('; ')
        student = Student(name, registration, 1, 'Calouro', [])
        student.enrolled_classes = subjects[:5]
        new_students.append(student)

    return new_students


def write_student_to_database(students):
    with open('students0.1.txt', 'w') as f:
        for student in students:
            f.write(student.formatStudentForDatabase())
            f.write('\n')


#students = read_students()
#students = read_calouros()

#write_student_to_database(students)

#print(students[0])
