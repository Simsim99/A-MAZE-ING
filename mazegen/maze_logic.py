from collections import deque
from mazegen.models import Cell, check_position, check_coordinates
import random
from typing import Tuple, List, Deque, Set, Dict, Optional


class MazeGenerator:
    """
    A class to generate and manipulate mazes using various algorithms.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
        grid (deque[deque[Cell]]): 2D grid o
        Cell objects representing the maze.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes a MazeGenerator with a grid of unvisited cells.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
        """
        self.width: int = width
        self.height: int = height
        self.grid: Deque[Deque[Cell]] = deque(
            deque(Cell() for i in range(self.width))
            for i in range(self.height)
        )

    def break_wall(self, x: int, y: int, direction: str) -> None:
        """Removes a wall between the specified cell and its neighbor.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
            direction (str): Direction of the wall to break
            ("north", "east", "south", "west").
        """
        if direction == "north":
            if check_coordinates(y - 1, x, self.width, self.height):
                self.grid[y][x].north = 0
                self.grid[y - 1][x].south = 0
        elif direction == "east":
            if check_coordinates(y, x + 1, self.width, self.height):
                self.grid[y][x].east = 0
                self.grid[y][x + 1].west = 0
        elif direction == "south":
            if check_coordinates(y + 1, x, self.width, self.height):
                self.grid[y][x].south = 0
                self.grid[y + 1][x].north = 0
        elif direction == "west":
            if check_coordinates(y, x - 1, self.width, self.height):
                self.grid[y][x].west = 0
                self.grid[y][x - 1].east = 0
        else:
            pass

    def tree_generate(self, the_seed: Optional[str] = None) -> None:
        """Generates a maze using a simple tree-based algorithm.

        Randomly breaks walls in the north or east direction
        to create a spanning tree.

        Args:
            the_seed (str): Seed for the random number generator.
        """
        random.seed(the_seed)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                possible_directions: list[str] = []
                if y > 0:
                    possible_directions.append("north")
                if x < self.width - 1:
                    possible_directions.append("east")
                if possible_directions and self.grid[y][x].visited is False:
                    direction = random.choice(possible_directions)
                    self.break_wall(x, y, direction)

    def aldous_generate(self, the_seed: Optional[str] = None) -> None:
        """Generates a maze using Aldous-Broder algorithm.

        Args:
            the_seed (str): Seed for the random number generator.
        """
        random.seed(the_seed)
        y: int
        x: int
        y, x = (0, 0)
        self.grid[y][x].visited = True
        count: int = 19
        while True:
            directions = check_position(y, x, self.height, self.width)
            where = random.choice(directions)
            if where == "e":
                x += 1
                if not check_coordinates(y, x, self.width, self.height):
                    x -= 1
                    pass
                elif self.grid[y][x].visited is False:
                    self.grid[y][x].visited = True
                    count += 1
                    self.grid[y][x].west = 0
                    self.grid[y][x - 1].east = 0
            elif where == "w":
                x -= 1
                if not check_coordinates(y, x, self.width, self.height):
                    x += 1
                    pass
                elif self.grid[y][x].visited is False:
                    self.grid[y][x].visited = True
                    count += 1
                    self.grid[y][x].east = 0
                    self.grid[y][x + 1].west = 0
            elif where == "n":
                y -= 1
                if not check_coordinates(y, x, self.width, self.height):
                    y += 1
                    pass
                elif self.grid[y][x].visited is False:
                    self.grid[y][x].visited = True
                    count += 1
                    self.grid[y][x].south = 0
                    self.grid[y + 1][x].north = 0
            elif where == "s":
                y += 1
                if not check_coordinates(y, x, self.width, self.height):
                    y -= 1
                    pass
                elif self.grid[y][x].visited is False:
                    self.grid[y][x].visited = True
                    count += 1
                    self.grid[y][x].north = 0
                    self.grid[y - 1][x].south = 0
            if count == self.width * self.height:
                break

    def braid(self, the_seed: Optional[str] = None) -> None:
        """Removes dead-ends in the maze to create loops (braiding).

        Args:
            the_seed (str): Seed for the random number generator.
        """
        random.seed(the_seed)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                standing_walls: List[str] = []
                if not check_coordinates(y, x, self.width, self.height):
                    pass
                else:
                    if cell.north == 1:
                        if y > 0:
                            standing_walls.append("north")
                    if cell.south == 1:
                        if y < self.height - 1:
                            standing_walls.append("south")
                    if cell.east == 1:
                        if x < self.width - 1:
                            standing_walls.append("east")
                    if cell.west == 1:
                        if x > 0:
                            standing_walls.append("west")
                    if len(standing_walls) == 3:
                        direction: str = random.choice(standing_walls)
                        self.break_wall(x, y, direction)

    def get_neighbors(self, x: int, y: int) -> List[tuple[int, int]]:
        """Returns a list of neighboring cells accessible from the given cell.
        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        Returns:
            List[Tuple[int, int]]: List of accessible neighbor coordinates.
        """
        cord_list: List[Tuple[int, int]] = []
        if y > 0 and self.grid[y][x].north == 0:
            cord_list.append((y - 1, x))
        if x > 0 and self.grid[y][x].west == 0:
            cord_list.append((y, x - 1))
        if y < self.height - 1 and self.grid[y][x].south == 0:
            cord_list.append((y + 1, x))
        if x < self.width - 1 and self.grid[y][x].east == 0:
            cord_list.append((y, x + 1))
        return cord_list

    def find_path(self, start_coords: Tuple[int, int],
                  end_coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Finds a path from start to end coordinates using BFS.

        Args:
            start_coords (Tuple[int, int]): Starting cell coordinates.
            end_coords (Tuple[int, int]): Ending cell coordinates.

        Returns:
            List[Tuple[int, int]]: Ordered list of coordinates
            representing the path.
        """
        queue: List[Tuple[int, int]] = [start_coords]
        visited: Set[Tuple[int, int]] = {start_coords}
        parent_map: Dict[Tuple[int, int], Tuple[int, int]] = {}
        while queue:
            current: Tuple[int, int] = queue.pop(0)
            if current == end_coords:
                break
            y, x = current
            neighbors_list: List[Tuple[int, int]] = self.get_neighbors(x, y)
            for i in neighbors_list:
                if i not in visited:
                    visited.add(i)
                    queue.append(i)
                    parent_map[i] = current
        path: List[Tuple[int, int]] = []
        step: Tuple[int, int] = end_coords
        while step in parent_map:
            path.append(step)
            step = parent_map[step]
        path.append(start_coords)
        path.reverse()
        return path

    def directions_path(self, start_coords: Tuple[int, int],
                        end_coords: Tuple[int, int], file_name: str) -> None:
        """Writes directions from start to end coordinates to a file.

        Args:
            start_coords (Tuple[int, int]): Starting coordinates.
            end_coords (Tuple[int, int]): Ending coordinates.
            file_name (str): File path to save directions.
        """
        path: List[Tuple[int, int]] = self.find_path(start_coords, end_coords)
        directions: List[str] = []
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
        with open(file_name, "a") as fd:
            y, x = start_coords
            a, b = end_coords
            clean_directions: str = "".join(directions)
            fd.write(f"{str(y)},{str(x)}\n")
            fd.write(f"{str(a)},{str(b)}\n")
            fd.write(str(clean_directions))

    def hexa_converter(self, file_name: str) -> None:
        """Converts the maze grid to hexadecimal
        representation and writes to a file.
        Args:
            file_name (str): File path to save the hexadecimal maze.
        """
        with open(file_name, "w") as fd:
            for index, row in enumerate(self.grid):
                hex_list: List[str] = []
                for cell in row:
                    lst: List[str] = []
                    binary: str = ""
                    lst.append(str(cell.west))
                    lst.append(str(cell.south))
                    lst.append(str(cell.east))
                    lst.append(str(cell.north))
                    binary = "".join(lst)
                    decimal: int = int(binary, 2)
                    hexadecimal: str = hex(decimal)[2:].upper()
                    hex_list.append(hexadecimal)
                line: str = "".join(hex_list)
                if index == self.height - 1:
                    fd.write(f"{line}\n\n")
                else:
                    fd.write(f"{line}\n")
