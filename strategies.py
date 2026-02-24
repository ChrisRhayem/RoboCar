import math
class Deplacement:
    def __init__(self,simulation):
        self.sim = simulation
        self.depart = None
        
    #Eviter les obstacles il faut reviser
            
    def avancer(self,vitesse):
        """Permet Flash d'avancer"""
        self.sim.set_vitesse_gauche(vitesse)
        self.sim.set_vitesse_droite(vitesse)
        
    def arreter(self):
        """met la vitesse des roues à 0 pour arrêter le robot"""
        self.sim.set_vitesse_gauche(0)
        self.sim.set_vitesse_droite(0)

    def tourner_sur_place(self,vitesse):
        self.sim.set_vitesse_gauche(-vitesse)
        self.sim.set_vitesse_droite(vitesse)

    def eviter_obstacles(self, vitesse_avance=80, vitesse_tourne=60, seuil=90):
        """Met à jour les vitesses des roues pour avancer et éviter les obstacles."""
        dist_obs = self.sim.distance_obstacle(max_range=140) #la distance au plus proche obstacle devant le robot
        dist_mur = self.sim.distance_mur(max_range=140) #la distance au mur le plus proche
        distance = min(dist_obs, dist_mur)

        if distance <seuil:
            # tourne
            self.tourner_sur_place(vitesse_tourne)
        else:
            # avance
            self.avancer(vitesse_avance)
            
    def avancer_x_metres(self, distance, vitesse):
        """Fait avancer le robot d'une distance donnée en mètres à une vitesse donnée."""
        distance_pixels = distance * 100 # Convertir la distance en pixels
        if self.depart is None: #Si c'est le premier appel, on memorise le point de depart
            self.depart =(self.sim.robot.x,self.sim.robot.y)
        
        #on avance tout droit
        self.avancer(vitesse)
        
        #distance déjà parcourue depuis le départ
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2
                                       )
        #si on a atteint la distance cible, on arrete le robot
        if distance_parcourue >= distance_pixels:
            self.arreter()
            self.depart = None #on reset le point de départ
            return True #la distance a été atteinte
        return False #le robot continue d'avancer
    

