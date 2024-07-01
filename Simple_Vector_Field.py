import pyglet
from pyglet.window import Window
from pyglet import app
from pyglet.graphics import Batch
from pyglet.shapes import *
from pyglet.window import key
import random
from Classes.camera import Camera
from Classes.vec2 import Vec2
import math
import time



class Vector_Line:
    def __init__(self, vector_batch, position: Vec2):
        self.position = position
        self.max_mag = 35
        self.direction = math.radians(0)
        self.visual = Line(self.position.a, self.position.b,
                           (self.max_mag * math.cos(self.direction) + self.position.a),
                           (self.max_mag * math.sin(self.direction) + self.position.b),
                           2, (255,0,0,255), vector_batch)
    
    def set_magnitude(self, value: float):
        self.visual.x2 = ((self.max_mag * value) + self.position.a)
        #self.visual.y2 = ((self.max_mag * value) * math.sin(self.direction) + self.position.b)

class Screen_Grid:
    def __init__(self, columns, screen_width, screen_height) -> None:
        self.set_columns(columns, screen_width, screen_height)
        self.batch = Batch()
        self.vector_batch = Batch()
        self.create_grid_visuals(screen_width, screen_height)
        self.vertex_vectors = []

    def set_vectors(self, screen_size: Vec2):
        self.vertex_vectors = []
        #Column major iteration
        for i in range(self.columns):
            for j in range(self.rows):
                self.vertex_vectors.append(Vector_Line(self.vector_batch, Vec2(i * (screen_size.a / self.columns), j * (screen_size.b / self.rows))))
    
    def update_vectors(self, mouse_position: Vec2):
        time_dis = []
        time_set_mag = []
        time_set_visual = []
        for i in range(len(self.vertex_vectors)):
            
            time_init = time.time()
            distance = (math.sqrt(abs(mouse_position.a - self.vertex_vectors[i].position.a) + 
                                  abs(mouse_position.b - self.vertex_vectors[i].position.b)))
            time_dis.append(time.time() - time_init)
            
            threshold = 20

            if distance == 0:
                self.vertex_vectors[i].visual.x2 = ((self.vertex_vectors[i].max_mag * (0)) + self.vertex_vectors[i].position.a)
            elif distance < threshold:
                self.vertex_vectors[i].visual.x2 = ((self.vertex_vectors[i].max_mag * (1 - (distance/threshold))) + self.vertex_vectors[i].position.a)
            else:
                self.vertex_vectors[i].visual.x2 = ((self.vertex_vectors[i].max_mag * (0)) + self.vertex_vectors[i].position.a)
            time_set_mag.append(time.time() - time_dis[i])

            delta_dir = math.atan2( mouse_position.b - self.vertex_vectors[i].position.b , self.vertex_vectors[i].position.a - mouse_position.a)
            self.vertex_vectors[i].visual.rotation = math.degrees(delta_dir)
            time_set_visual.append(time.time() - time_set_mag[i])

    def set_columns(self, columns, screen_width, screen_height) -> None:
        self.columns = columns
        self.__set_rows(self.columns, screen_width, screen_height)

    def __set_rows(self, columns, screen_width, screen_height) -> None:
        self.rows = int(columns * (screen_height/screen_width))

    def create_grid_visuals(self, screen_width, screen_height) -> None:
        self.grid_visuals = []
        for i in range(self.columns):
            self.grid_visuals.append(Line(int(i * (screen_width/self.columns)), 0, 
                                          int(i * (screen_width/self.columns) ), 
                                          screen_height, 1, (255,255,255,255), self.batch))
        for i in range(self.rows):
            self.grid_visuals.append(Line(0, int(i * (screen_height/self.rows)), 
                                          screen_width, int(i * (screen_height/self.rows)), 
                                          1, (255,255,255,255), self.batch))


if __name__ == "__main__":
    screen_dim = Vec2(1280, 720)
    main_window = Window(screen_dim.a, screen_dim.b, "Main Render Window")
    grid = Screen_Grid(36, screen_dim.a, screen_dim.b)
    grid.set_vectors(screen_dim)

    @main_window.event
    def on_mouse_motion(x, y, dx, dy):
        grid.update_vectors(Vec2(x, y))

    @main_window.event
    def on_draw():
        main_window.clear()
        grid.batch.draw()
        grid.vector_batch.draw()

    app.run(1/60)
