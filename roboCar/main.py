from Source import Simulation, GestionStrategies, Affichage

LARGEUR = 800
HAUTEUR = 600
FPS = 180

def main():
    affichage = Affichage(LARGEUR, HAUTEUR)
    sim = Simulation(LARGEUR, HAUTEUR)
    strat = GestionStrategies(sim)

    running = True
    strat.start()

    while running:
        affichage.clock.tick(FPS)
        strat.step()
        sim.update()
        running = affichage.update(sim.robot, sim.obstacles)

    affichage.stop()


if __name__ == "__main__":
    main()