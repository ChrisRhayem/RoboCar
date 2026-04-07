import unittest
import math

from Source.Model import Simulation, RoboCar, Obstacle
from Source.Controler import AdaptateurSimule


class TestAdaptateurSimule(unittest.TestCase):
    def setUp(self):
        """Prepare un monde simple avant chaque test"""
        self.sim = Simulation(800, 600)
        self.sim.obstacles = []  #on vide les obstacles pour maitriser les tests
        self.robocar = RoboCar("Flash", (100, 200), 0, simulation=self.sim)
        self.adaptateur = AdaptateurSimule(self.robocar)

    def test_set_vitesse_translation(self):
        """Verifie que set_vitesse(v, w) met les deux roues a la meme vitesse si w = 0"""
        self.adaptateur.set_vitesse(10, 0)
        self.assertEqual(self.robocar.vG, 10)
        self.assertEqual(self.robocar.vR, 10)

    def test_set_vitesse_rotation(self):
        """Verifie que set_vitesse(v, w) donne des vitesses differentes si le robot tourne"""
        self.adaptateur.set_vitesse(0, 2)
        self.assertNotEqual(self.robocar.vG, self.robocar.vR)

    def test_set_vitesse_recul(self):
        """Verifie que set_vitesse(v, w) permet de reculer si v est negatif"""
        self.adaptateur.set_vitesse(-3, 0)
        self.assertEqual(self.robocar.vG, -3)
        self.assertEqual(self.robocar.vR, -3)

    def test_arreter(self):
        """Verifie que arreter() remet les vitesses des roues a zero"""
        self.robocar.vG = 10
        self.robocar.vR = 20
        self.adaptateur.arreter()
        self.assertEqual(self.robocar.vG, 0)
        self.assertEqual(self.robocar.vR, 0)

    def test_get_distance_sans_obstacle(self):
        """Verifie que get_distance() retourne une distance positive s'il n'y a pas d'obstacle devant"""
        distance = self.adaptateur.get_distance()
        self.assertGreater(distance, 0)

    def test_get_distance_avec_obstacle_devant(self):
        """Verifie que get_distance() detecte un obstacle place devant le robot"""
        self.sim.obstacles.append(Obstacle("rectangle", (150, 180), (40, 40)))
        distance = self.adaptateur.get_distance()
        self.assertLess(distance, 120)

    def test_get_distance_parcourue(self):
        """Verifie que get_distance_parcourue() retourne une distance positive si la position du robot change"""
        self.robocar.appliquer(110, 200, self.robocar.angle)
        distance = self.adaptateur.get_distance_parcourue()
        self.assertAlmostEqual(distance, 10)

    def test_get_distance_parcourue_nulle(self):
        """Verifie que la distance parcourue vaut 0 si le robot n'a pas bouge"""
        distance = self.adaptateur.get_distance_parcourue()
        self.assertEqual(distance, 0)

    def test_get_angle_parcouru(self):
        """Verifie que get_angle_parcouru() retourne un angle positif si l'orientation change"""
        ancien_angle = self.robocar.angle
        nouvel_angle = ancien_angle + math.pi / 4  #45 degres
        self.robocar.appliquer(self.robocar.x, self.robocar.y, nouvel_angle)
        angle = self.adaptateur.get_angle_parcouru()
        self.assertAlmostEqual(angle, math.pi / 4)

    def test_get_angle_parcouru_nul(self):
        """Verifie que get_angle_parcouru() vaut 0 si l'angle n'a pas change"""
        angle = self.adaptateur.get_angle_parcouru()
        self.assertEqual(angle, 0)


if __name__ == "__main__":
    unittest.main()