import tkinter as samira
import random

#les grilles de jeu de la vie sont stockées dans un tableau booléen et stockées dans un tableau d'entiers dans lequel un bit représente une cellule et différentes opérations au niveau du bit sont utilisées pour accéder à des données de cellule spécifiques

def get_cell_val(x : int, y : int, grid : list) -> bool:
    return (grid[y] >> x) & 0b1

def set_cell_val(x : int, y : int, val : bool, grid : list):
    bit = 0b1 << x

    if val:
        grid[y] |= bit
    else:
        grid[y] &= ~bit

#utilisation de lambda!!
def in_bounds(x : int, y : int) -> bool:
    num_in_bounds = lambda n : n >= 0 and n < RESOLUTION
    return num_in_bounds(x) and num_in_bounds(y)

def get_neighbors(x : int, y : int, grid : list) -> int:
    n = 0
    #parcourir tous les décalages voisins
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            # ignore home cell
            if dx == 0 and dy == 0:
                continue
            
            #obtenir les coordonnées réelles du voisin
            nx = x + dx
            ny = y + dy
            if not in_bounds(nx, ny):
                continue

            if get_cell_val(nx, ny, grid):
                n += 1

    return n

# settings
CANVAS_SIZE = 600
RESOLUTION  = 65
INTERVAL    = 50
CELL_SIZE   = CANVAS_SIZE / RESOLUTION
PL = "purple"
WH = "white"

# les variables globales
root = samira.Tk()
canvas = samira.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=PL)
canvas.pack()

#fonction qui dessine 
def draw_cell(x : int, y : int):
    canvas_x = x * CELL_SIZE
    canvas_y = y * CELL_SIZE
    canvas.create_rectangle(canvas_x, canvas_y, canvas_x + CELL_SIZE, canvas_y + CELL_SIZE, fill=WH, outline="")

def update(old_grid : list):
    canvas.delete("all")
    grid = old_grid.copy()

    for y in range(RESOLUTION):
        for x in range(RESOLUTION):
            n = get_neighbors(x, y, old_grid)

            #appliquer les règles du jeu de la vie
            if n < 2 or n > 3:
                set_cell_val(x, y, False, grid)
            #sinon, les cellules sont identiques à celles de la génération précédente, ce qui est pris en compte dans la copie de l'ancienne grille dans la nouvelle grille
            elif n == 3:
                set_cell_val(x, y, True, grid)

            #dessiner uniquement la cellule si elle est vivante, pour la performance
            if get_cell_val(x, y, grid):
                draw_cell(x, y)

    root.after(INTERVAL, update, grid)

#le programme commence
#le stockage dans l'array grid
grid = []
max_val = 2**RESOLUTION - 1

#randomiser l'état initial de la grille
for y in range(RESOLUTION):
    #puisque les lignes sont stockées dans des entiers, nous pouvons randomzie les lignes en lui attribuant un int aléatoire
    grid.append(random.randint(0, max_val))

update(grid)
root.mainloop()