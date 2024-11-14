from __future__ import annotations
from svector import SVector2 as Vector
from sgridspace import World, WObject
from typing import Set, List


class PhysicWorld(World):
    def __init__(self, width: float, height: float, scale: float):
        World.__init__(self, width, height, scale)
        self.objects : Set[SCircle] = set()
    
    def sim_collisions(self):
        for obj in self.objects:
            others : List[SCircle] = self.overlap_circle(obj.position, obj.radius)
            for other in others:
                if other == obj:
                    continue
                obj.collide(other)
    
    def sim_wall_bounce(self):
        for obj in self.objects:
            if obj.position.x + obj.radius > self.W:
                if obj.velocity.x > 0:
                    obj.velocity.x *= -1
            elif obj.position.x - obj.radius < 0:
                if obj.velocity.x < 0:
                    obj.velocity.x *= -1
            if obj.position.y + obj.radius > self.H:
                if obj.velocity.y > 0:
                    obj.velocity.y *= -1
            elif obj.position.y - obj.radius < 0:
                if obj.velocity.y < 0:
                    obj.velocity.y *= -1
    
    def clear_objects(self):
        objs = list(self.objects)
        for o in objs:
            if o.dead:
                self.objects.remove(o)
    
    def simulate(self, delta : float):
        self.add_objects()
        for obj in self.objects:
            obj.sim_move(delta)
        self.sim_wall_bounce()
        self.sim_collisions()
        self.clear_objects()
                

class SCircle(WObject):
    def __init__(self, world : World, position: Vector, radius : float, mass : float):
        WObject.__init__(self, world, position, radius)
        self.velocity : Vector = Vector(0, 0)
        self.mass = mass
        
    def collide(self, other : SCircle):
        # 1- Check if closing in
        direction = other.position - self.position
        velocity = self.velocity - other.velocity
        invel = direction.dot(velocity)
        if invel < 0:
            return
        approach_speed = invel / direction.magnitude()
        approach_velocity = direction.normalized() * approach_speed
        
        # 2- Apply elastic velocity change
        total_mass = self.mass + other.mass
        
        v1f = approach_velocity*(self.mass - other.mass)/total_mass
        v2f = approach_velocity*(self.mass*2.0)/total_mass
        
        v1c = v1f - approach_velocity
        v2c = v2f
        
        self.velocity += v1c
        other.velocity += v2c
        
    def sim_move(self, delta : float):
        self.move(self.velocity * delta)
    