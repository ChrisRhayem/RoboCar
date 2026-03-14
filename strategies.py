import math


class AvancerXMetres:
    """
    Strategie qui fait avancer le robot d'une distance donnee
    Le robot avance jusqu'a ce que la distance parcourue atteigne la distance demandee (en metres)
    """

    def __init__(self, simulation, distance, vitesse, marge_mur=35):
        self.sim = simulation      # reference vers la simulation 
        self.distance = distance   # distance a parcourir en metres
        self.vitesse = vitesse     # vitesse des roues
        self.marge_mur = marge_mur # distance minimale autorisee avec un mur

        self.depart = None         # position de depart du robot
        self.terminee = False      # indique si la strategie est terminee

    def update(self, dt):
        """
        Fonction appelee a chaque frame qui fait avancer le robot et verifie si la distance demandee a ete parcourue
        """

        if self.terminee:
            return True
        distance_pixels = self.distance * 100  # conversion de metres en pixels 
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y) # on memorise la position de depart la premiere fois

        if self.sim.distance_mur(max_range=60) < self.marge_mur: #si on est trop proche d'un mur on arrete
            self.sim.freiner(dt)
            self.terminee = True
            return True

        self.sim.avancer(self.vitesse) # on fait avancer le robot

        # calcul de la distance parcourue depuis le depart
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)

        # si on a atteint la distance voulue
        if distance_parcourue >= distance_pixels:
            self.sim.freiner(dt)
            self.terminee = True
            return True

        return False


