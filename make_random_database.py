# |---------------------------------------------------------------| #
# | The only use for this file is to set up a random database.    | #
# | The execution of this program will stop when the first        | #
# | student becomes of type "Formando".                           | #
# | This way the database will have:                              | #
# |     last indexes: students of type "Calouro"                  | #
# |     first indexes: students of type "Formando"                | #
# |     in the middle: students of type "Continuo or "Individual" | #
# | At every iteration the students will get random grades for    | #
# | the subjects that they are attending and new students         | #
# | (calouros) will enter the database. Based on that they the    | #
# | program automaticlly enrolls them in the new semester.        | #
# |                                                               | #
# | USAGE:                                                        | #
# |     To test this program create an empty file named           | #
# |     "students0.1.txt                                          | #
# |---------------------------------------------------------------| #
from Student import *
from random import sample, randint, choice, seed
import sys

seed(101) # Random seed (RNG)
NEW_SUDENTS_MIN = 4 # Minimun number of new students
NEW_SUDENTS_MAX = 9 # Maximum number of new students

# Reads database and randomly assign grades to students enrolled classes
# for than enroll the student in the next semester
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
        
        # Random grades: if subject is from a semester before the grade is 
        # always above 7 for semplicity reasons
        # The flag sets if a student of type "Calouro" or "Continuo" becames "Individual" 
        flag = 0
        for sub in enrolled.split('&'):
            if type(subject_from_code(sub).semester) == str:
                grade = randint(67, 100) / 10
            elif subject_from_code(sub).semester < int(semester):
                grade = randint(7, 10)
            else:
                grade = randint(67, 100) / 10
            
            if grade < 7:
                flag = 1
            else:
                approved.append((sub, grade))
        

        if _type == 'Calouro' and len(approved) == 5:
            _type = 'Continuo'
        elif flag == 1:
            _type = 'Individual'
        elif len(approved) >= 32:
            _type = 'Formando'
            print('Max iteration reached')
            sys.exit()

        students.append(Student(name, registration, int(semester)+1, _type, approved))

    return students



# Enroll a student based on type in a simplistic way
def enroll(student):
    history = [i[0] for i in student.approved_classes]
    if student.type == 'Continuo':
        student.enrolled_classes = get_subjects_from_semester(student.semester)
        hours = sum([i.hours for i in student.enrolled_classes])
        

    elif student.type == 'Individual':
        prev_semester = get_subjects_from_semester(student.semester-1) 
        student.enrolled_classes = [i for i in prev_semester if not i.code in history]
     
        this_semester = get_subjects_from_semester(student.semester) 
        student.enrolled_classes = [i for i in this_semester if student.canTakeTheSubject(i)]
        
        hours = sum([i.hours for i in student.enrolled_classes])
    
    counter = 0
    eletivas = [i for i in get_subjects_from_semester('Eletiva') if not i.code in history]
    if len(eletivas):
        while hours < 360 and counter < len(eletivas):
            new_sub = eletivas[counter]
            if student.canTakeTheSubject(new_sub) and not check_conficts(student.enrolled_classes + [new_sub]):
                hours += 72
                student.enrolled_classes.append(new_sub)
            
            counter += 1
        
            


# Selects random names from file to make new students (calouros)
# and enroll them regularly
def make_new_entries():
    with open('random_names.txt', 'r') as f:    
        random_names = f.read().split()
        if random_names[-1] == '':
            random_names = random_names[:-1]

    students = read_students()
    # Registration number (numero de matricula)
    # if there are no students in the database the first number is 1111
    # else the number will be the registration of the last student in the database plus 1
    if len(students):
        registration_n = int(students[-1].registration) + 1
    else:
        registration_n = 1111

    new_entries = sample(random_names, randint(NEW_SUDENTS_MIN, NEW_SUDENTS_MAX))
    
    for s in students:
        enroll(s)

    for new in new_entries:
        s = Student(new, registration_n, 1, 'Calouro', [])
        s.enrolled_classes = subjects[:5]
        students.append(s)
        registration_n+=1

    return students


for i in range(9):
    students = make_new_entries()
    write_student_to_database(students)


