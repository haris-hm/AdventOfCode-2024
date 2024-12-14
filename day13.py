import re

class SystemMatrix():
    def __init__(self, eq_1: tuple[int], eq_2: tuple[int]) -> None:
        self.a = eq_1[0]
        self.b = eq_1[1]
        self.c = eq_2[0]
        self.d = eq_2[1]
        self.e = eq_1[2]
        self.f = eq_2[2]

    def __repr__(self) -> str:
        return f'[{self.a} {self.b}] [A] _ [{self.e}]\n[{self.c} {self.d}] [B] ̅  [{self.f}]'
    
    def solution_check(self, x, y) -> bool:
        return self.system.a*x+self.system.b*y == self.system.e and \
            self.system.c*x+self.system.d*y == self.system.f

    def determinant(self, a: int, b: int, c: int, d: int) -> int:
        return (a*d)-(b*c)
    
    def solve_cramer(self) -> tuple[int]:
        x_numerator_det: int = self.determinant(self.e, self.b, self.f, self.d)
        y_numerator_det: int = self.determinant(self.a, self.e, self.c, self.f)
        
        denominator_det: int = self.determinant(self.a, self.b, self.c, self.d)

        x: int = 0
        y: int = 0

        x = x_numerator_det // denominator_det
        y = y_numerator_det // denominator_det

        return (x, y)
    
class Machine():
    a_cost: int = 3
    b_cost: int = 1

    def __init__(self, eq_a: tuple[int], eq_b: tuple[int]) -> None:
        self.system: SystemMatrix = SystemMatrix(eq_a, eq_b)

    def solve(self, output: bool=False) -> int:
        x: int = 0
        y: int = 0

        x, y = self.system.solve_cramer()

        print(self.system) if output else None
        print(f'{x=}, {y=}') if output else None

        valid: bool = self.system.solution_check()
        
        if valid:
            return x*self.a_cost + y*self.b_cost
        else:
            return 0

    def __repr__(self) -> str:
        return f'[{self.eq_a = }, {self.eq_b = }]'

def main() -> None:
    machines: list[Machine] = []
    expensive_machines: list[Machine] = []
    total_cost: int = 0
    total_expensive_cost: int = 0

    with open('./inputs/day13/1.txt', 'r') as file:
        contents: list[str] = file.read().split('\n\n')
        
        for machine in contents:
            info: list[str] = machine.split('\n')
            
            eq_1: list[int] = [int(i) for i in re.findall('\d+', info[0])]
            eq_2: list[int] = [int (i) for i in re.findall('\d+', info[1])]
            solution: list[int] = [int(i) for i in re.findall('\d+', info[2])]

            machines.append(Machine((eq_1[0], eq_2[0], solution[0]), \
                                    (eq_1[1], eq_2[1], solution[1])))
            
            expensive_machines.append(Machine((eq_1[0], eq_2[0], solution[0]+10000000000000), \
                                              (eq_1[1], eq_2[1], solution[1]+10000000000000)))

    for machine in machines:
        total_cost += machine.solve()

    for machine in expensive_machines:
        total_expensive_cost += machine.solve()

    print(f'Total cost: {total_cost}')
    print(f'Total expensive cost: {total_expensive_cost}')

if __name__ == '__main__':
    main()