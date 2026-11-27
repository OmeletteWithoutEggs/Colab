from rendering import Renderer, Texture2D
from program import Player
import time
import os
from vectors import Vector2

class Animations():
    def __init__(self, path, frameRate):
        extraPaths = os.listdir(path)
        self.images = [Texture2D(path + extraPath) for extraPath in extraPaths]
        self.frames = len(self.images)
        self.frameRate = frameRate
        self.time = 0

    def update(self, deltaTime):

        self.time += deltaTime
        self.time = self.time % self.frames
        self.index = int(self.time)

    def getCurrentFrame(self):

        return self.images[self.index]