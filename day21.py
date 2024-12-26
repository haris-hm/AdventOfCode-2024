class Keypad():
    def __init__(self, type: str, target_code: str='') -> None:
        self.invalid_position: tuple[int] = None
        self.keypad = self.get_keypad(type)
        self.target_code = target_code

    def get_keypad(self, type: str) -> dict[str, tuple[int]]:
        match type:
            case 'NUMERIC': 
                self.invalid_position = (3,0)
                print(self.invalid_position)
                return {
                    '7': (0,0),
                    '8': (0,1),
                    '9': (0,2),
                    '4': (1,0),
                    '5': (1,1),
                    '6': (1,2),
                    '1': (2,0),
                    '2': (2,1),
                    '3': (2,2),
                    '0': (3,1),
                    'A': (3,2)
                }
            case 'DIRECTIONAL':
                self.invalid_position = (0,0)
                return {
                    '^': (0,1),
                    'A': (0,2),
                    '<': (1,0),
                    'v': (1,1),
                    '>': (1,2)
                }
            
    def get_vertical(self, new_y: int) -> str:
        return ('^' * abs(new_y)) if new_y < 0 else ('v' * new_y)

    def find_optimal_path(self, start: str, end: str) -> list[str]:
        y_1, x_1 = self.keypad[start]
        y_2, x_2 = self.keypad[end]

        new_y, new_x = ((y_2-y_1), (x_2-x_1))
        outputs: list[str] = []

        if new_x < 0:
            outputs.append(self.get_vertical(new_y) + '<' * abs(new_x))

            if (y_1, x_1 + new_x) != self.invalid_position:
                outputs.append('<' * abs(new_x) + self.get_vertical(new_y))
        else:
            outputs.append('>' * abs(new_x) + self.get_vertical(new_y))

            if (y_1 + new_y, x_1) != self.invalid_position:
                outputs.append(self.get_vertical(new_y) + '>' * abs(new_x))

        outputs = [i + 'A' for i in outputs]
        if len(outputs) > 1:
            outputs = [outputs[0]] if outputs[0] == outputs[1] else outputs
        return outputs
    
    def find_optimal_sequence(self) -> str:
        outputs: list[str] = ['']
        previous_char: str = 'A'

        for char in self.target_code:
            solutions: list[str] = self.find_optimal_path(previous_char, char)            
            new_outputs: list[str] = []

            for output in outputs:
                for solution in solutions:
                    sequence: str = output + solution
                    new_outputs.append(sequence)

            outputs = new_outputs
            previous_char = char

        outputs = sorted(outputs, key=lambda x: len(x))
        return outputs
    
    def solve(self, iterations: int=2) -> str:
        previous_codes: list[str] = self.find_optimal_sequence()
        self.keypad = self.get_keypad('DIRECTIONAL')
        print(previous_codes)

        for _ in range(iterations):
            new_codes: list[str] = []

            for code in previous_codes:
                self.target_code = code
                new_codes.extend(self.find_optimal_sequence())

            previous_codes = new_codes

        previous_codes = sorted(previous_codes, key=lambda x: len(x))
        return previous_codes[0]
    
def code_solver(codes: list[str]) -> int:
    len_sum: int = 0
    
    for code in codes:
        keypad: Keypad = Keypad('NUMERIC', code)
        sequence: str = keypad.solve()
        
        print(f'{code}: {sequence}')
        print(f'{len(sequence)} * {int(code[:3])}')
        len_sum += len(sequence) * int(code[:3])

    return len_sum


def main() -> None:
    with open('./inputs/day21/0.txt', 'r') as file:
        contents: list[str] = file.readlines()
        contents = [code.rstrip() for code in contents]
        print(code_solver(contents))

if __name__ == '__main__':
    main()