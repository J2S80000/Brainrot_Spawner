# 🧠 Brainrot Spawn Simulator - Web Interface

Application web interactive pour simuler le spawn de brainrots avec affichage en temps réel et détection de doublons!

## 📋 Fonctionnalités

✅ **Affichage temps réel** - Chaque brainrot spawné s'affiche instantanément sur la page
✅ **Détection de doublons** - Signal visuel quand un même brainrot respawn
✅ **Statistiques en direct** - Total de spawns, doublons détectés, brainrots uniques
✅ **Images des brainrots** - Affichage des images depuis le wiki
✅ **Simulation configurable** - Contrôle la vitesse et le nombre de spawns
✅ **Interface responsive** - Fonctionne sur desktop, tablette et mobile

## 🚀 Installation & Lancement

### Option 1: Version Simple (Recommandée - Plus rapide à démarrer)

```bash
# Installer les dépendances (seulement Flask et Flask-CORS)
pip install Flask flask-cors

# Lancer le serveur
python app_simple.py

# Ouvrir dans le navigateur
http://localhost:5000
```

### Option 2: Version avec WebSocket (Temps réel optimal)

```bash
# Installer toutes les dépendances
pip install -r requirements.txt

# Lancer le serveur
python app.py

# Ouvrir dans le navigateur
http://localhost:5000
```

## 🎮 Utilisation

### Contrôles

1. **Un seul spawn** - Crée un brainrot unique
2. **Lancer simulation** - Crée plusieurs spawns en rafale
   - Nombre de spawns: 1-100
   - Vitesse: délai en ms entre les spawns (50-1000ms)
3. **Effacer** - Vide l'historique

### Interface

- **📢 Flux des spawns** (gauche): Affichage en temps réel avec images
- **⚙️ Contrôles** (droite): Paramètres et statistiques
- **⚠️ DOUBLON**: Label rouge si le brainrot spawne à nouveau

### Statistiques

- **Total spawns** - Nombre total de brainrots générés
- **Doublons** - Nombre de brainrots qui ont spawné plusieurs fois
- **Uniques** - Nombre de brainrots différents
- **Brainrots dispo** - 254 brainrots dans la base

## 📊 Exemple d'Affichage

```
✓ SPAWN: Skibidi            | Common    | Normal   | None    => 100 $
✓ SPAWN: Ohio Rizzler       | Rare      | Gold     | Minor   => 750 $
✓ SPAWN: Sigma Grindset     | Epic      | Diamond  | Major   => 4800 $ ⚠️ DOUBLON
```

## 🛠️ Fichiers Créés

- **app_simple.py** - Serveur Flask (Version simple)
- **app.py** - Serveur Flask avec WebSocket (Version avancée)
- **templates/index_simple.html** - Interface web simple
- **templates/index.html** - Interface web avec WebSocket
- **requirements.txt** - Dépendances Python
- **README.md** - Ce fichier

## 📦 Dépendances

### Version Simple
- Flask
- flask-cors

### Version Complète
- Flask
- flask-cors
- flask-socketio
- python-socketio
- python-engineio

## 🎨 Personnalisation

### Couleurs des Raretés

Dans le HTML/CSS, vous pouvez modifier les couleurs:
- Common: Gris (#95a5a6)
- Rare: Bleu (#3498db)
- Epic: Violet (#9b59b6)
- Legendary: Orange (#f39c12)
- God: Rouge (#e74c3c)

### Vitesse par Défaut

Modifier dans `app_simple.py` ou `app.py`:
```python
SPAWN_DELAY = 0.2  # Délai par défaut en secondes
```

## 🔧 Résolution de Problèmes

### "Address already in use"
Le port 5000 est déjà utilisé. Modifier dans le code:
```python
app.run(port=5001)  # Utiliser le port 5001
```

### Les images ne s'affichent pas
Les URLs du wiki peuvent nécessiter d'être correctes. Vérifier dans `master_list_generated.py` que les URLs commencent par `https://static.wikia.nocookie.net/`

### Erreur de dépendance
Installer les dépendances manquantes:
```bash
pip install -r requirements.txt
```

## 🎯 Prochaines Étapes

- [ ] Ajouter export CSV des statistiques
- [ ] Historique persistant en base de données
- [ ] Graphiques de distribution (Chart.js)
- [ ] Classement des brainrots les plus spawné
- [ ] Notifications sonores sur doublon
- [ ] Mode sombre

## 📝 Notes

- L'historique est limité à 500 spawns (configurable)
- Les données se réinitialisent au redémarrage du serveur
- Les images proviennent du wiki Fandom directement
- La détection de doublon vérifie les 10 derniers spawns

## 👨‍💻 Support

En cas de problème, vérifier:
1. Python 3.11+ est installé
2. Les dépendances sont à jour: `pip install --upgrade -r requirements.txt`
3. Le port 5000 est disponible
4. master_list_generated.py existe et contient les brainrots

Bonne chance! 🎮
