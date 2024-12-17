class Map():
    def __init__(self, grid: list[list[str]], robot_location: tuple[int], movements: list[str]) -> None:
        self.grid = grid
        self.robot_y = robot_location[0]
        self.robot_x = robot_location[1]
        self.movements = movements

    def run_simulation(self) -> None:
        for movement in self.movements:
            self.move_robot(movement)

    def run_sim_manual(self) -> None:        
        while True:
            movement: str = input('Which way should the robot move? (E to exit): ')
            if (movement == 'E'):
                break
            self.move_robot(movement)
            print(f'\n\n\nMoved: {movement}')
            print(self)

    def translate_movement(self, movement: str) -> tuple[int]:
        match movement:
            case '^':
                return (-1, 0)
            case '>':
                return (0, 1)
            case 'v': 
                return (1, 0)
            case '<':
                return (0, -1)
            
    def move_x(self, dx: int) -> None:
        new_location: int = self.robot_x + dx

        if (self.grid[self.robot_y][new_location] == '#'):
            return
        elif (self.grid[self.robot_y][new_location] == '.'):
            self.grid[self.robot_y][new_location] = '@'
            self.grid[self.robot_y][self.robot_x] = '.'
            self.robot_x += dx
        else:
            i: int = 1

            while True:
                crate_new_location: int = new_location + dx*i

                if (self.grid[self.robot_y][crate_new_location] == '.'):
                    self.grid[self.robot_y][crate_new_location] = 'O'

                    self.grid[self.robot_y][new_location] = '@'
                    self.grid[self.robot_y][self.robot_x] = '.'
                    self.robot_x += dx
                    return
                elif (self.grid[self.robot_y][crate_new_location] == '#'):
                    return
                
                i += 1
        
    def move_y(self, dy: int) -> None:
        new_location: int = self.robot_y + dy

        if (self.grid[new_location][self.robot_x] == '#'):
            return
        elif (self.grid[new_location][self.robot_x] == '.'):
            self.grid[new_location][self.robot_x] = '@'
            self.grid[self.robot_y][self.robot_x] = '.'
            self.robot_y += dy
        else:
            i: int = 1
            while True:
                crate_new_location: int = new_location + dy*i

                if (self.grid[crate_new_location][self.robot_x] == '.'):
                    self.grid[crate_new_location][self.robot_x] = 'O'

                    self.grid[new_location][self.robot_x] = '@'
                    self.grid[self.robot_y][self.robot_x] = '.'
                    self.robot_y += dy
                    return
                elif (self.grid[crate_new_location][self.robot_x] == '#'):
                    return
                
                i += 1

    def move_robot(self, movement: str) -> None:
        movement_coord: tuple[int] = self.translate_movement(movement)

        if (movement_coord[0] == 0):
            self.move_x(movement_coord[1])
        else:
            self.move_y(movement_coord[0])

    def calc_gps(self) -> int:
        gps_sum: int = 0

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if (char == 'O'):
                    gps_sum += y*100 + x

        return gps_sum

    def __repr__(self) -> str:
        grid_lines: list[str] = [''.join(line) for line in self.grid]
        grid: str = '\n'.join(grid_lines)
        return grid
    
class WideMap(Map):
    def __init__(self, *args, **kwargs):
        super(WideMap, self).__init__(*args, **kwargs)
        self.widen_map()

    def widen_map(self) -> None:
        new_grid: list[list[str]] = []

        for line in self.grid:
            new_line: list[str] = []
            for char in line:
                new_char: list[str] = []
                match char:
                    case '#':
                        new_char = ['#', '#']
                    case 'O':
                        new_char = ['[', ']']
                    case '.':
                        new_char = ['.', '.']
                    case '@':
                        new_char = ['@', '.']

                new_line.extend(new_char)
            new_grid.append(new_line)

        self.grid = new_grid

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char == '@':
                    self.robot_x = x
                    self.robot_y = y

    def search_box_tree(self, dy: int, starting_node: tuple[int]) -> list[tuple[int]]:
        open_nodes: list[tuple[int]] = [starting_node]
        closed_nodes: list[str] = []

        while len(open_nodes) > 0:
            curr_node: tuple[int] = open_nodes.pop(0)
            closed_nodes.append(curr_node)
            y: int = curr_node[0]
            x_1: int = curr_node[1]
            x_2: int = curr_node[2]

            if (self.grid[y+dy][x_1] == '#' or self.grid[y+dy][x_2] == '#'):
                return []

            right_box: tuple[int] = (y+dy, x_2, x_2+1)
            left_box: tuple[int] = (y+dy, x_1-1, x_1)
            above_box: tuple[int] = (y+dy, x_1, x_2)

            is_right_box: bool = f'{self.grid[right_box[0]][right_box[1]]}{self.grid[right_box[0]][right_box[2]]}' == '[]'
            is_left_box: bool = f'{self.grid[left_box[0]][left_box[1]]}{self.grid[left_box[0]][left_box[2]]}' == '[]'
            is_above_box: bool = f'{self.grid[above_box[0]][above_box[1]]}{self.grid[above_box[0]][above_box[2]]}' == '[]'
            
            if (is_above_box):
                open_nodes.append(above_box)
                continue

            if (is_right_box):
                open_nodes.append(right_box)

            if (is_left_box):
                open_nodes.append(left_box)

        return closed_nodes
    
    def move_x(self, dx: int) -> None:
        new_location: int = self.robot_x + dx

        if (self.grid[self.robot_y][new_location] == '#'):
            return
        elif (self.grid[self.robot_y][new_location] == '.'):
            self.grid[self.robot_y][new_location] = '@'
            self.grid[self.robot_y][self.robot_x] = '.'
            self.robot_x += dx
        else:
            i: int = 1

            while True:
                crate_new_location: int = new_location + dx + i*2*dx
                print(self.grid[self.robot_y][crate_new_location])
                if (self.grid[self.robot_y][crate_new_location - dx] == '.'):
                    curr_bracket = ']' if dx > 0 else '['
                    step: int = -1 if dx > 0 else 1

                    for k in range(crate_new_location-dx, new_location, step):
                        self.grid[self.robot_y][k] = curr_bracket
                        if (curr_bracket == '['):
                            curr_bracket = ']'
                        else:
                            curr_bracket = '['

                    self.grid[self.robot_y][new_location] = '@'
                    self.grid[self.robot_y][self.robot_x] = '.'
                    self.robot_x += dx
                    return
                elif (self.grid[self.robot_y][crate_new_location - dx] == '#'):
                    return
                
                i += 1
    
    def move_y(self, dy: int) -> None:
        new_location: int = self.robot_y + dy

        if (self.grid[new_location][self.robot_x] == '#'):
            return
        elif (self.grid[new_location][self.robot_x] == '.'):
            self.grid[new_location][self.robot_x] = '@'
            self.grid[self.robot_y][self.robot_x] = '.'
            self.robot_y += dy
        else:
            nodes_to_update: list[tuple[int]] = []
            if (self.grid[self.robot_y+dy][self.robot_x] == '['):
                nodes_to_update = self.search_box_tree(dy, (self.robot_y+dy, self.robot_x, self.robot_x+1))
            elif (self.grid[self.robot_y+dy][self.robot_x] == ']'):
                nodes_to_update = self.search_box_tree(dy, (self.robot_y+dy, self.robot_x-1, self.robot_x))

            if (len(nodes_to_update) > 0):
                for node in nodes_to_update[::-1]:
                    self.grid[node[0]+dy][node[1]] = '['
                    self.grid[node[0]+dy][node[2]] = ']'

                    self.grid[node[0]][node[1]] = '.'
                    self.grid[node[0]][node[2]] = '.'

                self.grid[new_location][self.robot_x] = '@'
                self.grid[self.robot_y][self.robot_x] = '.'
                self.robot_y += dy

    def calc_gps(self) -> int:
        gps_sum: int = 0

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if (char == '['):
                    gps_sum += y*100 + x

        return gps_sum

def main() -> None:
    warehouse: Map = None
    wide_warehouse: WideMap = None

    with open('./inputs/day15/2.txt', 'r') as file:
        contents: list[str] = file.read().split('\n\n')
        grid: list[list[str]] = [[char for char in line] for line in contents[0].split('\n')]
        movements: list[str] = ''.join(contents[1].split('\n'))
        robot_location: tuple[int] = ()

        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                if char == '@':
                    robot_location = (y, x)

        warehouse = Map(grid, robot_location, movements)
        wide_warehouse = WideMap(grid, robot_location, movements)

    # Part 1
    print(warehouse)
    warehouse.run_simulation()
    print(warehouse)
    print(f'GPS Sum: {warehouse.calc_gps()}')

    # Part 2
    print(wide_warehouse)
    wide_warehouse.run_simulation()
    print(wide_warehouse)
    print(f'GPS Sum: {wide_warehouse.calc_gps()}')

if __name__ == '__main__':
    main()