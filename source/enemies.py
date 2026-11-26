from source.vectors import Vector2
from 

class Bullet:
    def __init__(self,position,size):
        self.position = Vector2(position)
        self.width , self.height = size
        self.collider = 