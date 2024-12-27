def mix(init_num: int, mixing_num: int) -> int:
    return init_num ^ mixing_num

def prune(init_num: int) -> int:
    return init_num % 16777216

def next_number(init_num: int) -> int:
    curr_num: int = prune(mix(init_num, init_num*64))
    curr_num = prune(mix(curr_num, curr_num//32))
    curr_num = prune(mix(curr_num, curr_num*2048))
    return curr_num

def solve_secrets(nums: list[int], secret_iterations: int) -> int:
    for i in range(len(nums)):
        for _ in range(secret_iterations):
            nums[i] = next_number(nums[i])

    return sum(nums)

def main() -> None:
    with open('./inputs/day22/0.txt', 'r') as file:
        contents: list[int] = [int(line.rstrip()) for line in file.readlines()]

        print(f'Secret number sum after 2000 iterations: {solve_secrets(contents, 2000)}')

if __name__ == '__main__':
    main()