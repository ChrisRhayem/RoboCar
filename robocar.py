class RoboCar(object):
    def __init__(self, nom:str, coordonnees:tuple, vitesse:int, angle:int):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.a = angle  # angle:int [0;360]
    
    def orientation(self)->str:
        """
        Renvoie une chaîne de caractère donnant la direction de la voiture
        """
        if self.s%8 == 0:
            return "↑"
        elif self.s%8 == 1:
            return "↗"
        elif self.s%8 == 2:
            return "→"
        elif self.s%8 == 3:
            return "↘"
        elif self.s%8 == 4:
            return "↓"
        elif self.s%8 == 5:
            return "↙"
        elif self.s%8 == 6:
            return "←"
        elif self.s%8 == 7:
            return "↖"