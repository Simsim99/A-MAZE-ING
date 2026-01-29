from mazegen.maze_logic import MazeGenerator
from typing import List, Dict, Tuple, Optional, Deque
import curses
from curses import wrapper
import random
import time
from collections import deque
from mazegen.models import (
    include_42_aldous,
    include_42_tree,
    draw_42,
    check_coordinates,
    Cell,
)


def draw_screen(
        stdscr: "curses.window", maze: MazeGenerator, is_animated: bool
                ) -> None:
    """Renders the maze grid onto the curses screen.

    Args:
        stdscr: The curses window object.
        maze (MazeGenerator): The maze object containing grid data.
        is_animated (bool): If True, draws the maze cell-by-cell with a delay.
    """
    before: Deque[Deque[Cell]] = deque(
        deque(Cell() for _ in range(maze.width)) for _ in range(maze.height)
        )
    for y, row in enumerate(before):
        for x, cell in enumerate(row):
            screen_y = y * 2
            screen_x = x * 3
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(screen_y, screen_x, "█")
            if cell.north == 1:
                stdscr.addstr(screen_y, screen_x + 1, "███")
            if cell.west == 1:
                stdscr.addstr(screen_y + 1, screen_x, "█")
            if x == maze.width - 1:
                stdscr.addstr(screen_y + 1, (x + 1) * 3, "█")
                stdscr.addstr(screen_y, (x + 1) * 3, "█")
            if y == maze.height - 1:
                stdscr.addstr((y + 1) * 2, screen_x, "████")
                if x == maze.width - 1:
                    stdscr.addstr((y + 1) * 2, (x + 1) * 3, "█")
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            screen_y = y * 2
            screen_x = x * 3
            stdscr.addstr(screen_y, screen_x, "█")
            if cell.north == 0:
                stdscr.addstr(screen_y, screen_x + 1, "   ")
            if cell.west == 0:
                stdscr.addstr(screen_y + 1, screen_x, " ")
            if x == maze.width - 1:
                stdscr.addstr(screen_y + 1, (x + 1) * 3, "█")
                stdscr.addstr(screen_y, (x + 1) * 3, "█")
            if y == maze.height - 1:
                stdscr.addstr((y + 1) * 2, screen_x, "████")
                if x == maze.width - 1:
                    stdscr.addstr((y + 1) * 2, (x + 1) * 3, "█")
            if is_animated is True:
                time.sleep(0.01)
            stdscr.refresh()
    stdscr.attroff(curses.color_pair(2))


def animate_path(stdscr: "curses.window",
                 path_list: List[Tuple[int, int]],
                 double_color: str,
                 single_color: str
                 ) -> None:
    """Animates the solution path or clears it from the screen.

    Args:
        stdscr (window): The curses window object.
        path_list (List[Tuple[int, int]]): Coordinates of the solution path.
        double_color (str): The string to use for 2-character wide blocks.
        single_color (str): The string to use for 1-character wide blocks.
    """
    for index, tuple in enumerate(path_list):
        if index == len(path_list) - 1:
            break
        y, x = tuple
        screen_y = (y * 2) + 1
        screen_x = (x * 3) + 1
        next_y, next_x = path_list[index + 1]
        stdscr.attron(curses.color_pair(4))
        if index == 0:
            pass
        else:
            stdscr.addstr(screen_y, screen_x, double_color)
        if next_x > x:
            stdscr.addstr((next_y * 2) + 1, (next_x * 3), single_color)
        elif next_x < x:
            stdscr.addstr((next_y * 2) + 1, (next_x * 3) + 3, single_color)
        elif next_y > y:
            stdscr.addstr((y * 2) + 2, (x * 3) + 1, double_color)
        elif next_y < y:
            stdscr.addstr((y * 2), (x * 3) + 1, double_color)
        stdscr.attroff(curses.color_pair(4))
        stdscr.refresh()
        if double_color == "  ":
            time.sleep(0.01)
        else:
            time.sleep(0.1)


def handle_generation(
    maze_object: MazeGenerator,
    is_perfect: bool,
    start_coords: Tuple[int, int],
    end_coords: Tuple[int, int],
    algo_gen: str,
    the_seed: Optional[str]
) -> List[Tuple[int, int]]:
    """Handles the algorithmic generation and solving of the maze.

    Args:
        maze_object (MazeGenerator): The object to generate the maze in.
        is_perfect (bool): Whether the maze should be perfect (no loops).
        start_coords (Tuple[int, int]): Entry (y, x).
        end_coords (Tuple[int, int]): Exit (y, x).
        algo_gen (str): The algorithm name ('tree' or 'aldous').
        the_seed (Optional[str]): The seed for random generation.

    Returns:
        List[Tuple[int, int]]: The calculated path from start to end.
    """
    if algo_gen == "tree":
        include_42_tree(maze_object.width, maze_object.height,
                        maze_object.grid)
        maze_object.tree_generate(the_seed)
    elif algo_gen == "aldous":
        include_42_aldous(maze_object.width, maze_object.height,
                          maze_object.grid)
        maze_object.aldous_generate(the_seed)
    else:
        raise ValueError(
            "This algrithm is not available. Available algorithms are: "
            "<tree>, <aldous>"
        )
    if is_perfect is False:
        maze_object.braid(the_seed)
    path: List[Tuple[int, int]] = maze_object.find_path(
        start_coords, end_coords
        )
    return path


def draw_all(stdscr: "curses.window",
             path: List[Tuple[int, int]],
             maze: MazeGenerator,
             my_dict: Dict[str, str],
             is_animated: bool) -> None:
    """Main drawing coordinator for the maze and UI elements.

    Args:
        stdscr (window): The curses window object.
        path (List[Tuple[int, int]]): The solution path coordinates.
        maze (MazeGenerator): The current maze object.
        my_dict (Dict[str, str]): Configuration dictionary.
        is_animated (bool): Whether to animate the maze drawing process.
    """
    stdscr.addstr((int(my_dict[("HEIGHT")]) * 2) + 2, 0, "=== A-Maze-ing ===")
    stdscr.addstr(
        (int(my_dict[("HEIGHT")]) * 2) + 3, 0, "1. Re-generate a new maze"
        )
    stdscr.addstr(
        (int(my_dict[("HEIGHT")]) * 2) + 4,
        0,
        "2. Show/Hide path from entry to exit",
    )
    stdscr.addstr(
        (int(my_dict[("HEIGHT")]) * 2) + 5, 0, "3. Rotate maze colors"
        )
    stdscr.addstr((int(my_dict[("HEIGHT")]) * 2) + 6, 0, "4. Quit")
    stdscr.addstr((int(my_dict[("HEIGHT")]) * 2) + 7, 0, "5. Choice? (1-4): ")
    draw_screen(stdscr, maze, is_animated)
    draw_42(maze.width, maze.height, stdscr)
    y, x = path[0]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(6))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(6))
    y, x = path[-1]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(3))
    try:
        stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
    except curses.error:
        pass


def read_file() -> Dict[str, str]:
    """Reads and validates configuration from config.txt.

    Returns:
        Dict[str, str]: Validated configuration keys.
    """
    dictt: Dict[str, str] = {}
    index = 0
    separators: List[str] = [' ', ':', '=', ',', '->', '-',
                             '+', '*']
    with open("config.txt", "r") as file:
        for line in file:
            if line[0] == "#":
                pass
            else:
                for sep in separators:
                    if sep in line:
                        parts = line.strip().split(sep)
                        dictt[parts[index].upper()] = parts[index + 1]
    height = int(dictt["HEIGHT"])
    width = int(dictt["WIDTH"])
    y_start, x_start = tuple(int(i) for i in dictt["ENTRY"].split(","))
    y_exit, x_exit = tuple(int(i) for i in dictt["EXIT"].split(","))
    if width < 0:
        raise Exception(f"Invalid width: {width}. "
                        f"Width must be a positive number.")
    elif height < 0:
        raise Exception(
            f"Invalid height: {height}. Height must be a positive number."
        )
    elif height < 7 or width < 9:
        raise Exception("ERROR: Maze too small for '42' logo!")
    # elif (y_start, x_start) == (y_exit, x_exit):
    #     raise Exception(
    #         "ERROR: Start and exit cannot be at the same position!"
    #         )
    elif y_start > height - 1 or x_start > width - 1:
        raise ValueError("The start can't be outside the Maze !")
    elif y_start < 0 or x_start < 0:
        raise ValueError("The start coordinates can't be negative!")
    elif y_exit > height - 1 or x_exit > width - 1:
        raise ValueError("The exit can't be outside the Maze !")
    elif y_exit < 0 or x_exit < 0:
        raise ValueError("The exit coordinates can't be negative!")
    elif (y_start, x_start) == (y_exit, x_exit):
        raise ValueError(
            "ERROR: Start and exit cannot" "be at the same position!"
            "")
    elif not check_coordinates(y_start, x_start, width, height):
        raise ValueError(
            f"ERROR: Start position ({y_start, x_start}) "
            f"is inside the '42' logo!")
    elif not check_coordinates(y_exit, x_exit, width, height):
        raise ValueError(
            f"ERROR: Exit position {y_exit, x_exit} "
            f"is inside the '42' logo!"
        )
    return dictt


def main(stdscr: "curses.window") -> None:
    """The main entry point for the curses application.

    Args:
        stdscr (window): The main curses window object.
    """

    my_dict: Dict[str, str] = read_file()
    ter_height, ter_width = stdscr.getmaxyx()
    if (
        ter_width < (int(my_dict.get("WIDTH", "0")) * 3) + 1
        or ter_height < (int(my_dict.get("HEIGHT", "0")) * 2) + 8
    ):
        raise ValueError("Screen too small for maze!")
    if my_dict["PERFECT"].upper() == "TRUE":
        is_perfect = True
    elif my_dict["PERFECT"].upper() == "FALSE":
        is_perfect = False
    else:
        raise ValueError("PERFECT is a Boolean. Expected input:"
                         " True or False")
    curses.curs_set(0)
    curses.start_color()
    # entry_tuple: Tuple[int, int] = tuple(
    #     int(i) for i in my_dict["ENTRY"].split(",")
    #     )
    en_list: List[int] = [int(i) for i in my_dict["ENTRY"].split(",")]
    entry_tuple: Tuple[int, int] = (en_list[0], en_list[1])
    # exit_tuple: Tuple[int, int] = tuple(
    #     int(i) for i in my_dict["EXIT"].split(",")
    #     )
    ex_list: List[int] = [int(i) for i in my_dict["EXIT"].split(",")]
    exit_tuple: Tuple[int, int] = (ex_list[0], ex_list[1])
    curses.init_color(1, 106, 286, 396)
    curses.init_color(2, 792, 913, 1000)
    curses.init_color(3, 1000, 419, 419)
    curses.init_color(4, 373, 658, 827)
    curses.init_color(5, 94, 204, 243)
    curses.init_color(6, 1000, 549, 0)
    curses.init_pair(1, 1, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, 3, curses.COLOR_BLACK)
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    curses.init_pair(6, 6, curses.COLOR_BLACK)
    curses.init_color(9, 500, 500, 500)
    curses.init_pair(11, 9, curses.COLOR_BLACK)
    try:
        temp_seed: Optional[str] = my_dict["SEED"]
        if temp_seed == "":
            raise ValueError("SEED must have an value!")
        the_seed: Optional[str] = None
        if temp_seed is not None:
            if temp_seed.upper() == "NONE":
                the_seed = None
            else:
                the_seed = temp_seed
    except KeyError:
        the_seed = None
    maze: MazeGenerator = MazeGenerator(
        int(my_dict["WIDTH"]), int(my_dict[("HEIGHT")])
        )
    try:
        path: List[Tuple[int, int]] = handle_generation(
            maze,
            is_perfect,
            entry_tuple,
            exit_tuple,
            my_dict["GEN_ALGO"],
            the_seed,
        )
    except KeyError:
        path = handle_generation(
            maze, is_perfect, entry_tuple, exit_tuple, "aldous", the_seed
        )
    maze.hexa_converter(my_dict["OUTPUT_FILE"])
    maze.directions_path(entry_tuple, exit_tuple, my_dict["OUTPUT_FILE"])
    try:
        draw_all(stdscr, path, maze, my_dict, True)
    except curses.error:
        pass
    curses.curs_set(2)
    path_shown: bool = False
    while True:
        key: int = stdscr.getch()
        if key == curses.KEY_RESIZE:
            ter_height, ter_width = stdscr.getmaxyx()
            if (
                ter_width < (int(my_dict.get("WIDTH", "0")) * 3) + 1
                or ter_height < (int(my_dict.get("HEIGHT", "0")) * 2) + 8
            ):
                # stdscr.clear()
                stdscr.erase()
                try:
                    stdscr.addstr(
                        0,
                        0,
                        "size of terminal is not enough. "
                        "Re-adjust to optimal size", curses.COLOR_WHITE
                    )
                except curses.error:
                    pass
            else:
                # stdscr.clear()
                stdscr.erase()
                draw_all(stdscr, path, maze, my_dict, False)

        if key == ord("1"):
            path_shown = False
            # stdscr.clear()
            stdscr.erase()
            maze = MazeGenerator(
                int(my_dict["WIDTH"]), int(my_dict[("HEIGHT")])
                )
            try:
                path = handle_generation(
                    maze,
                    is_perfect,
                    entry_tuple,
                    exit_tuple,
                    my_dict["GEN_ALGO"],
                    the_seed,
                )
            except KeyError:
                path = handle_generation(
                    maze,
                    is_perfect,
                    entry_tuple,
                    exit_tuple,
                    "aldous",
                    the_seed,
                )
            maze.hexa_converter(my_dict["OUTPUT_FILE"])
            maze.directions_path(
                entry_tuple, exit_tuple, my_dict["OUTPUT_FILE"]
                )
            try:
                draw_all(stdscr, path, maze, my_dict, True)
            except curses.error:
                pass
            curses.curs_set(2)
            stdscr.refresh()

        elif key == ord("2"):
            try:
                curses.curs_set(0)
                if path_shown is False:
                    animate_path(stdscr, path, "██", "█")
                    path_shown = True
                    stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
                    curses.curs_set(2)
                else:
                    animate_path(stdscr, path, "  ", " ")
                    stdscr.refresh()
                    path_shown = False
                    stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
                    curses.curs_set(2)
            except curses.error:
                pass
        elif key == ord("3"):
            stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
            curses.curs_set(2)
            colors: List[int] = [1, 6, 4, 3, 2, 5]
            random.shuffle(colors)
            curses.init_pair(2, colors[0], curses.COLOR_BLACK)
            curses.init_pair(4, colors[1], curses.COLOR_BLACK)
            curses.init_pair(3, colors[2], curses.COLOR_BLACK)
            curses.init_pair(6, colors[3], curses.COLOR_BLACK)
            stdscr.refresh()
        elif key == ord("4"):
            break


if __name__ == "__main__":
    try:
        try:
            wrapper(main)
        except NameError as e:
            print(e)
        except FileNotFoundError as e:
            print(
                f"Please make sure that you provide the file {e.filename} "
                f"before running your program ⚠️"
            )
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(f"Missing key: {e}")
            print(
                "Keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, "
                "PERFECT are obligatory!"
            )
        except Exception as e:
            print(e)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nExited A-MAZE-ING. See you next time!")
    except ModuleNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
