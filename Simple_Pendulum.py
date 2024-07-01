import pyglet
from pyglet.window import Window
from pyglet import app
from pyglet.graphics import Batch
from pyglet.shapes import *
from pyglet import gui
from pyglet.window import key
import random
from Classes.camera import Camera
from Classes.vec2 import Vec2
import math
import time

class Pendulum:
    def __init__(self, arm_length: float, gravity: float = 9.81, position: Vec2 = Vec2()) -> None:
        self.arm_length = arm_length
        self.gravity = gravity
        self.time = 0
        self.position = position
        self.period = self.__calculate_period()
        self.displacement = self.__calculate_displacement(0)
        self.end_position = self.__calculate_end_position()

    def __calculate_period(self):
        return ((2 * math.pi) * math.sqrt(self.arm_length / self.gravity))
    
    def __calculate_displacement(self, time):
        return (0.32 * math.cos(((2 * math.pi) / self.period) * time))

    def __calculate_end_position(self) -> Vec2:
        #need arm length and angular displacement
        return Vec2(self.position.a + self.arm_length * math.cos(self.displacement), self.position.b + self.arm_length * math.sin(self.displacement))

    def update(self, dt):
        self.time += dt
        self.displacement = self.__calculate_displacement(self.time + dt)

if __name__ == "__main__":
    screen_dim = Vec2(640, 480)
    main_window = Window(screen_dim.a, screen_dim.b, "Main Render Window")

    target = Pendulum(1, 3)
    target_line = Line(screen_dim.a / 2, screen_dim.b * 0.7, screen_dim.a / 2, screen_dim.b * 0.15, 3, (255, 255, 155, 255) )
    text_batch = Batch()

    def pendulum_update(dt):
        target.update(dt)

    @main_window.event
    def on_draw():
        target_line.rotation = math.degrees(target.displacement)
        main_window.clear()
        target_line.draw()
        text_batch.draw()

    pyglet.clock.schedule_interval(pendulum_update, 1/60)
    app.run(1/144)

