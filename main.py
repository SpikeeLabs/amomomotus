import argparse

from games.engine import MotusEngine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motus game")
    parser.add_argument("-t", "--team", type=int, default=2, help="Number of teams playing", choices=range(1, 6))

    namespace = parser.parse_args()

    application = MotusEngine(namespace.team)
    application.launch()
