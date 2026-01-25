from mazegen.maze_logic import MazeGenerator
import curses
from curses import wrapper
import random
import time
from models import include_42_aldous, include_42_tree, draw_42

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
    stdscr.attroff(curses.color_pair(3))
    stdscr.refresh()

# def  animate_path(stdscr,path_list):
#     for y, x in path_list[1:-1]:
#         screen_y = (y * 2) + 1
#         screen_x = (x * 3) + 1
#         stdscr.attron(curses.color_pair(1))
#         stdscr.addstr(screen_y, screen_x, "██")
#         stdscr.attroff(curses.color_pair(1))
#         stdscr.refresh()
#         curses.napms(95)
def  animate_path(stdscr,path_list):
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
            stdscr.addstr(screen_y, screen_x, "██")
        if next_x > x:
            stdscr.addstr((next_y * 2) + 1, (next_x * 3), "█")
        elif next_x < x:
            stdscr.addstr((next_y * 2) + 1, (next_x * 3) + 3, "█")
        elif next_y > y:
            stdscr.addstr((y  * 2) + 2, (x * 3) + 1, "██")
        elif next_y < y:
            stdscr.addstr((y * 2), (x * 3) + 1, "██")
        stdscr.attroff(curses.color_pair(4))
        stdscr.refresh()
        time.sleep(0.1)

def handle_generation(maze_object, is_perfect, start_coords, end_coords, algo_gen):
    if algo_gen == "tree":
        include_42_tree(maze_object)
        maze_object.tree_generate()
    else:
        include_42_aldous(maze_object)
        maze_object.aldous_generate()
    if is_perfect == False:
        maze_object.braid()
    path = maze_object.find_path(start_coords, end_coords)
    return (path)

def read_file():
    dictt = {}
    index = 0
    with open("config.txt", "r") as file:
        for line in file:
            line = line.strip().split("=")
            dictt[line[index]] = line[index + 1]
    return (dictt)

def main(stdscr):
    my_dict = read_file()
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
    maze = MazeGenerator(int(my_dict['WIDTH']), int(my_dict[('HEIGHT')]))
    
    path = handle_generation(maze, is_perfect, entry_tuple, exit_tuple, my_dict['GEN_ALGO'])
    maze.hexa_converter()
    maze.directions_path(entry_tuple, exit_tuple)
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
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 2, 0, "=== A-Maze-ing ===")
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 3, 0, "1. Re-generate a new maze")
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 4, 0, "2. Show/Hide path from entry to exit")
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 5, 0, "3. Rotate maze colors")
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 6, 0, "4. Quit")
    stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 7, 0, "5. Choice? (1-4): ")
    curses.curs_set(2)
    my_colors = [
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW
        ]
    color_index = 0
    path_shown = False
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            path_shown = False
            stdscr.clear()
            new_maze = MazeGenerator(int(my_dict['WIDTH']), int(my_dict[('HEIGHT')]))
            
            path = handle_generation(new_maze, is_perfect, entry_tuple, exit_tuple, my_dict['GEN_ALGO'])
            new_maze.hexa_converter()
            new_maze.directions_path(entry_tuple, exit_tuple)
            draw_screen(stdscr, new_maze)
            draw_42(new_maze, stdscr)
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
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 2, 0, "=== A-Maze-ing ===")
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 3, 0, "1. Re-generate a new maze")
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 4, 0, "2. Show/Hide path from entry to exit")
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 5, 0, "3. Rotate maze colors")
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 6, 0, "4. Quit")
            stdscr.addstr((int(my_dict[('HEIGHT')]) * 2) + 7, 0, "5. Choice? (1-4): ")
            curses.curs_set(2)

            stdscr.refresh()
            
        elif key == ord('2'):
            # curses.curs_set(0)
            # if path_shown == False:
            #     animate_path(stdscr, path)
            #     path_shown = True
            # else:
            #     for y, x in path[1:-1]:
            #         screen_y = (y * 2) + 1
            #         screen_x = (x * 3) + 1
            #         stdscr.addstr(screen_y, screen_x, "  ")
            #         path_shown = False
            #     stdscr.refresh()
            # stdscr.move((int(my_dict[('HEIGHT')]) * 2) + 7, 18)
            # curses.curs_set(2)
            curses.curs_set(0)
            if path_shown == False:
                animate_path(stdscr, path)
                path_shown = True
            else:
                for index, tup in enumerate(path):
                    if index == len(path) - 1:
                        break
                    y, x = tup
                    screen_y = (y * 2) + 1
                    screen_x = (x * 3) + 1
                    next_y, next_x = path[index + 1]
                    stdscr.attron(curses.color_pair(1))
                    if index == 0:
                        pass
                    else:    
                        stdscr.addstr(screen_y, screen_x, "  ")
                    if next_x > x:
                        stdscr.addstr((next_y * 2) + 1, (next_x * 3), " ")
                    elif next_x < x:
                        stdscr.addstr((next_y * 2) + 1, (next_x * 3) + 3, " ")
                    elif next_y > y:
                        stdscr.addstr((y  * 2) + 2, (x * 3) + 1, "  ")
                    elif next_y < y:
                        stdscr.addstr((y * 2), (x * 3) + 1, "  ")
                    stdscr.attroff(curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(0.01)
                    path_shown = False
            stdscr.move((int(my_dict[('HEIGHT')]) * 2) + 7, 18)
            curses.curs_set(2)
        elif key == ord('3'):
            stdscr.move((int(my_dict[('HEIGHT')]) * 2) + 7, 18)
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
        elif key == ord('4'):
            break


if __name__ == "__main__":
    wrapper(main)

