import re

class Robot():
    def __init__(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def tick(self, width: int, height: int) -> None:
        if (self.vel_x > 0):
            self.pos_x = (self.pos_x + self.vel_x) % width
        else:
            if (self.pos_x + self.vel_x < 0):
                self.pos_x = width + self.vel_x + self.pos_x
            else:
                self.pos_x = self.pos_x + self.vel_x

        if (self.vel_y > 0):
            self.pos_y = (self.pos_y + self.vel_y) % height
        else:
            if (self.pos_y + self.vel_y < 0):
                self.pos_y = height + (self.vel_y + self.pos_y)
            else:
                self.pos_y = self.pos_y + self.vel_y

    def __repr__(self) -> str:
        return f'{{Pos: ({self.pos_x}, {self.pos_y}) | Velocity: ({self.vel_x}, {self.vel_y})}}'

class Map():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.robots: list[Robot] = []
        self.robot_amount: int = 0

        self.current_tick: int = 0

        self.lowest_safety_factor: int = -1
        self.potential_tree_map: list[list[str]] = []

    def add_robot(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int) -> None:
        self.robots.append(Robot(pos_x, pos_y, vel_x, vel_y))
        self.robot_amount += 1
        
    def tick(self) -> None:
        self.current_tick += 1
        for robot in self.robots:
            robot.tick(self.width, self.height)

    def map_to_list(self) -> list[list[str]]:
        map_list: list[list[str]] = []

        for i in range(self.height):
            map_list.append(['.'] * self.width)

        for robot in self.robots:
            curr_char: str = map_list[robot.pos_y][robot.pos_x] 
            if curr_char == '.':
                map_list[robot.pos_y][robot.pos_x] = '1'
            else:
                map_list[robot.pos_y][robot.pos_x] = str(int(curr_char) + 1)

        return map_list
    
    def calc_quad_safety(self, quad: list[list[str]]) -> int:
        robot_count: int = 0
        for i, line in enumerate(quad):
            for k, char in enumerate(line):
                if char != '.':
                    robot_count += int(char)

        return robot_count
    
    def save_map(self) -> None:
        with open(f'./outputs/day14/{self.current_tick}.txt', 'w') as file:
            file.write(str(self))
            file.close()
    
    def calculate_safety_factor(self) -> int:
        map_list: list[list[str]] = self.map_to_list()
        top_half: list[list[str]] = map_list[self.height//2+1:]
        bottom_half: list[list[str]] = map_list[:self.height//2]

        top_left_quad: list[list[str]] = [i[self.width//2+1:] for i in top_half]
        top_right_quad: list[list[str]] = [i[:self.width//2] for i in top_half]
        bottom_left_quad: list[list[str]] = [i[self.width//2+1:] for i in bottom_half]
        bottom_right_quad: list[list[str]] = [i[:self.width//2] for i in bottom_half]

        score: int = self.calc_quad_safety(top_left_quad)      \
                     *self.calc_quad_safety(top_right_quad)    \
                     *self.calc_quad_safety(bottom_left_quad)  \
                     *self.calc_quad_safety(bottom_right_quad)
        
        if (self.lowest_safety_factor == -1 or self.lowest_safety_factor > score):
            self.lowest_safety_factor = score
            self.potential_tree_map = map_list
            self.save_map()
        
        return score
      
    def clustering(self, threshold: int) -> None:
        map_list: list[list[str]] = self.map_to_list()
        visited_nodes: set[tuple[int]] = set()
        is_cluster_present: bool = False

        for y, line in enumerate(map_list):
            for x, char in enumerate(line):
                curr_idx: tuple[int] = (y, x)
                count: int = 0

                if (curr_idx not in visited_nodes):
                    is_cluster_present = self.identify_cluster(curr_idx, threshold, visited_nodes, map_list, count)

                if (is_cluster_present):
                    break
        
    def __repr__(self) -> str:
        combined_strs: list[str] = []
        for line in self.map_to_list():
            combined_strs.append(''.join(line))

        repr_str: str = ''
        for line in combined_strs:
            repr_str += line + '\n'

        return repr_str
    
def tick_map(bathroom_map: Map, tick_amount: int) -> None:
    print(f'Starting Map:\n{bathroom_map}')
    for i in range(tick_amount):
        bathroom_map.tick()
        bathroom_map.calculate_safety_factor()
        if i % 1000 == 0:
            print(f'Iteration: {i}')
    
    print(f'Final Map:\n{bathroom_map}')
    print(f'Safety Factor: {bathroom_map.calculate_safety_factor()}')

def main() -> None:
    bathroom_map: Map = Map(101, 103)

    with open('./inputs/day14/1.txt', 'r') as file:
        contents: list[str] = file.read().split('\n')
        for line in contents:
            init_info: list[int] =  [int(i) for i in re.findall('(-*\d+)', line)]
            bathroom_map.add_robot(init_info[0], init_info[1], init_info[2], init_info[3])
    
    tick_map(bathroom_map, 100)

    tick_map(bathroom_map, 9900)

    # Part 2
    # curr_second: int = 0

    # while True:
    #     bathroom_map.tick()
    #     print(f'{bathroom_map}\nSeconds elapsed: {curr_second}\n\n')
    #     input('Continue?:')
    #     bathroom_map.clustering(50)
    #     curr_second += 1

if __name__ == '__main__':
    main()