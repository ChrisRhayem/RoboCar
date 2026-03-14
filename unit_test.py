import unittest
import math

from robocar import RoboCar
from simulation import Simulation
from strategies import (
    AvancerXMetres,
    Reculer,
    FreinageProgressif,
    EviterObstacles,
    GestionStrategies
)


class TestRoboCar(unittest.TestCase):

    def setUp(self):
        self.robot = RoboCar("Flash", (100, 200), 0)

    def test_initialisation(self):
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_calculer_vitesse(self):
        self.robot.set_vitesse_gauche(50)
        self.robot.set_vitesse_droite(50)

        v, w = self.robot.calculer_vitesse()

        self.assertEqual(v, 50)
        self.assertEqual(w, 0)

    def test_update(self):
        self.robot.set_vitesse_gauche(10)
        self.robot.set_vitesse_droite(10)

        self.robot.update(1)

        self.assertAlmostEqual(self.robot.x, 110)
        self.assertAlmostEqual(self.robot.y, 200)


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(800, 600)

    def test_avancer(self):
        self.sim.avancer(80)

        self.assertEqual(self.sim.robot.vG, 80)
        self.assertEqual(self.sim.robot.vR, 80)

    def test_reculer(self):
        self.sim.reculer(40)

        self.assertEqual(self.sim.robot.vG, -40)
        self.assertEqual(self.sim.robot.vR, -40)

    def test_tourner_sur_place(self):
        self.sim.tourner_sur_place(50)

        self.assertEqual(self.sim.robot.vG, 50)
        self.assertEqual(self.sim.robot.vR, -50)

    def test_freiner(self):
        self.sim.robot.vG = 100
        self.sim.robot.vR = 100

        self.sim.freiner(1)

        self.assertEqual(self.sim.robot.vG, 0)
        self.assertEqual(self.sim.robot.vR, 0)

    def test_distance_obstacle_positive(self):
        dist = self.sim.distance_obstacle()
        self.assertGreaterEqual(dist, 0)

    def test_obtenir_rectangle(self):
        rect = self.sim.obtenir_rectangle()
        self.assertEqual(len(rect), 4)

    def test_collision_type(self):
        obs = self.sim.obstacles[0]
        resultat = self.sim.collision(obs)
        self.assertIsInstance(resultat, bool)
