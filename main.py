from svector import SVector2 as Vector
from scircles import PhysicWorld as World
from scircles import SCircle as Circle
from time import sleep
import pygame
from pygame.locals import Rect
from math import sin, cos, pi
from random import random

pygame.init()
H = 1000
W = 1500
SCALE = 40
screen = pygame.display.set_mode([W, H])
world = World(W, H, SCALE)

min_vel = 50
max_vel = 100
min_size = 5
max_size = 20
n_objs = 1000

objects = []
for i in range(n_objs):
    angle = random()*pi*2.0
    speed = min_vel + random() * (max_vel - min_vel)
    radius = min_size + random() * (max_size - min_size)
    velocity = Vector(cos(angle), sin(angle)) * speed
    minx = radius
    miny = radius
    maxx = W - radius
    maxy = H - radius
    newpos = Vector(minx+random()*(maxx-minx), miny+random()*(maxy-miny))
    obj = Circle(world, newpos, radius, pi * radius ** 2)
    obj.velocity = velocity
    objects.append(obj)

def draw_grid():
    global world, screen
    for x in range(len(world.grid)):
        for y in range(len(world.grid[x])):
            color = [0, 0, 0]
            if len(world.grid[x][y]) > 0:
                color[0] = 100
            sx = x * world.scale
            ex = (x + 1) * world.scale
            sy = world.H - (y + 1) * world.scale
            ey = world.H - y * world.scale
            pygame.draw.rect(screen, color, Rect(sx, sy, ex-sx, ey-sy))

def draw_object(obj : Circle):
    global screen, W
    mopos = obj.position.as_list()
    mopos[1] = H - mopos[1]
    pygame.draw.circle(screen, [255, 255, 255], mopos, obj.radius)

screen.fill([0, 0, 0])
pygame.display.flip()

t = 0
delta = 0.05
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    world.simulate(delta)
    #draw_grid()
    screen.fill([0, 0, 0])
    for object in world.objects:
        draw_object(object)
    pygame.display.flip()
    t += delta
    sleep(0.05)