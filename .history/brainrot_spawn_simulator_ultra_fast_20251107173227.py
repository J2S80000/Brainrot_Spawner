import random
import time
import json
import requests
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from master_list_generated import MASTER_LIST

# === CONFIGURATION ===
RARITY_VALUES = {
    "Common": 100,
    "Rare": 500,
    "Epic": 1500,
    "Legendary": 5000,
    "God": 20000
}

TYPE_MULTIPLIERS = {"Normal": 1.0, "Gold": 1.5, "Diamond": 2.5}
TYPE_WEIGHTS = [80, 15, 5]

MUTATION_MULTIPLIERS = {"None": 1.0, "Minor": 1.2, "Major": 1.6, "Mythic": 2.0}
MUTATION_WEIGHTS = [70, 20, 8, 2]

# === CACHE ===
spawn_log = []
image_cache = {}
IMAGE_DIR = "brainrot_images"

def sanitize_filename(name):
    """Convertit un nom en nom de fichier valide."""
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    return safe_name.replace(" ", "_")[:50]

def get_image_path(brainrot_name):
    """Retourne le chemin de l'image pour un brainrot."""
    return f"{IMAGE_DIR}/{sanitize_filename(brainrot_name)}.png"

def image_exists(brainrot_name):
    """Verifie si l'image est deja en cache."""
    return os.path.exists(get_image_path(brainrot_name))

def download_image_silent(image_url, brainrot_name):
    """Telecharge une image en silence."""
    if not image_url or image_exists(brainrot_name):
        return
    
    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        img_path = get_image_path(brainrot_name)
        
        response = requests.get(image_url, timeout=3)
        response.raise_for_status()
        
        with open(img_path, 'wb') as f:
            f.write(response.content)
    except:
        pass

def preload_images(max_workers=5):
    """Pre-charge les images les plus rares en parallele."""
    print("PRELOADANT LES IMAGES...")
    
    # Trier par rarete (God d'abord)
    rarity_order = {"God": 0, "Legendary": 1, "Epic": 2, "Rare": 3, "Common": 4}
    sorted_list = sorted(MASTER_LIST, key=lambda x: rarity_order.get(x.get("rarity"), 5))
    
    # Pre-charger les 50 premiers (les plus rares)
    to_load = sorted_list[:50]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = []
        for brainrot in to_load:
            if brainrot.get("image_url"):
                tasks.append(executor.submit(download_image_silent, brainrot["image_url"], brainrot["name"]))
        
        # Attendre la completion
        for i, task in enumerate(tasks, 1):
            try:
                task.result(timeout=5)
            except:
                pass
            
            if i % 10 == 0:
                print(f"  [{i}/{len(tasks)}] images chargees...")
    
    print("Pre-chargement termine!\n")

def spawn_brainrot():
    """Spawn d'un brainrot avec affichage rapide."""
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
        "price": final_price,
        "image_url": selected.get("image_url")
    }
    spawn_log.append(spawn_info)
    
    # Affichage rapide
    img_indicator = "[IMG]" if image_exists(selected["name"]) else "     "
    print(f"{img_indicator} SPAWN: {selected['name']:30} | {selected['rarity']:10} | {type_selected:8} | {mutation_selected:7} => {final_price:8.0f}$")
    
    # Essayer d'ouvrir l'image si elle existe
    if image_exists(selected["name"]):
        try:
            if sys.platform == 'win32':
                img_path = get_image_path(selected["name"])
                os.startfile(img_path)
        except:
            pass

def simulate_spawns(num_spawns=20, preload=True):
    """Simulation rapide avec images."""
    print("="*100)
    print("BRAINROT SPAWN SIMULATOR - MODE ULTRA-RAPIDE")
    print("="*100)
    print(f"MASTER_LIST: {len(MASTER_LIST)} brainrots charges")
    
    if preload:
        preload_images()
    
    print(f"Spawning {num_spawns} brainrots...\n")
    
    start_time = time.time()
    
    for i in range(num_spawns):
        spawn_brainrot()
        time.sleep(0.05)  # Delai ultra-court
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*100)
    print(f"STATISTIQUES:")
    print(f"  Total spawns: {num_spawns}")
    print(f"  Temps total: {elapsed:.2f}s")
    print(f"  Vitesse moyenne: {num_spawns/elapsed:.1f} spawns/seconde")
    print(f"  Valeur totale: {sum(s['price'] for s in spawn_log):.0f}$")
    print("="*100)
    
    # Export du log
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=2)
    
    print(f"\nLog exporte: brainrot_spawn_log.json")
    print(f"Images sauvegardees dans: {IMAGE_DIR}/")

if __name__ == "__main__":
    simulate_spawns(num_spawns=20, preload=True)
