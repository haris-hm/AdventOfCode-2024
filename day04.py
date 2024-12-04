input_1: list[str] = []

with open('./inputs/day04/1.txt', 'r') as file:
    contents = file.read()
    input_1 = contents.split('\n')

def search_input(input: list[str]) -> int:
    xmas_count: int = 0
    for i in range(len(input)):
        curr_str: str = input[i]
        reversed_str: str = curr_str[::-1]

        # Horizontals
        xmas_count += len(curr_str.split("XMAS")) + len(reversed_str.split("XMAS")) - 2

        # Bottom Diagonals
        if (i < len(input)-3):
            for k in range(len(curr_str)):
                if (curr_str[k] != 'X'):
                    continue

                # Vertical
                if (input[i+1][k] == 'M' and input[i+2][k] == 'A' and input[i+3][k] == 'S'):
                    xmas_count += 1

                # Bottom Right
                if (k < len(curr_str)-3 and input[i+1][k+1] == 'M' and input[i+2][k+2] == 'A' and input[i+3][k+3] == 'S' ):
                    xmas_count += 1

                # Bottom Left
                if (k > 2 and input[i+1][k-1] == 'M' and input[i+2][k-2] == 'A' and input[i+3][k-3] == 'S'):
                    xmas_count += 1

        # Top Diagonals and verticals
        if (i > 2):
            for k in range(len(curr_str)):
                if (curr_str[k] != 'X'):
                    continue

                # Vertical
                if (input[i-1][k] == 'M' and input[i-2][k] == 'A' and input[i-3][k] == 'S'):
                    xmas_count += 1

                # Top right
                if (k < len(curr_str)-3 and input[i-1][k+1] == 'M' and input[i-2][k+2] == 'A' and input[i-3][k+3] == 'S'):
                    xmas_count += 1

                # Top left
                if (k > 2 and input[i-1][k-1] == 'M' and input[i-2][k-2] == 'A' and input[i-3][k-3] == 'S'):
                    xmas_count += 1

    return xmas_count

def search_xmasses(input: list[str]) -> int:
    xmas_count: int = 0
    masses: list[str] = ['MAS', 'SAM']

    for i in range(1, len(input)-1):
        curr_str: str = input[i]

        for k in range(1, len(curr_str)-1):
            if (curr_str[k] == 'A'):
                left_right_diagonal: str = input[i-1][k-1] + 'A' + input[i+1][k+1]
                right_left_diagonal: str = input[i-1][k+1] + 'A' + input[i+1][k-1]\
                
                if (left_right_diagonal in masses and right_left_diagonal in masses):
                    
                    xmas_count += 1

    return xmas_count

print(f'XMAS count: {search_input(input_1)}')
print(f'X-MAS count: {search_xmasses(input_1)}')