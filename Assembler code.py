opcode = {'add': '00000', 'sub': '00001', 'mov_imm': '00010', 'mov_reg':'00011', 
          'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111',
          'rs': '01000', 'ls': '01001', 'xor' : '01010', 'or':'01011',
          'and': '01100', 'not': '01101', 'cmp': '01110', 'jmp':'01111',
          'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010'}
l = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp',
             'jmp', 'jlt', 'jgt', 'je', 'hlt']
reg = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
          'FLAGS': '111'}


opcode1 = {'add': 'A', 'sub': 'A', 'mov_imm': 'B', 'mov_reg':'C',
          'ld': 'D', 'st':'D', 'mul':'A', 'div':'C',
          'rs':'B', 'ls':'B','xor': 'A', 'or':'A',
          'and':'A', 'not':'C', 'cmp':'C', 'jmp': 'E',
          'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F'}          

#type functions  .....

def typeA(inst, reg1, reg2, reg3,op):
    if inst in opcode.keys() and  reg1 in reg.keys() and reg2 in reg.keys():
        if reg3 in reg.keys():
                    op.writelines(str(opcode[inst] + '00' + reg[reg1] + reg[reg2] + reg[reg3] + '\n'))
def typeB(inst, reg1, imm, op):
    if inst in opcode.keys() and reg1 in reg.keys():
            op.writelines(str(opcode[inst]+ reg[reg1] + format(imm, '08b') + '\n'))
def typeC(inst, reg1, reg2, op):
    if inst in opcode.keys() and reg1 in reg.keys() and reg2 in reg.keys():
        op.writelines(str(opcode[inst] + '00000' + reg[reg1] + reg[reg2] + '\n'))
def typeD(inst, reg1, mem_add, op):
    if inst in opcode.keys() and reg1 in reg.keys():
            op.writelines(str(opcode[inst] + reg[reg1] + format(mem_add, '08b') + '\n'))
def typeE(inst, mem_add, op):
    if inst in opcode.keys():
        op.writelines(str(opcode[inst] + '000' + format(mem_add, '08b') + '\n'))
def typeF(inst, op):
    if inst in opcode.keys():
        op.writelines(str(opcode[inst] + '00000000000' + '\n'))


def main():
          #taking input from files ....
    with open("file_input.txt") as ip:
        data = ip.readlines()
        ip.close()
    
    op = open("file_output.txt","w")

    A = ['add', 'sub', 'mul', 'xor', 'or', 'and']
    B = ['ls', 'rs']
    C = ['div', 'not', 'cmp']
    D = ['ld', 'st']
    E = ['jmp', 'je', 'jgt', 'jlt']
    F = ['hlt']
    M = ['mov']



    l1 = []
    v1 = []
    lbl1 = []
    
    i = 0
    flag = 0
    count_label = 0
    while True:
        try:
            line = data[i].strip('\n')
            i += 1
            line = line.strip()
            if line == "":
                break
            l1.append(line + " " + str(i))
        except :
            break
    
    i = 0
    while i < len(l1):
        j = l1[i].strip()
        chk = j.split()
        for k in chk:
            if ':' in k:
                lbl1.append(k)
        i += 1

    for i in l1:
        i = i.strip()
        line = i.split()
        count_label=0
        
        index = 0
        length = len(line)

        while index < length:
            k = line[index]
            index = 0
            while index < len(l1):
                k = l1[index]
                if ':' in k:
                    count_label += 1
                    if line[1] == line[-1]:
                         # sys.stdout.write("Error ", line[-1], ": No Instruction after Label"+'\n')
                        print("Error ", line[-1], ": No Instruction after Label")
                        exit()
                index += 1

            index += 1

        if count_label > 1:
            # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
            print("Error", line[-1], ": Multiple Labels Used in the Same Line")
            exit()

        if line[0] not in l and 'var' not in line[0] and ':' not in line[0]:
            # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
            print("Syntax Error" + line[-1])
            exit()

        if line[0] == 'var':
            if flag == 0:
                v1.append(line[1])
            else:
                # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                print("error" + line[-1] + ": variable should be defined at the beginning")
                exit()
        for elt in A:
            if elt in line:
                addindex = line.index(elt)
                inst = line[addindex]
                list_add = []
                i = 1
                while i < 4:
                    if line[addindex + i] in reg.keys():
                            if line[addindex + i] == 'FLAGS':
                                # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                                print("Error" + line[-1] + ": Illegal use of FLAGS")
                                exit()
                            list_add.append(line[addindex + i])
                    else:
                        print("Error" + line[-1] + ": Register not found")
                        exit()
                    i += 1

                
                if len(list_add) == 3:
                    reg1, reg2, reg3 = list_add
                else:
                    # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                    print("Error" + line[-1] + ": Invalid syntax")
                    exit()

                if line[addindex + 4] != line[-1]:
                    # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                    print('General Syntax Error' + line[-1])
                    exit()

                typeA(inst, reg1, reg2, reg3, op)
                flag=1

        for elt in B:
            if elt in line:
                addindex = line.index(elt)
                inst = line[addindex]
                reg1 = line[addindex + 1]
                imm = None
        
                if reg1 == 'FLAGS':
                    # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                    print("Error " + line[-1] + ": Illegal use of FLAGS")
                    exit()
        
                if reg1 not in reg:
                    # sys.stdout.write("Error ", line[-1], ": Multiple Labels Used in the Same Line"+'\n')
                    print("Error " + line[-1] + ": Register not found")
                    exit()
                
                if line[addindex + 2].startswith('$'):
                    num = line[addindex + 2][1:]  # Remove the leading '$'
                    try:
                        imm = int(num)
                        if not 0 <= imm <= 255:
                            print("Error " + line[-1] + ": Immediate value out of range")
                            exit()
                    except ValueError:
                        print("Error " + line[-1] + ": Invalid syntax")
                        exit()
                else:
                    print("Error " + line[-1] + ": Invalid syntax")
                    exit()

                typeB(inst, reg1, imm, op)
                flag = 1
                break
        
    
        for elt in C:
            if elt in line:
                addindex = line.index(elt)
                inst = line[addindex]
                list_add = []
                #checking flags....
                i = 1
                while i < 3:
                    reg_key = line[addindex + i]
                    if reg_key in reg:
                        if reg_key == 'FLAGS':
                            print("Error " + line[-1] + ": Illegal use of FLAGS")
                            exit()
                        list_add.append(reg_key)
                    else:
                        print("Error " + line[-1] + ": Register not found")
                        exit()
                    i += 1

               
                if len(list_add) == 2:
                    reg1, reg2 = list_add
                else:
                    print("Error" + line[-1] + ": invalid syntax")
                    exit()

                if line[addindex + 3] != line[-1]:
                    print('General Syntax Error ' + line[-1])
                    exit()

                typeC(inst, reg1, reg2, op)
                flag = 1

        for elt in D:
            if elt in line:
                addindex = line.index(elt)
                inst = line[addindex]
                if line[addindex + 1] not in reg:
                    print("Error " + line[-1] + ": register not found")
                    exit()
        
                if line[addindex + 1] == 'FLAGS':
                    print("Error " + line[-1] + ": Illegal use of FLAGS")
                    exit()
        
                reg1 = line[1]

                var = line[addindex + 2]
                if var in lbl1:
                    error_msg = f'Error {line[-1]}: Misuse of label'
                    raise ValueError(error_msg)
                if var not in v1:
                    error_msg = f'Error {line[-1]}: Undefined Variable'
                    raise ValueError(error_msg)

                if line[addindex + 3] != line[-1]:
                    error_msg = f'General Syntax Error {line[-1]}'
                    raise ValueError(error_msg)
        
                flag = 0
                for k in v1:
                    if k == var:
                        typeD(inst, reg1, getVar(l1, var), op)
                        flag = 1
                        break
        
                if flag == 0:
                    print('Error ' + line[-1] + ' :Undefined Variable')
                    exit()

                i = 0
                flag = 0

                while i < len(v1):
                    if v1[i] == var:
                        typeD(inst, reg1, getVar(l1, var), op)
                        flag = 1
                        break
                    i += 1    



        for elt in E:
            if elt in line:
                addindex = line.index(elt)
                inst = line[addindex]
                lab = line[addindex + 1] + ':'
                if lab in v1:
                    print('Error ' + line[-1] + ' : Misuse of variable')
                    exit()
                if lab not in lbl1:
                    print('Error ' + line[-1] + ' : Undefined Label')
                    exit()
                if line[addindex+2] != line[-1]:
                    print('General Syntax Error ' + line[-1])
                    exit()
                i = 0
                flag = 0
                while i < len(l1):
                    if lab in l1[i]:
                        typeE(inst, getLbl(l1, l1[i]), op)
                        flag = 1
                        break
                    i += 1

        addindex = [line.index(elt) for elt in F if elt in line]
        inst = line[addindex[0]] if addindex else None

        if inst:
            if line[addindex[0] + 1] != line[-1]:
                print('General Syntax Error ' + line[-1])
                exit()
            flag = 1 if ":" in line[0] else 0
            if flag:
                typeF(inst, op)
            else:
                if int(line[-1]) == len(l1):
                    typeF(inst, op)
                    exit()
                else:
                    print("Error: hlt not being used as the last instruction")
                    exit()

        for elt in M:
            if elt in line:
                addindex = line.index(elt)
                if line[addindex + 1] not in reg:
                    print("Error " + line[-1] + ": Register not found")
                    exit()
        
                reg1 = line[addindex + 1]
        
                if line[addindex + 1] == 'FLAGS':
                    print("Error " + line[-1] + ": Illegal use of FLAGS")
                    exit()
        
                if '$' in line[addindex + 2]:
                    inst = 'mov_imm'
                    num = line[addindex + 2]
                    imm = int(num.replace('$', ''))
                    if line[addindex + 3] != line[-1]:
                        print('General Syntax Error ' + line[-1])
                        exit()
            
                    if imm < 0 or imm > 255:
                        print("Error " + line[-1] + ": Immediate value out of range")
                        exit()
            
                    typeB(inst, reg1, imm, op)
                    flag = 1
        
                elif line[addindex + 2] in reg:
                    inst = 'mov_reg'
                    reg2 = line[addindex + 2]
            
                    if line[addindex + 3] != line[-1]:
                        print('General Syntax Error ' + line[-1])
                        exit()
            
                    typeC(inst, reg1, reg2, op)
                    flag = 1
        
                else:
                    print("Error " + line[-1] + ": Invalid syntax")
                    exit()
        
                break


        index = 0
        while index < len(line):
            k = line[index]
            if ':' in k:
                for elt in opcode.keys():
                    if elt + ":" == k:
                        print("Error: Cannot use instructions as label names")
                        exit()
                lbl1.append(k)
                flag = 1
            index += 1

        index = 0
        while index < len(line):
            k = line[index]
            if ':' in k:
                for elt in opcode.keys():
                    if elt + ":" == k:
                        print("Error: Cannot use instructions as label names")
                        exit()
                lbl1.append(k)
                flag = 1
            index += 1

        if 'hlt' not in l1[-1]:
            print("Error: hlt not being used as the last instruction")
            exit()
            

def getVar(a, x):
    b = {}
    c = [i for i in a if 'var' not in i]
    d = [i for i in a if 'var' in i]
    n1 = len(a) - len(d)
    
    for j in d:
        e = j.split()
        b[e[1]] = n1
        n1 += 1
    return b[x]

def getLbl(a, lb):
    lblDict = {i: lst.index(i) for i in lst if ':' in i}
    return lblDict[lb]


if __name__ == "__main__":
    main()

