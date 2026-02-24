import simulation as sim
import math
class Deplacement:
    def __init__(self, robot, obstacles):
        self.robot = robot
        self.obstacles = obstacles
        self.depart = None
        
    #Eviter les obstacles il faut reviser
    def eviter_obstacles(self, dt):
        """Met à jour les vitesses des roues pour avancer et éviter les obstacles."""
        dist_obs = sim.distance_obstacle(self.robot, self.obstacles) #la distance au plus proche obstacle devant le robot
        dist_mur = sim.distance_mur(self.robot, 800, 600) #la distance au mur le plus proche
        distance = min(dist_obs, dist_mur)

        if distance < 40:
            # tourne
            sim.set_vitesse_gauche(self.robot, -60)
            sim.set_vitesse_droite(self.robot, 60)
        else:
            # avance
            sim.set_vitesse_gauche(self.robot, 30)
            sim.set_vitesse_droite(self.robot, 30)
            
    def avancer(self, vitesse):
        """Permet Flash d'avancer"""
        sim.set_vitesse_gauche(self.robot, vitesse)
        sim.set_vitesse_droite(self.robot, vitesse)
        
    def arreter(self):
        """met la vitesse des roues à 0 pour arrêter le robot"""
        sim.set_vitesse_gauche(self.robot, 0)
        sim.set_vitesse_droite(self.robot, 0)

    def avancer_x_metres(self, distance, dt, vitesse):
        """Fait avancer le robot d'une distance donnée en mètres à une vitesse donnée."""
        distance_pixels = distance * 100 # Convertir la distance en pixels
        if self.depart is None: #Si c'est le premier appel, on memorise le point de depart
            self.depart = self.robot.get_state()
        
        #on avance tout droit
        self.avancer(self.robot)
        self.robot.update(dt) #on met à jour la position du robot
        
        #distance déjà parcourue depuis le départ
        dx = - self.robot.x + self.depart[0]
        dy = self.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2
                                       )
        #si on a atteint la distance cible, on arrete le robot
        if distance_parcourue >= distance_pixels:
            self.arreter(self.robot, vitesse)
            self.depart = None #on reset le point de départ
            return True #la distance a été atteinte
        return False #le robot continue d'avancer
    

