class Graph():
    def __init__(self, nodes: list[list[int]]) -> None:
        pass

def main() -> None:
    I = float("inf")
    adjacency_matrix: list[list[str]] = []

    with open('./inputs/day10/2.txt', 'r') as file:
        contents = file.read()
        contents: list[str] = contents.split('\n')
        adjacency_matrix = [[I] * len(contents)*len(contents[0])] * len(contents)*len(contents[0])
        coord_idx: dict[tuple[int], int] = {}

        curr_idx: int = 0
        for i, line in enumerate(contents):
            for k, char in enumerate(line):
                coord_idx[(i, k)] = curr_idx
                curr_idx += 1

        for i, line in enumerate(contents):
            for k, char in enumerate(line):
                adjacency_matrix[coord_idx[(i, k)]][coord_idx[(i, k)]] = I

                if k+1 < len(line):
                    adjacency_matrix[coord_idx[(i, k)]][coord_idx[(i, k+1)]] = int(contents[i][k+1])
                if k-1 >= 0:
                    adjacency_matrix[coord_idx[(i, k)]][coord_idx[(i, k-1)]] = int(contents[i][k-1])

                if i+1 < len(contents):
                    adjacency_matrix[coord_idx[(i, k)]][coord_idx[(i+1, k)]] = int(contents[i+1][k])
                if i-1 >= 0:
                    adjacency_matrix[coord_idx[(i, k)]][coord_idx[(i-1, k)]] = int(contents[i-1][k])
                
        for i in adjacency_matrix:
            print(i)

        print(coord_idx)

if __name__ == '__main__':
    main()