class Keypad():
    def __init__(self, type: str, target_code: str='') -> None:
        self.keypad = self.get_keypad(type)
        self.target_code = target_code

    def get_keypad(self, type: str) -> dict[str, tuple[int]]:
        match type:
            case 'NUMERIC': 
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
                return {
                    '^': (0,1),
                    'A': (0,2),
                    '<': (1,0),
                    'v': (1,1),
                    '>': (1,2)
                }

    def find_optimal_path(self, start: str, end: str, prefer_vertical: bool) -> str:
        y_1, x_1 = self.keypad[start]
        y_2, x_2 = self.keypad[end]

        new_y, new_x = ((y_2-y_1), (x_2-x_1))
        output: str = ''

        if prefer_vertical:
            if new_y < 0:
                output += '^' * abs(new_y)
            else:
                output += 'v' * new_y

            if new_x < 0:
                output += '<' * abs(new_x)
            else:
                output += '>' * new_x
        else:
            if new_x < 0:
                output += '<' * abs(new_x)
            else:
                output += '>' * new_x

            if new_y < 0:
                output += '^' * abs(new_y)
            else:
                output += 'v' * new_y

        output += 'A'
        return output
    
    def find_optimal_sequence(self, prefer_vertical: bool) -> str:
        output: str = ''
        previous_char: str = ''

        for i, char in enumerate(self.target_code):
            if i == 0:
                previous_char = 'A'

            output += self.find_optimal_path(previous_char, char, prefer_vertical)            
            previous_char = char

        return output
    
def optimal_sequence(init: str, iterations: int) -> str:
    numeric_keypad: Keypad = Keypad('NUMERIC')
    directional_keypad: Keypad = Keypad('DIRECTIONAL')
    numeric_keypad.target_code = init
    
    open_sequences: list[str] = [
        numeric_keypad.find_optimal_sequence(True),
        numeric_keypad.find_optimal_sequence(False)
    ]
    new_sequences: list[str] = []

    for _ in range(iterations):
        for sequence in open_sequences:
            directional_keypad.target_code = sequence

            new_sequences.append(directional_keypad.find_optimal_sequence(True))
            new_sequences.append(directional_keypad.find_optimal_sequence(False))

        open_sequences = new_sequences
        new_sequences = []

    open_sequences = sorted(open_sequences, key=lambda x: len(x))
    print([len(sequence) for sequence in open_sequences])
    return open_sequences[0]
    
def code_solver(codes: list[str]) -> int:
    len_sum: int = 0
    
    for code in codes:
        sequence: str = optimal_sequence(code, 2)
        
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