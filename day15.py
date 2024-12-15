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

    def crate_count(self) -> int:
        count: int = 0
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if (char == 'O'):
                    count += 1

        return count

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
        return super().move_y(dy)

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
    # print(warehouse)
    # warehouse.run_simulation()
    # print(warehouse)
    # print(f'GPS Sum: {warehouse.calc_gps()}')

    print(f'\n\n{wide_warehouse}')
    wide_warehouse.run_sim_manual()

if __name__ == '__main__':
    main()