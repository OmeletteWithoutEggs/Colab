import math
import numpy as np
from swizzle import swizzle
from dataclasses import dataclass

@swizzle
@dataclass(init= False,slots = True)
class Vector2:
    x: float
    y: float


    def __init__(self, x, y=None):
        if y is not None:
            self.x = x
            self.y = y
        elif isinstance(x, (list, tuple, np.ndarray,Vector2)):
            self.x, self.y = x
        else:
            self.x = x
            self.y = x
    
    #addition
    def __add__(self,other):
        if isinstance(other,Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other,(list,tuple,np.ndarray)):
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return Vector2(self.x + other, self.y + other)
        
    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self,other):
        if isinstance(other,Vector2):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other,(list,tuple,np.ndarray)):
            self.x += other[0]
            self.y += other[1]
            return self
        else:
            self.x += other
            self.y += other
            return self
        
    #subtraction 
    def __sub__(self,other):
        if isinstance(other,Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other,(list,tuple,np.ndarray)):
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            return Vector2(self.x - other, self.y - other)
    
    def __rsub__(self, other):
        if isinstance(other,Vector2):
            return Vector2(other.x - self.x, other.y - self.y)
        elif isinstance(other,(list,tuple,np.ndarray)):
            return Vector2(other[0] - self.x, other[1] - self.y)
        else:
            return Vector2(other - self.x, other - self.y)
        
    
    def __isub__(self,other):
        if isinstance(other,Vector2):
            self.x -= other.x
            self.y -= other.y
            return self
        elif isinstance(other,(list,tuple,np.ndarray)):
            self.x -= other[0]
            self.y -= other[1]
            return self
            
        else:
            self.x -= other
            self.y -= other
            return self

    #multiplication
    def __mul__(self,other):
        if isinstance(other,Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other,(list,tuple,np.ndarray)):
            return Vector2(self.x * other[0], self.y * other[1])
        else:
            return Vector2(self.x * other, self.y * other)
        
    
    def __rmul__(self,other):
        return self.__mul__(other)
        
    def __imul__(self,other):
        if isinstance(other,Vector2):
            self.x *= other.x
            self.y *= other.y
            return self
        elif isinstance(other,(list,tuple,np.ndarray)):
            self.x *= other[0]
            self.y *= other[1]
            return self
            
        else:
            self.x *= other
            self.y *= other
            return self


    #division
    def __truediv__(self, other):
        try:
            if isinstance(other, Vector2):
                return Vector2(self.x / other.x, self.y / other.y)
            elif isinstance(other, (list, tuple, np.ndarray)):
                return Vector2(self.x / other[0], self.y / other[1])
            else:
                return Vector2(self.x / other, self.y / other)
        except :
            pass

    def __itruediv__(self, other):
        try:
            if isinstance(other, Vector2):
                self.x /= other.x
                self.y /= other.y
            elif isinstance(other, (list, tuple, np.ndarray)):
                self.x /= other[0]
                self.y /= other[1]
            else:
                self.x /= other
                self.y /= other
        except :
            pass

        return self

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y

        raise IndexError
        
    def __iter__(self):
        yield self.x
        yield self.y


    def __repr__(self):
        return f"Vector2({self.x},{self.y})"

    def __str__(self):
        return f"{self.x}, {self.y}"

    def abs(self):
        return Vector2(abs(self.x), abs(self.y))

    def floor(self):
        return Vector2(math.floor(self.x),math.floor(self.y))
    def ceil(self):
        return Vector2(math.ceil(self.x),math.ceil(self.y))
    
    def rounded(self,ndigits=0):
        return Vector2(round(self.x,ndigits),round(self.y,ndigits))



    #vector specifics
    def tupl(self):
        """deprecated"""
        return (self.x, self.y)
    
    def integer(self):
        return Vector2(int(self.x),int(self.y))

    @property
    def magnitude(self):
        return math.hypot(self.x,self.y )

    def normalised(self, length=1):
        try:
            mag = self.magnitude
            return self * (length / mag)
        
        except ZeroDivisionError:
            return Vector2(0, 0)

    
    def constrain(self, length):
        """deprecated"""
        self.normalise()
        self *= length
        
    @property
    def angle(self):
        """returns radians"""
        return math.atan2(self.y, self.x)

    def rotate(self,angle,degrees = False):
        if degrees:
            angle = math.radians(angle)

        magnitude = self.magnitude
        currentAngle = self.angle
        newAngle = currentAngle + angle
        self.x = magnitude * math.cos(newAngle)
        self.y = magnitude * math.sin(newAngle)
        


    def copy(self):
        return Vector2(self.x, self.y)
    

    @staticmethod
    def dot(vec1,vec2):
        return (vec1.x*vec2.x) + (vec1.y*vec2.y)

    @staticmethod
    def normalise(vector, length=1):
        try:
            mag = vector.magnitude

            vector.x = vector.x / mag * length
            vector.y = vector.y / mag * length
            return vector
        except ZeroDivisionError:
            return vector

    @staticmethod
    def fromAngleMagnitude(angle,magnitude,degrees = False):
        if degrees:
            angle = math.radians(angle)
        x = magnitude * math.sin(angle)
        y = magnitude * math.cos(angle)
        return Vector2(x,y)



def vector(target):
    """deprecated"""
    if isinstance(target, (list,tuple)):
        if len(target) == 2:
            return Vector2(target[0], target[1])
    elif isinstance(target,Vector2):
        return target

def tupl(obj):
    """deprecated"""
    if isinstance(obj,Vector2):
        return (obj.x, obj.y)  

    