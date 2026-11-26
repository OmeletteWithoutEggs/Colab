from source.vectors import Vector2
from source.collisions import AxisAlignedCollider
import source.collisions as collisions
class Player:
    def __init__(self,position,size):
        self.position = Vector2(position)
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))
        