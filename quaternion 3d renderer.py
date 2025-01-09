import sys
from typing import *
from functools import partial
import math
import numpy as np
import pygame
from pygame.locals import *
pygame.init()

MainClock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
surface = pygame.Surface((600, 600))
origin = (surface.get_width() // 2, surface.get_height() // 2)
current_input = []

class Camera:
    def __init__(self) -> None:
        self.angle1 = 0
        self.angle2 = 0
        self.controles = {K_RIGHT: partial(self.rotate, "angle1", 1),
                          K_LEFT: partial(self.rotate, "angle1", -1),
                          K_UP: partial(self.rotate, "angle2", 1),
                          K_DOWN: partial(self.rotate, "angle2", -1)}
    
    def rotate(self, attribute, speed: float):
        n = getattr(self, attribute)
        n += speed
        if n == 360:
            n = 0
        if n == -1:
            n = 35100
        setattr(self, attribute, n)

    def update(self):
        for key in current_input:
            if key in self.controles:
                self.controles[key]()
        
    def calcuate_point(self, point):
        def quaternion_multiply(q1, q2):
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2
            
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
            
            return np.array([w, x, y, z])
        
        def quaternion_rotation(point, axis, angle):
            
            # Compute quaternion components
            w = np.cos(angle / 2)
            x = axis[0] * np.sin(angle / 2)
            y = axis[1] * np.sin(angle / 2)
            z = axis[2] * np.sin(angle / 2)
            
            # Create quaternion and its inverse
            q = np.array([w, x, y, z])
            q_inv = np.array([w, -x, -y, -z])
            
            # Convert point to a pure quaternion
            p = np.array([0, point[0], point[1], point[2]])
            
            # Perform quaternion multiplication q * p
            temp = quaternion_multiply(q, p)
            
            # Perform quaternion multiplication (q * p) * q_inv
            p_prime = quaternion_multiply(temp, q_inv)
            
            # Extract the rotated point
            rotated_point = p_prime[1:]
            return rotated_point

        rotated_point = quaternion_rotation(point, [0, 1, 0], np.radians(self.angle1))
        rotated_point = quaternion_rotation(rotated_point, [1, 0, 0], np.radians(self.angle2))
        return rotated_point
    
    def render_point(self, point):
        rotated_point = self.calcuate_point(point)
        pygame.draw.circle(surface, [0, 0, 0], (rotated_point[0] + origin[0], rotated_point[1] + origin[1]), 4)

    def render_face(self, points):
        points = [(self.calcuate_point(point)[0] + origin[0], 
                   self.calcuate_point(point)[1] + origin[1]) for point in points]
        pygame.draw.polygon(surface, [0, 0, 0], points, 1)

class Shape():
    def __init__(self, points: list[list[float]], faces: list[list[float]]) -> None:
        self.points = points
        self.faces = [[points[faces[i][j]] for j in range(len(faces[i]))] for i in range(len(faces))]

#==================================================================================================

camera = Camera()
shapes = [Shape([[-100, 100, -100], 
                 [-100, 100, 100], 
                 [100, 100, 100], 
                 [100, 100, -100],
                 [-100, -100, -100], 
                 [-100, -100, 100], 
                 [100, -100, 100], 
                 [100, -100, -100]], 
                [[0, 1, 2, 3],
                 [0, 1, 5, 4],
                 [1, 2, 6, 5],
                 [4, 5, 6, 7],
                 [2, 3, 7, 6],
                 [3, 0, 4, 7]
                 ])]

def update():
    surface.fill((250, 250, 250))
    camera.update()
    for shape in shapes:
        for point in shape.points:
            camera.render_point(point)
        for face in shape.faces:
            camera.render_face(face)
    screen.blit(pygame.transform.scale(surface, (600, 600)), (0, 0))
    pygame.display.update()

running  = True
while running:
    update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            current_input.append(event.key)
            if event.key == K_ESCAPE:
                running = False
        if event.type == KEYUP:
            current_input.remove(event.key)
    MainClock.tick(30)

pygame.quit()
sys.exit()