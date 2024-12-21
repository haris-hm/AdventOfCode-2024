from typing import Self
from enum import Enum

class Orientation(Enum):
    NORTH = (-1 ,0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def get_opposite(orientation: Self) -> Self:
        match orientation:
            case Orientation.NORTH:
                return Orientation.SOUTH
            case Orientation.EAST:
                return Orientation.WEST
            case Orientation.SOUTH:
                return Orientation.NORTH
            case Orientation.WEST:
                return Orientation.EAST

class Node():
    def __init__(self, y: int, x: int, orientation: Orientation, cost: int | float=float('inf')):
        self.y = y
        self.x = x
        self.orientation = orientation
        self.cost: int | float = cost

    def __repr__(self) -> str:
        return f'[{self.y}, {self.x}, Cost: {self.cost}]'
    
    def __eq__(self, other: Self) -> bool:
        if (not isinstance(other, Node)):
            return False
        return (self.y, self.x) == (other.y, other.x)

    def __hash__(self) -> int:
        return hash((self.y, self.x))
    
class Path():
    def __init__(self, path: dict[Node, Node]={}, parent_costs: dict[Node, int] = {}) -> None:
        self.path: dict[Node, Node] = path
        self.parent_costs: dict[Node, int] = parent_costs

    def modify_child(self, parent: Node, child: Node) -> None:
        self.path[parent] = child
        self.parent_costs[parent] = parent.cost

    def get_path(self) -> dict[Node, Node]:
        return self.path

    def copy(self) -> Self:
        return Path(self.path)

    def __getitem__(self, node: Node) -> Node:
        return self.path[node]

    def __contains__(self, node: Node) -> bool:
        return node in self.path
    
    def __repr__(self) -> str:
        return_str: str = ''
        for key, val in self.path.items():
            return_str += f'[{key} -> {val}] '
        return return_str

class RaceTrack():
    def __init__(self, grid: list[str], threshold: int=0) -> None:
        self.grid = [[char for char in line.rstrip()] for line in grid]

        self.starting_node: Node = None
        self.ending_node: Node = None

        self.optimal_path: Path = Path()

        self.threshold = threshold

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if (char == 'S'):
                    self.starting_node = Node(y, x, None, 0)
                elif (char == 'E'):
                    self.ending_node = Node(y, x, None, float('inf'))

    def valid_grid_pos(self, y: int, x: int) -> bool:
        if (not (0 <= y < len(self.grid)) or not (0 <= x < len(self.grid[0]))):
            return False
        elif (self.grid[y][x] == '#'):
            return False
        return True

    def get_next_path_node(self, node: Node) -> Node:  
        next_node: Node = None
        orientations: list[Orientation] = [orientation for orientation in Orientation]
        
        if node.orientation != None:
            orientations = [i for i in orientations if i.value != Orientation.get_opposite(node.orientation).value]

        for orientation in orientations:
            dy: int = orientation.value[0]
            dx: int = orientation.value[1]
            y_prime: int = node.y+dy
            x_prime: int = node.x+dx

            if (self.valid_grid_pos(y_prime, x_prime)):
                next_node = Node(y_prime, x_prime, orientation, node.cost+1)
                if node.orientation == None:
                    node.orientation = Orientation.get_opposite(orientation)

                break

        return next_node
    
    def get_cheating_neighbors(self, node: Node) -> list[Node]:
        deltas: list[tuple[int]] = [(-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0), (1, -1), (0, -2), (-1, -1)]
        neighbors: list[Node] = []
        
        for dy, dx in deltas:
            y_prime: int = node.y+dy
            x_prime: int = node.x+dx

            if (self.valid_grid_pos(y_prime, x_prime)):
                neighbors.append(Node(y_prime, x_prime, None, node.cost+2))
        return neighbors
     
    def find_initial_path(self) -> None:
        open_nodes: list[Node] = [self.starting_node]
        closed: set[Node] = set()

        while open_nodes:
            curr_node: Node = open_nodes.pop(0)
            closed.add(curr_node)
            
            next_node: Node = self.get_next_path_node(curr_node)
            self.optimal_path.modify_child(curr_node, next_node)

            if next_node != None:
                open_nodes.append(next_node)
            else:
                self.ending_node = curr_node

    def cheating_paths(self) -> int:
        count: int = 0
        savings: list[int] = []

        self.find_initial_path()

        for node in self.optimal_path.get_path().keys():
            cheated_nodes: list[Node] = self.get_cheating_neighbors(node)
            cheated_nodes = [new_node for new_node in cheated_nodes if new_node.cost < self.optimal_path.parent_costs[new_node]]
            
            savings.extend([self.optimal_path.parent_costs[new_node] - new_node.cost for new_node in cheated_nodes])

            count += len(cheated_nodes)

        savings.sort()
        savings = [cheat for cheat in savings if cheat >= self.threshold]

        return len(savings)
    
    def upgraded_cheating_neighbors(self, node: Node) -> list[Node]:
        neighbors: list[Node] = []

        for dy in range(-20, 21):
            for dx in range(21-abs(dy)):
                y_prime: int = node.y+dy
                x_prime_1: int = node.x+dx
                x_prime_2: int = node.x-dx

                if (self.valid_grid_pos(y_prime, x_prime_1)):
                    neighbors.append(Node(y_prime, x_prime_1, None, node.cost+abs(dx)+abs(dy)))

                if (self.valid_grid_pos(y_prime, x_prime_2)):
                    neighbors.append(Node(y_prime, x_prime_2, None, node.cost+abs(dx)+abs(dy)))
        
        return neighbors
    
    def upgraded_cheats(self) -> int:
        count: int = 0
        savings: list[int] = []

        self.find_initial_path()

        for node in self.optimal_path.get_path().keys():
            cheated_nodes: list[Node] = list(set(self.upgraded_cheating_neighbors(node)))
            cheated_nodes = [new_node for new_node in cheated_nodes if new_node.cost < self.optimal_path.parent_costs[new_node]]
            
            savings.extend([self.optimal_path.parent_costs[new_node] - new_node.cost for new_node in cheated_nodes])

            count += len(cheated_nodes)

        savings.sort()
        savings = [cheat for cheat in savings if cheat >= self.threshold]

        return len(savings)
    
    def show_optimal_path(self) -> str:
        new_grid: list[list[str]] = []

        for line in self.grid:
            new_grid.append(line.copy())

        self.find_initial_path()

        curr_node: Node = self.starting_node

        while curr_node != None:
            new_grid[curr_node.y][curr_node.x] = 'O'
            curr_node = self.optimal_path[curr_node]

        return f'{self.grid_repr(new_grid)}\nOptimal Cost: {self.ending_node.cost}'

    def grid_repr(self, raw_grid: list[list[str]]) -> str:
        grid_lines: list[str] = [''.join(line) for line in raw_grid]
        grid: str = ''
        grid += '\n'.join(grid_lines)
        return grid
    
    def __repr__(self) -> str:
        return f'Grid:\n{self.grid_repr(self.grid)}'

def main() -> None:
    racetrack: RaceTrack = None
    with open('./inputs/day20/0.txt', 'r') as file:
        contents: list[str] = file.readlines()
        racetrack = RaceTrack(contents, 100)

    print(f'Number of cheats which save at least {racetrack.threshold} picoseconds: {racetrack.cheating_paths()}')
    print(f'Number of 20 picosecond cheats which save at least {racetrack.threshold} picoseconds: {racetrack.upgraded_cheats()}')

if __name__ == '__main__':
    main()