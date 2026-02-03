from robocar import *
import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()


def draw_flash(voiture):
    """
    Dessine la voiture à l'écran."""
    x, y = voiture.coo
    center = (int(x + 25), int(y + 25))

    pygame.draw.circle(screen, (34, 139, 34), center, 25)

    angle_rad = math.radians(voiture.a)

    tip = (
        center[0] + math.cos(angle_rad) * 15,
        center[1] + math.sin(angle_rad) * 15
    )
    left = (
        center[0] + math.cos(angle_rad + 2.5) * 12,
        center[1] + math.sin(angle_rad + 2.5) * 12
    )
    right = (
        center[0] + math.cos(angle_rad - 2.5) * 12,
        center[1] + math.sin(angle_rad - 2.5) * 12
    )

    pygame.draw.polygon(screen, (255, 255, 255), [tip, left, right])


def start_game():
    """
    Fonction principale du programme qui initialise la voiture et gère les événements clavier"""
    flash = RoboCar("Flash", (200, 200), 4, 0)

    rotation_speed = 3   
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        old_x, old_y = flash.coo

        # rotation (en degrés)
        if keys[K_LEFT]:
            flash.a = (flash.a - rotation_speed) % 360
        if keys[K_RIGHT]:
            flash.a = (flash.a + rotation_speed) % 360

        # déplacement
        angle_rad = math.radians(flash.a)

        if keys[K_UP]:
            flash.coo = (
                flash.coo[0] + math.cos(angle_rad) * flash.v,
                flash.coo[1] + math.sin(angle_rad) * flash.v
            )

        if keys[K_DOWN]:
            flash.coo = (
                flash.coo[0] - math.cos(angle_rad) * flash.v,
                flash.coo[1] - math.sin(angle_rad) * flash.v
            )

        # collision avec les bords
        if (flash.coo[0] < 0 or flash.coo[1] < 0 or
            flash.coo[0] + 50 > 500 or flash.coo[1] + 50 > 500):
            flash.coo = (old_x, old_y)

        screen.fill((0, 0, 0))
        draw_flash(flash)

       

        pygame.display.update()

    pygame.quit()


start_game()
