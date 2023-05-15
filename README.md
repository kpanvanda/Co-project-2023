# Co-project-2023

ASSEMBLER

made by:      Mayank Kankheria(2022286)
              Kashvi Panvanda(2022245)
              Aditri Paweria(2022027)
              Chaitanya Dhruv Sahu(2022139)

*********************************************************************************************************************************************************************

WORKFLOW:
1)This is a code that takes assembly language instructions as input and generates corresponding machine code as output.

The instruction set architecture is defined using dictionaries that hold the opcodes and instruction types of the supported instructions.


3) This is a code snippet that is part of an assembler program. The purpose of this code is to parse the instructions provided in an assembly language file and generate binary machine code instructions.

The code has several loops, each of which checks for a particular type of instruction format and then calls the appropriate function to generate the corresponding machine code instruction.

4) For example, the first loop is checking for type A instructions, which have the format ADD $n, REG. The loop checks if the instruction is of this type by looking for the ADD keyword and then checking if the first operand starts with a '$'. If it does, it converts the immediate value to an integer and checks that it is within the range of 0-255. If everything checks out, it calls the typeA() function to generate the corresponding machine code instruction.

The other loops are similar and handle other types of instructions (type B, C, D, E). They check the syntax of the instruction, validate the registers and operands, and generate the corresponding machine code instruction.

If any syntax or semantic errors are detected, the program outputs an error message and exits.

5) The assembler supports various types of instructions such as move, add, subtract, jump, and so on. It also supports the use of labels and variables in the code, which can be assigned values and used in subsequent instructions.

The implementation uses several functions to handle different types of instructions. The typeA function is used for instructions with a single register operand, the typeB function is used for instructions with an immediate operand, and the typeC function is used for instructions with two register operands.

The makeVar function is used to assign a memory location to a variable, and the makeLbl function is used to get the memory location of a label.














*********************************************************************************************************************************************************************

ERROR-REPORTING:

the assembler can report the following errors:
a) Typos in instruction name or register name
b) Use of undefined variables
c) Use of undefined labels
d) Illegal use of FLAGS register
e) Illegal Immediate values (more than 7 bits)
f) Misuse of labels as variables or vice-versa
g) Variables not declared at the beginning
h) Missing hlt instruction
i) hlt not being used as the last instruction
