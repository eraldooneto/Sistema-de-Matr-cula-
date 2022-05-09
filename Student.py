from Subjects import *
from random import randint, sample, seed


seed(101) # Random seed (RNG)
NEW_STUDENTS_MIN = 2 # Maximum number of new students
NEW_STUDENTS_MAX = 4 # Minimum number of new students

class Student:
    def __init__(self, name, registration, semester, _type, approved, enrolled=[]):
        self.name = name
        self.registration = registration
        self.semester = semester
        self.type = _type
        self.approved_classes = approved # list({'subject': grade}
        self.enrolled_classes = enrolled # list of Subject
        self.coefficent = sum([float(i[1]) for i in self.approved_classes]) / len(self.approved_classes) if len(self.approved_classes) else None

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




# |-------------------------------------| #
# |         Reading and Writing         | #
# |-------------------------------------| #
# Read subjects from file
def read_subjects():
    with open('subjects.txt', 'r') as f:
        raw_data = [i.split('\n') for i in f.read().split('\n\n')]

    if raw_data[-1][-1] == '':
        raw_data[-1] = raw_data[-1][:-1]

    subjects = []
    for i, s in enumerate(raw_data):
        if i == len(raw_data) - 1:
            p = 'Eletiva'
        else:
            p = i+1
        for j in s:
            try:
                name, hours, code, schedule, pre_req = j.split('; ')
                pre_req = pre_req.split('&')
            except ValueError:
                name, hours, code, schedule = j.split('; ')
                pre_req = None

            schedule = schedule.split('&')
            subjects.append(Subject(name, p, code, int(hours), schedule, pre_requisite=pre_req))

    return subjects



# Read subjects from file
def read_students():
    with open('students0.1.txt', 'r') as f:
        raw_data = f.read().split('\n')

    if raw_data[-1] == '':
        raw_data = raw_data[:-1]
    students = []
    for line in raw_data:
        name, registration, semester, _type, approved, enrolled = line.split('; ')
        if approved == '':
            approved = []
        else:
            approved = [tuple(i.split(',')) for i in approved.split('&')]

        if enrolled == '':
            enrolled = []
        else:
            enrolled = [subject_from_code(i) for i in enrolled.split('&')]

        students.append(Student(name, registration, int(semester), _type, approved, enrolled))

    return students


# Creates new students for the first semester
def make_new_students():
    with open('random_names.txt', 'r') as f:
        random_names = f.read().split()
        if random_names[-1] == '':
            random_names = random_names[:-1]

    # Registration number (numero de matricula)
    # if there are no students in the database the first number is 1111
    # else the number will be the registration of the last student in the database plus 1
    with open('students0.1.txt', 'r') as f:
        try:
            registration_n = int(f.readlines()[-1].split('; ')[1])
        except IndexError:
            registration_n = 1111

    new_entries = sample(random_names, randint(NEW_STUDENTS_MIN, NEW_STUDENTS_MAX))

    students = []
    for new in new_entries:
        students.append(Student(new, registration_n, 1, 'Calouro', []))
        registration_n+=1

    return students



def write_students_to_database(students):
    with open('students0.1.txt', 'w') as f:
        for student in students:
            f.write(student.formatStudentForDatabase())
            f.write('\n')

