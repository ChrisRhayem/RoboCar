from robocar import RoboCar
from affichage_pygame import Affichage
import math

flash = RoboCar("flash", (0,0), 0)

class Simulation():
    def __init__():
        return
    
    def update(voiture):
        return

    def get_wheel_speeds(voiture):
        """Recuperer la vitesse des roues"""
        return voiture.vG, voiture.vR
    
    def set_vitesse_gauche(voiture, v):
        """Modifier la vitesse du roue gauche"""
        voiture.vG = v
        
    def set_vitesse_droite(voiture, v):
        """Modifier la vitesse du roue droite"""
        voiture.vR = v
        
    def calculer_vitesse(voiture):
        """Cette fonction calcule la vitesse lineaire et angulaire"""
        v = (voiture.vR + voiture.vG) / 2
        w = (voiture.vR - voiture.vG) / voiture.WHEEL_BASE #c'est le theoreme de Thales applique au cercle de rotation
        return v, w

    def distance_obstacle(voiture, obstacles, max_range=120):
        """Cette fonction regarde l'obstacle le plus proche"""
        min_dist = max_range #distance minimale

        # vecteur direction du voiture
        dir_x = math.cos(voiture.angle)
        dir_y = math.sin(voiture.angle)
        
        for obs in obstacles:
            ox, oy = obs.pos
            dx = ox - voiture.x #on cree un vecteur du voiture vers l’obstacle
            dy = oy - voiture.y

            # projection dans la direction du voiture
            projection = dx * dir_x + dy * dir_y #produit scalaire
            if 0 < projection < max_range: #on regard si l'obstacle est proche
                dist = math.sqrt(dx**2 + dy**2)
                if dist < min_dist:
                    min_dist = dist #on garde l'obstacle le plus proche devant

        return min_dist

    def distance_mur(voiture, largeur, hauteur, max_range=120):
        """Cette fonction renvoie la distance au mur le plus proche dans la direction du voiture"""
        # point devant le voiture
        front_x = voiture.x + math.cos(voiture.angle) * max_range #on avance de 120 pixels dans la direction du voiture
        front_y = voiture.y + math.sin(voiture.angle) * max_range

        # distance au mur le plus proche
        dist_x = min(front_x, largeur - front_x)
        dist_y = min(front_y, hauteur - front_y)

        return min(dist_x, dist_y)

    def obtenir_rectangle(voiture):
        """cette fonction cree un rectangle simplifie autour du voiture pour faire les collisions"""
        half_L = voiture.longueur / 2 #le voiture est centre donc on calcule le centre pour le retrancher apres a x et y
        half_W = voiture.largeur / 2

        return (
            voiture.x - half_L, #on va du centre vers la gauche
            voiture.y - half_W, #on va du centre vers le haut
            voiture.longueur,
            voiture.largeur
        )

    def collision(voiture, obstacle):
        """Cette fonction detetcte la collision avec les 
        dimensitions complete (pas seulmenet son centre) du robot avec l'aide de obternir_retangle"""
        x1, y1, w1, h1 = voiture.obtenir_rectangle()
        x2, y2 = obstacle.pos
        w2, h2 = obstacle.dim

        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )