import simulation as sim
class Deplacement:
    def __init__(self, robot, obstacles):
        self.robot = robot
        self.obstacles = obstacles
        
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
            
    def avance(self):
        """Permet Flash d'avancer"""
        sim.set_vitesse_gauche(self.robot, 80)
        sim.set_vitesse_droite(self.robot, 80)
        
    def arreter(self):
        """met la vitesse des roues à 0 pour arrêter le robot"""
        sim.set_vitesse_gauche(self.robot, 0)
        sim.set_vitesse_droite(self.robot, 0)
    
        
            
