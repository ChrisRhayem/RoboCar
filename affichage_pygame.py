from robocar import *
from strategies import EviterObstacle
import pygame
import math
from pygame.locals import *
from obstacle import Obstacle

HAUTEUR=500
LARGEUR=500
RAYON=25
pygame.init()
screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()


def draw_flash(voiture):
    """Cette fonction dessine la voiture sur l'écran"""
    x, y = voiture.x, voiture.y

    pygame.draw.rect(screen, (34, 139, 34), (x,y, 50,30))

def draw_obstacles(obstacles):
    """Cette fonction dessine les obstacles sur l'écran"""
    for obs in obstacles:
        x, y = obs.pos
        w, h = obs.dim
        pygame.draw.rect(screen, (200, 0, 0), (x, y, w, h))

def main():
    """Cette fonction represente le main qui lance la boucle principale du programme"""
    flash = RoboCar("Flash", (200, 200), 90)

    v_rotation= 3
    running = True
    obstacles = [
        Obstacle("rectangle", (20, 0), (80, 50)),
        Obstacle("rectangle", (50, 0), (50, 50))
    ]
    for obs in obstacles : 
        obs.pos_aleatoire()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        old_x, old_y = flash.x, flash.y #on sauvegarde les anciennes coordonnees pour le cas de collision
        
        #Il faut changer la maniere que Flash se deplace
        if keys[K_LEFT]:
            flash.tourner_gauche(v_rotation)

        if keys[K_RIGHT]:
            flash.tourner_droite(v_rotation)

        if keys[K_UP]:
            flash.avancer()

        if keys[K_DOWN]:
            flash.reculer()

        for obs in obstacles:
            if flash.collision(obs):
                flash.contourne(flash.coo, flash.a, obstacles)
                break

        #Fonction n'existe plus -> Recreer?
        #flash.mur_collision(LARGEUR,HAUTEUR, (old_x, old_y))

        screen.fill((0, 0, 0))
        draw_flash(flash)
        draw_obstacles(obstacles)
        pygame.display.update()


    pygame.quit()


main()