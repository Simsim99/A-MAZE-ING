from pydantic import BaseModel, Field
class Cell(BaseModel):
    north: int = 1
    south: int = 1
    west: int = 1
    east: int = 1
    visited: bool = False


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

