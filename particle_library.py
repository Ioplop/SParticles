from __future__ import annotations
from typing import Dict, List
import pandas as pd
from pandas import DataFrame as DF
from sparticles import Particle, World
from svector import SVector2 as Vector

part_csv = "particles.csv"
reac_csv = "reactions.csv"

particle_dict: Dict[str, ParticleBlueprint] = {}
reaction_dict: Dict[str, str] = {}

class ParticleBlueprint:
    def __init__(self, name: str, symbol: str, mass: int, radius: int, color: List[int]):
        self.name: str = name
        self.symbol: str  = symbol
        self.mass: int = mass
        self.radius: int = radius
        self.color: List[int] = color
    
    def gen(self, world: World, position: Vector) -> Particle:
        return Particle(world, position, self.radius, self.mass, self.name, self.symbol, self.color)

def create_particle(symbol: str, world: World, position: Vector) -> Particle:
    return particle_dict[symbol].gen(world, position)

def read_particle(row: pd.Series) -> ParticleBlueprint:
    name = row['Name']
    symbol = row['Symbol']
    mass = int(row['Mass'])
    radius = int(row['Radius'])
    color = [int(row['R']), int(row['G']), int(row['B'])]
    return ParticleBlueprint(name, symbol, mass, radius, color)

def gen_particle_dict(plist: str):
    global particle_dict
    df = pd.read_csv(plist, header=0, sep=";")
    for index, row in df.iterrows():
        pb = read_particle(row)
        particle_dict[pb.symbol] = pb
    print(f"Loaded {len(particle_dict)} particles...")

def re_key(re1: str, re2: str) -> str:
    if re1 <= re2:
        return f"{re1}-{re2}"
    return f"{re2}-{re1}"

def get_reaction(re1: str, re2: str)->str:
    global reaction_dict
    return reaction_dict[re_key(re1, re2)]

def gen_reaction_dict(rlist: str):
    global reaction_dict
    df = pd.read_csv(rlist, sep=";")
    for index, row in df.iterrows():
        re1 = row['re1']
        re2 = row['re2']
        product = row['product']
        reaction_dict[re_key(re1, re2)] = product
    print(f"Loaded {len(reaction_dict)} reactions...")

def init():
    global part_csv, reac_csv
    gen_particle_dict(part_csv)
    gen_reaction_dict(reac_csv)

init()