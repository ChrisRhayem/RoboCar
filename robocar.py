class RoboCar(object):
    def __init__(self, nom, coordonnees, vitesse, sens):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.s = sens  # orientation (nord:0, nord-est:1, est:2, sud-est:3, sud:4, sud-ouest:5,
                    #                   ouest:6, nord-ouest:7)
    