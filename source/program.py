lazy import raylibpy as raylib
from raylibpy import Color
from source.vectors import Vector2
from source.player import Player
from source.rendering import Renderer
from source.recording import Recorder
from source.world import Scene, StaticPlatform, Finish, Ghost
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

        self.scene = Scene("saves/best.json")
        # self.scene.addPlatform(StaticPlatform((100,200),(200,40)))
        # self.scene.addPlatform(StaticPlatform((400,300),(200,40)))
        # self.scene.addPlatform(StaticPlatform((100,400),(200,40)))
        # self.scene.addPlatform(StaticPlatform((400,500),(200,40)))
        # self.scene.addPlatform(StaticPlatform((100,600),(200,40)))


        #self.scene.addPlatform(StaticPlatform((500,350),(200,40)))
        # self.scene.addPlatform(StaticPlatform((100,0),(40,200)))

        self.scene.addSpawnPoint(Vector2(0,800))
        self.scene.addSpawnPoint(Vector2(700,800))
        self.scene.addSpawnPoint(Vector2(350,800))
        self.scene.addSpawnPoint(Vector2(700,0))

        self.scene.setFinish(Finish((-200,40),(120,120)))
        self.player = Player((950,500),(30,50),Color(250, 189, 47,255))
        self.recorder = Recorder(0.05)

        self.renderer = Renderer(700,800,"Program")
        self.renderer.loadFont("assets\\fonts\\firjar\\Firjar-Bold.ttf")

        self.timer = 0
        self.roundDuration = 10
        self.activeSpawn = Vector2(0,0)
        self.player.setPosition(self.activeSpawn)


    def start(self):
        self.runStart = time.time()
        self.state = GameStates.RUNNING
        self.recorder.record(self.player.position,self.timer)

    def reset(self):
        self.state = GameStates.PAUSED
        self.player.reset(self.activeSpawn)
        self.scene.reset()
        self.recorder.reset()
        self.timer = 0

    def run(self):
        print(self.scene.bounds)
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
        self.timer = time.time() - self.runStart

        self.scene.updateGhosts(self.timer)
        self.updatePlayer()
        self.recorder.record(self.player.position,self.timer)
        self.checkGameConditions()


    def updatePlayer(self):
        self.player.processInput()
        self.player.updatePhysics(self.deltaTime)
        self.player.collide(self.scene.getColliders(),self.scene.bounds)

    def checkGameConditions(self):
        if self.player.checkFinish(self.scene.finish):
            # self.activeSpawn = self.recorder.recording[list(self.recorder.recording.keys())[len(self.recorder.recording.keys())//2]].copy()
            # self.activeSpawn = self.scene.getSpawnPoint()
            self.activeSpawn = Vector2(random.randint(-950,950),random.randint(-500,500))
            self.recorder.record(self.player.position,self.timer,hard = True)
            recording = self.recorder.getRecording()
            self.scene.addGhost(Ghost(recording,self.player.width,self.player.height))
            self.reset()
            while self.player.checkGhosts(self.scene.getGhostColliders()):
                self.activeSpawn = Vector2(random.randint(-950,950),random.randint(-500,500))
                

        elif self.player.checkGhosts(self.scene.getGhostColliders()) or self.timer > self.roundDuration:
            self.reset()   

    def renderDebug(self):
        self.player.drawDebug(self.renderer)
        self.scene.drawDebug(self.renderer)
        self.recorder.drawDebug(self.renderer)
        raylib.draw_fps(10,10)

    def render(self):
        with self.renderer:
            self.scene.draw(self.renderer)
            self.player.draw(self.renderer)
            self.renderer.drawText(round(self.timer,2),(10,10),30,(255,255,255,255),alignement="left")

            if self.debugMode:
                self.renderDebug()





