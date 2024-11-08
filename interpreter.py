### O seguinte código é um interpretador de uma linguagem simples baseada um stack,
# Essa linguagem é composta por apenas 8 instruções, sendo elas:
# PUSH: coloca um número no topo do stack
# POP: remove um número do stack e o retorna
# ADD: remove 2 números do stack e retorna sua soma
# SUB: remove 2 números do stack e retorna sua subtração
# PRINT: printa o string_literal no terminal
# READ: permite que o usuário adicione um número ao stack
# JUMP.EQ.0: se o topo do stack for igual a 0, pula para a etiqueta(uma posição no código)
# JUMP.GT.0: se o topo do stack for maior que 0, pula para a etiqueta ###


import sys

# ler argumentos
program_filepath = sys.argv[1]



# ler linhas do arquivo
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    # checar por linha vazia
    if opcode == "":
        continue

    # checar se é uma etiqueta(label)
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    # guardar token opcode
    program.append(opcode)
    token_counter += 1

    if opcode =="PUSH":
        # esperando um número
        number = int(parts[1])
        program.append(number)
        token_counter +=1
    elif opcode == "PRINT":
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "JUMP.EQ.0":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "JUMP.GT.0":
        label = parts[1]
        program.append(label)
        token_counter += 1


# INTERPRETER

## criando classe definindo o Stack e definindo suas funções
class Stack:

    # o construtor recebe um tamanho e cria um array desse tamanho, com 0 em todos as posições,  
    # também cria um ponteiro que aponta para -1
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    # essa função recebe um número, incrementa o valor do ponteiro
    #  e insere o número onde o ponteiro está apontando
    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    # guarda o número no topo do Stack, decrementa o ponteiro e retorna o valor do número
    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number
    
    # não recebe nenhum argumento, apenas  retorna o valor no topo do Stack, sem mover o ponteiro
    def top(self): 
        return self.buf[self.sp]
    
    

#Iniciando um Stack de tamanho 256 e o program counter
pc = 0
stack = Stack(256)

# o programa funcionará até que encontre a função para sua finalização
while program[pc] != "HALT":
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        number = program[pc]
        pc += 1
        stack.push(number)
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)
    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1
        print(string_literal)
    elif opcode == "READ":
        number = int(input())
    elif opcode == "JUMP.EQ.0":
        number = stack.top()
        if number == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "JUMP.GT.0":
        number = stack.top()
        if number > 0:
            pc = label_tracker[program[pc]]
        else: 
            pc += 1

