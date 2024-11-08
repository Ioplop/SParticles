from typing import Dict, List
import pandas as pd
from pandas import DataFrame as DF
from sparticles import Particle, World
from svector import SVector2 as Vector

particle_dict: Dict[str, DF] = {}

class ParticleBlueprint:
    def __init__(self, name: str, symbol: str, mass: int, radius: int, color: List[int]):
        self.name: str = name
        self.symbol: str  = symbol
        self.mass: int = mass
        self.radius: int = radius
        self.color: List[int] = color
    
    def gen_particle(self, world: World, position: Vector):
        return Particle(world, position, self.radius, self.mass, self.name, self.symbol, self.color)

def read_particle(row: pd.Series) -> ParticleBlueprint:
    name = row['Name']
    symbol = row['Symbol']
    mass = int(row['Mass'])
    radius = int(row['Radius'])
    color = [int(row['R']), int(row['G']), int(row['B'])]
    return ParticleBlueprint(name, symbol, mass, radius, color)
    

def gen_particle_dict(plist: str):
    global particle_dict
    df = pd.read_csv(plist, header=0)
    for index, row in df.iterrows():
        pb = read_particle(row)
        particle_dict[pb.symbol] = pb

def gen_reaction_dict(rlist: str):
    # TODO: Generate a dictionary with all reactions
    pass