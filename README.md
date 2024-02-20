# $${\color{gray} A \color{black} MO \color{gray} MO \color{black} M \color{orange} O  \color{black} TUS }$$


Ce projet est conçu pour fournir une expérience incroyable en utilisant les dernières technologies pour une immersion totale dans le monde des grandes émissions de la télévision.

# Requirements

1. Python, at least 3.10

2. Poetry, any stable version since 1.2 but idealy requires 1.3 or above <br>
<https://python-poetry.org/docs/#installation>

# Installation

**Windows**

```sh
poetry install
poetry run python main.py -h
```

**Linux**

```sh
poetry install
poetry run python main.py -h
```

You may also need additional requirements for Ubuntu users:

```sh
sudo apt-get install -y libxcb-cursor
```

# Règles du jeu Motus

## Nombre d'équipes

Le jeu peut accueillir 1 à 5 équipes. Chaque équipe joue à tour de rôle.

> Les équipes (avec leur mini-grille de bingo et leur score) sont affichés sur la gauche. L'équipe qui joue est encadrée en blanc.

## Déroulement d'un tour

Le but est de trouver le mot mystère en maximum 6 propositions et marquer le plus de points.

**Proposition mot**

Les mots proposés doivent en théorie exister dans le dictionnaire. Les mots plus petit sont acceptés.

> La case lumineuse indique le curseur.<br>
> Les lettres présentes et bien placées sont indiquées en rouge 🟥.<br>
> Les lettres présentes mais mal placées sont cerclées de jaune 🟡.

<!-- markdownlint-disable MD033 -->
1. Si l'équipe <u>ne trouve pas le mot</u> :<br>
1.1. elle passe la main à l'équipe suivante.

1. Si l'équipe <u>trouve le mot</u> :<br>
2.1. elle gagne des points en fonction du nombre d'essais utilisés ;<br>
2.2. elle tire une première boule.


**Tirage boule**

Le but est compléter une ligne, une colonne ou une diagonale pour marquer un bonus de points. Les tirages des boules se font sans remise. Quand un bingo est compléter, l'équipe marque 100 points et la grille est réinitialisée.

> La grille détaillée de l'équipe qui joue est affichée en haut à gauche.

1. Si l'équipe tire <u>une boule présente</u> dans sa grille :<br>
1.1. elle coche cette case dans la grille ;<br>
1.2. si la boule est noire ou termine un bingo, l'équipe passe la main sinon tire une seconde boule.<br>

2. Si l'équipe tire <u>une boule noire</u> :<br>
2.1. elle perd 20 points et passe la main.

**Fin du Tour**

Le tour se termine une fois que toutes les équipes ont joué et que chaque équipe a eu l'opportunité de proposer un mot.

**Fin du Jeu**

Le jeu continue avec des tours successifs jusqu'à ce qu'un certain nombre de tours prédéfini soit atteint ou jusqu'à ce qu'une condition de fin soit remplie, selon les préférences des joueurs.
