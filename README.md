# Astraya

## Idée de base
Notre première version du jeu était basé sur **Pyxel** et était un jeu avec histoire ou le but était de s'échapper d'une île en répondant au énigmes de ses habitants.
Après reconsidération nous somme passé sur **Pygames** et avons décidé de faire un jeu a monde ouvert type **Zelda**

## Principe
La map est générée grâce au fameux **Perlin noise** ou **bruit de Perlin** en français qui permet de générér un carte aléatoire sous forme d'un tableau.
Ce tableau est ensuite affiché sous formes de "tiles" ou tuiles en fonction de sa valeur dans le tableau *ex: "beach" afficheras une tile plage*.

<<<<<<< HEAD
### Utilisation
Pour lancer le jeu il s'uffit de lancer le fichier **start.bat** (sur Windows Uniquement) dans le dosssier **Astraya2.0**
=======
## Table des matières
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b

**Il est obligatoire pour le bon fonctionnement de Pygames d'utilise Python<=3.12**

<<<<<<< HEAD
**Modules requis** : lancer un cmd dans requirement.txt -> *pip install requierement.txt*
=======
---

## Historique du projet

La première version d'Astraya était développée sous **Pyxel**, un moteur de jeu rétro pour Python. Il s'agissait d'un jeu narratif linéaire : le joueur était échoué sur une île et devait s'en échapper en résolvant les énigmes proposées par ses habitants.

Face aux limitations de Pyxel en matière de performances et de flexibilité, le projet a été entièrement repensé. Astraya 2.0 passe sur **Pygame** et abandonne le format narratif au profit d'un monde ouvert sandbox, avec génération procédurale, système de combat, quêtes dynamiques et exploration libre.

---

## Fonctionnalités

### Actuellement implémenté

- Génération procédurale du monde via le bruit de Perlin
- Système de biomes avec transitions et tuiles de bordure
- Rendu par tuiles de 32x32 pixels avec zoom configurable
- Architecture en chunks pour la gestion spatiale de la carte
- Cache de rendu statique avec scrolling optimisé
- Système de collision par hitbox
- Placement et destruction de blocs
- Entités : joueur, ennemis, PNJ
- Système de projectiles
- Système de quêtes basé sur des événements (`QuestManager`, `Objective`)
- Dialogues avec effet machine à écrire
- Minimap
- Menu de paramètres (FPS, touches)
- Support manette via l'API joystick de Pygame
- Génération de donjons et zones de corruption
- Chargement du monde en thread de fond

### En cours / prévu

- Inventaire et système d'items
- Crafting
- Sauvegarde et chargement de partie
- Bande sonore et effets audio
- Contenu narratif et scénario principal

---

## Architecture technique

Astraya 2.0 repose sur plusieurs systèmes interconnectés :

| Système    | Description                                                                           |
| ---------- | ------------------------------------------------------------------------------------- |
| Rendu      | Cache statique par chunk, séparation des tuiles animées, Y-sorting pour la profondeur |
| Génération | Bruit de Perlin multi-octaves, biomes, zones de corruption, donjons                   |
| Spatial    | Index de chunks pour les entités et la végétation, collision O(1) par ensemble        |
| Entités    | Classe de base commune, héritage pour joueur / ennemi / PNJ                           |
| Quêtes     | Architecture événementielle, objectifs vérifiables, manager centralisé                |
| Threading  | Génération du monde en arrière-plan, accès partagé protégé via module `world_data`    |

---

## Prérequis

- **Python 3.12 ou antérieur** — Pygame n'est pas compatible avec Python 3.13+
- **pip**

Dépendances listées dans `requirements.txt`.

---

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/Jaguardu34/Astraya.git
cd Astraya/Astraya2.0
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Il est recommandé d'utiliser un environnement virtuel :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Lancer le jeu

```bash
python main.py
```

Le fichier `main.py` se trouve à la racine du dossier `Astraya2.0`.

---

## Contrôles

| Action               | Clavier         |
| -------------------- | --------------- |
| Se déplacer          | `Z` `Q` `S` `D` |
| Interagir / Attaquer | `E`             |
| Placer un bloc       | Clic gauche     |
| Détruire un bloc     | Clic droit      |
| Ouvrir le menu       | `Echap`         |
| Zoom                 | Molette souris  |

Les touches sont reconfigurables depuis le menu des paramètres. La manette est également supportée.

---

## Structure du projet

```
Astraya2.0/
├── main.py                  # Point d'entrée
├── requirements.txt
├── settings.py              # Constantes globales (taille des tuiles, FPS, etc.)
├── world_data.py            # Module partagé pour l'accès thread-safe à la carte
├── assets/
│   ├── tiles/               # Textures des tuiles par biome
│   ├── entities/            # Sprites joueur, ennemis, PNJ
│   └── ui/                  # Éléments d'interface
├── engine/
│   ├── world.py             # Génération et gestion du monde
│   ├── renderer.py          # Système de rendu et cache
│   ├── camera.py            # Caméra et scrolling
│   └── chunk.py             # Gestion des chunks
├── entities/
│   ├── player.py
│   ├── enemy.py
│   ├── npc.py
│   └── projectile.py
├── systems/
│   ├── quest_manager.py
│   ├── menu_manager.py
│   └── collision.py
└── ui/
    ├── minimap.py
    ├── dialog.py
    └── hud.py
```

---

## Génération du monde

La carte est générée via le **bruit de Perlin** (bibliothèque `noise`), qui produit un tableau 2D de valeurs continues entre -1 et 1. Ces valeurs sont ensuite mappées vers des biomes selon des seuils définis :

| Valeur      | Biome    |
| ----------- | -------- |
| < -0.3      | Océan    |
| -0.3 à -0.1 | Plage    |
| -0.1 à 0.2  | Plaine   |
| 0.2 à 0.5   | Forêt    |
| 0.5 à 0.75  | Montagne |
| > 0.75      | Neige    |

Les transitions entre biomes sont gérées par un système de tuiles de bordure (`TILE_EDGE`) indexées par `(biome_id, direction)`, permettant des rendus de bords et de coins cohérents visuellement. Des zones de corruption et des donjons sont ensuite injectés dans la carte via des passes de post-traitement.

### Utilisation

Pour lancer le jeu il s'uffit de lancer le fichier **start.bat** (sur Windows Uniquement) dans le dosssier **Astraya2.0**

## Roadmap

**Modules requis** : lancer un cmd dans requirement.txt -> _pip install requierement.txt_

> Projet en développement actif. Les contributions et retours sont les bienvenus.
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
