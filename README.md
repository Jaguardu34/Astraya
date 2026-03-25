# Astraya

## Idée de base
Notre première version du jeu était basé sur **Pyxel** et était un jeu avec histoire ou le but était de s'échapper d'une île en répondant au énigmes de ses habitants.
Après reconsidération nous somme passé sur **Pygames** et avons décidé de faire un jeu a monde ouvert type **Zelda**

## Principe
La map est générée grâce au fameux **Perlin noise** ou **bruit de Perlin** en français qui permet de générér un carte aléatoire sous forme d'un tableau.
Ce tableau est ensuite affiché sous formes de "tiles" ou tuiles en fonction de sa valeur dans le tableau *ex: "beach" afficheras une tile plage*.

### Utilisation
Pour lancer le jeu il s'uffit de lancer le fichier **start.bat** (sur Windows Uniquement) dans le dosssier **Astraya2.0**

**Il est obligatoire pour le bon fonctionnement de Pygames d'utilise Python<=3.12**

**Modules requis** : lancer un cmd dans requirement.txt -> *pip install requierement.txt*
