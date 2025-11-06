import random
import time
import json
# === LISTE MAÎTRESSE DES OBJETS BRAINROT ===


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
TYPE_WEIGHTS = [80, 15, 5]  # pour random.choices

MUTATION_MULTIPLIERS = {"None": 1.0, "Minor": 1.2, "Major": 1.6, "Mythic": 2.0}
MUTATION_WEIGHTS = [70, 20, 8, 2]

# === JOURNAL DE SPAWN ===
spawn_log = []

# === FONCTION DE SPAWN ===
def spawn_brainrot():
    # Sélection pondérée de l’objet
    selected = random.choices(MASTER_LIST, weights=[b["spawn_weight"] for b in MASTER_LIST], k=1)[0]
    
    # Sélection du type et mutation (également pondérée)
    type_selected = random.choices(list(TYPE_MULTIPLIERS.keys()), weights=TYPE_WEIGHTS, k=1)[0]
    mutation_selected = random.choices(list(MUTATION_MULTIPLIERS.keys()), weights=MUTATION_WEIGHTS, k=1)[0]
    
    # Calcul du prix
    base_value = RARITY_VALUES[selected["rarity"]]
    final_price = base_value * TYPE_MULTIPLIERS[type_selected] * MUTATION_MULTIPLIERS[mutation_selected]
    final_price = round(final_price, 2)
    
    # Enregistrement
    spawn_info = {
        "name": selected["name"],
        "rarity": selected["rarity"],
        "type": type_selected,
        "mutation": mutation_selected,
        "price": final_price
    }
    spawn_log.append(spawn_info)
    
    # Affichage en temps réel
    print(f"🧠 {selected['name']} | {selected['rarity']} | {type_selected} | {mutation_selected} → 💰 {final_price}$")
    
# === BOUCLE DE SIMULATION ===
def simulate_spawns(duration_seconds=20):
    print("=== Simulation de Spawn Brainrot ===")
    num_spawns = duration_seconds // 2  # toutes les 2 secondes
    for _ in range(num_spawns):
        spawn_brainrot()
        time.sleep(2)
    
    # Export JSON
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=4)
    print("\n✅ Journal exporté dans brainrot_spawn_log.json")

# === LANCEMENT ===
if __name__ == "__main__":
    simulate_spawns(20)
