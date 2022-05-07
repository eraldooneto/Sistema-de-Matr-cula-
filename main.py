from collections import deque
# import disciplina as ds
from subject import Subject, subjects

print("#-#-#-#- MENU -#-#-#-#")
print('''
(1) - Matrícula
(2) - Ajuste
(3) - Reajuste
(99) - Encerrar o programa''')


def check_name(name):
    '''Return True if the name is valid'''
    if name.isalpha():
        return True
    return False

#TODO Uma função para checar se o input é um número inteiro
def check_number(number):
    if number is.num():
        return True
    return False

# q = deque()

should_continue = True
all_right = False
while should_continue:
    # Checa se a escolha digitada é um número
    try:
        choice = int(input("Digite umas das opcões: "))
        all_right = True 
    except:
        print("Digite apenas o número da opção válida!")
    
    if  all_right:
        if choice == 99:
            should_continue = False

        elif choice == 1:
            print("Você selecionou a opção de Matrícula no Curso de Ciência da Computação")

            # Check if the name is valid
            name = input("Nome: ").strip() 
            while not check_name(name.replace(' ', "")):
                print("Digite um nome válido!")
                name = input("Nome: ").strip()
            
            student_type = input("Seleciona a opção que você se encaixa:\n(1) Calouro\n(2)Fluxo Padrão\n(3)Fluxo Individual\n") #TODO Checar o formato da entrada
            if student_type == '1':
                for subject in subjects:
                    print(subject.name)
            elif student_type == '2':
                semester = input("Digite qual o período que você irá cursar: ")
            elif student_type == '3':
                pass
                
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        else:
            print("Escolha uma opção válida, entre as opções (1), (2) e (3)")
