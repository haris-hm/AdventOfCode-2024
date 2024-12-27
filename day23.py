import re

from typing import Self

class ConnectionSubset():
    def __init__(self, connection_set: tuple[str]) -> None:
        self.connections = connection_set

    def __repr__(self) -> str:
        return f'{self.connections[0]}-{self.connections[1]}-{self.connections[2]}'
    
    def __eq__(self, other: Self) -> bool:
        if (not isinstance(other, ConnectionSubset)):
            return False
        return set(self.connections) == set(other.connections)

    def __hash__(self) -> int:
        return hash(sum([ord(i[0]) * ord(i[1]) for i in self.connections]))

class Connection():
    def __init__(self, name: str, init_connections: list[str]) -> None:
        self.computer_name = name
        self.connected_computers: set[str] = set()

        for connection in init_connections:
            self.add_connection(connection)

    def is_connected(self, name: str) -> bool:
        if name in self.connected_computers:
            return True
        return False

    def add_connection(self, name: str) -> None:
        self.connected_computers.add(name)

    def all_subsets(self, graph) -> list[ConnectionSubset]:
        connections: list[str] = list(self.connected_computers)
        subsets: list[tuple[int]] = []

        for i, name in enumerate(connections):
            for k in range(i+1, len(connections)):
                second_name: str = connections[k]
                first_connection: Self = graph.get_connection(name)
                second_connection: Self = graph.get_connection(second_name)
                print(first_connection, second_connection)

                if first_connection == None or second_connection == None:
                    continue

                if first_connection.is_connected(second_name) and second_connection.is_connected(name):
                    subsets.append(ConnectionSubset((self.computer_name, name, second_name)))

        return subsets

    def __repr__(self) -> str:
        return f'{self.computer_name}: {self.connected_computers}'
    
class LANGraph():
    def __init__(self) -> None:
        self.connections: list[Connection] = []

    def get_connection(self, name: str) -> Connection:
        connection: list[Connection] = [i for i in self.connections if i.computer_name == name]
        if len(connection) > 0:
            return connection[0]
        else:
            return None

    def filtered(self, key: str) -> Self:
        new_graph: Self = LANGraph()
        new_graph.connections = [i for i in self.connections if re.search(f'^{key}', i.computer_name) != None]
        return new_graph
    
    def __getitem__(self, key: int) -> Connection:
        return self.connections[key]

    def __repr__(self) -> str:
        output: str = ''
        for i in [str(connection) + '\n' for connection in self.connections]:
            output += i

        return output

def main() -> None:
    lan_graph: LANGraph = LANGraph()

    with open('./inputs/day23/0.txt', 'r') as file:
        contents: list[str] = [line.rstrip() for line in file.readlines()]

        connections: dict[str, Connection] = {}
        raw_connections: list[list[str]] = [line.split('-') for line in contents]
        
        for x, y in raw_connections:
            if x in connections:
                connections[x].add_connection(y)
            else:
                connections[x] = Connection(x, [y])
            
            if y in connections:
                connections[y].add_connection(x)
            else:
                connections[y] = Connection(y, [x])

        for val in connections.values():
            lan_graph.connections.append(val)

    filtered_graph: LANGraph = lan_graph.filtered('t')
    subsets: list[ConnectionSubset] = []

    for connection in filtered_graph:
        subsets.extend(connection.all_subsets(lan_graph))

    print(list(set(subsets)))
    print(len(set(subsets)))

if __name__ == '__main__':
    main()