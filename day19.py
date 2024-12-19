def promising_branch(design: str, patterns: set[str], pattern_lengths: set[int]) -> bool:
    is_promising: bool = False
    for length in pattern_lengths:
        if design[:length] in patterns:
            is_promising = True
            break
    return is_promising

def promising(design: str, pattern: str) -> bool:
    # print(design[len(pattern):], design[:len(pattern)], pattern)
    if design[:len(pattern)] == pattern:
        return True
    return False

def valid_pattern(design: str, patterns: list[str], pattern_lengths: set[int], idx: int=0) -> bool:
    if promising_branch(design[idx:], set(patterns), pattern_lengths):
        for i, pattern in enumerate(patterns):
            if promising(design[idx:], pattern):
                if idx == len(design)-1:
                    return True
                
                branch: bool = valid_pattern(design, patterns, pattern_lengths, idx+len(pattern))

                if branch:
                    return branch
                else:
                    continue

    return False

def main() -> None:
    patterns: list[str] = []
    designs: list[str] = []
    pattern_lengths: set[int] = set()

    with open('./inputs/day19/0.txt', 'r') as file:
        contents: list[str] = file.readlines()
        patterns = [i.rstrip() for i in contents[0].split(', ')]
        designs = [i.rstrip() for i in contents[2:]]
        for pattern in patterns:
            pattern_lengths.add(len(pattern))

    print(patterns)
    print(designs)
    print(pattern_lengths)

    valid_count: int = 0
    for i, design in enumerate(designs):
        valid: bool = valid_pattern(design, patterns, pattern_lengths)
        valid_count += 1 if valid else 0
        print(f'Design: {i}/{len(designs)}')

    print(valid_count)

if __name__ == '__main__':
    main()