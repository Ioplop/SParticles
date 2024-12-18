from random import random, randint
from math import sin, cos, pi
from time import sleep
from colorsys import rgb_to_hsv, hsv_to_rgb

import pygame
from pygame.locals import Rect

import sparticles
from svector import SVector2 as Vector
from scircles import PhysicWorld as World
from sparticles import Particle

pygame.init()
pygame.font.init()

# Energy displays
main_font = pygame.font.SysFont(None, 30)
symbol_font = pygame.font.SysFont(None, 15)


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((150, 150))

W, H = screen.get_size()
SCALE = 40
world = World(W, H, SCALE)

min_vel = 50
max_vel = 100
volume_density = 0.0003
background_color = [0, 0, 15]

#n_objs = 2
n_objs = int(W * H * volume_density)
for i in range(n_objs):
    angle = random()*pi*2.0
    speed = min_vel + random() * (max_vel - min_vel)
    velocity = Vector(cos(angle), sin(angle)) * speed
    maxx = W
    maxy = H
    minx = 0
    miny = 0
    newpos = Vector(minx+random()*(maxx-minx), miny+random()*(maxy-miny))
    symbol = ['Re', 'Gr', 'Bl'][randint(0, 2)]
    part = sparticles.create_particle(symbol, world, newpos)
    part.velocity = velocity

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
    global screen, W, H, symbol_font
    mopos = particle.position.as_list()
    mopos[1] = H - mopos[1]
    pygame.draw.circle(screen, particle.color, mopos, particle.radius)
    # draw text
    h, s, v = rgb_to_hsv(particle.color[0], particle.color[1], particle.color[2])
    nh = (h + 0.5) % 1
    ns = s
    nv = 100
    brightness = sum(particle.color)
    text = symbol_font.render(particle.symbol, True, hsv_to_rgb(nh, ns, nv))
    text_rect = text.get_rect(center=(particle.position.x, H - particle.position.y))
    screen.blit(text, text_rect)

screen.fill(background_color)
pygame.display.flip()

t = 0
delta = 0.01
running = True
step_by_step = True
continuous_step = False
fast_forward = False
while running:
    step = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_COMMA:
                step = True
                fast_forward = True
            if event.key == pygame.K_SPACE:
                step_by_step = not step_by_step
            if event.key == pygame.K_PERIOD:
                continuous_step = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PERIOD:
                continuous_step = False
            if event.key == pygame.K_COMMA:
                fast_forward = False
    if step_by_step and not step and not continuous_step:
        continue
    world.simulate(delta)
    #draw_grid()
    screen.fill(background_color)
    ie = 0
    te = 0
    for object in world.objects:
        draw_object(object)
        ie += object.internal_energy
        te += object.total_energy()
    for object in world.new_objects:
        draw_object(object)
        ie += object.internal_energy
        te += object.total_energy()
    
    ie_surface = main_font.render(f'IE: {round(ie)}', False, (255, 255, 255))
    te_surface = main_font.render(f'TE: {round(te)}', False, (255, 255, 255))
    screen.blit(ie_surface, (10, 10))
    screen.blit(te_surface, (10, 40))
    pygame.display.flip()
    t += delta
    if not fast_forward:
        sleep(delta)
