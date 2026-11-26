lazy import pyray as raylib
from pyray import Color
from source.vectors import Vector2
from source.rendering import Renderer
import enum
import time
import random

class GameStates(enum.Enum):
    PAUSED = enum.auto()
    RUNNING = enum.auto()


class Program:

    def __init__(self,debugMode):
        self.state = GameStates.PAUSED
        self.debugMode = debugMode


        self.renderer = Renderer(700,800,"Program")
        self.renderer.loadFont("assets\\fonts\\firjar\\Firjar-Bold.ttf")





    def start(self):
        self.runStart = time.time()
        self.state = GameStates.RUNNING

    def reset(self):
        self.state = GameStates.PAUSED

    def run(self):

        while not raylib.window_should_close():
            if raylib.is_key_pressed(raylib.KeyboardKey.KEY_GRAVE):
                self.debugMode = not self.debugMode

            match self.state:
                case GameStates.RUNNING:
                    self.tick()
                case GameStates.PAUSED:
                    if raylib.is_key_pressed(raylib.KEY_ENTER):
                        self.start()

            self.render()


    def tick(self):
        self.deltaTime = raylib.get_frame_time()







 

    def renderDebug(self):
        raylib.draw_fps(10,10)

    def render(self):
        with self.renderer:


            if self.debugMode:
                self.renderDebug()





