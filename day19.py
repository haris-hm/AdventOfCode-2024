def solve(design: str, patterns: list[str], memo: dict[str, int]) -> int:
    if len(design) == 0:
        return 1
    
    value: int = 0
    
    for pattern in patterns:
        if design[:len(pattern)] == pattern:
            new_design: str = design[len(pattern):]
            if new_design in memo:
                value += memo[new_design]
            else:
                solution: int = solve(new_design, patterns, memo)
                value += solution
                memo[new_design] = solution

    return value

def validate_designs(designs: list[str], patterns: list[str]) -> tuple[int]:
    memo: dict[tuple[str], int] = {}
    sum: int = 0
    all_possibilities: int = 0

    for design in designs:
        solution: int = solve(design, patterns, memo)
        sum += 1 if solution > 0 else 0
        all_possibilities += solution

    return sum, all_possibilities

def main() -> None:
    patterns: list[str] = []
    designs: list[str] = []
    pattern_lengths: set[int] = set()

    with open('./inputs/day19/0.txt', 'r') as file:
        contents: list[str] = file.readlines()
        patterns = [i.rstrip() for i in contents[0].split(', ')]
        designs = [i.rstrip() for i in contents[2:]]

    possibilites, all_possibilities = validate_designs(designs, patterns)
    
    print(f'Possibilities: {possibilites}\nAll Possibilities: {all_possibilities}')

if __name__ == '__main__':
    main()