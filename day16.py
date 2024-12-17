from collections import defaultdict
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
        self.starting_node: Node = None
        self.ending_nodes: list[Node] = []

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

    def dijkstra(self) -> int:
        touch: heapq[Node] = []
        heapq.heappush(touch, self.starting_node)

        distances: dict[Node| int] = {self.starting_node: 0}

        while touch:
            curr_node: Node = touch.pop(0)

            for next_node in self.next_nodes(curr_node):
                if (self.check_grid(next_node.y, next_node.x, '#')):
                    continue
               
                if (next_node not in distances or next_node.cost < distances[next_node]):
                    distances[next_node] = next_node.cost
                    heapq.heappush(touch, next_node)

        ending_variations: list[Node] = [node for node in self.ending_nodes if node in distances]
        min_distance: int = min([distances[node] for node in ending_variations])

        return min_distance

    def __repr__(self) -> str:
        grid_lines: list[str] = [''.join(line) for line in self.grid]
        grid: str = '      '
        grid += '\n      '.join(grid_lines)

        return f'Graph:\n   Starting Node: {self.starting_node}\n   Ending Nodes: {self.ending_nodes}\n   Grid:\n{grid}'
        
def main() -> None:
    maze: Maze = None
    with open('./inputs/day16/1.txt', 'r') as file:
        contents: str = file.read()
        maze = Maze(contents)

    print(maze)
    print(f'The minimum cost path is: {maze.dijkstra()}')

if __name__ == '__main__':
    main()