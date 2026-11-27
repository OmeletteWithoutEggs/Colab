from source.vectors import Vector2
from source.collisions import AxisAlignedCollider, Solver
from source.animations import Animations
import enum
import pyray as raylib
from source.rendering import Renderer

class PlayerStates(enum.Enum):
    DEAD = enum.auto()
    NORMAL = enum.auto()


class Player:
    def __init__(self,position,size):
        self.position = Vector2(position)
        self.velocity = Vector2(0,0)
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))
        self.moveSpeed = 300
        self.images = Animations("assets/images/player", 6)
    

    def collideLevel(self,colliders:list[AxisAlignedCollider]):
        for collider in colliders:
            overlap = Solver.getAABBCollision(self.collider,collider)

    def collideBullets(self,colliders:list[AxisAlignedCollider]):
        for collider in colliders:
            if Solver.getAABBCollision(self.collider,collider):
                self.state = PlayerStates.DEAD
                break

    def handleInput(self):
        movement = Vector2(0,0)
        if raylib.is_key_down(raylib.KeyboardKey.KEY_W):
            movement.y -= 1
        if raylib.is_key_down(raylib.KeyboardKey.KEY_S):
            movement.y += 1
        if raylib.is_key_down(raylib.KeyboardKey.KEY_A):
            movement.x -= 1
        if raylib.is_key_down(raylib.KeyboardKey.KEY_D):
            movement.x += 1

        self.velocity += movement.normalised() * self.moveSpeed

    def updatePhysics(self,deltaTime):
        self.position += self.velocity * deltaTime
        self.velocity = Vector2(0,0)


    def draw(self, renderer:Renderer):
        #renderer.drawRectanglePro(self.position, (self.width,self.height),(self.width/2,self.height/2),0,(255,255,255,255))
        renderer.drawTexturePro(self.images.getCurrentFrame(), self.position, (self.width, self.height))
