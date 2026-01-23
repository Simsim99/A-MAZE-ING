from maze_logic import MazeGenerator
import curses
from curses import wrapper
import random


def draw_screen(stdscr, maze):
    stdscr.clear()
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            screen_y = y * 2
            screen_x = x * 3
            stdscr.attron(curses.color_pair(4))
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
    stdscr.attroff(curses.color_pair(4))
    stdscr.refresh()

def  animate_path(stdscr,path_list):
    
    # stdscr.refresh()
    # stdscr.getch()
    for y, x in path_list[1:-1]:
        screen_y = (y * 2) + 1
        screen_x = (x * 3) + 1
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(screen_y, screen_x, "██")
        stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()
        curses.napms(95)
    
    # stdscr.refresh()

def handle_generation(maze_object, is_perfect, start_coords, end_coords):
    maze_object.generate()
    if is_perfect == False:
        maze_object.braid()
    path = maze_object.find_path(start_coords, end_coords)
    return (path)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    maze = MazeGenerator(20, 15)
    path = handle_generation(maze, True, (14, 0), (0, 0))
    draw_screen(stdscr, maze)
    y, x = path[0]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(2))

    y, x = path[-1]
    screen_y = (y * 2) + 1
    screen_x = (x * 3) + 1
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(screen_y, screen_x, "██")
    stdscr.attroff(curses.color_pair(3))
    my_colors = [
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW
        ]
    color_index = 0
    path_shown = False
    # path = []
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            path_shown = False
            stdscr.clear()
            new_maze = MazeGenerator(20, 15)
            path = handle_generation(new_maze, False, (14, 0), (0, 0))
            draw_screen(stdscr, new_maze)
            y, x = path[0]
            screen_y = (y * 2) + 1
            screen_x = (x * 3) + 1
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(screen_y, screen_x, "██")
            stdscr.attroff(curses.color_pair(2))

            y, x = path[-1]
            screen_y = (y * 2) + 1
            screen_x = (x * 3) + 1
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(screen_y, screen_x, "██")
            stdscr.attroff(curses.color_pair(3))
            stdscr.refresh()
        elif key == ord('2'):
            if path_shown == False:
                animate_path(stdscr, path)
                path_shown = True
            else:
                for y, x in path[1:-1]:
                    screen_y = (y * 2) + 1
                    screen_x = (x * 3) + 1
                    stdscr.addstr(screen_y, screen_x, "  ")
                    path_shown = False
                stdscr.refresh()
        elif key == ord('3'):
            # color_index = (color_index + 1) % len(my_colors)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(1, my_colors[color_index], curses.COLOR_BLACK)
            # color_index = (color_index + 1) % len(my_colors)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(2, my_colors[color_index], curses.COLOR_BLACK)
            # color_index = (color_index + 1) % len(my_colors)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(3, my_colors[color_index], curses.COLOR_BLACK)
            # color_index = (color_index + 1) % len(my_colors)
            color_index = random.choice([0, 1, 2, 3])
            curses.init_pair(4, my_colors[color_index], curses.COLOR_BLACK)
            stdscr.refresh()
        elif key == ord('4'):
            break


if __name__ == "__main__":
    wrapper(main)

