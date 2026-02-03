class RoboCar(object):
    def __init__(self, nom:str, coordonnees:tuple, vitesse:int, angle:int):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.a = angle  # angle:int [0;360]
    
    