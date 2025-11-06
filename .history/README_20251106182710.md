# 🧠 Brainrot Spawn Simulator - Extraction Dynamique

## 📋 Vue d'ensemble

Ce projet utilise une **extraction dynamique** des données depuis le wiki Fandom pour populator une `MASTER_LIST` de brainrots. Le scraper se connecte au wiki en temps réel via l'API Fandom et génère les fichiers nécessaires automatiquement.

## 🏗️ Architecture

### 1. **scraper_brainrots.py** - Scraper Dynamique
- Récupère la liste des brainrots depuis l'API Fandom: `https://stealabrainrot.fandom.com/api/v1/Articles/List`
- Filtre intelligent des fichiers multimédias (.png, .jpg, .gif, .webp, etc.)
- Supporte la pagination pour extraire **tous les brainrots disponibles**
- Génère deux fichiers:
  - `master_list.json` - Format JSON pour inspection
  - `master_list_generated.py` - Module Python importable

**Résultats d'extraction:**
- **Total brainrots extraits**: 254 (258 - 4 fichiers multimédias)
- **Source**: Catégorie officielle du wiki Fandom

**Distribution de raretés:**
- **Common** (35%): 89 brainrots - Poids de spawn 40
- **Rare** (20%): 51 brainrots - Poids de spawn 25
- **Epic** (20%): 51 brainrots - Poids de spawn 15
- **Legendary** (15%): 38 brainrots - Poids de spawn 10
- **God** (10%): 25 brainrots - Poids de spawn 5

### 2. **brainrot_spawn_simulator.py** - Simulateur
- Importe la `MASTER_LIST` générée
- Simule le spawn de brainrots avec:
  - Types: Normal, Gold, Diamond
  - Mutations: None, Minor, Major, Mythic
  - Calcul du prix basé sur rareté × type × mutation
- Exporte le journal en JSON

## 🚀 Utilisation

### Étape 1: Générer la MASTER_LIST
```bash
python scraper_brainrots.py
```

**Sortie attendue:**
```
============================================================
🧠 GÉNÉRATEUR DE MASTER LIST - BRAINROT SIMULATOR
============================================================
🔄 Scraping du wiki Fandom en cours (API method)...
  📡 Requête vers l'API Fandom...
  ✅ API: 254 brainrots trouvés!

✅ Total final: 254 brainrots extraits!

✅ Total brainrots générés: 254

📊 Distribution par rareté:
  Common       |  89 items |  35.04%
  Rare         |  51 items |  20.08%
  Epic         |  51 items |  20.08%
  Legendary    |  38 items |  14.96%
  God          |  25 items |   9.84%

💾 Fichiers générés:
  - master_list.json
  - master_list_generated.py

✨ Extraction complète!
============================================================
```

### Étape 2: Lancer le simulateur
```bash
python brainrot_spawn_simulator.py
```

**Sortie attendue:**
```
📊 MASTER_LIST: 254 brainrots chargés
=== Simulation de Spawn Brainrot ===
🧠 Aquanut | Common | Normal | None → 💰 100.0$
🧠 Tigrilini Watermelini | Legendary | Normal | None → 💰 5000.0$
...
✅ Journal exporté dans brainrot_spawn_log.json
```

## 📁 Fichiers du Projet

### Structure
```
Brainrot/
├── scraper_brainrots.py          (12.9 KB) - Scraper dynamique
├── brainrot_spawn_simulator.py    (2.0 KB) - Simulateur principal
├── master_list_generated.py       (19.2 KB) - Liste générée (importable)
├── master_list.json               (23.6 KB) - Export JSON
├── brainrot_spawn_log.json        (1.6 KB) - Journal de simulation
├── README.md                      (4.4 KB) - Documentation
```

### `master_list_generated.py`
Module Python contenant la liste complète des 254 brainrots avec leurs raretés:

```python
MASTER_LIST = [
    {"name": "1x1x1x1", "rarity": "Common", "spawn_weight": 40},
    {"name": "67", "rarity": "Common", "spawn_weight": 40},
    ...
    {"name": "Zombie Tralala", "rarity": "God", "spawn_weight": 5},
]
```

### `master_list.json`
Format JSON pour analyse et inspection des données. Peut être utilisé pour:
- Analyse statistique
- Intégration avec d'autres outils
- Vérification des données

### `brainrot_spawn_log.json`
Journal des spawns générés pendant la simulation:
```json
[
  {
    "name": "Aquanut",
    "rarity": "Common",
    "type": "Normal",
    "mutation": "None",
    "price": 100.0
  },
  ...
]
```

## 🔧 Méthodes de Scraping

### Méthode 1: API Fandom (Primaire) ⭐
- Utilise l'endpoint officiel: `/api/v1/Articles/List`
- Paramètres: `category`, `limit`, `offset`
- Limite augmentée à 500 pour capturer tous les articles
- Support de la pagination pour déborder la limite

### Méthode 2: HTML Scraping (Fallback)
- Extraction directe depuis la page HTML
- Utilise BeautifulSoup pour parser les liens
- Utilisé si l'API retourne peu de résultats

### Filtrage Intelligent
Exclut automatiquement:
- Fichiers multimédias (.png, .jpg, .gif, .webp, .svg, .mp4, .webm)
- Pages système (Category, File, User, Talk, Special, Help)
- Contenu de gestion de wiki (Gallery, blog, Discuss)
- Éléments UI (Edit, Sign, View, NEXT)

## 💡 Avantages de l'Extraction Dynamique

✅ **Complétude** - 254 brainrots authentiques extraits (vs 199 en scraping HTML)  
✅ **Mise à jour automatique** - Nouvelles données du wiki intégrées directement  
✅ **API officielle** - Utilise l'endpoint Fandom approuvé  
✅ **Filtrage intelligent** - Exclut les fichiers non pertinents  
✅ **Flexibilité** - Facile à adapter les filtres  
✅ **Traçabilité** - Source des données clairement identifiée  
✅ **Scalabilité** - Support de la pagination  
✅ **Fallback robuste** - Utilise une liste par défaut en cas de problème réseau  

## 🐛 Dépannage

### Erreur: "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests beautifulsoup4
```

### Erreur: "No module named 'master_list_generated'"
S'assurer que le scraper a été exécuté au préalable:
```bash
python scraper_brainrots.py
```

### Erreur: "Connection timeout"
Le réseau peut être instable. Le scraper basculera automatiquement sur la liste par défaut.

### Brainrots insuffisants extraits
Vérifier:
1. Que la limite API est bien à 500
2. Que le filtrage ne supprime pas trop de résultats
3. Que la connexion Internet fonctionne

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| **Total brainrots** | 254 |
| **Méthode** | API Fandom v1 |
| **Temps d'extraction** | ~2-5 secondes |
| **Taille JSON** | 23.6 KB |
| **Taille Python** | 19.2 KB |
| **Brainrots Common** | 89 (35%) |
| **Brainrots God** | 25 (10%) |

## 🔗 Source des Données

- **Wiki Principal**: https://stealabrainrot.fandom.com/wiki/Category:Brainrots
- **API Endpoint**: https://stealabrainrot.fandom.com/api/v1/Articles/List
- **Catégorie**: Brainrots
- **Mise à jour**: En temps réel lors du scraping

## 🎨 Exemples de Brainrots

### Common
- 1x1x1x1
- 67
- Aquanut
- Bananita Dolphinita

### Rare
- Chachechi
- Dragon Cannelloni
- Espresso Signora

### Epic
- Garama and Madundung
- Headless Horseman
- John Pork

### Legendary
- Matteo
- Meowl
- Mythic Lucky Block

### God
- Noobini Pizzanini
- Sigma Boy
- Yess my examine
- Zombie Tralala

## 🔄 Workflow Complet

```
┌─────────────────────────────────────┐
│ 1. Exécuter scraper_brainrots.py    │
│    - Se connecte à l'API Fandom     │
│    - Télécharge 254 brainrots       │
│    - Génère master_list_generated.py│
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. Exécuter brainrot_spawn_simulator│
│    - Importe master_list_generated  │
│    - Lance la simulation            │
│    - Génère spawn_log.json          │
└─────────────────────────────────────┘
```

---

**Version**: 2.0 (Extraction API complète - 254 brainrots)  
**Dernière mise à jour**: 2025-11-06  
**Auteur**: GitHub Copilot
