"""
Serveur Flask simple pour l'application Brainrot Spawn Simulator
(Version alternative sans WebSocket si les dépendances posent problème)
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import time
import json
import threading
from master_list_generated import MASTER_LIST

app = Flask(__name__)
CORS(app)

# === PRIX DE BASE ===
RARITY_VALUES = {
    "Common": 100,
    "Rare": 500,
    "Epic": 1500,
    "Legendary": 5000,
    "God": 20000
}

# === VARIANTES ET MUTATIONS ===
TYPE_MULTIPLIERS = {"Normal": 1.0, "Gold": 1.5, "Diamond": 2.5}
TYPE_WEIGHTS = [80, 15, 5]

MUTATION_MULTIPLIERS = {"None": 1.0, "Minor": 1.2, "Major": 1.6, "Mythic": 2.0}
MUTATION_WEIGHTS = [70, 20, 8, 2]

# === ETAT DE L'APPLICATION ===
spawn_history = []
max_history = 500
simulation_running = False

def spawn_brainrot():
    """Génère un brainrot aléatoire avec toutes ses statistiques."""
    selected = random.choices(MASTER_LIST, weights=[b["spawn_weight"] for b in MASTER_LIST], k=1)[0]
    type_selected = random.choices(list(TYPE_MULTIPLIERS.keys()), weights=TYPE_WEIGHTS, k=1)[0]
    mutation_selected = random.choices(list(MUTATION_MULTIPLIERS.keys()), weights=MUTATION_WEIGHTS, k=1)[0]
    
    base_value = RARITY_VALUES[selected["rarity"]]
    final_price = base_value * TYPE_MULTIPLIERS[type_selected] * MUTATION_MULTIPLIERS[mutation_selected]
    final_price = round(final_price, 2)
    
    spawn_data = {
        "id": f"{len(spawn_history)}_{int(time.time()*1000)}",
        "name": selected["name"],
        "rarity": selected["rarity"],
        "type": type_selected,
        "mutation": mutation_selected,
        "price": final_price,
        "image_url": selected.get("image_url", ""),
        "timestamp": time.time(),
        "is_duplicate": False
    }
    
    # Vérifier si c'est un doublon
    for recent_spawn in spawn_history[-10:]:  # Vérifier les 10 derniers spawns
        if recent_spawn["name"] == spawn_data["name"]:
            spawn_data["is_duplicate"] = True
            break
    
    # Garder historique limité
    spawn_history.append(spawn_data)
    if len(spawn_history) > max_history:
        spawn_history.pop(0)
    
    return spawn_data

@app.route('/')
def index():
    """Servir la page HTML principale."""
    return render_template('index_simple.html')

@app.route('/api/spawn', methods=['POST'])
def api_spawn():
    """API pour créer un spawn."""
    spawn_data = spawn_brainrot()
    return jsonify(spawn_data)

@app.route('/api/spawn-many', methods=['POST'])
def api_spawn_many():
    """API pour créer plusieurs spawns."""
    data = request.json
    count = min(data.get('count', 1), 100)  # Limiter à 100 max
    speed = data.get('speed', 1.0)
    
    spawns = []
    for i in range(count):
        spawn_data = spawn_brainrot()
        spawns.append(spawn_data)
        time.sleep(max(0.05 / speed, 0.01))  # Délai minimum
    
    return jsonify(spawns)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retourner les statistiques globales."""
    duplicates = sum(1 for s in spawn_history if s["is_duplicate"])
    
    return jsonify({
        "total_spawns": len(spawn_history),
        "duplicates": duplicates,
        "unique_brainrots": len(set(s["name"] for s in spawn_history)),
        "rarity_breakdown": get_rarity_breakdown(),
        "type_breakdown": get_type_breakdown()
    })

def get_rarity_breakdown():
    """Calculer la répartition des raretés."""
    breakdown = {}
    for spawn in spawn_history:
        rarity = spawn["rarity"]
        breakdown[rarity] = breakdown.get(rarity, 0) + 1
    return breakdown

def get_type_breakdown():
    """Calculer la répartition des types."""
    breakdown = {}
    for spawn in spawn_history:
        type_ = spawn["type"]
        breakdown[type_] = breakdown.get(type_, 0) + 1
    return breakdown

@app.route('/api/history', methods=['GET'])
def get_history():
    """Retourner l'historique des spawns."""
    limit = request.args.get('limit', 100, type=int)
    return jsonify(spawn_history[-limit:])

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Effacer l'historique."""
    global spawn_history
    spawn_history.clear()
    return jsonify({"message": "Historique effacé"})

if __name__ == '__main__':
    print(f"Serveur démarré avec {len(MASTER_LIST)} brainrots disponibles")
    print("Accédez à: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
