import pyray as raylib
from pyray import Color
from source.vectors import Vector2
from source.rendering import Renderer,Texture2D
from source.player import Player
from source.world import Scene
from source.enemies import Enemy
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

        self.scene = Scene((self.renderer.width,self.renderer.height))
        self.scene.addEnemy(Enemy(Vector2(300,300),(30,30),800))

        self.player = Player((-200,-200),(50,50))
        self.texture = Texture2D("assets/images/test/mountain.jpg")

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
        self.scene.enemies[0].move(self.player)
        self.scene.enemies[0].update(self.deltaTime)

    def renderDebug(self):
        raylib.draw_fps(10,10)

    def render(self):
        with self.renderer:
            position = raylib.get_screen_to_world_2d(raylib.get_mouse_position(),self.camera)

            # self.renderer.drawTexturePro(self.texture,(position.x,position.y),self.texture.size,rotation=-90,origin=(self.texture.size/2))
            self.player.draw(self.renderer)
            self.scene.enemies[0].draw(self.renderer)


            if self.debugMode:
                self.renderDebug()
       
        raylib.draw_fps(10,10)

        self.renderer.display()
