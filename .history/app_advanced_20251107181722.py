"""
Serveur Flask avancé avec statistiques probabilistes et système de jeu
Version avec Dashboard de stats avancées pour les étudiants en base de données
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import time
import json
import threading
from collections import Counter
from master_list_generated import MASTER_LIST
import math

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
max_history = 1000
game_state = {
    "total_price": 0,
    "spawns_count": 0,
    "rare_count": 0,
    "epic_count": 0,
    "legendary_count": 0,
    "god_count": 0,
    "combo_count": 0  # Nombre de brainrots qui ont spawné plus de 2 fois
}

def calculate_rarity_distribution():
    """Calculer la distribution des raretés dans MASTER_LIST"""
    distribution = {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 0, "God": 0}
    for brainrot in MASTER_LIST:
        distribution[brainrot["rarity"]] += 1
    
    # Calculer les probabilités
    total = len(MASTER_LIST)
    probabilities = {}
    for rarity, count in distribution.items():
        probabilities[rarity] = round((count / total) * 100, 2)
    
    return distribution, probabilities

def calculate_cumulative_probability(spawn_list):
    """Calculer la probabilité cumulée d'avoir la combinaison actuelle"""
    if not spawn_list:
        return 100.0
    
    rarity_counts = Counter(s["rarity"] for s in spawn_list)
    distribution, probabilities = calculate_rarity_distribution()
    
    # Probabilité binomiale simplifiée
    prob = 1.0
    for rarity, count in rarity_counts.items():
        p = probabilities[rarity] / 100  # Convertir en probabilité
        # P(k succès) = p^k
        prob *= (p ** count)
    
    # Convertir en "chance sur X"
    if prob > 0:
        chance_on_x = 1 / prob
        return round(chance_on_x, 0)
    return float('inf')

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
        "is_duplicate": False,
        "spawn_count": 1
    }
    
    # Vérifier si c'est un doublon
    duplicate_count = 0
    for recent_spawn in spawn_history[-20:]:  # Vérifier les 20 derniers spawns
        if recent_spawn["name"] == spawn_data["name"]:
            spawn_data["is_duplicate"] = True
            duplicate_count += 1
    
    spawn_data["spawn_count"] = duplicate_count + 1
    
    # Mettre à jour les stats globales
    game_state["total_price"] += final_price
    game_state["spawns_count"] += 1
    
    rarity = selected["rarity"]
    if rarity == "Rare":
        game_state["rare_count"] += 1
    elif rarity == "Epic":
        game_state["epic_count"] += 1
    elif rarity == "Legendary":
        game_state["legendary_count"] += 1
    elif rarity == "God":
        game_state["god_count"] += 1
    
    if duplicate_count > 1:
        game_state["combo_count"] += 1
    
    # Garder historique limité
    spawn_history.append(spawn_data)
    if len(spawn_history) > max_history:
        spawn_history.pop(0)
    
    return spawn_data

@app.route('/')
def index():
    """Servir la page HTML principale."""
    return render_template('index_advanced.html')

@app.route('/api/spawn', methods=['POST'])
def api_spawn():
    """API pour créer un spawn."""
    spawn_data = spawn_brainrot()
    return jsonify(spawn_data)

@app.route('/api/spawn-many', methods=['POST'])
def api_spawn_many():
    """API pour créer plusieurs spawns."""
    data = request.json
    count = min(data.get('count', 1), 100)
    speed = data.get('speed', 1.0)
    
    spawns = []
    for i in range(count):
        spawn_data = spawn_brainrot()
        spawns.append(spawn_data)
        time.sleep(max(0.05 / speed, 0.01))
    
    return jsonify(spawns)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retourner les statistiques globales."""
    distribution, probabilities = calculate_rarity_distribution()
    duplicates = sum(1 for s in spawn_history if s["is_duplicate"])
    
    return jsonify({
        "total_spawns": len(spawn_history),
        "total_price": game_state["total_price"],
        "average_price": round(game_state["total_price"] / max(len(spawn_history), 1), 2),
        "duplicates": duplicates,
        "unique_brainrots": len(set(s["name"] for s in spawn_history)),
        "rarity_breakdown": get_rarity_breakdown(),
        "type_breakdown": get_type_breakdown(),
        "god_count": game_state["god_count"],
        "legendary_count": game_state["legendary_count"],
        "epic_count": game_state["epic_count"],
        "rare_count": game_state["rare_count"],
        "combo_count": game_state["combo_count"],
        "rarity_distribution": distribution,
        "rarity_probabilities": probabilities
    })

@app.route('/api/advanced-stats', methods=['GET'])
def get_advanced_stats():
    """Statistiques avancées pour étudiants en base de données."""
    if not spawn_history:
        return jsonify({"error": "Aucun spawn"}), 400
    
    # Compter les occurrences
    name_counts = Counter(s["name"] for s in spawn_history)
    rarity_counts = Counter(s["rarity"] for s in spawn_history)
    type_counts = Counter(s["type"] for s in spawn_history)
    mutation_counts = Counter(s["mutation"] for s in spawn_history)
    price_list = [s["price"] for s in spawn_history]
    
    # Calculs statistiques
    total = len(spawn_history)
    total_price = sum(price_list)
    
    # Statistiques de prix
    min_price = min(price_list) if price_list else 0
    max_price = max(price_list) if price_list else 0
    avg_price = total_price / total if total > 0 else 0
    median_price = sorted(price_list)[total // 2] if total > 0 else 0
    
    # Écart-type
    variance = sum((p - avg_price) ** 2 for p in price_list) / total if total > 0 else 0
    std_dev = math.sqrt(variance)
    
    # Brainrots les plus communs
    top_brainrots = name_counts.most_common(10)
    
    # Distribution des raretés
    rarity_distribution, rarity_probabilities = calculate_rarity_distribution()
    
    # Probabilité cumulée
    cumulative_prob = calculate_cumulative_probability(spawn_history)
    
    # Entropie de Shannon (mesure de diversité)
    entropy = 0.0
    for rarity, count in rarity_counts.items():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return jsonify({
        "total_spawns": total,
        "total_price": round(total_price, 2),
        "average_price": round(avg_price, 2),
        "median_price": round(median_price, 2),
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "std_dev": round(std_dev, 2),
        "unique_brainrots": len(name_counts),
        "top_brainrots": [{"name": name, "count": count} for name, count in top_brainrots],
        "rarity_distribution": dict(rarity_counts),
        "type_distribution": dict(type_counts),
        "mutation_distribution": dict(mutation_counts),
        "cumulative_probability": f"1 sur {int(cumulative_prob)}" if cumulative_prob != float('inf') else "Extrêmement rare",
        "shannon_entropy": round(entropy, 3),
        "theoretical_entropy": round(math.log2(len(MASTER_LIST)), 3)
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
    global spawn_history, game_state
    spawn_history.clear()
    game_state = {
        "total_price": 0,
        "spawns_count": 0,
        "rare_count": 0,
        "epic_count": 0,
        "legendary_count": 0,
        "god_count": 0,
        "combo_count": 0
    }
    return jsonify({"message": "Historique effacé"})

if __name__ == '__main__':
    print(f"Serveur démarré avec {len(MASTER_LIST)} brainrots disponibles")
    print("Accédez à: http://localhost:5000")
    print("\n📊 Statistiques disponibles:")
    print("  - Probabilités cumulées")
    print("  - Entropie de Shannon")
    print("  - Analyse statistique avancée")
    app.run(debug=True, host='0.0.0.0', port=5000)
