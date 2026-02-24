import pygame
import math

from robocar import RoboCar
from obstacle import Obstacle
from simulation import Simulation
from strategies import Deplacement

LARGEUR = 800
HAUTEUR = 600
FPS = 60

def draw_robot(screen, robot):
    """Cette fonction dessine le robot"""
    x, y, angle = robot.get_state()

    L = robot.longueur
    W = robot.largeur

    half_L = L / 2
    half_W = W / 2
    corners = [
        (-half_L, -half_W),
        (-half_L,  half_W),
        ( half_L,  half_W),
        ( half_L, -half_W),
    ]

    rotated = []
    for cx, cy in corners:
        rx = x + cx * math.cos(angle) - cy * math.sin(angle)
        ry = y + cx * math.sin(angle) + cy * math.cos(angle)
        rotated.append((rx, ry))

    pygame.draw.polygon(screen, (0, 200, 0), rotated)

    # ligne direction (avant)
    front_x = x + math.cos(angle) * half_L
    front_y = y + math.sin(angle) * half_L
    pygame.draw.line(screen, (255, 255, 255), (x, y), (front_x, front_y), 3)

def draw_obstacles(screen, obstacles):
    """Cette fonction dessine l'obstacle"""
    for obs in obstacles:
        pygame.draw.rect(screen, (200, 0, 0), (*obs.pos, *obs.dim))


