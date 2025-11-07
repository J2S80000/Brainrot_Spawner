# 🧠 Brainrot Simulator - Advanced Dashboard Documentation

## 📚 Guide Complet pour Étudiants en Base de Données

Application web interactive avec **statistiques avancées**, **analyse probabiliste** et **système de jeu gamifié**.

---

## 🎯 Fonctionnalités Principales

### 1️⃣ **Simulateur de Spawn** (`🎮 Simulateur`)
- Génération aléatoire de brainrots
- Gestion des **variantes** (Normal/Gold/Diamond)
- Gestion des **mutations** (None/Minor/Major/Mythic)
- **Affichage en temps réel** avec images
- **Détection de doublons** automatique

### 2️⃣ **Prix & Finances** 💰
```
Prix = Base_Rareté × Type_Multiplier × Mutation_Multiplier

Base:
  - Common:    100$
  - Rare:      500$
  - Epic:      1,500$
  - Legendary: 5,000$
  - God:       20,000$

Multiplicateurs:
  - Normal:    ×1.0
  - Gold:      ×1.5
  - Diamond:   ×2.5
  
  - None:      ×1.0
  - Minor:     ×1.2
  - Major:     ×1.6
  - Mythic:    ×2.0
```

**Exemple**: Un God Diamond Mythic = 20,000 × 2.5 × 2.0 = **100,000$**

### 3️⃣ **Statistiques Avancées** (`📊 Statistiques`)

#### Graphiques Disponibles:
- **Répartition Raretés** (Pie chart): Distribution des 5 niveaux de rareté
- **Distribution Types** (Bar chart): Normal vs Gold vs Diamond
- **Distribution Mutations** (Donut chart): Répartition des 4 mutations
- **Top 10 Brainrots**: Les plus spawné

#### Métriques Statistiques:
- **Total spawns**: Nombre total de brainrots générés
- **Prix total**: Somme cumulée de tous les prix
- **Moyenne (μ)**: Prix moyen par spawn
- **Médiane**: Valeur médiane de la distribution
- **Min/Max**: Valeurs extrêmes
- **Écart-type (σ)**: Mesure de dispersion
- **Brainrots uniques**: Nombre de noms différents

### 4️⃣ **Analytics Avancée** (`📈 Analytics`)
*Pour étudiants en base de données et statistiques*

#### 🎲 Probabilités Cumulées
La probabilité d'avoir exactement cette combinaison de spawns est calculée comme:

$$P(\text{combinaison}) = \prod_{i=1}^{n} p_i^{k_i}$$

où:
- $p_i$ = probabilité théorique de la rareté $i$
- $k_i$ = nombre de spawns avec cette rareté
- Résultat: "1 sur X" (plus c'est grand, plus c'est rare!)

#### 📊 Entropie de Shannon
Mesure la diversité/uniformité de la distribution:

$$H = -\sum_{i} p_i \log_2(p_i)$$

- **H observée**: Entropie réelle de vos spawns
- **H théorique**: Entropie maximale possible (log₂(254) ≈ 8.0 bits)
- **Interprétation**: 
  - Si H proche du max → Distribution très uniforme
  - Si H faible → Distribution très biaisée

#### 💰 Distribution des Prix
- Histogramme du coût de chaque spawn
- Courbe cumulée du prix total
- Visualisation de la concentration de prix

#### Analyse Rarity
- Distribution des 5 raretés
- Comparaison avec MASTER_LIST théorique
- Écarts statistiques

### 5️⃣ **Mode Jeu** (`🎯 Jeu`)
Système de points gamifié pour progresser!

#### 🎮 Objectifs:

| Objectif | Cible | Points |
|----------|-------|--------|
| Accumuler 100,000$ | 100 K$ | ✓ Progress bar |
| Obtenir 5 Gods | 5 Gods | ✓ Progress bar |
| 50 Spawns uniques | 50 uniques | ✓ Progress bar |

#### ⭐ Système de Score:

```
+1 pt     = Chaque spawn
+5 pts    = Chaque Rare
+15 pts   = Chaque Epic
+50 pts   = Chaque Légendaire
+200 pts  = Chaque God
×2 mult   = Doublon (multiplicateur)
```

**Exemple**: Un God avec doublon = 200 × 2 = **400 pts** 🔥

#### 🏆 Achievements
- Débloqués automatiquement lors de la progression
- Bonus de points supplémentaires

---

## 🚀 Installation & Démarrage

### Prérequis
```bash
Python 3.11+
Flask
Flask-CORS
Chart.js (inclus via CDN)
```

### Installation des dépendances
```bash
pip install Flask flask-cors
```

### Lancement du serveur
```bash
python app_advanced.py
```

Puis accédez à: **http://localhost:5000**

---

## 📊 Cas d'Usage pour Étudiants BD

### 1. Analyse de Distribution
```sql
-- Requête équivalente SQL
SELECT rarity, COUNT(*) as count, 
       ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM spawns), 2) as percentage
FROM spawns
GROUP BY rarity
ORDER BY count DESC;
```

### 2. Statistiques Descriptives
```sql
SELECT 
  COUNT(*) as total_spawns,
  AVG(price) as avg_price,
  MIN(price) as min_price,
  MAX(price) as max_price,
  STDDEV(price) as std_deviation,
  MEDIAN(price) as median_price
FROM spawns;
```

### 3. Détection de Doublons (Duplicates)
```sql
SELECT name, COUNT(*) as spawn_count
FROM spawns
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY spawn_count DESC;
```

### 4. Entropie de Shannon (Base de Données)
```sql
SELECT 
  -SUM((count * 1.0 / total) * LOG2(count * 1.0 / total)) as shannon_entropy
FROM (
  SELECT rarity, COUNT(*) as count,
    (SELECT COUNT(*) FROM spawns) as total
  FROM spawns
  GROUP BY rarity
);
```

---

## 📈 Exemples de Résultats

### Exemple 1: Session Équilibrée
```
Total spawns: 100
Prix total: 125,500$
Moyenne: 1,255$
Entropie: 2.8 / 3.3 (84%)
Doublons: 5
Brainrots uniques: 95
```

**Interprétation**: Distribution assez uniforme, quelques doublons

### Exemple 2: Session Concentrée en Rares
```
Total spawns: 50
Prix total: 45,200$
Moyenne: 904$
Entropie: 1.2 / 3.3 (36%)
God count: 0
Rare count: 40
```

**Interprétation**: Distribution biaisée vers les Rares, pas de Gods

---

## 🎯 Conseils Pédagogiques

### Pour comprendre les Probabilités:
1. Générez 1000 spawns
2. Observez la probabilité cumulée (diminue avec chaque nouveau spawn)
3. Comparez avec la théorie: P = (prob_rarity)^count

### Pour comprendre l'Entropie:
1. Une session avec distribution uniforme → H haute
2. Une session avec beaucoup de Gods → H basse
3. L'entropie maximale = log₂(254) ≈ 8.0 bits

### Pour les Requêtes SQL:
Utilisez l'API Flask pour exporter les données en JSON:
```javascript
fetch('/api/advanced-stats')
  .then(r => r.json())
  .then(data => console.table(data))
```

---

## 🔧 Architecture Technique

### Backend (`app_advanced.py`)
```
/api/spawn              POST  → Génère 1 spawn
/api/spawn-many         POST  → Génère N spawns
/api/stats              GET   → Stats de base
/api/advanced-stats     GET   → Stats avancées (probabilités, entropie)
/api/history            GET   → Historique complet
/api/clear              POST  → Réinitialise
```

### Frontend (`index_advanced.html`)
```
Tab 1: Simulateur       → Contrôles, prix, compteurs
Tab 2: Statistiques     → Graphiques, distributions
Tab 3: Analytics        → Probabilités, entropie, analyse
Tab 4: Jeu              → Objectifs, score, achievements
```

---

## 📚 Ressources pour Approfondir

### Probabilités:
- [Loi Binomiale](https://fr.wikipedia.org/wiki/Loi_binomiale)
- [Probabilité Conditionnelle](https://fr.wikipedia.org/wiki/Probabilit%C3%A9_conditionnelle)

### Statistiques:
- [Entropie de Shannon](https://fr.wikipedia.org/wiki/Entropie_de_Shannon)
- [Écart-type et Variance](https://fr.wikipedia.org/wiki/%C3%89cart_type)

### Base de Données:
- SQL GROUP BY et agrégations
- Window Functions pour analyses avancées
- Indexation pour performances

---

## 🎓 Défi pour Étudiants

**Défi 1**: Générez 500 spawns et analysez l'écart avec la distribution théorique

**Défi 2**: Calculez la probabilité exacte d'obtenir 3 Gods en 100 spawns

**Défi 3**: Écrivez une requête SQL pour trouver le brainrot le plus "rentable" (prix/rareté)

**Défi 4**: Implémentez un système de recommandation basé sur les patterns de spawn

---

## 🆘 Troubleshooting

| Problème | Solution |
|----------|----------|
| "Port 5000 already in use" | `python app_advanced.py --port 5001` |
| Pas de graphiques | Vérifier la connexion internet (Chart.js CDN) |
| Stats vides | Générez au moins 1 spawn d'abord |
| Calculs incorrects | Rafraîchir la page (F5) |

---

## 📝 Fichiers du Projet

```
Brainrot/
├── app_advanced.py                    # Serveur Flask avancé
├── templates/
│   └── index_advanced.html            # Dashboard avec onglets
├── master_list_generated.py           # 254 brainrots
├── requirements.txt                   # Dépendances
└── ADVANCED_README.md                 # Ce fichier
```

---

## 🎉 Amusez-vous bien!

Cette application combine **gaming**, **statistiques** et **base de données** pour créer une expérience d'apprentissage interactive.

Questions? Ouvrez un issue sur GitHub! 📧

**Bonne chance dans vos spawns!** 🧠✨
