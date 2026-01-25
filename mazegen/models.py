from pydantic import BaseModel, Field
import curses
import time
class Cell(BaseModel):
    north: int = 1
    south: int = 1
    west: int = 1
    east: int = 1
    visited: bool = False
    last: int = 1


def check_position(y: int, x: int, height: int, width: int) -> list:
    diractions = ["e", "n", "s", "w"]
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
    return(diractions)

def check_grid(grid):
    for row in grid:
        for cell in row:
            if cell.visited == False:
                return (False)
    return (True)

def check_coordinates(y, x, width, hight):
    x_s = int(width / 2) - int(7 / 2)
    y_s = int(hight / 2) - int(5 / 2)
    close = [
            (y_s, x_s), (y_s, x_s + 4), (y_s, x_s + 5), (y_s, x_s + 6),
            (y_s + 1, x_s), (y_s + 1, x_s + 6), (y_s + 2, x_s), (y_s + 2, x_s + 1),
            (y_s + 2, x_s +  2), (y_s + 2, x_s + 4), (y_s + 2, x_s + 5), (y_s + 2, x_s + 6),
            (y_s + 3, x_s + 2), (y_s + 3, x_s + 4), (y_s + 4, x_s + 2), (y_s + 4, x_s + 4),
            (y_s + 4, x_s + 5), (y_s + 4, x_s + 6)
        ]
    if (y, x) in close:
        return (False)
    return (True)


def include_42_tree(maze):
    x_s = int(maze.width / 2) - int(7 / 2)
    y_s = int(maze.height / 2) - int(5 / 2)
    close = [
            (y_s, x_s), (y_s, x_s + 4), (y_s, x_s + 5), (y_s, x_s + 6),
            (y_s + 1, x_s), (y_s + 1, x_s + 6), (y_s + 2, x_s), (y_s + 2, x_s + 1),
            (y_s + 2, x_s +  2), (y_s + 2, x_s + 4), (y_s + 2, x_s + 5), (y_s + 2, x_s + 6),
            (y_s + 3, x_s + 2), (y_s + 3, x_s + 4), (y_s + 4, x_s + 2), (y_s + 4, x_s + 4),
            (y_s + 4, x_s + 5), (y_s + 4, x_s + 6)
        ]
    open_north = [
            (y_s, x_s - 1), (y_s + 1, x_s - 1), (y_s + 2, x_s - 1),
            (y_s, x_s + 3), (y_s + 4, x_s + 1), (y_s + 2, x_s + 3),
            (y_s + 3, x_s + 3), (y_s + 4, x_s + 3), (y_s + 3, x_s - 1),
            (y_s + 1, x_s + 3), (y_s + 5, x_s + 1)
        ]
    open_east = [
        (y_s + 3, x_s), (y_s + 3, x_s + 5),  (y_s + 3, x_s + 6), (y_s + 5, x_s + 4),
        (y_s + 5, x_s + 5), (y_s + 5, x_s + 6), (y_s + 5, x_s + 4),
        (y_s + 1, x_s + 3), (y_s + 1, x_s + 4), (y_s + 5, x_s + 3),
        (y_s + 4, x_s - 1), (y_s + 3, x_s - 1), (y_s + 5, x_s + 2)
    ]
    open_west = [
        (y_s + 3, x_s + 1), (y_s + 1, x_s + 5)
    ]
    for tuple in close:
        y, x = tuple
        maze.grid[y][x].visited = True
    for tuple in open_north:
        y, x = tuple
        maze.grid[y][x].north = 0
        maze.grid[y][x].visited = True
        maze.grid[y - 1][x].south = 0
    for tuple in open_east:
        y, x = tuple
        maze.grid[y][x].east = 0
        maze.grid[y][x].visited = True
        maze.grid[y][x + 1].west = 0
    for tuple in open_west:
        y, x = tuple
        maze.grid[y][x].visited = True


def include_42_aldous(maze):
    x_s = int(maze.width / 2) - int(7 / 2)
    y_s = int(maze.height / 2) - int(5 / 2)
    close = [
            (y_s, x_s), (y_s, x_s + 4), (y_s, x_s + 5), (y_s, x_s + 6),
            (y_s + 1, x_s), (y_s + 1, x_s + 6), (y_s + 2, x_s), (y_s + 2, x_s + 1),
            (y_s + 2, x_s +  2), (y_s + 2, x_s + 4), (y_s + 2, x_s + 5), (y_s + 2, x_s + 6),
            (y_s + 3, x_s + 2), (y_s + 3, x_s + 4), (y_s + 4, x_s + 2), (y_s + 4, x_s + 4),
            (y_s + 4, x_s + 5), (y_s + 4, x_s + 6)
        ]
    for tuple in close:
        y, x = tuple
        maze.grid[y][x].visited = True


def draw_42(maze, stdscr):
    x_s = int(maze.width / 2) - int(7 / 2)
    y_s = int(maze.height / 2) - int(5 / 2)
    close = [
            (y_s, x_s), (y_s, x_s + 4), (y_s, x_s + 5), (y_s, x_s + 6),
            (y_s + 1, x_s), (y_s + 1, x_s + 6), (y_s + 2, x_s), (y_s + 2, x_s + 1),
            (y_s + 2, x_s +  2), (y_s + 2, x_s + 4), (y_s + 2, x_s + 5), (y_s + 2, x_s + 6),
            (y_s + 3, x_s + 2), (y_s + 3, x_s + 4), (y_s + 4, x_s + 2), (y_s + 4, x_s + 4),
            (y_s + 4, x_s + 5), (y_s + 4, x_s + 6)
        ]
    for tuple in close:
        y, x = tuple
        stdscr.attron(curses.color_pair(11))
        stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
        stdscr.attroff(curses.color_pair(11))
        stdscr.refresh()
        # time.sleep(0.000)