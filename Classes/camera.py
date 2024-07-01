from Classes.vec2 import Vec2
from enum import Enum

class DIRECTIONS(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class Camera:
    def __init__(self, speed: float = 1.0, zoom: float = 1.0) -> None:
        self.position = Vec2(0, 0)
        self.speed = speed
        self.zoom = zoom
    
    def move(self, direction: DIRECTIONS) -> None:
        if direction == "UP":
            self.position = self.position.add(Vec2(0, 1 * self.speed))
        if direction == "DOWN":
            self.position = self.position.add(Vec2(0, -1 * self.speed))
        if direction == "LEFT":
            self.position = self.position.add(Vec2(-1 * self.speed, 0))
        if direction == "RIGHT":
            self.position = self.position.add(Vec2(1 * self.speed, 0))