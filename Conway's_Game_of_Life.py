#from __future__ import annotations
import pyglet
from pyglet.window import Window
from pyglet import app
from pyglet.graphics import Batch
from pyglet.shapes import *
from pyglet.window import key
import random
from Classes.camera import Camera
from Classes.camera import DIRECTIONS

class Cell:
    def __init__(self, col, row):
        self.column = col
        self.row = row
        self.alive = False
        self.visual = None
        self.neighbors = 0

    def kill(self):
        self.alive = False

    def birth(self):
        self.alive = True

def reproduction(cell_matrix):
    """Determine if cells are to reproduce or die"""
    for i in range(len(cell_matrix)):
        for j in range(len(cell_matrix[i])):
            neighbors = 0
            
            try:
                if cell_matrix[i - 1][j - 1].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i - 1][j].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i - 1][j + 1].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i][j - 1].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i][j + 1].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i + 1][j - 1].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i + 1][j].alive == True: neighbors += 1
            except:None
            try:
                if cell_matrix[i + 1][j + 1].alive == True: neighbors += 1
            except:None

            cell_matrix[i][j].neighbors = neighbors

    for i in range(len(cell_matrix)):
        for j in range(len(cell_matrix[i])):
            if cell_matrix[i][j].alive == False:    #If the current cell is dead
                if cell_matrix[i][j].neighbors == 3:    #Birth Case
                    cell_matrix[i][j].alive = True
                    

            elif cell_matrix[i][j].alive == True:   #If the current cell is alive
                if cell_matrix[i][j].neighbors < 2:                                         #Isolation Case
                    cell_matrix[i][j].alive = False
                elif cell_matrix[i][j].neighbors == 2 or cell_matrix[i][j].neighbors == 3:  #Survival Case
                    pass
                elif cell_matrix[i][j].neighbors > 3:                                       #Overcrowding Case
                    cell_matrix[i][j].alive = False

    return cell_matrix
                

def visualization(cell_matrix, visualization_matrix):
    """Update cell color based on living status"""
    for i in range(len(cell_matrix)):
        for j in range(len(cell_matrix[i])):
            if cell_matrix[i][j].alive == True:
                visualization_matrix[i][j].color = (255, 255, 255, 175)
            else:
                visualization_matrix[i][j].color = (25, 25, 25, 175)
    return visualization_matrix


rows = 128
columns =  128
width, height = 1280, 720
render_window = Window(width, height, "Visualization Window")
cellBatch = Batch()

#Creates 2D List of Cells
cellList = []
cellListDraw = []
for i in range(rows):
    cellList.append([])
    cellListDraw.append([])
    for j in range(columns):
        cellList[i].append(Cell(j, i))

        cellListDraw[i].append(
            Rectangle(
            x = (i * (width/columns)),
            y = (j * (height/rows)),
            width = (width/columns),
            height = (height/rows),
            color = (255, 255, 50, 175),
            batch = cellBatch
        ))




for i in range(len(cellList)):
    for j in range(len(cellList[i])):
        if random.randint(0, 100) < 35:
            cellList[i][j].alive = True



cellListDraw = visualization(cellList, cellListDraw)


window_camera = Camera(0.1)
keys = key.KeyStateHandler()
render_window.push_handlers(keys)
grid_lines_batch = Batch()
grid_lines_vert, grid_lines_horz = [], []




for i in range(rows):
    grid_lines_horz.append(Line(0, i * (height/rows), width, i * (height/rows), 1, (255,255,255,175), grid_lines_batch, None))

for i in range(columns):
    grid_lines_vert.append(Line(i * (width/columns), 0, i * (width/columns), height, 1, (255, 255, 0, 175), grid_lines_batch, None))



@render_window.event
def on_draw():
    global cellList
    global cellListDraw
    if keys[key.W]:
        window_camera.move(DIRECTIONS.UP)
    if keys[key.S]:
        window_camera.move(DIRECTIONS.DOWN)
    if keys[key.A]:
        window_camera.move(DIRECTIONS.LEFT)
    if keys[key.D]:
        window_camera.move(DIRECTIONS.RIGHT)

    for i in range(len(grid_lines_horz)):
        pass

    for i in range(len(grid_lines_vert)):
        pass

    cellList = reproduction(cellList)
    cellListDraw = visualization(cellList, cellListDraw)
    

    
    render_window.clear()
    cellBatch.draw()
    #grid_lines_batch.draw()

app.run(1/60)