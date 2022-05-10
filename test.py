from Student import *


# Load students data
students = read_students();
# Search for a student
s = student_from_registration(1128, students)
# Displays all student infos
s.studentOverview()

# Select a subject
sub = subject_from_code('CC1923')
s.enroll(sub)
s.UNenroll(sub)



# Display Historico
print(s.getGrades())
# Display Matricula
print(s.getComprovant())
