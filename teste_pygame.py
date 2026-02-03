from robocar import *
import pygame
from pygame.locals import *

# INITIALISATION
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()

# DESSIN DU JOUEUR
def draw_flash(voiture):
    """
    Fonction IA pour avoir la direction du robot (temporaire)
    """
    x, y = voiture.coo
    # Créer une surface avec le carré
    flash_surface = pygame.Surface((50, 50))
    flash_surface.fill((0, 0, 0))  # Fond transparent (noir)
    flash_surface.set_colorkey((0, 0, 0))  # Rendre le noir transparent
    pygame.draw.rect(flash_surface, (34, 139, 34), (0, 0, 50, 50))
    # Ajouter une bande pour voir la rotation
    pygame.draw.rect(flash_surface, (255, 0, 0), (20, 0, 10, 50))
    
    # Rotation de la surface
    rotated_surface = pygame.transform.rotate(flash_surface, voiture.a)
    rotated_rect = rotated_surface.get_rect(center=(int(x) + 25, int(y) + 25))
    
    # Afficher la surface rotée
    screen.blit(rotated_surface, rotated_rect)

# JEU PRINCIPAL 
def start_game():
    flash = RoboCar("Flash", (200, 200), 4, 0)
    move_speed = 4  # Vitesse de déplacement
    rotation_speed = 5  # Vitesse de rotation

    running = True 
    while running:
        clock.tick(60)

        # Permet de fermer la fenêtre
        for event in pygame.event.get():  
            if event.type == QUIT:
                running = False

        # Récupération des touches pressées
        keys = pygame.key.get_pressed()

        # Sauvegarde de l'ancienne position
        old_x, old_y = flash.coo

        x, y = flash.coo

        # Déplacement selon les flèches du clavier
        if keys[K_UP]:
            y -= move_speed
        if keys[K_DOWN]:
            y += move_speed
        if keys[K_LEFT]:
            flash.a = (flash.a +rotation_speed) % 360
        if keys[K_RIGHT]:
            flash.a = (flash.a - rotation_speed) % 360


        # Mise à jour de la nouvelle position
        flash.coo = (x, y)

        # COLLISION AVEC LES MURS
        # on remet l'ancienne position si on sort de l'écran
        if (flash.coo[0] < 0 or
            flash.coo[1] < 0 or
            flash.coo[0] + 50 > 500 or
            flash.coo[1] + 50 > 500):
            flash.coo = (old_x, old_y)

        # AFFICHAGE
        screen.fill((0, 0, 0))
        draw_flash(flash)
        pygame.display.update()

    pygame.quit()

# LANCEMENT
start_game()