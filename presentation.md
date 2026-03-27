# Présentation du projet : Astraya

## Informations générales

* **Nom du projet** : *Astraya*
* **Type de projet** : Jeu vidéo
* **Niveau de scolarité** : Première
* **Professeur de NSI** : Clément Bringuier
* **Établissement** : Lycée Frédéric Bazille

---

## I - Présentation globale du projet

### Naissance de l’idée

Astraya est née d'un premier projet de deux membres du groupe. À la base, le jeu était très simple : le joueur se déplaçait case par case et les graphismes étaient très minimalistes.
À l'annonce des trophées de NSI, nous avons eu l'idée de reprendre ce projet et de l'améliorer.

### Problématique initiale

Notre projet ne répond pas vraiment à une problématique, étant donné qu'il s'agit d'un jeu. On peut tout de même se poser les questions suivantes :

* **Comment générer un monde procédural ?**
* **Comment créer un système de quêtes narratif ?**
* **Comment implémenter un système de donjons et de combat ?**
* **Comment créer des animaux et des ennemis capables de réaliser des actions ?**

### Objectifs

Le but de notre projet est de proposer un jeu entièrement développé en Python par notre équipe et de voir jusqu'à quel point nous pouvons le rendre complet et fonctionnel.

---

## II - Organisation du travail

### Présentation de l'équipe

Notre équipe est composée de 4 élèves de première.

### Rôle de chacun

* **Lucas** : Développement du moteur de jeu et de la physique, déplacements des entités, menus
* **Pau** : Développement de la carte, quêtes, boss principal
* **Saina** : Développement du système d'inventaire, des items et de la pose de blocs
* **Elouan** : Développement des textures et de la trame narrative

### Répartition des tâches

Nous avons réparti le travail de manière à éviter de travailler sur les mêmes aspects, afin de rendre le projet le plus abouti possible.

### Temps passé sur le projet

Nous n'avons pas compté précisément le nombre d'heures passées sur le projet, mais cela représente sans doute plusieurs dizaines d'heures par membre.

---

## III - Présentation des étapes du projet

Le développement de notre jeu s'est déroulé en plusieurs étapes :

1. Adaptation du moteur de jeu initialement développé avec Pyxel vers Pygame
2. Génération de la carte à l’aide de Perlin Noise et de NumPy
3. Création des classes d'animaux, d'ennemis, de PNJ et des autres éléments de gameplay
4. Mise en place des quêtes, des mécaniques de combat et des donjons
5. Création des graphismes et des textures
6. Tests et correction des bugs mineurs

Cependant, certaines étapes se sont déroulées tout au long du projet. Par exemple, les textures ont été réalisées progressivement afin de visualiser l'avancement du jeu.

---

## IV - Validation de l’opérationnalité et du fonctionnement

### État d'avancement

Le jeu est jouable :

* Le monde se génère sans problème
* Le joueur peut se déplacer, attaquer et utiliser des outils
* Les animaux, ennemis et PNJ fonctionnent et réalisent leurs actions définies
* Le système de quêtes est fonctionnel et les donjons sont accessibles

### Vérification de l'absence de bugs

Nous avons fait tester notre jeu à nos familles et amis dans le but qu'ils trouvent d'éventuels bugs.

### Difficultés rencontrées et solutions

Nous avons rencontré plusieurs difficultés auxquelles nous avons trouvé des solutions :
