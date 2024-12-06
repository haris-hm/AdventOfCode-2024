import time

guard_map: list[str] = []

with open('./inputs/day06/1.txt', 'r') as file:
    contents = file.read()
    guard_map = contents.split('\n')

def update_checked_squares(checked_squares: list[list[int]], location: list[int]):
    if location in checked_squares:
        checked_squares
    else:
        checked_squares.append(location.copy())

def trace_path(guard_map: list[str]) -> tuple[int, list[str]] | None:
    guard_location: list[int] = []
    guard_map_copy: list[str] = guard_map.copy()
    checked_squares: list[list[int]] = []
    done: bool = False
    loop_limit: int = len(guard_map)*len(guard_map[0])
    hit_blocks: list[list[int]] = []

    for i, line in enumerate(guard_map):
        if '^' in line:
            guard_index: int = line.index('^')
            guard_location = [i, guard_index]
            guard_map_copy[i] = guard_map_copy[i].replace('^', '.')
            update_checked_squares(checked_squares, guard_location)
        
    directions: tuple[int] = ('UP', 'RIGHT', 'DOWN', 'LEFT')
    guard_direction: str = 0 # WASD
    loop_count: int = 0

    while not done and loop_count < loop_limit:
        loop_count += 1
        x: int = guard_location[1]
        y: int = guard_location[0]

        x_len: int = len(guard_map[0])
        y_len: int = len(guard_map)

        curr_location_y: str = guard_map_copy[y]
        updated_y: str = ''
        for i, char in enumerate(curr_location_y):
            if i == x:
                updated_y += 'X'
            else:
                updated_y += char

        guard_map_copy[y] = updated_y

        if directions[guard_direction] == 'UP':
            if y-1 < 0:
                done = True
                break
            elif guard_map_copy[y-1][x] == '#':
                if [y-1, x, guard_direction] in hit_blocks:
                    return None
                else:
                    hit_blocks.append([y-1, x, guard_direction])
                    guard_direction = (guard_direction + 1) % 4
                    continue
            else:
                guard_location[0] = y-1
                update_checked_squares(checked_squares, guard_location)
                continue
        elif directions[guard_direction] == 'RIGHT':
            if x+1 >= x_len:
                done = True
                break
            elif guard_map_copy[y][x+1] == '#':
                if [y, x+1, guard_direction] in hit_blocks:
                    return None
                else:
                    hit_blocks.append([y, x+1, guard_direction])
                    guard_direction = (guard_direction + 1) % 4
                    continue
            else:
                guard_location[1] = x+1
                update_checked_squares(checked_squares, guard_location)
                continue
        if directions[guard_direction] == 'DOWN':
            if y+1 >= y_len:
                done = True
                break
            elif guard_map_copy[y+1][x] == '#':
                if [y+1, x, guard_direction] in hit_blocks:
                    return None
                else:
                    hit_blocks.append([y+1, x, guard_direction])
                    guard_direction = (guard_direction + 1) % 4
                    continue
            else:
                guard_location[0] = y+1
                update_checked_squares(checked_squares, guard_location)
                continue
        elif directions[guard_direction] == 'LEFT':
            if x-1 < 0:
                done = True
                break
            elif guard_map_copy[y][x-1] == '#':
                if [y, x-1, guard_direction] in hit_blocks:
                    return None
                else:
                    hit_blocks.append([y, x-1, guard_direction])
                    guard_direction = (guard_direction + 1) % 4
                    continue
            else:
                guard_location[1] = x-1
                update_checked_squares(checked_squares, guard_location)
                continue
    
    if loop_count == loop_limit:
        return None
    
    return len(checked_squares), guard_map_copy

def check_blockings(guard_map: list[str], map_with_path: list[str]) -> int:
    block_count: int = 0
    estimate: int = 0
    estimates: list[float] = []

    for i, line in enumerate(map_with_path):
        for k, char in enumerate(line):
            if char == 'X' and guard_map[i][k] != '^':
                estimate += 1

    for i, line in enumerate(map_with_path):
        start_time: float = time.time_ns()
        lines_left: int = len(map_with_path) - i
        time_taken: float = sum(estimates)

        for k, char in enumerate(line):
            if char == 'X' and guard_map[i][k] != '^':
                new_guard_map: list[str] = guard_map.copy()

                new_line = list(new_guard_map[i])
                new_line[k] = '#'
                new_line = ''.join(new_line)
                new_guard_map[i] = new_line

                if trace_path(new_guard_map) == None:
                    block_count += 1

        end_time: float = time.time_ns()
        estimates.append(end_time-start_time)
            
        print(f'Estimated time remaining: {(((time_taken/len(estimates))*len(map_with_path))-time_taken)/1.0e-9} seconds')

    return block_count

guard_squares, new_map = trace_path(guard_map)
print(f'Guard Squares: {guard_squares}\nCalculating Blocks...')

start_time: float = time.time()
print(f'Block Count: {check_blockings(guard_map, new_map)}')
end_time: float = time.time()
print(f'Calculation took {(end_time-start_time)/60} minutes')