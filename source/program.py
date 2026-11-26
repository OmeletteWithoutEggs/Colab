import pyray as raylib
from pyray import Color
from source.vectors import Vector2
from source.rendering import Renderer
from source.player import Player
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
        self.camera = self.renderer.camera

        self.player = Player((0,0),(30,30))

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
                    
                    self.start()

            self.render()


    def tick(self):
        self.deltaTime = raylib.get_frame_time()
        self.player.handleInput()
        self.player.updatePhysics(self.deltaTime)

    def renderDebug(self):
        raylib.draw_fps(10,10)

    def render(self):
        with self.renderer:
            self.player.draw(self.renderer)


            if self.debugMode:
                self.renderDebug()





