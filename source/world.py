from source.enemies import Bullet,Enemy
from vectors import Vector2

class Scene:
    def __init__(self,size):
        self.bullets : list[Bullet] = []
        self.enemies : list[Enemy] = []
        self.bounds = Vector2(size)
    def getEnemyColliders(self):
        pass

    