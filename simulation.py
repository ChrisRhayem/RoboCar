import math

class Simulation():
    def __init__(self, robot, obstacles, largeur, hauteur):
        self.robot = robot
        self.obstacles = obstacles
        self.largeur = largeur
        self.hauteur = hauteur

    def get_wheel_speeds(self):
        return self.robot.vG, self.robot.vR

    def set_vitesse_gauche(self, v):
        self.robot.set_vitesse_gauche(v)

    def set_vitesse_droite(self, v):
        self.robot.set_vitesse_droite(v)
    
    def distance_obstacle(self,max_range=120):
        """Cette fonction regarde l'obstacle le plus proche"""
        min_dist = max_range #distance minimale

        # vecteur direction du voiture
        dir_x = math.cos(self.robot.angle)
        dir_y = math.sin(self.robot.angle)
        
        for obs in self.obstacles:
            ox, oy = obs.pos
            dx = ox - self.robot.x #on cree un vecteur du voiture vers l’obstacle
            dy = oy - self.robot.y

            # projection dans la direction du voiture
            projection = dx * dir_x + dy * dir_y #produit scalaire
            if 0 < projection < max_range: #on regard si l'obstacle est proche
                dist = math.sqrt(dx**2 + dy**2)
                if dist < min_dist:
                    min_dist = dist #on garde l'obstacle le plus proche devant

        return min_dist

    def distance_mur(self,max_range=120):
        """Cette fonction renvoie la distance au mur le plus proche dans la direction du voiture"""
        # point devant le voiture
        front_x = self.robot.x + math.cos(self.robot.angle) * max_range #on avance de 120 pixels dans la direction du voiture
        front_y = self.robot.y + math.sin(self.robot.angle) * max_range

        # distance au mur le plus proche
        dist_x = min(front_x, self.largeur - front_x)
        dist_y = min(front_y, self.hauteur - front_y)

        return min(dist_x, dist_y)

    def obtenir_rectangle(self):
        """cette fonction cree un rectangle simplifie autour du voiture pour faire les collisions"""
        half_L = self.robot.longueur / 2 #le voiture est centre donc on calcule le centre pour le retrancher apres a x et y
        half_W = self.robot.largeur / 2

        return (
            self.robot.x - half_L, #on va du centre vers la gauche
            self.robot.y - half_W, #on va du centre vers le haut
            self.robot.longueur,
            self.robot.largeur
        )

    def collision(self, obstacle):
        """Cette fonction detetcte la collision avec les 
        dimensitions complete (pas seulmenet son centre) du robot avec l'aide de obternir_retangle"""
        x1, y1, w1, h1 = self.obtenir_rectangle()
        x2, y2 = obstacle.pos
        w2, h2 = obstacle.dim

        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )
    def appliquer_murs(self):
        """Empeche le robot de sortir de la fenetre"""
        half_L = self.robot.longueur / 2.0
        half_W = self.robot.largeur / 2.0
        self.robot.x = max(half_L, min(self.robot.x, self.largeur - half_L)) #si x est trop petit on le force à half_L si x est trop grand on le force à largeur - half_L et sinon on garde x
        self.robot.y = max(half_W, min(self.robot.y, self.hauteur - half_W))

    def resoudre_collisions(self, old_state):
        """Empecher le robot de traverser un obstacle"""
        for obs in self.obstacles:
            if self.collision(obs):
                self.robot.x, self.robot.y = old_state
                return True
        return False

    def update(self, dt):
        """Met à jour le robot et l'environnement."""
        old_state = (self.robot.x, self.robot.y)
        self.robot.update(dt)
        self.appliquer_murs()
        a_collision = self.resoudre_collisions(old_state)
        return a_collision