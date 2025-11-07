"""
Serveur Flask pour l'application Brainrot Spawn Simulator avec WebSocket
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import time
import json
import threading
from master_list_generated import MASTER_LIST

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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
active_sessions = {}
spawn_history = []
max_history = 500

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
    return render_template('index.html')

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

# === WEBSOCKET EVENTS ===

@socketio.on('connect')
def handle_connect():
    """Nouvelle connexion établie."""
    print(f"Client connecté: {request.sid}")
    active_sessions[request.sid] = {
        "connected_at": time.time(),
        "spawns_received": 0
    }
    emit('connection_response', {
        'status': 'Connecté au serveur',
        'client_id': request.sid,
        'total_brainrots': len(MASTER_LIST)
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Déconnexion du client."""
    if request.sid in active_sessions:
        del active_sessions[request.sid]
    print(f"Client déconnecté: {request.sid}")

@socketio.on('start_simulation')
def handle_start_simulation(data):
    """Démarrer la simulation de spawns."""
    speed = data.get('speed', 1.0)  # Multiplicateur de vitesse
    duration = data.get('duration', 60)  # Durée en secondes
    
    def simulate():
        interval = max(0.5 / speed, 0.05)  # Au minimum 20 spawns/sec
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                spawn_data = spawn_brainrot()
                
                # Émettre le spawn à tous les clients connectés
                socketio.emit('brainrot_spawned', spawn_data, broadcast=True)
                
                if request.sid in active_sessions:
                    active_sessions[request.sid]["spawns_received"] += 1
                
                time.sleep(interval)
            except Exception as e:
                print(f"Erreur lors du spawn: {e}")
                break
        
        socketio.emit('simulation_ended', {
            'total_spawns': len(spawn_history),
            'message': 'Simulation terminée'
        }, broadcast=True)
    
    # Lancer la simulation dans un thread
    thread = threading.Thread(target=simulate, daemon=True)
    thread.start()
    
    emit('simulation_started', {
        'status': 'Simulation lancée',
        'speed': speed,
        'duration': duration
    })

@socketio.on('single_spawn')
def handle_single_spawn():
    """Générer un seul spawn."""
    spawn_data = spawn_brainrot()
    socketio.emit('brainrot_spawned', spawn_data, broadcast=True)

@socketio.on('clear_history')
def handle_clear_history():
    """Effacer l'historique."""
    global spawn_history
    spawn_history.clear()
    socketio.emit('history_cleared', {'message': 'Historique effacé'}, broadcast=True)

@socketio.on('get_stats')
def handle_get_stats():
    """Demander les statistiques."""
    stats = {
        "total_spawns": len(spawn_history),
        "duplicates": sum(1 for s in spawn_history if s["is_duplicate"]),
        "unique_brainrots": len(set(s["name"] for s in spawn_history)),
        "rarity_breakdown": get_rarity_breakdown(),
        "type_breakdown": get_type_breakdown(),
        "active_sessions": len(active_sessions)
    }
    emit('stats_update', stats)

if __name__ == '__main__':
    print(f"Serveur démarré avec {len(MASTER_LIST)} brainrots disponibles")
    print("Accédez à: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
