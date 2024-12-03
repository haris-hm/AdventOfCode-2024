numbers: list[str] = [str(i) for i in range(10)]
program: str = ''

with open('./inputs/day03/1.txt', 'r') as file:
    program = file.read()

def parse_parens(input: str) -> int | None:
    comma_found: bool = False
    first_num: str = ''
    second_num: str = ''

    print(f'{f" Parsing {input} ":-^40}')
    for i in range(1, len(input)):
        curr_char: str = input[i]
        if curr_char in numbers and not comma_found:
            first_num += curr_char
        elif curr_char in numbers and comma_found:
            second_num += curr_char
        elif curr_char == ',':
            comma_found = True
        elif curr_char == ')' and comma_found:
            print(f'{first_num} * {second_num} = {int(first_num)*int(second_num)}')
            return int(first_num)*int(second_num)
        else:
            return None
    
def scan_corrupted(input: str) -> int:
    instructions: list[str] = input.split('mul')
    print(instructions)
    sum: int = 0
    enabled: bool = True

    for i in instructions:
        if i.find('(') == 0 and enabled:
            parsed: int | None = parse_parens(i)
            sum += parsed if parsed != None else 0
        if 'don\'t()' in i:
            enabled = False
        elif 'do()' in i:
            enabled = True

    return sum

print(f'Sum: {scan_corrupted(program)}')