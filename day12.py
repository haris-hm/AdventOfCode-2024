class Region():
    def __init__(self, region_id: str, area: int=0, perimeter: int=0, sides: int=0) -> None:
        self.region_id = region_id
        self.area = area
        self.perimeter = perimeter
        self.sides = sides

        self.row_sides_visited: set[tuple[int]] = []
        self.column_sides_visited: set[tuple[int]] = []

    def add_horizontal_side(self, coord: tuple[int]) -> None:
        self.row_sides_visited.append(coord)

    def add_vertical_side(self, coord: tuple[int]) -> None:
        self.column_sides_visited.append(coord)

    def calculate_sides(self) -> int:
        sorted_row_sides: list[tuple[int]] = sorted(list(self.row_sides_visited), key = lambda x: (x[0], x[1]))
        sorted_column_sides: list[tuple[int]] = sorted(list(self.column_sides_visited), key = lambda x: (x[1], x[0]))

        row_sides: int = 0
        column_sides: int = 0

        curr_row_val: int = None
        i: int = 0

        while i < len(sorted_row_sides) - 1:
            same_side: bool = True
            marked_side: bool = False
            curr_row_val = sorted_row_sides[i][0] 
            curr_col_val = sorted_row_sides[i][1] 
            
            while same_side and i < len(sorted_row_sides) - 1:
                if sorted_row_sides[i+1][0] == curr_row_val and sorted_row_sides[i+1][1] == curr_col_val+1:
                    if not marked_side:
                        row_sides += 1
                        marked_side = True
                else:
                    same_side = False
                
                i+= 1

        curr_row_val: int = None
        i = 0

        while i < len(sorted_column_sides) - 1:
            same_side: bool = True
            marked_side: bool = False
            curr_row_val = sorted_column_sides[i][0] 
            curr_col_val = sorted_column_sides[i][1] 
            
            while same_side and i < len(sorted_row_sides) - 1:
                if sorted_column_sides[i+1][1] == curr_col_val and sorted_column_sides[i+1][0] == curr_row_val+1:
                    if not marked_side:
                        row_sides += 1
                        marked_side = True
                else:
                    same_side = False
                
                i+= 1


        return row_sides + column_sides

    def get_price(self) -> int:
        return self.area*self.perimeter
    
    def get_bulk_price(self) -> int:
        return self.area*self.sides
    
    def copy(self):
        return Region(self.region_id, self.area, self.perimeter)
    
    def __repr__(self) -> str:
        return f'[ID: {self.region_id}, Area: {self.area}, Perimeter: {self.perimeter}, Sides: {self.calculate_sides()}]'
    
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
            region.add_horizontal_side(up)

        if (self.different_id(curr_char, down)):
            region.perimeter += 1
            region.add_horizontal_side(down)

        if (self.different_id(curr_char, left)):
            region.perimeter += 1
            region.add_vertical_side(left)

        if (self.different_id(curr_char, right)):
            region.perimeter += 1
            region.add_vertical_side(right)

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
    with open('./inputs/day12/2.txt', 'r') as file:
        contents = file.read().split('\n')
        plot_map = Map([[char for char in line] for line in contents])
    
    plot_map.segment_regions()
    print(f'Normal price: {plot_map.get_full_price()}\nBulk price: {plot_map.get_full_price(bulk=True, output=True)}')

if __name__ == '__main__':
    main()