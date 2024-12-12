def dynamic_stones(stone: int, blinks: int, memo: dict[tuple[int], int]) -> int:
    stone_str: str = str(stone)
    stone_str_length: int = len(stone_str)

    if blinks == 0:
        return 1
    
    if stone == 0:
        zero_rule_key: tuple[int] = (1, blinks - 1)

        if (zero_rule_key in memo):
            return memo[zero_rule_key]
        else:
            zero_rule_val: int = dynamic_stones(zero_rule_key[0], zero_rule_key[1], memo)
            memo[zero_rule_key] = zero_rule_val
            return zero_rule_val
        
    elif stone_str_length % 2 == 0:
        left: int = 0
        right: int = 0

        left_key: tuple[int] = (int(stone_str[:stone_str_length//2]), blinks - 1)
        right_key: tuple[int] = (int(stone_str[stone_str_length//2:]), blinks - 1)

        if (left_key in memo):
            left = memo[left_key]
        else:
            left = dynamic_stones(left_key[0], left_key[1], memo)
            memo[left_key] = left

        if (right_key in memo):
            right = memo[right_key]
        else:
            right = dynamic_stones(right_key[0], right_key[1], memo)
            memo[right_key] = right

        return left + right
    
    else:
        year_rule_key: tuple[int] = (stone*2024, blinks - 1)

        if (year_rule_key in memo):
            return memo[year_rule_key]
        else:
            year_rule_val: int = dynamic_stones(year_rule_key[0], year_rule_key[1], memo)
            memo[year_rule_key] = year_rule_val
            return year_rule_val
        
def calculate_stones(stones: list[int], blinks: int) -> int:
    memo: dict[tuple[int], int] = {}
    sum: int = 0

    for stone in stones:
        sum += dynamic_stones(stone, blinks, memo)       
            
    return sum

def main() -> None:
    stones: list[int] = []

    with open('./inputs/day11/1.txt', 'r') as file:
        contents = file.read()
        stones = [int(i) for i in contents.split()]

    print(f'Number of stones at 25 blinks: {calculate_stones(stones, 25)}')
    print(f'Number of stones at 75 blinks: {calculate_stones(stones, 75)}')

if __name__ == '__main__':
    main()