from source.vectors import Vector2
from source.player import Player
from source.rendering import Renderer
from source.animations import Animations
from source.collisions import AxisAlignedCollider



class Bullet:
    def __init__(self,position,size,speed):
        self.position = Vector2(position)
        self.targetPosition = Vector2(0,0)
        self.speed = speed
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))

    def update(self,deltaTime):
        self.position += (self.targetPosition - self.position).normalised() * self.speed * deltaTime


class Enemy:
    def __init__(self,position,size,speed):
        self.position = Vector2(position)
        self.velocity = Vector2(0,0)
        self.moveSpeed = speed
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))
        self.images = Animations("assets/images/enemy", 6)

    def update(self,deltaTime):
        self.position += self.velocity * deltaTime

    def draw(self, renderer:Renderer):
        renderer.drawTexturePro(self.images.getCurrentFrame(), self.position, (self.width, self.height))

    def move(self, player:Player):
        diffPos = self.position - player.position
        diffPos.normalised(self.moveSpeed)
        self.velocity = diffPos
