import pygame as p
import random
import math
import numpy as np
# Constants
WIDTH, HEIGHT = 1000, 1000
MAX_SPEED = 4
NEIGHBOR_RADIUS = 120
AVOID_RADIUS = 20
ALIGNMENT_WEIGHT = 0.5
COHESION_WEIGHT = 0.1
SEPARATION_WEIGHT = 0.1
BIRDS = 20


class Bird:
    def __init__(self):
        self.x = random.randint(0,WIDTH)
        self.y = random.randint(0,HEIGHT)
        self.vx = 3
        self.vy = 3
        


    def update(self, birds):
        avoid = False
        gen_dir = []
        coords = []
        too_close = []
        # allignment
        for bird in birds:
            if bird == self:
                continue  # Skip self

            dx = bird.x - self.x  # Notice the flipped dx
            dy = bird.y - self.y
            dist_sq = dx**2 + dy**2  # Squared distance check
            if dist_sq < AVOID_RADIUS**2:
                too_close.append((bird.x, bird.y))
                continue
            if dist_sq < NEIGHBOR_RADIUS**2:

                angle = math.atan2(dy, dx)
                if angle < 0:
                    angle += 2 * math.pi  # Convert to 0-2π

                if 1/4 * math.pi < angle < 3/2 * math.pi:  # Forward cone
                    gen_dir.append((bird.vx, bird.vy))
                    coords.append((bird.x, bird.y))
        if too_close:
            centroid = np.mean(np.array(too_close)-(self.x, self.y), axis=0)
            fx, fy =  centroid[0],centroid[1]
            mag = np.sqrt(fx**2 + fy**2)
            dirx , diry = fx/mag, fy/mag
            alignx, aligny = dirx*4, diry*4
            self.vx += (-alignx-self.vx ) *0.001
            self.vy += (-aligny -self.vy) *0.001

        elif gen_dir:
            mean_dir = np.mean(gen_dir, axis=0)
            centroid = np.mean(coords, axis=0)
            fcx, fcy = (self.x - centroid[0]), (self.y - centroid[1])
            fx, fy = mean_dir[0], mean_dir[1]
            mag = np.sqrt(fx**2 + fy**2)
            dirx , diry = fx/mag, fy/mag
            alignx, aligny = dirx*4, diry*4

            
            # # Smooth steering instead of hard override
            self.vx += (-fcx-self.vx) *0.001
            self.vy += (-fcy-self.vy) *0.001

            
            self.vx += (alignx-self.vx ) * 0.1
            self.vy += (aligny -self.vy) * 0.1
      
        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT



       
    def draw(self, surface):
        p.draw.circle(surface, (255,255,255),(self.x, self.y), 5)
    

# Initialize Pygame
p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()
birds = [Bird() for i in range(50)]
# Main loop
running = True
while running:
    clock.tick(100)
    screen.fill((0, 0, 0))  # Clear screen

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    for bird in birds:
        bird.update(birds)
        bird.draw(screen)
    p.display.flip()
    clock.tick(30)  # Limit frame rate

p.quit()
