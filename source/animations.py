from source.rendering import Renderer, Texture2D
import time
import os

class Animations():
    def __init__(self, path, frameRate):
        extraPaths = os.listdir(path)
        self.images = [Texture2D(path+"/" + extraPath) for extraPath in extraPaths]
        self.frames = len(self.images)
        self.secPerFrame = 1/frameRate
        self.frameRate = frameRate

    def getCurrentFrame(self):

        self.index = int(time.time() / self.secPerFrame) % int(self.frameRate)
        return self.images[self.index]