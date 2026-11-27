from source.enemies import Bullet,Enemy
from source.vectors import Vector2
from source.collisions import AxisAlignedCollider

class Scene:
    def __init__(self,size):
        self.bullets : list[Bullet] = []
        self.enemies : list[Enemy] = []
        self.bounds = Vector2(size)

    def getEnemyColliders(self) -> list[AxisAlignedCollider]:
        colliders  = []
        for enemy in self.enemies:
            if hasattr(enemy,"collider"):
                colliders.append(enemy.collider())
        return colliders
    
    def getBulletColliders(self) -> list[AxisAlignedCollider]:
        colliders  = []
        for bullet in self.bullets:
            if hasattr(bullet,"collider"):
                colliders.append(bullet.collider())
        return colliders

    def addEnemy(self,enemy):
        self.enemies.append(enemy)

    def addBullet(self,bullet):
        self.bullets.append(bullet)

    