def node_paths(topo_map: list[list[int]], head_coord: tuple[int], tails_seen: set[tuple[int]]=set()) -> tuple[int | set[tuple[int]]]:
    score: int = 0

    y: int = head_coord[0]
    x: int = head_coord[1]

    curr_weight: int = topo_map[y][x]

    topo_map_height: int = len(topo_map)
    topo_map_width: int = len(topo_map[0])

    if curr_weight == 9:
        tails_seen.add((y, x))
        return 1

    if y+1 < topo_map_height:
        if topo_map[y+1][x] == curr_weight + 1:
            node_paths(topo_map, (y+1, x), tails_seen)
    
    if y-1 >= 0:
        if topo_map[y-1][x] == curr_weight + 1:
            node_paths(topo_map, (y-1, x), tails_seen)

    if x+1 < topo_map_width:
        if topo_map[y][x+1] == curr_weight + 1:
            node_paths(topo_map, (y, x+1), tails_seen)
    
    if x-1 >= 0:
        if topo_map[y][x-1] == curr_weight + 1:
            node_paths(topo_map, (y, x-1), tails_seen)

    # print(head_coord, score)

    return len(tails_seen), tails_seen

def trailhead_ratings(topo_map: list[list[int]], head_coord: tuple[int]) -> int:
    score: int = 0

    y: int = head_coord[0]
    x: int = head_coord[1]

    curr_weight: int = topo_map[y][x]

    topo_map_height: int = len(topo_map)
    topo_map_width: int = len(topo_map[0])

    if curr_weight == 9:
        return 1

    if y+1 < topo_map_height:
        if topo_map[y+1][x] == curr_weight + 1:
            score += trailhead_ratings(topo_map, (y+1, x))
    
    if y-1 >= 0:
        if topo_map[y-1][x] == curr_weight + 1:
            score += trailhead_ratings(topo_map, (y-1, x))

    if x+1 < topo_map_width:
        if topo_map[y][x+1] == curr_weight + 1:
            score += trailhead_ratings(topo_map, (y, x+1))
    
    if x-1 >= 0:
        if topo_map[y][x-1] == curr_weight + 1:
            score += trailhead_ratings(topo_map, (y, x-1))

    return score

def calc_distinct_paths(topo_map: list[list[int]], trailheads: set[tuple[int]]) -> tuple[int]:
    score_sum: int = 0
    rating_sum: int = 0

    for head in trailheads:
        score, tails = node_paths(topo_map, head, set())
        rating = trailhead_ratings(topo_map, head)
        # print(f'{head = } {tails = }, {score = }')
        score_sum += score
        rating_sum += rating

    return score_sum, rating_sum

def main() -> None:
    I = float("inf")
    topo_map: list[list[int]] = []
    trailheads: list[tuple[int]] = []

    with open('./inputs/day10/1.txt', 'r') as file:
        contents = file.read()
        contents: list[str] = contents.split('\n')
        topo_map = [[int(k) for k in i] for i in contents]

        for y, line in enumerate(topo_map):
            for x, num in enumerate(line):
                if num == 0:
                    trailheads.append((y, x))

    score, ratings = calc_distinct_paths(topo_map, trailheads)
    print(f'Score: {score}\nRatings: {ratings}')

if __name__ == '__main__':
    main()