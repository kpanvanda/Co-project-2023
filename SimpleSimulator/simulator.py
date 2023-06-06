opDict = {'add': '00000', 'sub': '00001', 'mov_imm': '00010', 'mov_reg': '00011',
          'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111',
          'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011',
          'and': '01100', 'not': '01101', 'cmp': '01110', 'jmp': '01111',
          'jlt': '10000', 'jgt': '10001', 'je': '10010', 'hlt': '10011'}

rf= {'000': '0000000000000000', '001': '0000000000000000', '010': '0000000000000000', '011': '0000000000000000',
           '100': '0000000000000000', '101': '0000000000000000', '110': '0000000000000000', '111': '0000000000000000'}


#conversion_to_binary
def decimal_to_binary(decimal_number):
    binary_number = format(decimal_number, '07b')
    return binary_number

#print(decimal_to_binary(4))
rdict={}

def typeA(l,i):
    r, op1, op2 = l[0][7:10], l[0][10:13], l[0][13:16]
    r1, r2, r3 = [rdict[i] for i in [r, op1, op2]]

    opdict = {
    '00000': lambda: int(r2, 2) + int(r3, 2),
    '00001': lambda: int(r2, 2) - int(r3, 2),
    '01100': lambda: int(r2, 2) & int(r3, 2),
    '00110': lambda: int(r2, 2) * int(r3, 2),
    '01010': lambda: int(r2, 2) ^ int(r3, 2),
    '01011': lambda: int(r2, 2) | int(r3, 2) }
    op = opdict.get(i)    

    if op:
        x=op()
        y=format(x,"016b")
          
        if x>2 ** 16:
                rdict["111"]= "0000000000001000"
                rdict[r] = y[-16:]
        elif x<0:
              rdict['111'] = '0000000000001000'
              rdict[r] = '0000000000000000'
        else:
            rdict["111"] = '0000000000000000'
            rdict[r] = y


def typeB(l, i):
    r ,imm = l[0][5:8], l[0][8:16]
    r1 = rdict[r]
    op= {
    '00010': lambda: format(int(imm, 2), '016b'),
    '01000': lambda: format(int(r1, 2) >> int(imm, 2), '016b'),
    '01001': lambda: format(int(r1, 2) << int(imm, 2), '016b')}
    x = op.get(i, lambda: '')()  
    rdict.update({r: x, '111': '0000000000000000'})


def typeC(l, i):
    op1,op2 = l[0][10:13], l[0][13:16]
    r1, r2 = [rdict[i] for i in [op1, op2]]

    if i == '00011':
         rdict[op1] = r2
    elif i == '00111':
        quotient = int(r1, 2) // int(r2, 2)
        remainder = int(r1, 2) % int(r2, 2)
        rdict.update({'000': format(quotient, '016b'), '001': format(remainder, '016b')})
    elif i == '01101':
        rdict[op1] = ''.join(['1' if bit == '0' else '0' for bit in r2])
    elif i == '01110':
        ele1 = int(r1, 2)
        ele2 = int(r2, 2)
    if ele1 == ele2:
        rdict['111'] = '0000000000000001'
    elif ele1 > ele2:
        rdict['111'] = '0000000000000010'
    elif ele1 < ele2:
        rdict['111'] = '0000000000000100'
        rdict['111'] = '0000000000000000'


def typeD(l, i, memory, t, c):
    r, memadd = l[0][5:8] , l[0][8:16]
    address = int(memadd, 2)

    switch = {
        '00101': lambda: memory.__setitem__(address, rdict[r]),
        '00100': lambda: rdict.__setitem__(r, memory[address]),
    }

    switch.get(i, lambda: None)()
    rdict['111'] = '0000000000000000'
    t.append([c, address])


def typeE(l, i):
    global pc
    memadd = l[0][8:16]
    address = int(memadd, 2)

    switch = {
        '01111': lambda: pc.__setitem__(0, address),
        '10010': lambda: pc.__setitem__(0, address) if rdict['111'] == '0000000000000001' else pc.__setitem__(0, pc[0] + 1),
        '10000': lambda: pc.__setitem__(0, address) if rdict['111'] == '0000000000000100' else pc.__setitem__(0, pc[0] + 1),
        '10001': lambda: pc.__setitem__(0, address) if rdict['111'] == '0000000000000010' else pc.__setitem__(0, pc[0] + 1),
    }

    switch.get(i, lambda: None)()
    rdict['111'] = '0000000000000000'

def typeF(l, i):
    flag = 1
    rdict['111'] = '0000000000000000'

def mem_dump(memory):
    for i in memory:
        print(i)
     

def main():

    #readfile
    with open("file_output.txt") as f:
        data = f.readlines()
        data = [i.rstrip('\n') for i in data]

    
    memory = [format(0, '016b') for i in range(128)]

    memory= [data[i] if i < len(data) else memory[i] for i in range(len(memory))]
    pc=0
    instruction = "1101000000000000"
    while memory[pc]!= instruction:
            print(memory[pc])

            pc+=1
    
    flag=0        
    c= 0
    t=[]
    pd=0

    l1=["00000","00001","00110","01010","01011","01100"] #0001-00-r1-r2-r3
    l2=["01000","01001","00010"] #01000-0-r1-imm_value
    l3=['00011', '00111','01101','01110']
    l4=['00100', '00101']
    l5=['01111','10000', '10001','10010']

    while memory[pc] != instruction:
        if pc == int(memory[pc][-1]):
            t.append([c, pc])

            if memory[pc][:5] in l1:
                i = memory[pc][:5]
                typeA(memory[pc],i)
                out(pc)
                pc+=1

            if memory[pc][:5] in l2:
                i = memory[pc][:5]
                typeB(memory[pc], i)
                out(pc)
                pc+=1

            if memory[pc][:5] in l3:
                i = memory[pc][:5]
                typeC(memory[pc], i)
                out(pc)
                pc+=1

            if memory[pc][:5] in l4:
                i = memory[pc][:5]
                typeD(memory[pc],i,memory,t,c) 
                out(pc)
                pc+=1

            if memory[pc][:5] in l5:
                i = memory[pc][:5]
                pd=pc
                typeE(memory[pc], i)
                out(pd)
    

            if memory[pc][:5]== "10011":
                i=memory[pc][:5]
                typeF(memory[pc],i)
                out(pc)
                pc+=1

            c+=1
    mem_dump(memory)

def out(pc):
    a = format(pc, '08b')
    b = ''
    for i in rdict.values():
        b = b + i + ' '
    print(a + ' ' + b)

if __name__ == "__main__":
    main()                     

