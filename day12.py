class Region():
    def __init__(self, region_id: str, area: int=0, perimeter: int=0, sides: int=0) -> None:
        self.region_id = region_id
        self.area = area
        self.perimeter = perimeter
        self.sides = sides

        self.sides_above: list[tuple[int]] = []
        self.sides_on_right: list[tuple[int]] = []
        self.sides_below: list[tuple[int]] = []
        self.sides_on_left: list[tuple[int]] = []

    def calculate_sub_sides(self, sides: list[tuple[int]], axis_key: int, val_key: int) -> int:
        same_side: bool = False
        side_count: int = 0

        for i, val in enumerate(sides):
            if not same_side:
                side_count += 1

            if i == len(sides) - 1:
                break

            if sides[i+1][axis_key] == val[axis_key] and \
                (sides[i+1][val_key] == val[val_key] + 1 or sides[i+1][val_key] == val[val_key]):
                same_side = True
            else:
                same_side = False

        return side_count

    def calculate_sides(self) -> int:
        sorted_up_sides: list[tuple[int]] = sorted(list(self.sides_above), key = lambda x: (x[0], x[1]))
        sorted_right_sides: list[tuple[int]] = sorted(list(self.sides_on_right), key = lambda x: (x[1], x[0]))
        sorted_down_sides: list[tuple[int]] = sorted(list(self.sides_below), key = lambda x: (x[0], x[1]))
        sorted_left_sides: list[tuple[int]] = sorted(list(self.sides_on_left), key = lambda x: (x[1], x[0]))

        # print(f'{sorted_up_sides = }\n{sorted_right_sides = }\n{sorted_down_sides = }\n{sorted_left_sides = }\n')

        up_side_count: int = self.calculate_sub_sides(sorted_up_sides, 0, 1)
        right_side_count: int = self.calculate_sub_sides(sorted_right_sides, 1, 0)
        down_side_count: int = self.calculate_sub_sides(sorted_down_sides, 0, 1)
        left_side_count: int = self.calculate_sub_sides(sorted_left_sides, 1, 0)

        return (up_side_count + right_side_count + down_side_count + left_side_count)

    def get_price(self) -> int:
        return self.area*self.perimeter
    
    def get_bulk_price(self) -> int:
        return self.area*self.calculate_sides()
    
    def copy(self):
        return Region(self.region_id, self.area, self.perimeter)
    
    def __repr__(self) -> str:
        return f'[ID: {self.region_id}, Area: {self.area}, Perimeter: {self.perimeter}, Sides: {12}]'
    
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

        # Area calculation
        if (self.promising(curr_char, up)):
            self.identify_region_bounds(up, region)

        if (self.promising(curr_char, down)):
            self.identify_region_bounds(down, region)
        
        if (self.promising(curr_char, left)):
            self.identify_region_bounds(left, region)
        
        if (self.promising(curr_char, right)):
            self.identify_region_bounds(right, region)

        # Perimeter and Sides Calculation
        if (self.different_id(curr_char, up)):
            region.perimeter += 1
            region.sides_above.append(up)

        if (self.different_id(curr_char, down)):
            region.perimeter += 1
            region.sides_below.append(down)

        if (self.different_id(curr_char, left)):
            region.perimeter += 1
            region.sides_on_left.append(left)

        if (self.different_id(curr_char, right)):
            region.perimeter += 1
            region.sides_on_right.append(right)

        return region

    def segment_regions(self):
        for y, line in enumerate(self.plot_map):
            for x, char in enumerate(line):
                curr_idx: tuple[int] = (y, x)

                if (curr_idx not in self.visited_nodes):
                    curr_region: Region = Region(char)

                    curr_region = self.identify_region_bounds(curr_idx, curr_region)
                    self.regions.append(curr_region)
        return self
    
    def get_full_price(self, bulk: bool=False, output: bool=False) -> int:
        price_sum: int = 0

        for region in self.regions:
            print(region) if output else None
            price_sum += region.get_bulk_price() if bulk else region.get_price()

        return price_sum

def main() -> None:
    plot_map: Map = None
    with open('./inputs/day12/3.txt', 'r') as file:
        contents = file.read().split('\n')
        plot_map = Map([[char for char in line] for line in contents])
    
    plot_map.segment_regions()
    print(f'Normal price: {plot_map.get_full_price()}\nBulk price: {plot_map.get_full_price(bulk=True, output=True)}')

if __name__ == '__main__':
    main()