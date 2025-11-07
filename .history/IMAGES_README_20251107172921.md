# BRAINROT SPAWN SIMULATOR - AFFICHAGE DES IMAGES

## Vue d'ensemble

Le simulateur a été amélioré pour télécharger et afficher les images des brainrots lors de chaque spawn!

## Fichiers

### 1. `brainrot_spawn_simulator.py`
Le simulateur principal qui:
- Importe la `MASTER_LIST` avec les URLs d'images
- Spawn aléatoirement des brainrots
- **Télécharge et ouvre l'image** du brainrot
- Enregistre les données dans `brainrot_spawn_log.json`

### 2. `add_images_to_list.py`
Script utilitaire pour ajouter les images:
- Scrape chaque page de brainrot
- Extrait l'URL de l'image
- Ajoute les URLs à `master_list_generated.py`

### 3. `master_list_generated.py`
La liste maître avec:
- Nom du brainrot
- Rareté (Common, Rare, Epic, Legendary, God)
- Poids de spawn
- **URL de l'image** (nouveau!)

## Utilisation

### Étape 1: Ajouter les images (optional)
```bash
python add_images_to_list.py
```
**Note**: Cela peut prendre du temps (plusieurs minutes) car il doit accéder à chaque page.

### Étape 2: Lancer le simulateur avec images
```bash
python brainrot_spawn_simulator.py
```

Le simulateur va:
1. Spawn un brainrot aléatoire
2. Si une image est disponible:
   - Créer un dossier `brainrot_images/`
   - Télécharger l'image
   - L'ouvrir automatiquement dans la visionneuse par défaut
3. Afficher les informations du spawn

## Exemple de sortie

```
MASTER_LIST: 258 brainrots charges
=== SIMULATION DE SPAWN BRAINROT ===
SPAWN: Noobini Pizzanini | Common | Gold | Minor => 180.0$
  Telechargement de l'image...
  Image sauvegardee: brainrot_images/Noobini_Pizzanini.png
[Image s'ouvre automatiquement]

SPAWN: Strawberry Elephant | God | Diamond | Mythic => 100000.0$
  Telechargement de l'image...
  Image sauvegardee: brainrot_images/Strawberry_Elephant.png
[Image s'ouvre automatiquement]

...
```

## Structure des images

```
brainrot_images/
├── 1x1x1x1.png
├── 67.png
├── Admin_Lucky_Block.png
├── Noobini_Pizzanini.png
└── ...
```

## Dépendances

```bash
pip install requests beautifulsoup4
```

## Fonctionnalités

✨ **Téléchargement automatique** - Les images sont téléchargées lors du spawn
✨ **Affichage automatique** - L'image s'ouvre dans le programme par défaut
✨ **Cache local** - Les images sont sauvegardées pour réutilisation rapide
✨ **Gestion d'erreurs** - Pas de crash si une image est indisponible

## Notes

- Les premières exécutions seront plus lentes (téléchargement des images)
- Après cela, les images sont en cache local
- Toutes les images sont sauvegardées dans `brainrot_images/`
- La limite de taille des images aide à économiser la bande passante

---

**Version**: 2.0 (avec images)
**Date**: 2025-11-07
