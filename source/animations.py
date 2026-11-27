from rendering import Renderer, Texture2D
from program import Player
import time
from vectors import Vector2


class Animations():
    def __init__(self, images, frameRate):
        self.images = images
        self.frames = len(images)
        self.frameRate = frameRate
        self.time = 0

    def update(self, deltaTime):

        self.time += deltaTime
        self.time = self.time % self.frames
        self.index = int(self.time)

    def image(self):

        return self.images[self.index]