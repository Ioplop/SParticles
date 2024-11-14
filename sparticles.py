from __future__ import annotations
from typing import List, Dict
from random import randint, random

import pandas as pd
from pandas import DataFrame as DF

from scircles import SCircle as WObject, PhysicWorld as World
from svector import SVector2 as Vector

part_csv = "particles.csv"
reac_csv = "reactions.csv"

particle_dict: Dict[str, ParticleBlueprint] = {}
reaction_dict: Dict[str, str] = {}

class Particle(WObject):
    energy = "E"
    def __init__(self, world : World, position : Vector, radius : float, mass : float, name : str, symbol : str, color : List[int], max_energy: float, stability: float):
        WObject.__init__(self, world, position, radius, mass)
        self.name = name
        self.color = color
        self.symbol = symbol
        self.internal_energy = 0.0
        self.max_energy = max_energy
        self.stability = stability
        
    def collide(self, other : Particle):
        if self.dead or other.dead:
            return
        if self.symbol == Particle.energy or other.symbol == Particle.energy:
            return
        reaction = get_reaction(self.symbol, other.symbol)
        if reaction:
            self.react(other, reaction)
        else:
            super().collide(other)
    
    def react(self, other: Particle, result: str):
        energy = self.mass * self.velocity.sqr_magnitude() + other.mass * other.velocity.sqr_magnitude() + self.internal_energy + other.internal_energy
        new_vel = (self.mass * self.velocity + other.mass * other.velocity)/(self.mass + other.mass)
        new_pos = (self.mass * self.position + other.mass * other.position)/(self.mass + other.mass)
        new_kenergy = new_vel.sqr_magnitude() * (self.mass + other.mass)
        injected_energy = energy - new_kenergy
        product = create_particle(result, self.world, new_pos)
        product.velocity = new_vel
        product.internal_energy = injected_energy
        self.remove()
        other.remove()
    
    def split(self):
        self.dead = True
        #TODO: Make particle split

    def sim_move(self, delta : float):
        if self.internal_energy > self.max_energy:
            if random() > self.stability:
                self.split()
        if self.dead:
            return
        super().move(delta)

class ParticleBlueprint:
    def __init__(self, name: str, symbol: str, mass: int, radius: int, color: List[int], max_energy: float, stability: float):
        self.name: str = name
        self.symbol: str  = symbol
        self.mass: int = mass
        self.radius: int = radius
        self.color: List[int] = color
        self.max_energy: float = max_energy
        self.stability: float = stability
    
    def gen(self, world: World, position: Vector) -> Particle:
        return Particle(world, position, self.radius, self.mass, self.name, self.symbol, self.color, self.max_energy, self.stability)

def create_particle(symbol: str, world: World, position: Vector) -> Particle:
    return particle_dict[symbol].gen(world, position)

def random_symbol(exclude_energy: bool = True):
    symbols = list(particle_dict.keys())
    s = symbols[randint(0, len(symbols) - 1)]
    while exclude_energy and s == "E":
        s = symbols[randint(0, len(symbols) - 1)]
    return s

def read_particle(row: pd.Series) -> ParticleBlueprint:
    name = row['Name']
    symbol = row['Symbol']
    mass = int(row['Mass'])
    radius = int(row['Radius'])
    color = [int(row['R']), int(row['G']), int(row['B'])]
    max_e = float(row['Max_E'])
    stability = float(row['Stability'])
    return ParticleBlueprint(name, symbol, mass, radius, color, max_e, stability)

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
    return reaction_dict.get(re_key(re1, re2), None)

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