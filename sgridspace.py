from __future__ import annotations
from svector import SVector2 as Vector
from typing import List, Tuple, Set
from math import ceil, floor

class World:
    def __init__(self, width: float, height: float, scale: float):
        self.W : float = width
        self.H : float = height
        self.scale : float = scale
        self.grid : List[List[List[WObject]]]= [[[] for y in range(ceil(height/scale)+1)] for x in range(ceil(width/scale)+1)]
        self.objects : Set[WObject] = set()
        self.new_objects : Set[WObject] = set()
    
    def overlap_circle(self, pos : Vector, radius : float) -> List[WObject]:
        objSet : List[WObject] = []
        startGX = max(floor((pos.x-radius)/self.scale), 0)
        endGX = min(floor((pos.x+radius)/self.scale), len(self.grid)-1)
        startGY = max(floor((pos.y-radius)/self.scale), 0)
        endGY = min(floor((pos.y+radius)/self.scale), len(self.grid[0])-1)
        for gx in range(startGX, endGX+1):
            for gy in range(startGY, endGY+1):
                subset = self.grid[gx][gy]
                for obj in subset:
                    sqrdist = (obj.position - pos).sqr_magnitude()
                    if sqrdist < (radius+obj.radius) ** 2:
                        objSet.append(obj)
        return objSet
    
    def get_limits(self, pos : Vector, radius : float) -> WLimits:
        return WLimits(
                floor((pos.x-radius)/self.scale),
                floor((pos.x+radius)/self.scale),
                floor((pos.y-radius)/self.scale),
                floor((pos.y+radius)/self.scale)
            )
    
    def update_grid(self, obj : WObject, trans : WLTransition):
        for x, y in trans.grid_remove:
            if x >= 0 and x < len(self.grid) and y >= 0 and y < len(self.grid[0]):
                if obj in self.grid[x][y]:
                    self.grid[x][y].remove(obj)
        for x, y in trans.grid_add:
            if x >= 0 and x < len(self.grid) and y >= 0 and y < len(self.grid[0]):
                if not (obj in self.grid[x][y]):
                    self.grid[x][y].append(obj)
    
    def add_objects(self):
        for o in self.new_objects:
            self.objects.add(o)
        self.new_objects.clear()
   
class WObject:
    # An object in worldspace
    def __init__(self, world : World, position: Vector, radius : float):
        self.world : World = world
        self.position : Vector = position
        self.radius : float = radius
        self.limits : WLimits = None
        self.dead : bool = False
        world.new_objects.add(self)
        self.update_grid()
    
    def update_grid(self):
        new_limits = self.world.get_limits(self.position, self.radius)
        self.world.update_grid(self, WLTransition(self.limits, new_limits))
        self.limits = new_limits
    
    def set_position(self, new_position: Vector):
        self.position = new_position
        self.update_grid()
        
    def move(self, movement : Vector):
        self.set_position(self.position + movement)
        
    def remove(self):
        self.world.update_grid(self, WLTransition(self.limits, None))
        #self.world.objects.remove(self)
        self.dead = True
        
class WLimits:
    # Defines the grid limits in which an object lives.
    def __init__(self, minX, maxX, minY, maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        
    def contains(self, x : int, y : int) -> bool:
        return (self.minX <= x <= self.maxX) and self.minY <= y <= self.maxY
    
class WLTransition:
    # Defines what parts of the grid must an object be added to or removed from.
    def __init__(self, sLimit : WLimits, eLimit : WLimits):
        self.grid_remove : List[Tuple[int, int]] = []
        self.grid_add : List[Tuple[int, int]] = []
        self.calculate(sLimit, eLimit)
        
    def calculate(self, sLimit : WLimits, eLimit : WLimits):
        if not eLimit:
            for x in range(sLimit.minX, sLimit.maxX + 1):
                for y in range(sLimit.minY, sLimit.maxY + 1):
                    self.grid_remove.append((x, y))
        elif not sLimit:
            for x in range(eLimit.minX, eLimit.maxX + 1):
                for y in range(eLimit.minY, eLimit.maxY + 1):
                    self.grid_add.append((x, y))
        else:
            for x in range(sLimit.minX, sLimit.maxX + 1):
                for y in range(sLimit.minY, sLimit.maxY + 1):
                    if not eLimit.contains(x, y):
                        self.grid_remove.append((x, y))
            for x in range(eLimit.minX, eLimit.maxX + 1):
                for y in range(eLimit.minY, eLimit.maxY + 1):
                    if not sLimit.contains(x, y):
                        self.grid_add.append((x, y))
