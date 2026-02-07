import math
class RoboCar(object):
    def __init__(self, nom:str, coordonnees:tuple, vitesse:int, angle:int):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.a = angle  # angle:int [0;360]
    def avancer(self, vitesse):
        """Avance la voiture selon son angle"""
        angle_rad = math.radians(self.a)
        x = self.coo[0] + math.cos(angle_rad) * vitesse
        y = self.coo[1] + math.sin(angle_rad) * vitesse
        self.coo = (x, y)
    def reculer(self, vitesse):
        """Recule la voiture selon son angle"""
        angle_rad = math.radians(self.a) #on met en radians pour que cos et sin puissent marcher 
        x = self.coo[0] - math.cos(angle_rad) * vitesse
        y = self.coo[1] - math.sin(angle_rad) * vitesse
        self.coo = (x, y)
    def Rotation(self):
        """Tourne la voiture sur elle-même"""
        #si self.v est negatif alors flash tourne a gauche 
        #si self.v est positif alors flash tourne a droite
        self.a = (self.a + self.v) % 360 #on veut que l'angle reste entre 0 et 360 donc on fait un modulo 360