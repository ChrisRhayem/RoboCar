import pygame, random, math
from pygame.locals import *

# -------------------- FONCTIONS UTILES --------------------
def on_grid_random():
    x = random.randint(0,450)
    y = random.randint(0,450)
    return (x//50 * 50, y//50 * 50)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# -------------------- DESSIN DU CERCLE + TRIANGLE --------------------
def draw_flash(position, angle):
    x, y = position
    center = (int(x + 25), int(y + 25))
    radius = 25

    pygame.draw.circle(screen, (34,139,34), center, radius)

    tip = (
        center[0] + math.cos(angle) * 15,
        center[1] + math.sin(angle) * 15
    )

    left = (
        center[0] + math.cos(angle + 2.5) * 12,
        center[1] + math.sin(angle + 2.5) * 12
    )

    right = (
        center[0] + math.cos(angle - 2.5) * 12,
        center[1] + math.sin(angle - 2.5) * 12
    )

    pygame.draw.polygon(screen, (255,255,255), [tip, left, right])

# -------------------- CONSTANTES --------------------
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Flash Run')


# -------------------- RESTART --------------------
def restart_game():
    restart_font = pygame.font.Font('freesansbold.ttf',35)
    restart_screen = restart_font.render('Press Space to Restart', True, (50, 50, 50))
    restart_rect = restart_screen.get_rect()
    restart_rect.midtop = (250, 250)

    screen.blit(restart_screen, restart_rect)

    while True:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                start_game()

        pygame.display.update()

# -------------------- JEU PRINCIPAL --------------------
def start_game():
    flash = [(200, 200)]
    angle = math.pi
    rotation_speed = 0.1
    move_speed = 10
    flash_speed = 10

    game_over = False

    while not game_over:
        clock.tick(flash_speed)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        # Rotation
        if keys[K_LEFT]:
            angle -= rotation_speed
        if keys[K_RIGHT]:
            angle += rotation_speed

        # Avancer / Reculer
        if keys[K_UP]:
            flash[0] = (
                flash[0][0] + math.cos(angle) * move_speed,
                flash[0][1] + math.sin(angle) * move_speed
            )
        if keys[K_DOWN]:
            flash[0] = (
                flash[0][0] - math.cos(angle) * move_speed,
                flash[0][1] - math.sin(angle) * move_speed
            )

        # Collision mur
        if (flash[0][0] < 0 or flash[0][1] < 0 or
            flash[0][0] + 50 > 500 or flash[0][1] + 50 > 500):
            break

        screen.fill((0,0,0))
        draw_flash(flash[0], angle)
        pygame.display.update()

    # ---------------- GAME OVER ----------------
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (100,100,100))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (250, 100)

    screen.fill((0,0,0))
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(1000)

    restart_game()

# -------------------- LANCEMENT --------------------
start_game()
