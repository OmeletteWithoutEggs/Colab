from source.vectors import Vector2
from source.player import Player
from source.rendering import Renderer
from source.collisions import AxisAlignedCollider
import enum

class Bullet:
    def __init__(self,position,size,speed):
        self.position = Vector2(position)
        self.targetPosition = Vector2(0,0)
        self.speed = speed
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))

    def update(self,deltaTime):
        self.position += (self.targetPosition - self.position).normalised() * self.speed * deltaTime

class EnemyStates(enum.Enum):
    IDLE = enum.auto()
    FLEEING = enum.auto()
    MOVING = enum.auto()


class Enemy:
    def __init__(self,position,size,speed):
        self.state = EnemyStates.IDLE
        self.fleeDistance = 200
        self.fleeStep = 400
        self.targetPosition = None
        self.position = Vector2(position)
        self.velocity = Vector2(0,0)
        self.moveSpeed = speed
        self.width , self.height = size
        self.collider = AxisAlignedCollider(self.position,(self.width,self.height),(self.width/2,self.height/2))

    def update(self,deltaTime):
        self.position += self.velocity * deltaTime
        self.velocity = Vector2(0,0)

    def draw(self, renderer:Renderer):
        renderer.drawRectanglePro(self.position, (self.width,self.height),(self.width/2,self.height/2),0,(255,0,0,255))

    def move(self, player:Player):
        playerToSelf = self.position - player.position
        distanceToPlayer = playerToSelf.magnitude
        match self.state:
            case EnemyStates.IDLE:
                if distanceToPlayer < self.fleeDistance:
                    self.targetPosition = self.position + playerToSelf.normalised(self.fleeStep)
                    self.state = EnemyStates.FLEEING
                else:
                    self.targetPosition = None
            case EnemyStates.FLEEING:
                selfToTarget = self.targetPosition - self.position

                if distanceToPlayer < self.fleeStep:
                    self.velocity = selfToTarget.normalised(self.moveSpeed)
                else:
                    self.state = EnemyStates.IDLE
