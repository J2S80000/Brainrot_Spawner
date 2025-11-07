# 📊 Tableau Comparatif - Avant/Après

## État des 3 Graphiques

### AVANT ❌

| Graphique | État | Raison |
|-----------|------|--------|
| 📊 Distribution Théorique | ❌ Vide | Code JavaScript manquant |
| 💰 Distribution Prix | ❌ Vide | Pas de bucketisation des prix |
| 📈 Prix Cumulé | ❌ Vide | Pas de cumsum calculé |

### APRÈS ✅

| Graphique | État | Détails |
|-----------|------|---------|
| 📊 Distribution Théorique | ✅ Fixé | Bar chart (Common/Rare/Epic/Legendary/God) |
| 💰 Distribution Prix | ✅ Fixé | Bar chart (5 buckets: 100-500$, 500-2K$, etc) |
| 📈 Prix Cumulé | ✅ Fixé | Line chart courbe verte croissante |

---

## 🔧 Modifications Effectuées

### Fichier: `index_advanced.html`

#### 1. Function `updateCharts(stats)` - Ligne ~580
**Avant:**
```javascript
// Seulement 2 graphiques (rarity et type)
```

**Après:**
```javascript
// +1 graphique: mutations distribution
const mutationCtx = document.getElementById('mutationChart');
// ... code pour créer graphique mutations
```

---

#### 2. Function `updateAdvancedStats(adv)` - Ligne ~620
**Avant:**
```javascript
// Seulement affichage des stats textuelles
document.getElementById('sumTotal').textContent = adv.total_spawns;
// ... etc
```

**Après:**
```javascript
// +3 graphiques complets
// 1. Distribution Théorique (bar chart)
const theoreticalCtx = document.getElementById('theoreticalChart');
charts.theoretical = new Chart(theoreticalCtx, { ... });

// 2. Distribution des Prix (bar chart)
const priceDistCtx = document.getElementById('priceDistributionChart');
fetch('/api/history?limit=1000').then(r => r.json()).then(history => {
  // Bucketiser les prix
  // Créer graphique
});

// 3. Prix Cumulé (line chart)
const cumulativePriceCtx = document.getElementById('cumulativePriceChart');
fetch('/api/history?limit=1000').then(r => r.json()).then(history => {
  // Calculer cumsum
  // Créer courbe
});
```

---

### Fichier: `app_advanced.py`

#### Route `/test` - Nouvelle
```python
@app.route('/test')
def test():
    """Servir la page HTML de test."""
    return render_template('test_graphs.html')
```

---

## 📊 Les Graphiques Détaillés

### #1: Distribution Théorique 📊
```
Type: Bar Chart
Source: adv.rarity_distribution (de MASTER_LIST)
Axe X: Common | Rare | Epic | Legendary | God
Axe Y: Nombre de brainrots
Couleurs: [Gris, Bleu, Violet, Orange, Rouge]
Utilité: Comparer avec distribution observée
```

**Exemple de données:**
```
Common:    95 brainrots
Rare:      45 brainrots
Epic:      45 brainrots
Legendary: 45 brainrots
God:       24 brainrots
```

---

### #2: Distribution des Prix 💰
```
Type: Bar Chart
Source: Historique des spawns buckétisé
Axe X: 100-500$ | 500-2K$ | 2K-5K$ | 5K-10K$ | 10K+$
Axe Y: Nombre de spawns
Couleur: Bleu gradient (#667eea)
Utilité: Voir concentration des coûts
```

**Logique de buckétisation:**
```javascript
if (price < 500) priceBuckets['100-500']++;
else if (price < 2000) priceBuckets['500-2000']++;
else if (price < 5000) priceBuckets['2000-5000']++;
else if (price < 10000) priceBuckets['5000-10000']++;
else priceBuckets['10000+']++;
```

---

### #3: Prix Cumulé 📈
```
Type: Line Chart (Courbe)
Source: Calcul cumulatif de l'historique
Axe X: Numéro du spawn (échantillonné tous les 5%)
Axe Y: Prix total accumulé ($)
Couleur: Vert (#27ae60) avec fill léger
Utilité: Voir croissance progressive
```

**Calcul du cumsum:**
```javascript
let cumsum = 0;
history.forEach((spawn, idx) => {
  cumsum += spawn.price;
  // Ajouter un point à chaque 5% de l'historique
  if (idx % Math.max(1, Math.floor(history.length / 20)) === 0) {
    cumulativePrices.push(cumsum);
    labels.push(`#${idx + 1}`);
  }
});
```

---

## 🎯 Résultats Observables

### Après 50 spawns typiques:

**Distribution Théorique:**
```
Common:    95     █████████████████████████████
Rare:      45     █████████████
Epic:      45     █████████████
Legendary: 45     █████████████
God:       24     ████████
```

**Distribution Prix:**
```
100-500$:    30 spawns  ██████████████████
500-2K$:     12 spawns  ███████
2K-5K$:      5 spawns   ███
5K-10K$:     2 spawns   █
10K+$:       1 spawn    █
```

**Prix Cumulé:**
```
$
100,000  │                                    ╱
50,000   │                          ╱╱╱╱╱╱╱╱
10,000   │                    ╱╱╱╱╱
  0      │╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱
         └─────────────────────────
           0   10  20  30  40  50 spawns
```

---

## 🧮 Formules Utilisées

### Distribution des Prix (Buckétisation)
```
bucket = {
  '100-500':    count(100 ≤ p < 500),
  '500-2000':   count(500 ≤ p < 2000),
  '2000-5000':  count(2000 ≤ p < 5000),
  '5000-10000': count(5000 ≤ p < 10000),
  '10000+':     count(p ≥ 10000)
}
```

### Prix Cumulé
```
CumSum(i) = Σ(price[0] à price[i])
Label(i) = "#" + spawn_number[i]
```

---

## 🚀 Utilisation Immédiate

### Accès Direct
```
1. Ouvrez: http://localhost:5000
2. Onglet "📈 Analytics"
3. Génériez 50 spawns
4. Voyez les 3 graphiques se remplir!
```

### Test Isolé
```
1. Ouvrez: http://localhost:5000/test
2. Cliquez "📊 Générer 50 spawns"
3. Attendez...
4. 4 graphiques apparaissent!
```

---

## ✅ Validation

Les graphiques sont corrects si:
- [ ] Distribution Théorique montre 5 barres (inégales)
- [ ] Distribution Prix a peak à gauche (beaucoup de Common)
- [ ] Prix Cumulé est une courbe croissante
- [ ] Les valeurs correspondent aux stats (en haut)
- [ ] Pas d'erreur dans la console (F12)

---

## 📚 Pour Aller Plus Loin

### Améliorations Futures
1. **Export CSV** des données
2. **Animation** des graphiques
3. **Comparaison** multiple de sessions
4. **Analyse de tendance** (moindres carrés)
5. **Heatmap** des spawns

### Concepts Connexes
- Loi des Grands Nombres
- Théorème Central Limite
- Analyse de Variance (ANOVA)
- Régression Linéaire

---

**Bon apprentissage!** 🎓📊
