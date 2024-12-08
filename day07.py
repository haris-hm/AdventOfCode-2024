class Equation:
    def __init__(self, result: int, variables: list[int]):
        self.result = result
        self.variables = variables
        self.operators: list[str] = [''] * (len(self.variables) - 1)

    def __repr__(self) -> str:
        return f'(Result: {self.result}, Variables: {self.variables})'
    
    def __concat(self, left: int, right: int) -> int:
        left_str: str = str(left)
        right_str: str = str(right)
        return int(left_str+right_str)

    def __promising(self, i: int, weight: int) -> bool:
        if i == len(self.variables)-1 and weight == self.result:
            return True
        elif i+1 == len(self.variables):
            return False
        else:
            are_branches_possible: bool = weight + self.variables[i+1] <= self.result or \
                weight * self.variables[i+1] <= self.result or \
                self.__concat(weight, self.variables[i+1])
            return are_branches_possible 

    def __validate(self, i: int, weight: int) -> bool:
        if (self.__promising(i, weight)):
            if (weight == self.result and i == len(self.variables)-1):
                return True
            else:
                mult: bool = self.__validate(i+1, weight*self.variables[i+1])
                if mult:
                    return True
                
                add: bool = self.__validate(i+1, weight+self.variables[i+1])
                if add:
                    return True
                
                concat: bool = self.__validate(i+1, self.__concat(weight, self.variables[i+1]))
                if concat:
                    return True
        else:
            return False
    
    def validate(self) -> bool:
        return self.__validate(0, self.variables[0])
    
def validate_equations(equations: list[Equation]) -> int:
    valid_sum: int = 0

    for eq in equations:
        if eq.validate():
            valid_sum += eq.result
    
    return valid_sum

equations: list[Equation] = []

with open('./inputs/day07/1.txt', 'r') as file:
    contents = file.read()
    for line in contents.split('\n'):
        line_split = line.split(':')
        equations.append(Equation(int(line_split[0]), [int(i) for i in line_split[1].split()]))

print(equations)
print(f'Valid Sum: {validate_equations(equations)}')