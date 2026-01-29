*This project has been created as part of the 42 curriculum by rel-ouan, ouchouir*.

# Description A-MAZE-ING:
**"A-MAZE-ING"** 
is an interactive maze generation tool designed to demonstrate professional Python packaging and algorithmic logic. The project allows users to generate either **perfect mazes** (where exactly one path exists between any two points) or **braided mazes** (non-perfect, containing loops) using multiple algorithms.

The core logic handles the deconstruction of walls (N, S, E, W) for each "Cell" in a grid. The goal is use Breadth-First Search (BFS) to find the shortest path, all while the interface preserves a custom "42" logo at the center of the grid.

# Instructions:
### Installation & Setup
* **Install dependencies:**
```bash
make install
```
This ensures Poetry is installed and sets up the virtual environment.

* **Run the project:**
```bash
make run
```

* **Build the Reusable Module:**
```bash
make build
```
This creates the .whl and .tar.gz files and moves them to the project root for easy distribution.

* **Debugging:**
```bash
make debug
```
Runs the project with GDB
* **Cleanup:**
```bash
make clean
```
Removes environments, build artifacts, and caches
* **Linting (less strict):**
```bash
make lint
```
Runs Flake8 and MyPy with standard checks

* **Linting (Maximum strictness):**
```bash
make lint-strict
```
Runs MyPy with the --strict flag for maximum type safety.

* **The project reads maze parameters from a plain text file. The format must follow a KEY=VALUE structure:**


```Plaintext
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=14,19
OUTPUT_FILE=maze.txt
PERFECT=True
```
* **WIDTH (20) & HEIGHT (15): The maze will be a matrix of 300 cells total.**
* **ENTRY (0,0): The starting point is the top-left corner of the maze.**
* **EXIT (14,19): The destination is the bottom-right corner.**
* **PERFECT=True: This ensures the maze is "perfect". There are no loops and exactly one unique path from the entry to the exit. If "False", the maze becomes "non-perfect", multiple paths to the exit**
* **OUTPUT_FILE: The solution and maze data will be saved to maze.txt in hexadecimal and direction formats.**

## Installing and importing the whole project process:
### Move the mazegen package
    ```bash
    mv mazegen ..
    ```
### Install the file
    ```bash
    pip install mazegen-1.0.0-py3-none-any.whl
    ```
### Run:
    '''bash
    python3 file_name.py config_file.txt
    '''
### Move the package back
    ```bash
    mv ../mazegen .
    ```

* we used two algorithms, each one can create a perfect maze
## 1-Binary Tree algorithm:
The Binary Tree algorithm iterates through the grid and, for each cell, randomly chooses to carve a path either North or East.

We chose this for its extreme efficiency and as a demonstration of "algorithmic bias." Because the North and East boundaries always form straight corridors, it provides a unique architectural style that is easily distinguishable during evaluation.

## 2-aldous algorithm:
This algorithm is based on a "random walk." It picks a random neighbor; if the neighbor has not been visited, it carves a path and moves there. If it has been visited, it simply moves there without carving.

We chose this because it produces a Uniform Spanning Tree, meaning it has no bias. The resulting mazes are more organic and difficult to solve than the Binary Tree, showcasing the flexibility of our generation logic.

## Reusability:
While the entire mazegen package is installable, the core reusability lies within the MazeGenerator class in maze_logic.py. This component is UI-agnostic, meaning it generates the maze structure as a data object without dependencies on the curses library. This allows other developers to import our generation algorithm into any Python environment

## Team & Project Management:
### Roles
    [ouchouir]:[Algorithms, Documentation, Packaging, curses]
    [rel-ouan]:[Algorithms, Curses, error handling, 42logo]

### Planning & Evolution
    Week1: logic
    Week2: Packaging, error handling, Animation, Makefile and Readme

### Retrospective
    Using Poetry made dependency management easy and safe.

    Early project coordination could have been improved to avoid duplicate work. Additionally, we recognized that more thorough commenting on complex snippets would have allowed for faster implementation of error-handling blocks (try/except) without needing to re-read the entire logic.

### Tools Used
    Poetry, Git, Make and Python 3.13

# Resources:
* https://www.kufunda.net/publicdocs/Mazes%20for%20Programmers%20Code%20Your%20Own%20Twisty%20Little%20Passages%20(Jamis%20Buck).pdf

## AI Usage Disclosure:
Used for debugging imports, assissting with the Makefile and Readme, and structuring the pyproject.toml.
Used specifically to understand Python packaging and distribution standards.


