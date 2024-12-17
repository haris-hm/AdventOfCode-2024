from collections import defaultdict
import heapq
from typing import Self

class Node():
    def __init__(self, y: int, x: int, direction: str='E') -> None:
        self.y = y
        self.x = x
        self.direction = direction

    def __lt__(self, other: Self) -> bool:
        return (self.y, self.x) < (other.y, other.x)
    
    def __repr__(self) -> str:
        return f'[({self.y}, {self.x}) | {self.direction}]'
    
    def __hash__(self) -> int:
        return hash(self.x*self.y*ord(self.direction[0]))

class Graph():
    def __init__(self, grid: list[list[str]]) -> None:
        self.adjacency_list: dict[Node, tuple[Node | int]] = defaultdict(list)

        self.grid = grid
        self.starting_node: Node = None
        self.ending_node: Node = None

    def add_node(self, src: Node, dest: Node, weight: int) -> None:
        self.adjacency_list[src].insert(0, (dest, weight))

    def find_adjacent_nodes(self, src: Node) -> None:
        count: int = 1
        for x in range(src.x+1, len(self.grid)):
            if (self.grid[src.y][x] == '#'):
                break
            elif (self.grid[src.y+1][x] == '.' or self.grid[src.y-1][x] == '.'):
                direction_multiplier: int = 1000 if src.direction != 'E' else 0
                weight: int = count + direction_multiplier
                self.add_node(src, Node(src.y, x, 'E'), weight)
                break
            count += 1

        count = 1
        for x in range(src.x-1, 0, -1):
            if (self.grid[src.y][x] == '#'):
                break
            elif (self.grid[src.y+1][x] == '.' or self.grid[src.y-1][x] == '.'):
                direction_multiplier: int = 1000 if src.direction != 'W' else 0
                weight: int = count + direction_multiplier
                self.add_node(src, Node(src.y, x, 'W'), weight)
                break
            count += 1

        count = 1
        for y in range(src.y+1, len(self.grid)):
            if (self.grid[y][src.x] == '#'):
                break
            elif (self.grid[y][src.x+1] == '.' or self.grid[y][src.x-1] == '.'):
                direction_multiplier: int = 1000 if src.direction != 'S' else 0
                weight: int = count + direction_multiplier
                self.add_node(src, Node(y, src.x, 'S'), weight)
                break
            count += 1

        count = 1
        for y in range(src.y-1, 0, -1):
            if (self.grid[y][src.x] == '#'):
                break
            elif (self.grid[y][src.x+1] == '.' or self.grid[y][src.x-1] == '.'):
                direction_multiplier: int = 1000 if src.direction != 'N' else 0
                weight: int = count + direction_multiplier
                self.add_node(src, Node(y, src.x, 'N'), weight)
                break
            count += 1

    def dijkstra(self) -> int:
        pq: heapq = []
        heapq.heappush(pq, (0, 0))

        distances: dict[Node, int] = {self.starting_node: 0}
        visited: set[Node] = set()

        nodes: dict[int, Node] = {0: self.starting_node}
        curr_node_idx: int = 1

        while pq:
            curr_dist, curr_node_key = heapq.heappop(pq)
            curr_node: Node = nodes[curr_node_key]

            if (curr_node in visited):
                continue
            visited.add(curr_node)

            self.find_adjacent_nodes(curr_node)

            if (len(self.adjacency_list[curr_node]) == 0):
                continue

            for neighbor, weight in self.adjacency_list[curr_node]:
                if (neighbor in visited):
                    continue

                new_dist = curr_dist + weight

                if (new_dist < distances.get(neighbor, float('inf'))):
                    distances[neighbor] = new_dist
                    nodes[curr_node_idx] = neighbor
                    heapq.heappush(pq, (new_dist, curr_node_idx))
                    curr_node_idx += 1
        
        return distances

    def __repr__(self) -> str:
        grid_lines: list[str] = [''.join(line) for line in self.grid]
        grid: str = '\n'.join(grid_lines)

        return f'Graph:\n   Vertices: {self.adjacency_list}\n   Starting Node: {self.starting_node}\n   Ending Node: {self.ending_node}\n   Grid:\n{grid}'
        
def main() -> None:
    graph: Graph = None
    with open('./inputs/day16/0.txt', 'r') as file:
        contents = file.read()
        grid: list[list[str]] = [[char for char in line] for line in contents.split('\n')]
        graph = Graph(grid)

        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                if (char == 'S'):
                    graph.starting_node = Node(y, x, 'E')
                elif (char == 'E'):
                    graph.ending_node = Node(y, x)

    print(graph)
    print(graph.dijkstra())
    print(graph)

if __name__ == '__main__':
    main()