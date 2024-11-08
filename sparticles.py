from __future__ import annotations
from typing import List, Dict
from scircles import SCircle as WObject, PhysicWorld as World
from svector import SVector2 as Vector

particle_file = ""
particle_set: Dict[str, Particle]= {}

class Particle(WObject):
    def __init__(self, world : World, position : Vector, radius : float, mass : float, name : str, symbol : str, color : List[int]):
        WObject.__init__(self, world, position, radius, mass)
        self.name = name
        self.color = color
        self.symbol = symbol
        
    def collide(self, other : Particle):
        super().collide(other)

def scan_particle_dict():
    # TODO: Scan particle csv file
    pass