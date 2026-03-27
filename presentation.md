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

Astraya est née d'un premier projet de deux membres du groupe. À la base, le jeu était très simple : le joueur bougeait case par case et les graphismes étaient très minimalistes.
À l'annonce des trophées de NSI, nous avons eu l'idée de reprendre ce projet et de l'améliorer.

### Problématique initiale

Notre projet ne répond pas vraiment à une problématique étant donné qu'il s'agit d'un jeu. On peut tout de même se demander :

* **Comment générer un monde procédural ?**
* **Comment créer un système de quêtes narratif ?**
* **Comment implémenter un système de donjon et de combat ?**
* **Comment créer des animaux et ennemis qui réalisent des actions ?**

### Objectifs

Le but de notre projet est de proposer un jeu entièrement développé en Python par notre équipe et de voir à quels points

---

## II - Organisation du travail

### Présentation de l'équipe

Notre équipe est composée de 4 élèves de première.

### Rôle de chacun

* **Lucas** : Développement du moteur de jeu et de physique + déplacement des entités + menus
* **Pau** : Développement de la map + quêtes + boss principal
* **Saina** : Développement du système d'inventaire, des items + pose de blocs
* **Elouan** : Développement des textures + trame narrative

### Répartition des tâches

Nous avons réparti le travail de manière à ne pas passer du temps sur des choses similaires, afin de rendre un projet le plus abouti possible.

### Temps passé sur le projet

Nous n'avons pas compté le nombre d'heures passées sur le projet, mais cela se compte sans doute en plusieurs dizaines d'heures par membre.

---

## III - Présentation des étapes du projet

Le développement du notre jeu s'est déroulé en plusieurs étapes : 

1. Adaptation du moteur de jeu initialement développé avec Pyxel vers Pygame.
2. Génération de la carte à l’aide de Perlin Noise et de NumPy
3. Création des classes d'animaux, d'ennemis, des PNJ, et des autres éléments de gameplay
4. Mise en place des quêtes, des méchaniques de combats et des donjons
5. Création des graphismes et des textures
6. Tests et correction des bugs mineurs

Cependant certaines étapes se sont déroulés tout au long du projet par exemples les textures ont été faites tout au long du projet dans le nut de voir l'avancement du projet

## IV - Validation de l’opérationnalité et du fonctionnement 

### Etat d'avancement 

Le jeu est jouable  :

* Le monde se génère sans problème
* Le joueur peut se déplacer, attaquer et utiliser des outils
* Les animaux, enemis et PNJ fonctionent et réalisent leurs actions définis
* Le système de quête est fonctionel, les donjons sont accessibles 

### Vérification de l'absence de bugs

Nous avons fait tester notre jeu a nos familles et amis dans le but qu'ils trouvent des bugs.

### Difficultés rencontrées et solutions

Nous avons rencontrés plusieurs difficultés auquels nous avons trouver des solutions :

