from collections import deque

class DiskBlock():
    def __init__(self, starting_idx: int, size: int) -> None:
        self.starting_idx = starting_idx
        self.size = size

    def __lt__(self, other) -> bool:
        if other.starting_idx > self.starting_idx:
            return True
        else:
            False

    def __repr__(self) -> str:
        return f'[Starting IDX = {self.starting_idx}, Size = {self.size}]'

class ExpandedDiskMap():
    def __init__(self, disk_map: str) -> None:
        self.disk_map: list[int | None] = []
        self.free_space_queue: list[int] = []
        self.free_block_queue: list[DiskBlock] = []
        self.free_blocks_available: set[int] = set()
        self.file_queue: deque[DiskBlock] = deque()
        self.curr_id: int = 0
        self.free_amount: int = 0

        for i, char in enumerate(disk_map):
            curr_num: int = int(char)
            if i % 2 == 0:
                self.add_file(curr_num)
            else:
                self.add_free_space(curr_num)

    def add_file(self, size: int) -> None:
        starting_idx: int = len(self.disk_map) + size - 1

        for _ in range(size):
            self.disk_map.append(self.curr_id)

        self.file_queue.append(DiskBlock(starting_idx, size))
        self.curr_id += 1

    def add_free_space(self, size: int) -> None:
        starting_idx: int = len(self.disk_map)
        for _ in range(size):
            curr_idx: int = len(self.disk_map)
            self.free_amount += 1
            self.free_space_queue.append(curr_idx)
            self.disk_map.append(None)

        self.free_block_queue.append(DiskBlock(starting_idx, size))
        self.free_blocks_available.add(size)

    def compact_files(self, output: bool=False) -> None:
        i: int = 1
        curr_file: DiskBlock = self.file_queue.pop()
        disk_map_idx: int = curr_file.starting_idx
        curr_file_id: int = self.disk_map[disk_map_idx]

        print(self) if output else None

        while i < self.free_amount:
            if disk_map_idx < curr_file.size:
                curr_file = self.file_queue.pop()
                disk_map_idx = curr_file.starting_idx
                curr_file_id = self.disk_map[disk_map_idx]
            elif self.disk_map[disk_map_idx] != curr_file_id:

                curr_file = self.file_queue.pop()
                disk_map_idx = curr_file.starting_idx
                curr_file_id = self.disk_map[disk_map_idx]
                
            curr_free_space_idx: int = self.free_space_queue.pop(0)

            if curr_free_space_idx > disk_map_idx:
                break

            self.disk_map[curr_free_space_idx] = curr_file_id

            self.disk_map[disk_map_idx] = None
            self.free_space_queue.append(disk_map_idx)
            self.free_space_queue.sort()

            print(self) if output else None

            disk_map_idx -= 1
            i += 1

    def defrag_compact(self, output: bool=False) -> None:
        i: int = 1
        curr_file: DiskBlock = None
        file_idx: int = None
        curr_file_id: int = None

        print(self) if output else None

        while i < self.free_amount:
            curr_file: DiskBlock = self.file_queue.pop()
            file_idx: int = curr_file.starting_idx
            curr_file_id: int = self.disk_map[file_idx]

            # print(f'{curr_file = }', f'{curr_file_id = }')

            free_block_idx: int = 0
            free_block: DiskBlock = None

            for k, block in enumerate(self.free_block_queue):
                if block.size >= curr_file.size:
                    free_block = self.free_block_queue.pop(k)
                    free_block_idx = free_block.starting_idx
                    break

            if free_block == None:
                continue

            self.free_block_queue.append(DiskBlock(file_idx, curr_file.size))
            if free_block_idx + curr_file.size < free_block_idx + free_block.size:
                self.free_block_queue.insert(0, DiskBlock(free_block_idx + curr_file.size, free_block.size-curr_file.size))
            self.free_block_queue.sort()
            
            for k in range(curr_file.size):
                # print(self)
                self.disk_map[free_block_idx + k] = curr_file_id
                self.disk_map[file_idx + k - 2] = None

            print(self) if output else None
            # print(self.free_block_queue)

            i += 1
    
    def checksum(self) -> int:
        sum: int = 0
        for i, val in enumerate(self.disk_map): 
            if val == None:
                continue

            sum += i*val

        return sum
    
    def save_output(self, output_path: str) -> None:
        f = open(output_path, 'w')
        f.write(str(self))
        f.close()

    def __repr__(self) -> str:
        return_str: str = ''

        for i in self.disk_map:
            if i == None:
                return_str += '.'
            elif len(str(i)) > 1:
                return_str += f'[{str(i)}]'
            else:
                return_str += f'{str(i)}'

        return return_str

def main() -> None:
    disk_map: str = ''

    with open('./inputs/day09/0.txt', 'r') as file:
        disk_map = file.read()

    expanded_disk_map: ExpandedDiskMap = ExpandedDiskMap(disk_map)
    print(f'Expanded Disk Map: {expanded_disk_map}')
    expanded_disk_map.defrag_compact(output=True)
    expanded_disk_map.save_output('./inputs/day09/1out.txt')
    print(f'Compacted Disk Map: {expanded_disk_map}')
    print(f'Checksum: {expanded_disk_map.checksum()}')

    expanded_disk_map: ExpandedDiskMap = ExpandedDiskMap('12345')
    print(f'Expanded Disk Map: {expanded_disk_map}')
    expanded_disk_map.compact_files()
    # expanded_disk_map.save_output('./inputs/day09/1out.txt')
    print(f'Compacted Disk Map: {expanded_disk_map}')
    print(f'Checksum: {expanded_disk_map.checksum()}')

if __name__ == '__main__':
    main()