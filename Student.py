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
        return 'Name: %s\nSemester: %s\nCoeff: %s'%(self.name, self.semester, round(self.coefficent, 1))
        

    def enroll(self, subject):
        '''
        Expects subject to be of type Subject
        This method doesn't change the subject attributes
        '''
        # Check that the students ha prerequisites 
        if self.canTakeTheSubject(subject):
            # check that the time of the classes aren't overlapping
            if not check_conficts(self.enrolled_classes + [subject]):
                self.enrolled_classes.append(subject)

    
    def UNenroll(self, subject):
        '''
        Expects subject to be of type Subject
        This method doesn't change the subject attributes
        '''
        self.enrolled_classes.remove(subject) 


    # Returns calendar for enrolled classes
    def getComprovant(self):
        string = '-'*88 + '\n' + '#'*24 + '\t\tMatricula\t\t' + '#'*24 + '\n' + '-'*88+'\n'
        if not len(self.enrolled_classes):    
            string += 'Sem matricula'
        else:
            string += calendar(self.enrolled_classes)
        return string
        

    # Returns all past grades 
    def getGrades(self):
        string = '-'*88 + '\n' + '#'*24 + '\t\tHistorico\t\t' + '#'*24 + '\n' + '-'*88+'\n'
        for sub in self.approved_classes:
            sub_name = subject_from_code(sub[0]).name
            spaces = 60 - len(sub_name)
            string += '%s - %s'%(sub[0], sub_name) 
            string += ' '*spaces + str(sub[1]) + '\n'
        return string


    # Check if this students has the pre requisites for taking a given subject 
    def canTakeTheSubject(self, subject):
        history = [i[0] for i in self.approved_classes]
        if subject.code in history:
            return 0    # Student already took the subject

        if subject.pre_requisite:
            for pre in subject.pre_requisite:
                if not pre in history:
                    return 0    # Missing prerequisites
        return 1    # ok


    def studentOverview(self):
        print(self)
        print(self.getGrades())
        print(self.getComprovant())



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
# Read students from file
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

        students.append(Student(name, int(registration), int(semester), _type, approved, enrolled))

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
            line = f.readlines()[-1]
            registration_n = int(line.split('; ')[1]) + 1
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



def student_from_registration(registration, students):
    for student in students:
        if registration == student.registration:
            return student
