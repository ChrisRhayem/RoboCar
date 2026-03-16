import math


class AvancerXMetres:
    """
    Fait avancer le robot d'une distance donnée.
    """

    def __init__(self, simulation, distance, vitesse, marge_mur=35):
        self.sim = simulation
        self.distance = distance
        self.vitesse = vitesse
        self.marge_mur = marge_mur
        self.depart = None
        self.terminee = False

    def reset(self, distance=None, vitesse=None):
        if distance is not None:
            self.distance = distance
        if vitesse is not None:
            self.vitesse = vitesse
        self.depart = None
        self.terminee = False

    def update(self, dt):
        if self.terminee:
            return True

        distance_pixels = self.distance * 100

        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y)

        if self.sim.distance_mur(max_range=60) < self.marge_mur:
            self.sim.freiner(dt)
            self.terminee = True
            return True

        self.sim.avancer(self.vitesse)

        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)

        if distance_parcourue >= distance_pixels:
            self.sim.freiner(dt)
            self.terminee = True
            return True

        return False


class Reculer:
    """
    Fait reculer le robot sur une petite distance.
    """

    def __init__(self, simulation, vitesse=45, distance=0.3):
        self.sim = simulation
        self.vitesse = vitesse
        self.distance = distance
        self.depart = None
        self.actif = False

    def declencher(self):
        self.depart = None
        self.actif = True

    def update(self, dt):
        if not self.actif:
            return True

        distance_pixels = self.distance * 100

        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y)

        self.sim.reculer(self.vitesse)

        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)

        if distance_parcourue >= distance_pixels:
            self.sim.freiner(dt)
            self.actif = False
            return True

        return False


class TournerPendant:
    """
    Tourne pendant un temps donné.
    Sens = "gauche" ou "droite"
    """

    def __init__(self, simulation, duree, vitesse, sens):
        self.sim = simulation
        self.duree = duree
        self.vitesse = vitesse
        self.sens = sens
        self.temps_restant = duree
        self.terminee = False

    def reset(self, duree=None, vitesse=None, sens=None):
        if duree is not None:
            self.duree = duree
        if vitesse is not None:
            self.vitesse = vitesse
        if sens is not None:
            self.sens = sens
        self.temps_restant = self.duree
        self.terminee = False

    def update(self, dt):
        if self.terminee:
            return True

        self.temps_restant -= dt

        if self.sens == "gauche":
            self.sim.tourner_gauche(self.vitesse)
        else:
            self.sim.tourner_droite(self.vitesse)

        if self.temps_restant <= 0:
            self.sim.freiner(dt)
            self.terminee = True
            return True

        return False


class ContournerObstacle:
    """
    Manœuvre complète de contournement.

    Étapes :
    1. choisir un côté
    2. tourner
    3. avancer pour se décaler
    4. re-tourner pour revenir parallèle
    5. avancer pour dépasser l'obstacle
    """

    def __init__(self, simulation):
        self.sim = simulation
        self.phase = "INACTIVE"
        self.direction = None

        self.tourne1 = TournerPendant(simulation, duree=0.6, vitesse=60, sens="gauche")
        self.avance1 = AvancerXMetres(simulation, distance=0.5, vitesse=55)
        self.tourne2 = TournerPendant(simulation, duree=0.6, vitesse=60, sens="droite")
        self.avance2 = AvancerXMetres(simulation, distance=0.9, vitesse=60)

    def declencher(self):
        dist_gauche = self.sim.distance_cote_gauche(max_range=80)
        dist_droite = self.sim.distance_cote_droite(max_range=80)

        if dist_gauche > dist_droite:
            self.direction = "gauche"
            self.tourne1.reset(sens="gauche")
            self.tourne2.reset(sens="droite")
        else:
            self.direction = "droite"
            self.tourne1.reset(sens="droite")
            self.tourne2.reset(sens="gauche")

        self.avance1.reset(distance=0.5, vitesse=55)
        self.avance2.reset(distance=0.9, vitesse=60)

        self.phase = "TOURNE_1"

    def update(self, dt):
        if self.phase == "INACTIVE":
            return True

        elif self.phase == "TOURNE_1":
            fini = self.tourne1.update(dt)
            if fini:
                self.phase = "AVANCE_1"

        elif self.phase == "AVANCE_1":
            fini = self.avance1.update(dt)
            if fini:
                self.phase = "TOURNE_2"

        elif self.phase == "TOURNE_2":
            fini = self.tourne2.update(dt)
            if fini:
                self.phase = "AVANCE_2"

        elif self.phase == "AVANCE_2":
            fini = self.avance2.update(dt)
            if fini:
                self.phase = "INACTIVE"
                return True

        return False


class GestionStrategies:
    """
    Gère toutes les stratégies du robot.
    """

    def __init__(self, simulation):
        self.sim = simulation

        self.depart = AvancerXMetres(simulation, distance=1, vitesse=80)
        self.recul = Reculer(simulation, vitesse=45, distance=0.3)
        self.contournement = ContournerObstacle(simulation)

        self.phase = "DEPART"

    def update(self, dt):
        if self.phase == "DEPART":
            fini = self.depart.update(dt)
            if fini:
                self.phase = "NORMAL"

        elif self.phase == "RECUL":
            fini = self.recul.update(dt)
            if fini:
                self.phase = "NORMAL"

        elif self.phase == "CONTOURNEMENT":
            fini = self.contournement.update(dt)
            if fini:
                self.phase = "NORMAL"

        elif self.phase == "NORMAL":
            dist_obs = self.sim.distance_obstacle(max_range=150)
            dist_mur = self.sim.distance_mur(max_range=70)
            dist_gauche = self.sim.distance_cote_gauche(max_range=60)
            dist_droite = self.sim.distance_cote_droite(max_range=60)

            distance = min(dist_obs, dist_mur)

            # Si vraiment coincé : reculer
            if distance < 20 and dist_gauche < 25 and dist_droite < 25:
                self.recul.declencher()
                self.phase = "RECUL"

            # Si obstacle proche devant : lancer une vraie manœuvre
            elif distance < 55:
                self.contournement.declencher()
                self.phase = "CONTOURNEMENT"

            else:
                self.sim.avancer(65)