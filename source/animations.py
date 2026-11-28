from rendering import Renderer, Texture2D
from program import Player
import time
from vectors import Vector2


class Animations():
    def __init__(self, images, frameRate):
        self.images = images
        self.frameRate = frameRate
        self.currentImage = self.images[0]