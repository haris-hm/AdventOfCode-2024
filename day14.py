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

    def add_robot(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int) -> None:
        self.robots.append(Robot(pos_x, pos_y, vel_x, vel_y))
        self.robot_amount += 1
        
    def tick(self) -> None:
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
    
    def calculate_safety_factor(self) -> int:
        map_list: list[list[str]] = self.map_to_list()
        top_half: list[list[str]] = map_list[self.height//2+1:]
        bottom_half: list[list[str]] = map_list[:self.height//2]

        top_left_quad: list[list[str]] = [i[self.width//2+1:] for i in top_half]
        top_right_quad: list[list[str]] = [i[:self.width//2] for i in top_half]
        bottom_left_quad: list[list[str]] = [i[self.width//2+1:] for i in bottom_half]
        bottom_right_quad: list[list[str]] = [i[:self.width//2] for i in bottom_half]

        print(self.calc_quad_safety(bottom_right_quad))

        score: int = self.calc_quad_safety(top_left_quad)      \
                     *self.calc_quad_safety(top_right_quad)    \
                     *self.calc_quad_safety(bottom_left_quad)  \
                     *self.calc_quad_safety(bottom_right_quad)
        
        return score
    
    def promising(self, curr_char: str, 
                  coord: tuple[int], 
                  map_list: list[list[str]], 
                  visited_nodes: set[tuple[int]]) -> bool:
        y: int = coord[0]
        x: int = coord[1]

        within_bounds: bool = 0 <= y < len(map_list) and 0 <= x < len(map_list[0])
        not_visited: bool = (y, x) not in visited_nodes
        same_id: bool = False

        if (within_bounds):
            same_id = map_list[y][x] == curr_char

        if (same_id and not_visited and within_bounds):
            return True
        else:
            return False
    
    def identify_cluster(self, starting_idx: tuple[int], 
                         threshold: int, 
                         visited_nodes: set[tuple[int]], 
                         map_list: list[list[str]],
                         count: int) -> bool:
        y: int = starting_idx[0]
        x: int = starting_idx[1]

        curr_char: str = map_list[y][x]

        visited_nodes.add(starting_idx)

        up: tuple[int] = (y-1, x)
        down: tuple[int] = (y+1, x)
        left: tuple[int] = (y, x-1)
        right: tuple[int] = (y, x+1)

        if count == threshold:
            return True
        
        up_cluster: bool = False
        down_cluster: bool = False
        left_cluster: bool = False
        right_cluster: bool = False
        
        if (self.promising(curr_char, up, map_list, visited_nodes)):
            up_cluster = self.identify_cluster(up, threshold, visited_nodes, map_list, count)
        
        if (self.promising(curr_char, down, map_list, visited_nodes)):
            down_cluster = self.identify_cluster(down, threshold, visited_nodes, map_list, count)

        if (self.promising(curr_char, left, map_list, visited_nodes)):
            left_cluster = self.identify_cluster(left, threshold, visited_nodes, map_list, count)

        if (self.promising(curr_char, right, map_list, visited_nodes)):
            right_cluster = self.identify_cluster(right, threshold, visited_nodes, map_list, count)

        return up_cluster or down_cluster or left_cluster or right_cluster
      
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

        print(is_cluster_present)

        if (is_cluster_present):
            with open('./outputs/day14.txt', 'w') as file:
                file.write(self)
                file.close()
        
    def __repr__(self) -> str:
        combined_strs: list[str] = []
        for line in self.map_to_list():
            combined_strs.append(''.join(line))

        repr_str: str = ''
        for line in combined_strs:
            repr_str += line + '\n'

        return repr_str
    
def part_one(bathroom_map: Map) -> None:
    print(bathroom_map)
    for i in range(100):
        bathroom_map.tick()
        if i % 10000 == 0:
            print(i)
    
    print(bathroom_map)
    print(bathroom_map.calculate_safety_factor())

def main() -> None:
    bathroom_map: Map = Map(101, 103)

    with open('./inputs/day14/1.txt', 'r') as file:
        contents: list[str] = file.read().split('\n')
        for line in contents:
            init_info: list[int] =  [int(i) for i in re.findall('(-*\d+)', line)]
            bathroom_map.add_robot(init_info[0], init_info[1], init_info[2], init_info[3])
    
    # part_one(bathroom_map)

    # Part 2
    curr_second: int = 0

    while True:
        bathroom_map.tick()
        print(f'{bathroom_map}\nSeconds elapsed: {curr_second}\n\n')
        input('Continue?:')
        bathroom_map.clustering(50)
        curr_second += 1

if __name__ == '__main__':
    main()