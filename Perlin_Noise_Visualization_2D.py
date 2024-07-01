import pyglet
from pyglet.window import Window
from pyglet import app
from pyglet.graphics import Batch
from pyglet.shapes import *
from pyglet import gui
from pyglet.window import key
from pyglet import gl
import random
from Classes.camera import Camera
from Classes.vec2 import Vec2
import math
import time

def denormalize(noisevalue: float, minelevation, maxelevation) -> float:
    return (noisevalue * (maxelevation - minelevation) + minelevation)


    

if __name__ == "__main__":
    screen_dim = Vec2(720, 720)
    main_window = Window(screen_dim.a, screen_dim.b, "Main Render Window")
    pyglet.gl.glClearColor(0.15, 0.25, 0.1, 1.0)

    grid_lines_batch = Batch()
    mark_batch = Batch()


    """
    SET PROGRAM VALUES HERE
    """
    #Elevation values are float from 0.0 to 1.0
    min_elevation = 0.4
    max_elevation = 0.55
    #Resolution is the number of 'columns'
    resolution = 144
    #Frequency is the value that determines the number of sample noise points taken at equal intervals
    #Lower means more [For the sake of your sanity and time keep the value greater than 1 atleast]
    frequency = 2




    sample_amount = math.floor(math.pow(resolution, 1/frequency))
    sample_map, height_map = [], [None] * (resolution + 1)
    for i in range(sample_amount + 1):
        sample_map.append(denormalize(random.randint(0, 100) / 100, min_elevation, max_elevation))
    print(sample_map)

    print(len(sample_map), sample_amount)

    for i in range(len(sample_map)):
        height_map[int(i * resolution * (1 / (sample_amount)))] = sample_map[i]
    

    #Attempting to plot set of circles to visualize the terrain height
    fcirc = []
    marco_increment = screen_dim.a / sample_amount
    micro_increment = (screen_dim.a / sample_amount) / sample_amount
    for i in range(sample_amount):
        index = int(i * resolution * (1 / (sample_amount)))
        for j in range(sample_amount * (index + 1) - sample_amount * index):
            fcirc.append(Circle(
                ((i * (marco_increment)) + (j * (micro_increment))),
                (sample_map[i] * screen_dim.b) - (screen_dim.b * ((sample_map[i] - sample_map[i + 1]) * (j / sample_amount))), 
                4,
                8,
                (0,0,255,155), mark_batch))
            #print(fcirc[len(fcirc) - 1].x)

            print((math.pi * (j / sample_amount)) - (math.pi / 2))


    #Maps points on the screen of the sample heights
    test_vis = []
    for i in range(sample_amount):
        if i != 0:
            test_vis.append(Circle((i/sample_amount) * screen_dim.a, sample_map[i] * screen_dim.b, 5, 12, (255,0,0,155), mark_batch))

        else:
            test_vis.append(Circle((0) * screen_dim.a, sample_map[0] * screen_dim.b, 12, 12, (255,0,0,155), mark_batch))

    map_batch = Batch()
        
    test_vis.append(Circle((1) * screen_dim.a, sample_map[len(sample_map) - 1] * screen_dim.b, 12, 12, (255,0,0,155), mark_batch))

    #Grid line initialization
    vertical_lines, horizontal_lines = [], []
    for i in range(resolution):
        vertical_lines.append(Line((1/resolution) * screen_dim.a * i, 0, (1/resolution) * screen_dim.a * i, screen_dim.b, 1, (255,255,255,100), grid_lines_batch))
        horizontal_lines.append(Line(0, (1/resolution) * screen_dim.b * i, screen_dim.a, (1/resolution) * screen_dim.b * i, 1, (255,255,255,100), grid_lines_batch))
    

    @main_window.event
    def on_draw():
        main_window.clear()
        grid_lines_batch.draw()
        mark_batch.draw()
        map_batch.draw()

    app.run(1/30)