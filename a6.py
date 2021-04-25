import tkinter as samira
import random

# settings

CANVAS_SIZE = 750
RESOLUTION  = 75
INTERVAL    = 50
CELL_SIZE   = CANVAS_SIZE / RESOLUTION

BG = "black"
FG = "purple"

# les variables globales

root = samira.Tk()
canvas = samira.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG)
canvas.pack()

def get_cell_val(x : int, y : int, grid : list) -> bool:
    return (grid[y] >> x) & 0b1

def set_cell_val(x : int, y : int, val : bool, grid : list):
    bit = 0b1 << x

    if val:
        grid[y] |= bit
    else:
        grid[y] &= ~bit

def in_bounds(x : int, y : int) -> bool:
    num_in_bounds = lambda n : n >= 0 and n < RESOLUTION
    return num_in_bounds(x) and num_in_bounds(y)

def get_neighbors(x : int, y : int, grid : list) -> int:
    n = 0

    # cycle through all neighboring offsets
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            # ignore home cell
            if dx == 0 and dy == 0:
                continue
            
            # get actual coordinates of neighbor
            nx = x + dx
            ny = y + dy

            if not in_bounds(nx, ny):
                continue

            if get_cell_val(nx, ny, grid):
                n += 1

    return n

def draw_cell(x : int, y : int):
    canvas_x = x * CELL_SIZE
    canvas_y = y * CELL_SIZE
    canvas.create_rectangle(canvas_x, canvas_y, canvas_x + CELL_SIZE, canvas_y + CELL_SIZE, fill=FG, outline="")

def update(old_grid : list):
    canvas.delete("all")
    grid = old_grid.copy()

    for y in range(RESOLUTION):
        for x in range(RESOLUTION):
            n = get_neighbors(x, y, old_grid)

            # apply game of life rules
            if n < 2 or n > 3:
                set_cell_val(x, y, False, grid)
            elif n == 3:
                set_cell_val(x, y, True, grid)
            # else, cells are the same as previous generation which is accounted for in copying the old grid to the new grid
            
            # only draw cell if it's alive, for performance
            if get_cell_val(x, y, grid):
                draw_cell(x, y)

    root.after(INTERVAL, update, grid)

# le programme commence
grid = []
max_val = 2**RESOLUTION - 1

# randomize initial grid state
for y in range(RESOLUTION):
    # since rows are stored in integers, we can randomzie rows by assigning it a random int
    grid.append(random.randint(0, max_val))

update(grid)
root.mainloop()