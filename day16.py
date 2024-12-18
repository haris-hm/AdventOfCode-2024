import heapq
from typing import Self
from enum import Enum

class Orientation(Enum):
    NORTH = (-1 ,0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def rotate(orientation: Self, turn_direction: int) -> Self:
        orientations: dict[int, Self] = {
            0: Orientation.NORTH,
            1: Orientation.EAST,
            2: Orientation.SOUTH,
            3: Orientation.WEST
        }

        orientation_to_index: dict[Self, int] = {
            Orientation.NORTH: 0,
            Orientation.EAST: 1,
            Orientation.SOUTH: 2,
            Orientation.WEST: 3
        }

        return orientations[(orientation_to_index[orientation] + turn_direction) % 4]
        
class Node():
    def __init__(self, y: int, x: int, orientation: Orientation, cost: int | float):
        self.y = y
        self.x = x
        self.orientation = orientation
        self.cost: int | float = cost

    def __repr__(self) -> str:
        return f'[{self.y}, {self.x}, Facing: {self.orientation.name}, Cost: {self.cost}]'
    
    def __eq__(self, other: Self) -> bool:
        return (self.y, self.x, self.orientation) == (other.y, other.x, other.orientation)

    def __hash__(self) -> bool:
        return hash((self.y, self.x, self.orientation))
    
    def __lt__(self, other: Self) -> bool:
        return self.cost < other.cost

class Maze():
    def __init__(self, grid: str) -> None:
        self.grid = [[char for char in line] for line in grid.split('\n')]
        self.optimal_paths_grid: list[list[str]] = None
        self.starting_node: Node = None
        self.ending_nodes: list[Node] = []
        self.valid_ending_nodes: list[Node] = []

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if (char == 'S'):
                    self.starting_node = Node(y, x, Orientation.EAST, 0)
                elif (char == 'E'):
                    for orientation in Orientation:
                        self.ending_nodes.append(Node(y, x, orientation, float('inf')))

    def next_nodes(self, node: Node) -> list[Node]:
        dy, dx = node.orientation.value
        y_prime, x_prime = node.y+dy, node.x+dx
        
        return [
            Node(y_prime, x_prime, node.orientation, node.cost+1),        
            Node(node.y, node.x, Orientation.rotate(node.orientation, 1), node.cost+1000),
            Node(node.y, node.x, Orientation.rotate(node.orientation, -1), node.cost+1000),
        ]
    
    def check_grid(self, y: int, x: int, char: str) -> bool:
        if (self.grid[y][x] == char):
            return True
        return False

    def dijkstra(self, previous_nodes: dict[Node, list[Node]]={}) -> int:
        touch: heapq[Node] = []
        heapq.heappush(touch, self.starting_node)

        distances: dict[Node, int] = {self.starting_node: 0}

        while touch:
            curr_node: Node = touch.pop(0)

            for next_node in self.next_nodes(curr_node):
                if (self.check_grid(next_node.y, next_node.x, '#')):
                    continue
               
                if (next_node not in distances or next_node.cost < distances[next_node]):
                    distances[next_node] = next_node.cost
                    heapq.heappush(touch, next_node)

                    previous_nodes[next_node] = [curr_node]
                elif (next_node.cost == distances[next_node]):
                    previous_nodes[next_node].append(curr_node)

        ending_variations: list[Node] = [Node(node.y, node.x, node.orientation, distances[node]) for node in self.ending_nodes if node in distances]
        min_distance: int = min([distances[node] for node in ending_variations])
        self.valid_ending_nodes = [node for node in ending_variations if node.cost == min_distance]

        return min_distance
    
    def optimal_seat_count(self) -> int:
        paths: dict[Node, list[Node]] = {}
        self.dijkstra(previous_nodes=paths)
        
        open = [paths[self.valid_ending_nodes[0]]]
        closed: set[Node] = {self.valid_ending_nodes[0]}
        while open:
            nodes = open.pop(0)

            for node in nodes:
                if node in paths and node not in closed:
                    open.append(paths[node])
                closed.add(node)

        self.optimal_paths_grid: list[list[str]] = self.generate_optimal_paths(closed)
        seats: int = 0
        seen_nodes: set[tuple[int]] = set()

        for node in closed:
            y, x = node.y, node.x
            if (y, x) not in seen_nodes:
                seats += 1
                seen_nodes.add((y, x))
        
        return seats
    
    def generate_optimal_paths(self, nodes: set[Node]) -> list[list[str]]:
        grid: list[list[str]] = []
        for y, line in enumerate(self.grid):
            grid.append(line.copy())

        for node in nodes:
            y: int = node.y
            x: int = node.x
            grid[y][x] = 'O'

        return grid
    
    def show_optimal_paths(self) -> str:
        return '\n'.join([''.join(line) for line in self.optimal_paths_grid]) if self.optimal_paths_grid != None else ''

    def __repr__(self) -> str:
        grid_lines: list[str] = [''.join(line) for line in self.grid]
        grid: str = '      '
        grid += '\n      '.join(grid_lines)

        return f'Graph:\n   Starting Node: {self.starting_node}\n   Ending Nodes: {self.ending_nodes}\n   Grid:\n{grid}'
        
def main() -> None:
    file_name: str = '1'
    maze: Maze = None
    with open(f'./inputs/day16/{file_name}.txt', 'r') as file:
        contents: str = file.read()
        maze = Maze(contents)

    print(f'The minimum cost path is: {maze.dijkstra()}.')
    print(f'There are {maze.optimal_seat_count()} optimal seat(s).')
    
    with open(f'./outputs/day16/{file_name}.txt', 'w') as file:
        file.write(maze.show_optimal_paths())
        file.close()

if __name__ == '__main__':
    main()