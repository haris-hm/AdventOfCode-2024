from __future__ import annotations
import re

class Instruction():
    def __init__(self, opcode: int, operand: int) -> None: # type: ignore
        self.opcode = opcode
        self.operand = operand
        self.computer: Computer = None

    def execute(self, computer: Computer) -> None:
        self.computer = computer
        match self.opcode:
            case 0:
                self.adv()
            case 1:
                self.bxl()
            case 2:
                self.bst()
            case 3:
                self.jnz()
            case 4:
                self.bxc()
            case 5:
                self.out()
            case 6:
                self.bdv()
            case 7:
                self.cdv()

    def get_combo(self) -> int | None:
        match self.operand:
            case 0 | 1 | 2 | 3:
                return self.operand
            case 4:
                return self.computer.reg_a
            case 5: 
                return self.computer.reg_b
            case 6:
                return self.computer.reg_c
            case 7:
                return None

    def adv(self) -> None:
        numerator = self.computer.reg_a
        denominator = self.get_combo()
        result: int = numerator // 2**denominator
        self.computer.set_register('A', result)
    
    def bxl(self) -> None:
        result: int = self.computer.reg_b ^ self.operand
        self.computer.set_register('B', result)
    
    def bst(self) -> None:
        result: int = self.get_combo() % 8
        self.computer.set_register('B', result)

    def jnz(self) -> None:
        if (self.computer.reg_a == 0):
            return
        self.computer.move_pointer(self.operand - 1)

    def bxc(self) -> None:
        result: int = self.computer.reg_b ^ self.computer.reg_c
        self.computer.set_register('B', result)

    def out(self) -> None:
        result: int = self.get_combo() % 8
        self.computer.output(result)

    def bdv(self) -> None:
        numerator = self.computer.reg_a
        denominator = self.get_combo()
        result: int = numerator // 2**denominator
        self.computer.set_register('B', result)

    def cdv(self) -> None:
        numerator = self.computer.reg_a
        denominator = self.get_combo()
        result: int = numerator // 2**denominator
        self.computer.set_register('C', result)

    def __repr__(self) -> str:
        return f'({self.opcode}, {self.operand})'
   
class Computer():
    def __init__(self) -> None:
        self.reg_a: int = None
        self.reg_b: int = None
        self.reg_c: int = None

        self.program: list[Instruction] = []
        self.instruction_pointer: int = 0

        self.outputs: list[int] = []

    def set_register(self, register: str, val: int) -> None:
        match register:
            case 'A':
                self.reg_a = val
            case 'B':
                self.reg_b = val
            case 'C':
                self.reg_c = val
            case _:
                print(f'\'{register}\' is not a valid register.')
    
    def move_pointer(self, position: int) -> None:
        self.instruction_pointer = position

    def output(self, output: int) -> None:
        self.outputs.append(output)

    def run_program(self) -> str:
        while self.instruction_pointer < len(self.program):
            curr_instruction: Instruction = self.program[self.instruction_pointer]
            curr_instruction.execute(self)
            self.instruction_pointer += 1

        return self.outputs

    def __repr__(self) -> str:
        output: str = ','.join([str(i) for i in self.outputs])
        return f'Register A: {self.reg_a}\nRegister B: {self.reg_b}\nRegister C: {self.reg_c}\n\nProgram: {self.program}\n\nOutputs: {output}'

def main() -> None:
    computer: Computer = Computer()

    with open('./inputs/day17/0.txt', 'r') as file:
        contents: str = file.readlines()
        computer.set_register('A', int(re.findall(r'\d+', contents[0])[0]))
        computer.set_register('B', int(re.findall(r'\d+', contents[1])[0]))
        computer.set_register('C', int(re.findall(r'\d+', contents[2])[0]))

        for instruction in re.findall(r'\d,\d', contents[4]):
            computer.program.append(Instruction(int(instruction[0]), int(instruction[2])))
        
    print(f'Before running:\n{computer}')
    computer.run_program()
    print(f'\n\nAfter running:\n{computer}')

if __name__ == '__main__':
    main()