from source.vectors import *
from source.rendering import Renderer
import sys

@dataclass(init=True)
class AxisAlignedCollider:
    width :float
    height:float
    position:Vector2
    offset: Vector2

    def __init__(self,position,size,offset = None):
        self.width, self.height = Vector2(size)
        if isinstance(position,Vector2):
            self.position = position
        else:
            self.position = Vector2(position)

        if offset:
            self.offset = Vector2(offset)
        else:
            self.offset = Vector2(0,0)

    @property
    def left(self):
        return self.position.x - self.offset.x

    @property
    def right(self):
        return self.position.x + self.width - self.offset.x

    @property
    def top(self): 
        return self.position.y - self.offset.y

    @property
    def bottom(self):
        return self.position.y + self.height - self.offset.y

    @property
    def center(self):
        return self.position - self.offset + (Vector2(self.width,self.height)/2)


    def draw(self,renderer:Renderer):
        renderer.drawRectangleLines(self.position-self.offset,(self.width,self.height),3,(142, 179, 95, 255))

    def __repr__(self):
        return f"AxisAlignedCollider(\n  Position:{self.position-self.offset}\n  Size:({self.width}, {self.height}))"


class MeshCollider:
    def __init__(self,points: list[Vector2]):
        "points in clockwise order"

        self.points : list[Vector2] = [Vector2(point) for point in points]
        self._constructNormals()

    def _constructNormals(self):
        self.normals = []
        for i in range(len(self.points)):
            vector = self.points[i] - self.points[i-1]
            vector.rotate(-90,degrees=True)
            self.normals.append(vector.normalised())


    def draw(self,position,renderer:Renderer):
        renderer.drawLineStrip(self.points,3,(142, 179, 95, 255),position=position)

class Solver:
    @staticmethod
    def getAABBCollision(collider1:AxisAlignedCollider, collider2:AxisAlignedCollider):
        xOverlap = min(collider1.right,collider2.right) - max(collider1.left,collider2.left)
        yOverlap = min(collider1.bottom,collider2.bottom) - max(collider1.top,collider2.top)

        if xOverlap > 0 and yOverlap > 0:
            return Vector2(xOverlap,yOverlap)

        return False
    
    @staticmethod
    def checkMeshCollision(collider1:MeshCollider, position1:Vector2, collider2:MeshCollider, position2:Vector2, renderer:Renderer):
        normals = collider1.normals + collider2.normals
        bestMinimumTranslationDistance = sys.maxsize
        heldNormal = None
        for normal in normals:
            axisPointsCollider1 = Solver._projectPointsOnAxis(collider1,position1,normal)
            axisPointsCollider2 = Solver._projectPointsOnAxis(collider2,position2,normal)

            collider1MaxAxis = max(axisPointsCollider1)
            collider1MinAxis = min(axisPointsCollider1)
            collider2MaxAxis = max(axisPointsCollider2)
            collider2MinAxis = min(axisPointsCollider2)

            

            if collider1MaxAxis > collider2MinAxis and collider2MaxAxis > collider1MinAxis:
                translationDistance = collider1MaxAxis - collider2MinAxis

                if translationDistance < bestMinimumTranslationDistance:
                    bestMinimumTranslationDistance = translationDistance
                    heldNormal = normal

            else:
                #no collision
                Solver._drawDebugAxis(renderer, normal, position1, position2, collider1MinAxis, collider1MaxAxis, collider2MinAxis, collider2MaxAxis)
                return None
            if normal == normals[-1]:
                pass

        Solver._drawDebugAxis(renderer, heldNormal, position1, position2, collider1MinAxis, collider1MaxAxis, collider2MinAxis, collider2MaxAxis)
        return bestMinimumTranslationDistance
    
    @staticmethod
    def _projectPointsOnAxis(collider:MeshCollider, position:Vector2, axis:Vector2):
        axisPoints = []
        for point in collider.points:
            axisPoints.append(Vector2.dot(point+position,axis))

        return axisPoints

    @staticmethod
    def _drawDebugAxis(renderer:Renderer, normal:Vector2, position1:Vector2, position2:Vector2, c1Min, c1Max, c2Min, c2Max):
        midpoint = (position1 + position2) * 0.5
        tangent = Vector2(-normal.y, normal.x)

        padding = 50.0
        perpendicularOffset = tangent * (Vector2.dot(midpoint, tangent) + padding)

        totalMinPos = (normal * min(c1Min, c2Min)) + perpendicularOffset
        totalMaxPos = (normal * max(c1Max, c2Max)) + perpendicularOffset

        c1MinPos = (normal * c1Min) + perpendicularOffset
        c1MaxPos = (normal * c1Max) + perpendicularOffset
        c2MinPos = (normal * c2Min) + perpendicularOffset
        c2MaxPos = (normal * c2Max) + perpendicularOffset


        renderer.drawLineDashed(totalMaxPos, totalMinPos, 3, 3, (110, 155, 120, 255))
        renderer.drawCircle(c1MinPos, 2, (240, 128, 28, 255))
        renderer.drawCircle(c1MaxPos, 2, (240, 128, 28, 255))
        renderer.drawCircle(c2MinPos, 2, (85, 145, 152, 255))
        renderer.drawCircle(c2MaxPos, 2, (85, 145, 152, 255))
