import re

from typing import Self
from heapq import heappush, heappop

class Node():
    def __init__(self, y: int, x: int, cost: int | float=float('inf')):
        self.y = y
        self.x = x
        self.cost: int | float = cost
        self.priority: float = 0
        self.parent: Node = None

    def set_priority(self, h: float) -> None:
        self.priority = self.cost + h

    def __repr__(self) -> str:
        return f'[{self.y}, {self.x}, Cost: {self.cost}]'
    
    def __eq__(self, other: Self) -> bool:
        if (not isinstance(other, Node)):
            return False
        return (self.y, self.x) == (other.y, other.x)

    def __hash__(self) -> int:
        return hash((self.y, self.x))
    
    def __lt__(self, other: Self) -> bool:
        return self.priority < other.priority

class ByteMaze():
    def __init__(self, dimensions: int, byte_coords: list[str], byte_amount: int) -> None:
        self.dimensions = dimensions

        self.byte_coords = byte_coords
        self.byte_amount = byte_amount
        
        self.grid: list[list[str]] = []
        self.starting_node: Node = Node(0, 0, cost=0)
        self.ending_node: Node = Node(dimensions, dimensions)

        self.setup_grid()

    def setup_grid(self) -> None:
        for _ in range(self.dimensions+1):
            self.grid.append(['.']*(self.dimensions+1))

        for i in range(self.byte_amount):
            x, y = [int(k) for k in re.findall(r'\d+', self.byte_coords[i])]
            self.grid[y][x] = '#'

    def valid_grid_pos(self, y: int, x: int) -> bool:
        if (not (0 <= y <= self.dimensions) or not (0 <= x <= self.dimensions)):
            return False
        elif (self.grid[y][x] == '#'):
            return False
        return True

    def get_neighbors(self, node: Node) -> list[Node]:  
        next_nodes: list[Node] = []

        for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            y_prime: int = node.y+dy
            x_prime: int = node.x+dx

            if (self.valid_grid_pos(y_prime, x_prime)):
                next_nodes.append(Node(y_prime, x_prime, node.cost+1))

        return next_nodes
    
    def a_star_heuristic(self, a: Node, b: Node) -> float:
        return abs(a.x-b.x) + abs(a.y-b.y)
    
    def a_star(self) -> int:
        open_nodes: list[Node] = []
        heappush(open_nodes, self.starting_node)

        closed: set[Node] = set()
        distance: dict[Node, int] = {self.starting_node: 0}

        while open_nodes:
            curr_node: Node = heappop(open_nodes)
            closed.add(curr_node)

            if curr_node == self.ending_node:
                self.ending_node = curr_node
                break

            for neighbor in self.get_neighbors(curr_node):
                if (neighbor not in distance or neighbor.cost < distance[neighbor]):
                    distance[neighbor] = neighbor.cost
                    neighbor.set_priority(self.a_star_heuristic(neighbor, self.ending_node))
                    heappush(open_nodes, neighbor)
                    neighbor.parent = curr_node

        return self.ending_node
    
    def show_optimal_path(self) -> str:
        new_grid: list[list[str]] = []

        for line in self.grid:
            new_grid.append(line.copy())

        self.a_star()

        curr_node: Node = self.ending_node

        while curr_node != None:
            new_grid[curr_node.y][curr_node.x] = 'O'
            curr_node = curr_node.parent

        return f'{self.grid_repr(new_grid)}\nOptimal Cost: {self.ending_node.cost}'

    def grid_repr(self, raw_grid: list[list[str]]) -> str:
        grid_lines: list[str] = [''.join(line) for line in raw_grid]
        grid: str = ''
        grid += '\n'.join(grid_lines)
        return grid
    
    def __repr__(self) -> str:
        return f'Grid:\n{self.grid_repr(self.grid)}'

def main() -> None:
    maze: ByteMaze = None

    with open('./inputs/day18/0.txt', 'r') as file:
        contents: str = file.readlines()

        # maze = ByteMaze(6, contents, 12)
        maze = ByteMaze(70, contents, 1024)

    print(maze)

    print(maze.show_optimal_path())
    
if __name__ == '__main__':
    main()