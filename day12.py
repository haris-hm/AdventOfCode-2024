class Region():
    def __init__(self, region_id: str, area: int=0, perimeter: int=0) -> None:
        self.region_id = region_id
        self.area = area
        self.perimeter = perimeter

    def get_price(self) -> int:
        return self.area*self.perimeter
    
    def copy(self):
        return Region(self.region_id, self.area, self.perimeter)
    
    def __repr__(self) -> str:
        return f'[ID: {self.region_id}, Area: {self.area}, Perimeter: {self.perimeter}]'
    
class Map():
    def __init__(self, plot_map: list[list[str]]) -> None:
        self.plot_map = plot_map
        self.visited_nodes: set[tuple[int]] = set()
        self.regions: list[Region] = []

    def promising(self, curr_char: str, coord: tuple[int]) -> bool:
        y: int = coord[0]
        x: int = coord[1]

        within_bounds: bool = 0 <= y < len(self.plot_map) and 0 <= x < len(self.plot_map[0])
        not_visited: bool = (y, x) not in self.visited_nodes
        same_id: bool = False

        if (within_bounds):
            same_id = self.plot_map[y][x] == curr_char

        if (same_id and not_visited and within_bounds):
            return True
        else:
            return False
        
    def different_id(self, curr_char: str, coord: tuple[int]) -> bool:
        y: int = coord[0]
        x: int = coord[1]

        within_bounds: bool = 0 <= y < len(self.plot_map) and 0 <= x < len(self.plot_map[0])

        if within_bounds:
            if self.plot_map[y][x] == curr_char:
                return False

        return True

    def identify_region_bounds(self, starting_idx: tuple[int], region: Region) -> Region:
        y: int = starting_idx[0]
        x: int = starting_idx[1]

        curr_char: str = region.region_id
        region.area += 1

        self.visited_nodes.add(starting_idx)

        up: tuple[int] = (y-1, x)
        down: tuple[int] = (y+1, x)
        left: tuple[int] = (y, x-1)
        right: tuple[int] = (y, x+1)

        if (self.promising(curr_char, up)):
            self.identify_region_bounds(up, region)

        if (self.promising(curr_char, down)):
            self.identify_region_bounds(down, region)
        
        if (self.promising(curr_char, left)):
            self.identify_region_bounds(left, region)
        
        if (self.promising(curr_char, right)):
            self.identify_region_bounds(right, region)


        if (self.different_id(curr_char, up)):
            region.perimeter += 1

        if (self.different_id(curr_char, down)):
            region.perimeter += 1

        if (self.different_id(curr_char, left)):
            region.perimeter += 1

        if (self.different_id(curr_char, right)):
            region.perimeter += 1

        return region

    def segment_regions(self) -> int:
        for y, line in enumerate(self.plot_map):
            for x, char in enumerate(line):
                curr_idx: tuple[int] = (y, x)

                if (curr_idx not in self.visited_nodes):
                    curr_region: Region = Region(char)

                    curr_region = self.identify_region_bounds(curr_idx, curr_region)
                    self.regions.append(curr_region)
        
        price_sum: int = 0

        for region in self.regions:
            print(region)
            price_sum += region.get_price()

        return price_sum


def main() -> None:
    plot_map: Map = None
    with open('./inputs/day12/3.txt', 'r') as file:
        contents = file.read().split('\n')
        plot_map = Map([[char for char in line] for line in contents])
    
    price: int = plot_map.segment_regions()
    print(price)

if __name__ == '__main__':
    main()