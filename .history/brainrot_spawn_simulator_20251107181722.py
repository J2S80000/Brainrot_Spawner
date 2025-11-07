import random
import time
import json
import os
import sys

from master_list_generated import MASTER_LIST

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

# === JOURNAL DE SPAWN ===
spawn_log = []

def spawn_brainrot():
    """Spawn d'un brainrot (sans images, mode rapide)."""
    selected = random.choices(MASTER_LIST, weights=[b["spawn_weight"] for b in MASTER_LIST], k=1)[0]
    type_selected = random.choices(list(TYPE_MULTIPLIERS.keys()), weights=TYPE_WEIGHTS, k=1)[0]
    mutation_selected = random.choices(list(MUTATION_MULTIPLIERS.keys()), weights=MUTATION_WEIGHTS, k=1)[0]
    
    base_value = RARITY_VALUES[selected["rarity"]]
    final_price = base_value * TYPE_MULTIPLIERS[type_selected] * MUTATION_MULTIPLIERS[mutation_selected]
    final_price = round(final_price, 2)
    
    spawn_info = {
        "name": selected["name"],
        "rarity": selected["rarity"],
        "type": type_selected,
        "mutation": mutation_selected,
        "price": final_price
    }
    spawn_log.append(spawn_info)
    
    print(f"SPAWN: {selected['name']:30} | {selected['rarity']:10} | {type_selected:8} | {mutation_selected:7} => {final_price:8.0f}$")
    
def simulate_spawns(num_spawns=20):
    """Simulation rapide sans images."""
    print("="*100)
    print("BRAINROT SPAWN SIMULATOR - MODE RAPIDE (SANS IMAGES)")
    print("="*100)
    print(f"MASTER_LIST: {len(MASTER_LIST)} brainrots charges\n")
    
    start_time = time.time()
    
    for _ in range(num_spawns):
        spawn_brainrot()
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*100)
    print(f"STATISTIQUES:")
    print(f"  Total spawns: {num_spawns}")
    print(f"  Temps total: {elapsed:.3f}s")
    print(f"  Vitesse: {num_spawns/elapsed:.0f} spawns/seconde")
    print(f"  Valeur totale: {sum(s['price'] for s in spawn_log):.0f}$")
    print("="*100)
    
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=2)
    
    print(f"\nLog exporte: brainrot_spawn_log.json")

if __name__ == "__main__":
    simulate_spawns(20)
