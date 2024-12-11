def split_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        left_stone: str = str(stone)[:len(str(stone))//2]
        right_stone: str = str(stone)[len(str(stone))//2:]
        return [int(left_stone), int(right_stone)]
    else:
        return [stone*2024]
    
def dynamic_splitting(stones: list[int], memo: dict[list[int], tuple[list[int], int]]) -> tuple[list[int], int]:
    stones_amount: int = len(stones)

    if stones_amount == 1:
        base_stone: tuple[list[int], int] = split_stone(stones[0])
        return base_stone, len(base_stone)
    elif tuple(stones) in memo:
        # print('hit', stones_amount)
        return memo[tuple(stones)]

    left: list[int] = stones[:stones_amount//2]
    right: list[int] = stones[stones_amount//2:]

    left_stones, left_val = dynamic_splitting(left, memo) 
    memo[tuple(left)] = (left_stones, left_val)
    right_stones, right_val = dynamic_splitting(right, memo)
    memo[tuple(right)] = (right_stones, right_val)

    left_stones.extend(right_stones)

    return left_stones, (left_val + right_val)

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

if __name__ == '__main__':
    main()