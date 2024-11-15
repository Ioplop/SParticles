from __future__ import annotations
from typing import List, Dict
import math
from math import cos, sin, asin

class SVector2:
    def __init__(self, x : float, y : float):
        self.x : float = x
        self.y : float = y
    
    def __add__(self, other : SVector2) -> SVector2:
        return SVector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other : SVector2) -> SVector2:
        return SVector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other : float) -> SVector2:
        return SVector2(self.x * other, self.y * other)
    
    def __rmul__(self, other : float) -> SVector2:
        return self.__mul__(other)
    
    def __truediv__(self, other : float) -> SVector2:
        return SVector2(self.x / other, self.y / other)
    
    def sqr_magnitude(self) -> float:
        """Return the squared magnitude of the vector"""
        return self.x * self.x + self.y * self.y
    
    def __abs__(self) -> float:
        """Returns the magnitude of the vector. (x**2 + y**)**0.5"""
        return self.magnitude()
    
    def magnitude(self) -> float:
        """Returns the magnitude of the vector. (x**2 + y**)**0.5"""
        return self.sqr_magnitude() ** 0.5
    
    def dot(self, other : SVector2) -> float:
        """Calculates the dot product between this vector and another one."""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other : SVector2) -> float:
        """Calculates the magnitude of the cross product between this vector and another one."""
        return self.x * other.y - self.y * other.x
    
    def angle(self, other : SVector2) -> float:
        """Return the angle of this vector in radians."""
        return asin(self.cross(other) / (self.magnitude() * other.magnitude()))
    
    def normalized(self) -> SVector2:
        """Returns a vector of magnitud one that points in the same direction as this vector."""
        return self/self.magnitude()
    
    def rotate(self, deg: float) -> SVector2:
        """Rotates this vector in "deg" radians."""
        x = cos(deg) * self.x - sin(deg) * self.y
        y = sin(deg) * self.x + cos(deg) * self.y
        return SVector2(x, y)
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            if item is int:
                raise(Exception(f"Cannot get {item} from an SVector2. Only 0 and 1 are allowed."))
            else:
                raise(TypeError(f"SVector2 getitem can only take int, not {type(item)}"))
    
    def as_dict(self) -> Dict[str, float]:
        """Returns a dictionary in the form {"x": self.x, "y": self.y}"""
        return {"x": self.x, "y": self.y}
    
    def as_list(self) -> List[float, float]:
        """Returns a list in the form [self.x, self.y]"""
        return [self.x, self.y]
    
    def __str__(self) -> str:
        """Returns a readable version of this vector in the form (self.x, self.y)"""
        return f"({self.x}, {self.y})"

    @staticmethod
    def normal(angle: float) -> SVector2:
        """Returns a normal vector that points in a given angle in radians."""
        return SVector2(cos(angle), sin(angle))
    
    @staticmethod
    def angled(angle: float, magnitude: float) -> SVector2:
        """Returns a vector with given magnitude that points in a given angle in radians."""
        return SVector2(cos(angle)*magnitude, sin(angle)*magnitude)