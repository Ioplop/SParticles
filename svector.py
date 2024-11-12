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
        return self.x * self.x + self.y * self.y
    
    def __abs__(self) -> float:
        return self.magnitude()
    
    def magnitude(self) -> float:
        return self.sqr_magnitude() ** 0.5
    
    def dot(self, other : SVector2) -> float:
        return self.x * other.x + self.y * other.y
    
    def cross(self, other : SVector2) -> float:
        return self.x * other.y - self.y * other.x
    
    def angle(self, other : SVector2) -> float:
        return asin(self.cross(other) / (self.magnitude() * other.magnitude()))
    
    def normalized(self) -> SVector2:
        return self/self.magnitude()
    
    def rotate(self, deg) -> SVector2:
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
        return {"x": self.x, "y": self.y}
    
    def as_list(self) -> List[float, float]:
        return [self.x, self.y]
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    