from collections import deque
from models import Cell, check_position, check_grid
import random


class MazeGenerator():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = deque(
            deque(Cell() for i in range(self.width))
            for i in range(self.height)
        )

    def break_wall(self, x, y, direction: str):
        if direction == "north":
            self.grid[y][x].north = 0
            self.grid[y - 1][x].south = 0 
        elif direction == "east":
            self.grid[y][x].east = 0
            self.grid[y][x + 1].west = 0
        elif direction == "south":
            self.grid[y][x].south = 0
            self.grid[y + 1][x].north = 0
        elif direction == "west":
            self.grid[y][x].west = 0
            self.grid[y][x - 1].east = 0

    def tree_generate(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                possible_directions : list[str] = []
                if y > 0:
                    possible_directions.append("north")
                if x < self.width - 1:
                    possible_directions.append("east")
                if possible_directions:
                    direction = random.choice(possible_directions)
                    self.break_wall(x, y, direction)
    
    def aldous_generate(self):
        y, x = (0, 0)
        self.grid[y][x].visited = True
        while True:
            directions = check_position(y, x, self.height, self.width)
            where = random.choice(directions)
            if where == "e":
                x += 1
                if self.grid[y][x].visited == False: 
                    self.grid[y][x].visited = True
                    self.grid[y][x].west = 0
                    self.grid[y][x - 1].east = 0
            if where == "w":
                x -= 1
                if self.grid[y][x].visited == False: 
                    self.grid[y][x].visited = True
                    self.grid[y][x].east = 0
                    self.grid[y][x + 1].west = 0
            if where == "n":
                y -= 1
                if self.grid[y][x].visited == False: 
                    self.grid[y][x].visited = True
                    self.grid[y][x].south = 0
                    self.grid[y + 1][x].north = 0
            if where == "s":
                y += 1
                if self.grid[y][x].visited == False: 
                    self.grid[y][x].visited = True
                    self.grid[y][x].north = 0
                    self.grid[y - 1][x].south = 0
            if check_grid(self.grid) is True:
                break

    def braid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                standing_walls = []
                if cell.north == 1:
                    if y > 0:
                        standing_walls.append("north")
                if cell.south ==1:
                    if y < self.height - 1:
                        standing_walls.append("south")
                if cell.east == 1:
                    if x < self.width - 1:
                        standing_walls.append("east")
                if cell.west == 1:
                    if x > 0:
                        standing_walls.append("west")
                if len(standing_walls) == 3:
                    direction = random.choice(standing_walls)
                    self.break_wall(x, y ,direction)

    def get_neighbors(self, x, y):
        cord_list = []
        if y > 0 and self.grid[y][x].north == 0:
            cord_list.append((y - 1, x))
        if x > 0 and self.grid[y][x].west == 0:
            cord_list.append((y, x - 1))
        if y < self.height- 1 and self.grid[y][x].south == 0:
            cord_list.append((y + 1, x))
        if x < self.width- 1 and self.grid[y][x].east == 0:
            cord_list.append((y, x + 1))
        return (cord_list)

    def find_path(self, start_coords, end_coords):
        queue = [start_coords]
        visited = {start_coords}
        parent_map = {}
        while queue:
            current = queue.pop(0)
            if current == end_coords:
                break
            y, x = current
            neighbors_list = (self.get_neighbors(x, y))
            for i in neighbors_list:
                if i not in visited:
                    visited.add(i)
                    queue.append(i)
                    parent_map[i]= current
        path = []
        step = end_coords
        while step in parent_map:
            path.append(step)
            step = parent_map[step]
        path.append(start_coords)
        path.reverse()
        return (path)
    
    def directions_path(self, start_coords, end_coords):
        path = self.find_path(start_coords, end_coords)
        directions = []
        for index, i in enumerate(path):
            if index == len(path) - 1:
                break
            c_y, c_x = path[index]
            n_y, n_x = path[index + 1]
            if c_y > n_y and c_x == n_x:
                directions.append("N")
            elif c_y < n_y and c_x == n_x:
                directions.append("S")
            elif c_y == n_y and c_x > n_x:
                directions.append("W")
            elif c_y == n_y and c_x < n_x:
                directions.append("E")
            
        with open("output.txt", "a") as fd:
            y, x = start_coords
            a, b = end_coords
            clean_directions = "".join(directions)
            fd.write(f"{str(y)},{str(x)}\n")
            fd.write(f"{str(a)},{str(b)}\n")
            fd.write(str(clean_directions))

    def hexa_converter(self):
        with open("output.txt", "w") as fd:
            for index,row in enumerate(self.grid):
                hex_list = []
                for cell in row:
                    lst = []
                    binary = ""
                    lst.append(str(cell.west))
                    lst.append(str(cell.south))
                    lst.append(str(cell.east))
                    lst.append(str(cell.north))
                    binary = "".join(lst)
                    decimal = int(binary, 2)
                    hexadecimal = hex(decimal)[2:].upper()
                    hex_list.append(hexadecimal)
                line = "".join(hex_list)
                if index == self.height - 1:
                    fd.write(f"{line}\n\n")
                else:
                    fd.write(f"{line}\n")



