from pydantic import BaseModel
import curses
from typing import List, Deque, Tuple


class Cell(BaseModel):
    """
    Represents a single cell in the maze.

    Attributes:
        north (int): North wall (1 = closed, 0 = open).
        south (int): South wall (1 = closed, 0 = open).
        west (int): West wall (1 = closed, 0 = open).
        east (int): East wall (1 = closed, 0 = open).
        visited (bool): Whether the cell has been visited.
        last (int): Marker for rendering or path logic.
    """
    north: int = 1
    south: int = 1
    west: int = 1
    east: int = 1
    visited: bool = False
    last: int = 1


def check_position(y: int, x: int, height: int, width: int) -> List[str]:
    """
    Determines valid movement directions from a given cell.

    Directions are constrained based on the cell's position
    within the maze boundaries.

    Args:
        y (int): Y-coordinate of the cell.
        x (int): X-coordinate of the cell.
        height (int): Height of the maze.
        width (int): Width of the maze.

    Returns:
        List[str]: List of allowed directions
        ("n", "s", "e", "w").
    """
    diractions: List[str] = ["e", "n", "s", "w"]
    if x == width - 1 and y == 0:
        diractions = ["s", "w"]
    elif x == 0 and y == 0:
        diractions = ["e", "s"]
    elif x == 0 and y == height - 1:
        diractions = ["n", "e"]
    elif x == width - 1 and y == height - 1:
        diractions = ["n", "w"]
    elif x == width - 1:
        diractions = ["n", "s", "w"]
    elif x == 0:
        diractions = ["n", "s", "e"]
    elif y == 0:
        diractions = ["s", "e", "w"]
    elif y == height - 1:
        diractions = ["n", "e", "w"]
    return diractions


def check_grid(grid: Deque[Deque[Cell]]) -> bool:
    """
    Checks whether all cells in the maze grid have been visited.

    Args:
        grid (Deque[Deque[Cell]]): 2D grid of maze cells.

    Returns:
        bool: True if all cells are visited, False otherwise.
    """
    for row in grid:
        for cell in row:
            if cell.visited is False:
                return False
    return True


def check_coordinates(y: int, x: int, width: int, hight: int) -> bool:
    """
    Determines whether a coordinate is allowed (not part of
    the blocked central pattern).

    Args:
        y (int): Y-coordinate.
        x (int): X-coordinate.
        width (int): Maze width.
        hight (int): Maze height.

    Returns:
        bool: False if the coordinate is blocked, True otherwise.
    """
    x_s: int = int(width / 2) - int(7 / 2)
    y_s: int = int(hight / 2) - int(5 / 2)
    close: List[Tuple[int, int]] = [
        (y_s, x_s),
        (y_s, x_s + 4),
        (y_s, x_s + 5),
        (y_s, x_s + 6),
        (y_s + 1, x_s),
        (y_s + 1, x_s + 6),
        (y_s + 2, x_s),
        (y_s + 2, x_s + 1),
        (y_s + 2, x_s + 2),
        (y_s + 2, x_s + 4),
        (y_s + 2, x_s + 5),
        (y_s + 2, x_s + 6),
        (y_s + 3, x_s + 2),
        (y_s + 3, x_s + 4),
        (y_s + 4, x_s + 2),
        (y_s + 4, x_s + 4),
        (y_s + 4, x_s + 5),
        (y_s + 4, x_s + 6),
    ]
    if (y, x) in close:
        return False
    return True


def include_42_tree(width: int, height: int,
                    grid: Deque[Deque[Cell]]) -> None:
    """
    Embeds a predefined '42' pattern into the maze for tree-based generation.

    This function marks specific cells as visited and opens walls
    to form the pattern.

    Args:
        maze (MazeGenerator): Maze instance to modify.
    """
    x_s: int = int(width / 2) - int(7 / 2)
    y_s: int = int(height / 2) - int(5 / 2)
    close: List[Tuple[int, int]] = [
        (y_s, x_s),
        (y_s, x_s + 4),
        (y_s, x_s + 5),
        (y_s, x_s + 6),
        (y_s + 1, x_s),
        (y_s + 1, x_s + 6),
        (y_s + 2, x_s),
        (y_s + 2, x_s + 1),
        (y_s + 2, x_s + 2),
        (y_s + 2, x_s + 4),
        (y_s + 2, x_s + 5),
        (y_s + 2, x_s + 6),
        (y_s + 3, x_s + 2),
        (y_s + 3, x_s + 4),
        (y_s + 4, x_s + 2),
        (y_s + 4, x_s + 4),
        (y_s + 4, x_s + 5),
        (y_s + 4, x_s + 6),
    ]
    open_north: List[Tuple[int, int]] = [
        (y_s, x_s - 1),
        (y_s + 1, x_s - 1),
        (y_s + 2, x_s - 1),
        (y_s, x_s + 3),
        (y_s + 4, x_s + 1),
        (y_s + 2, x_s + 3),
        (y_s + 3, x_s + 3),
        (y_s + 4, x_s + 3),
        (y_s + 3, x_s - 1),
        (y_s + 1, x_s + 3),
        (y_s + 5, x_s + 1),
    ]
    open_east: List[Tuple[int, int]] = [
        (y_s + 3, x_s),
        (y_s + 3, x_s + 5),
        (y_s + 3, x_s + 6),
        (y_s + 5, x_s + 4),
        (y_s + 5, x_s + 5),
        (y_s + 5, x_s + 6),
        (y_s + 5, x_s + 4),
        (y_s + 1, x_s + 3),
        (y_s + 1, x_s + 4),
        (y_s + 5, x_s + 3),
        (y_s + 4, x_s - 1),
        (y_s + 3, x_s - 1),
        (y_s + 5, x_s + 2),
    ]
    open_west: List[Tuple[int, int]] = [
        (y_s + 3, x_s + 1),
        (y_s + 1, x_s + 5)]
    for coordinates in close:
        y, x = coordinates
        grid[y][x].visited = True
    for coordinates in open_north:
        y, x = coordinates
        grid[y][x].north = 0
        grid[y][x].visited = True
        grid[y - 1][x].south = 0
    for coordinates in open_east:
        y, x = coordinates
        grid[y][x].east = 0
        grid[y][x].visited = True
        grid[y][x + 1].west = 0
    for coordinates in open_west:
        y, x = coordinates
        grid[y][x].visited = True


def include_42_aldous(width: int, height: int,
                      grid: Deque[Deque[Cell]]) -> None:
    """
    Embeds a predefined '42' pattern into the maze
    for Aldous-Broder generation.

    Args:
        maze (MazeGenerator): Maze instance to modify.
    """
    x_s: int = int(width / 2) - int(7 / 2)
    y_s: int = int(height / 2) - int(5 / 2)
    close: list[Tuple[int, int]] = [
        (y_s, x_s),
        (y_s, x_s + 4),
        (y_s, x_s + 5),
        (y_s, x_s + 6),
        (y_s + 1, x_s),
        (y_s + 1, x_s + 6),
        (y_s + 2, x_s),
        (y_s + 2, x_s + 1),
        (y_s + 2, x_s + 2),
        (y_s + 2, x_s + 4),
        (y_s + 2, x_s + 5),
        (y_s + 2, x_s + 6),
        (y_s + 3, x_s + 2),
        (y_s + 3, x_s + 4),
        (y_s + 4, x_s + 2),
        (y_s + 4, x_s + 4),
        (y_s + 4, x_s + 5),
        (y_s + 4, x_s + 6),
    ]
    for coordinates in close:
        y, x = coordinates
        grid[y][x].visited = True


def draw_42(width: int, height: int, stdscr: "curses.window") -> None:
    """
    Draws the '42' pattern on the curses screen.

    Uses color highlighting to visually render the pattern
    inside the maze.

    Args:
        maze (MazeGenerator): Maze instance.
        stdscr (curses.window): Curses window for drawing.
    """
    x_s: int = int(width / 2) - int(7 / 2)
    y_s: int = int(height / 2) - int(5 / 2)
    close: List[Tuple[int, int]] = [
        (y_s, x_s),
        (y_s, x_s + 4),
        (y_s, x_s + 5),
        (y_s, x_s + 6),
        (y_s + 1, x_s),
        (y_s + 1, x_s + 6),
        (y_s + 2, x_s),
        (y_s + 2, x_s + 1),
        (y_s + 2, x_s + 2),
        (y_s + 2, x_s + 4),
        (y_s + 2, x_s + 5),
        (y_s + 2, x_s + 6),
        (y_s + 3, x_s + 2),
        (y_s + 3, x_s + 4),
        (y_s + 4, x_s + 2),
        (y_s + 4, x_s + 4),
        (y_s + 4, x_s + 5),
        (y_s + 4, x_s + 6),
    ]
    for coordinates in close:
        y, x = coordinates
        stdscr.attron(curses.color_pair(11))
        stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
        stdscr.attroff(curses.color_pair(11))
        stdscr.refresh()
