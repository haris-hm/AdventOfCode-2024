import re
import numpy as np

class Machine():
    a_cost: int = 3
    b_cost: int = 1

    def __init__(self, eq_a: tuple[int], eq_b: tuple[int]) -> None:
        self.eq_a = eq_a
        self.eq_b = eq_b

    def solve_100(self) -> int:
        solution: tuple[int] = ()

        for i in range(101):
            for k in range(101):
                xs_equal: bool = self.eq_a[0]*i + self.eq_a[1]*k == self.eq_a[2]
                ys_equal: bool = self.eq_b[0]*i + self.eq_b[1]*k == self.eq_b[2]

                if xs_equal and ys_equal:
                    solution = (i, k)
                    break

        if len(solution) == 0:
            return 0
        else:
            cost: int = solution[0]*self.a_cost + solution[1]*self.b_cost
            return cost
        
    def solve_general(self) -> int:
        def solve_x(y) -> float:
            coeff_1: int = self.eq_b[0]
            coeff_2: int = self.eq_b[1]
            potential_x: int = (self.eq_a[2]-self.eq_a[1]*y)/self.eq_a[0]

            validation: float = coeff_1*potential_x+coeff_2*y

            # print(coeff_1, coeff_2, potential_x)

            return potential_x, validation
        
        y_val: int = -1
        x_val: int = 0
        while True:
            y_val += 1
            x_val, validation = solve_x(y_val)
            
            if validation  == self.eq_b[2]:
                break
            elif validation > self.eq_b[2]:
                x_val = 0
                y_val = 0
                break

        xs_equal: bool = self.eq_a[0]*x_val + self.eq_a[1]*y_val == self.eq_a[2]
        ys_equal: bool = self.eq_b[0]*x_val + self.eq_b[1]*y_val == self.eq_b[2]
        cost: int = 0

        if xs_equal and ys_equal:
            cost: int = x_val*self.a_cost + y_val*self.b_cost
        
        return cost
    
    def solve_np(self) -> int:
        equations = np.array([[self.eq_a[0], self.eq_a[1]], [self.eq_b[0], self.eq_b[1]]])
        solutions = np.array([self.eq_a[2], self.eq_b[2]])
        solved = np.linalg.solve(equations, solutions)

        print(solved[0], solved[1])
        cost = solved[0]*self.a_cost + solved[1]*self.b_cost

        if cost.is_integer():
            return cost
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
        total_cost += machine.solve_100()

    for i, machine in enumerate(expensive_machines):
        total_expensive_cost += machine.solve_np()

    print(f'Total cost: {total_cost}')
    print(f'Total expensive cost: {total_expensive_cost}')

if __name__ == '__main__':
    main()