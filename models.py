from pydantic import BaseModel, Field
class Cell(BaseModel):
    north: int = 1
    south: int = 1
    west: int = 1
    east: int = 1
    # visited: bool = False
    # distance: int = -1

def hexa_converter(maze):
    with open("output.txt", "w") as fd:
        for index,row in enumerate(maze):
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
            if index == hight - 1:
                fd.write(f"{line}")
            else:
                fd.write(f"{line}\n")
