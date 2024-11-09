from svector import SVector2 as Vector
from scircles import PhysicWorld as World
from sparticles import Particle as Particle
from time import sleep
import pygame
from pygame.locals import Rect
from math import sin, cos, pi
from random import random, randint
import particle_library

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((800, 600))

W, H = screen.get_size()
SCALE = 40
world = World(W, H, SCALE)

min_vel = 50
max_vel = 100
min_size = 5
max_size = 20
obj_density = 0.0002
n_objs = int(W * H * obj_density)
background_color = [0, 0, 15]

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
    color = [randint(25, 255), randint(25, 255), randint(25, 255)]
    obj = Particle(world, newpos, radius, pi * radius ** 2, "", "", color)
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

def draw_object(particle : Particle):
    global screen, W
    mopos = particle.position.as_list()
    mopos[1] = H - mopos[1]
    pygame.draw.circle(screen, particle.color, mopos, particle.radius)

screen.fill(background_color)
pygame.display.flip()

t = 0
delta = 0.05
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    world.simulate(delta)
    #draw_grid()
    screen.fill(background_color)
    for object in world.objects:
        draw_object(object)
    pygame.display.flip()
    t += delta
    sleep(0.05)