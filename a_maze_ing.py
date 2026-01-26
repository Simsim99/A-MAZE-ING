from mazegen.maze_logic import MazeGenerator
import curses
from curses import wrapper
import random
import time
from mazegen.models import (
    include_42_aldous,
    include_42_tree,
    draw_42,
    check_coordinates,
)


def draw_screen(stdscr, maze):
    stdscr.clear()
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            screen_y = y * 2
            screen_x = x * 3
            stdscr.attron(curses.color_pair(3))
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
            # time.sleep(0.01)
            stdscr.refresh()
    stdscr.attroff(curses.color_pair(3))


def animate_path(stdscr, path_list, double_color: str, single_color):
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
    maze_object, is_perfect, start_coords, end_coords, algo_gen, the_seed
):
    if algo_gen == "tree":
        include_42_tree(maze_object)
        maze_object.tree_generate(the_seed)
    elif algo_gen == "aldous":
        include_42_aldous(maze_object)
        maze_object.aldous_generate(the_seed)
    else:
        raise ValueError(
            "This algrithm is not available. Available algorithms are: "
            "<tree>, <aldous>"
        )
    if is_perfect is False:
        maze_object.braid(the_seed)
    path = maze_object.find_path(start_coords, end_coords)
    return path


def draw_all(stdscr, path, maze, my_dict):
    draw_screen(stdscr, maze)
    draw_42(maze, stdscr)
    y, x = path[0]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(2))
    y, x = path[-1]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(1))
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


def read_file():
    dictt = {}
    index = 0
    with open("config.txt", "r") as file:
        for line in file:
            line = line.strip().split("=")
            dictt[line[index]] = line[index + 1]
    height = int(dictt.get("HEIGHT"))
    width = int(dictt.get("WIDTH"))
    y_start, x_start = tuple(int(i) for i in dictt["ENTRY"].split(","))
    y_exit, x_exit = tuple(int(i) for i in dictt["EXIT"].split(","))
    if width < 0:
        raise Exception(
            f"❌ Invalid width: {width}. Width must be a positive number."
            )
    elif height < 0:
        raise Exception(
            f"❌ Invalid height: {height}. Height must be a positive number."
        )
    elif height < 7 or width < 9:
        raise Exception("❌ ERROR: Maze too small for '42' logo!")
    elif (y_start, x_start) == (y_exit, x_exit):
        raise Exception(
            "❌ ERROR: Start and exit cannot be at the same position!"
            )
    elif not check_coordinates(y_start, x_start, width, height):
        raise Exception(
            f"❌ ERROR: Start position ({y_start, x_start}) "
            f"is inside the '42' logo!"
        )
    elif not check_coordinates(y_exit, x_exit, width, height):
        raise Exception(
            f"❌ ERROR: Exit position {y_exit, y_exit} is inside the '42' logo!"
        )
    return dictt


def main(stdscr):
    my_dict = read_file()
    ter_height, ter_width = stdscr.getmaxyx()
    if (
        ter_width < (int(my_dict.get("WIDTH")) * 3) + 1
        or ter_height < (int(my_dict.get("HEIGHT")) * 2) + 8
    ):
        raise ValueError("Screen too small for maze!")
    if my_dict["PERFECT"] == "True":
        is_perfect = True
    else:
        is_perfect = False
    curses.curs_set(0)
    curses.start_color()
    entry_tuple = tuple(int(i) for i in my_dict["ENTRY"].split(","))
    exit_tuple = tuple(int(i) for i in my_dict["EXIT"].split(","))
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_color(9, 500, 500, 500)
    curses.init_pair(11, 9, curses.COLOR_BLACK)
    try:
        the_seed = my_dict["SEED"]
        if the_seed == "None":
            the_seed = None
    except KeyError:
        the_seed = None
    maze = MazeGenerator(int(my_dict["WIDTH"]), int(my_dict[("HEIGHT")]))
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
            maze, is_perfect, entry_tuple, exit_tuple, "aldous", the_seed
        )
    maze.hexa_converter(my_dict["OUTPUT_FILE"])
    maze.directions_path(entry_tuple, exit_tuple, my_dict["OUTPUT_FILE"])
    draw_all(stdscr, path, maze, my_dict)
    curses.curs_set(2)
    my_colors = [
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW,
    ]
    color_index = 0
    path_shown = False
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            ter_height, ter_width = stdscr.getmaxyx()
            if (
                ter_width < (int(my_dict.get("WIDTH")) * 3) + 1
                or ter_height < (int(my_dict.get("HEIGHT")) * 2) + 8
            ):
                stdscr.clear()
                stdscr.addstr(
                    0, 0, "size of terminal is not enough. "
                          "Re-adjust to optimal size"
                )
            else:
                stdscr.clear()
                draw_all(stdscr, path, maze, my_dict)

        if key == ord("1"):
            path_shown = False
            stdscr.clear()
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
            draw_all(stdscr, path, maze, my_dict)
            curses.curs_set(2)
            stdscr.refresh()

        elif key == ord("2"):

            curses.curs_set(0)
            if path_shown is False:
                animate_path(stdscr, path, "██", "█")
                path_shown = True
            else:
                animate_path(stdscr, path, "  ", " ")
                stdscr.refresh()
                path_shown = False
                stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
                curses.curs_set(2)

        elif key == ord("3"):

            stdscr.move((int(my_dict[("HEIGHT")]) * 2) + 7, 18)
            curses.curs_set(2)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(1, my_colors[color_index], curses.COLOR_BLACK)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(2, my_colors[color_index], curses.COLOR_BLACK)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(3, my_colors[color_index], curses.COLOR_BLACK)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(4, my_colors[color_index], curses.COLOR_BLACK)
            stdscr.refresh()

        elif key == ord("4"):

            break


if __name__ == "__main__":
    try:
        try:
            wrapper(main)
        except NameError as e:
            print(e)
        except curses.error:
            print("⚠️ Screen too small for maze!")
            print("Resize terminal and restart.")
        except FileNotFoundError as e:
            print(
                f"Please make sure that you provide the file {e.filename} "
                f"before running your program ⚠️"
            )
        except TypeError:
            print("❌ Error: Filename cannot be None!")
        except KeyError as e:
            print(f"Missing key: {e}")
            print(
                "Keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, "
                "PERFECT are oblegatory!"
            )
        except Exception as e:
            print(e)
    except ValueError as e:
        print(e)
    except ModuleNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
