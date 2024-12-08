class Frequency:
    dimensions: int = 0

    def __init__(self) -> None:
        self.nodes: list[tuple[int]] = []

    def __repr__(self) -> str:
        return str(self.nodes)

    def calc_antinodes(self) -> list[tuple[int]]:
        nodes_left: list[tuple[int]] = self.nodes.copy()
        antinodes: list[tuple[int]] = []

        while len(nodes_left) > 0:
            first_node = nodes_left.pop(0)

            for second_node in self.nodes:
                if first_node == second_node:
                    continue

                first_node_diff_x: int = second_node[0] - first_node[0]
                first_node_diff_y: int = second_node[1] - first_node[1]

                for i in range(0, round(self.dimensions/first_node_diff_y)):
                    first_antinode = (second_node[0] + i*first_node_diff_x, second_node[1] + i*first_node_diff_y)
                    antinodes.append(first_antinode)

                second_node_diff_x: int = first_node[0] - second_node[0]
                second_node_diff_y: int = first_node[1] - second_node[1]

                for i in range(0, round(self.dimensions/second_node_diff_y*2)):
                    second_antinode = (first_node[0] - i*second_node_diff_x, first_node[1] - i*second_node_diff_y)     
                    antinodes.append(second_antinode)

        antinodes = filter(lambda x: 0 <= x[0] <= self.dimensions and 0 <= x[1] <= self.dimensions, antinodes)

        return list(antinodes)
    
def display_map(antennae_map: list[str], antinodes: list[tuple[int]]) -> None:
    antennae_map = antennae_map.copy()
    for i, line in enumerate(antennae_map):
        antennae_map[i] = list(line)

    for i in antinodes:
        if antennae_map[i[1]][i[0]] == '.':
            antennae_map[i[1]][i[0]] = '#'
        else:
            antennae_map[i[1]][i[0]] = antennae_map[i[1]][i[0]] + u'\u0301'

    for i, line in enumerate(antennae_map):
        antennae_map[i] = ''.join(line)
        print(antennae_map[i])

def calc_all_antinodes(antennae: dict[str, Frequency], antennae_map: list[str], display: bool=True) -> int:
    antinodes: set[tuple[int]] = set()

    for freq in antennae.values():
        freq_antinodes = freq.calc_antinodes()

        for i in freq_antinodes:
            antinodes.add(i)

    display_map(antennae_map, list(antinodes)) if display else None

    return len(antinodes)        

def main() -> None:
    antennae: dict[str, Frequency] = {}
    contents: list[str] = []

    with open('./inputs/day08/1.txt', 'r') as file:
        contents = file.read()
        contents = contents.split('\n')

        for i, line in enumerate(contents):
            for k, char in enumerate(line):
                if char != '.':
                    if char not in antennae.keys():
                        antennae[char] = Frequency()
                    antennae[char].nodes.append((k, i))
                    antennae[char].dimensions = len(contents) - 1

    print('Frequencies & Nodes:')
    for key, val in antennae.items():
        print(f"'{key}: {val}")

    print(f'\n\nUnique Antinodes: {calc_all_antinodes(antennae, contents)}')

if __name__ == '__main__':
    main()