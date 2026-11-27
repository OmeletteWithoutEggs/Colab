from source.rendering import Renderer, Texture2D
import time
import os

class Animations():
    def __init__(self, path, frameRate):
        extraPaths = os.listdir(path)
        self.images = [Texture2D(path + extraPath) for extraPath in extraPaths]
        self.frames = len(self.images)
        self.frameRate = frameRate
        self.startTime = time.time()

    def getCurrentFrame(self):

        self.time = time.time() - self.startTime
        self.index = int(self.time % self.frames)
        return self.images[self.index]