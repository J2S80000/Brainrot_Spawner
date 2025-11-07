import random
import time
import json
import requests
import os
import sys
import threading
from threading import Thread
from pathlib import Path
import shutil

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

# === CACHE D'IMAGES (EN MEMOIRE) ===
image_cache = {}
image_lock = threading.Lock()

# === TELECHARGER LES IMAGES EN ARRIERE-PLAN ===
def download_image_async(image_url, brainrot_name):
    """Telecharge l'image en arriere-plan (asynchrone)."""
    if not image_url or not brainrot_name:
        return
    
    try:
        os.makedirs("brainrot_images", exist_ok=True)
        safe_name = "".join(c for c in brainrot_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        safe_name = safe_name.replace(" ", "_")[:50]
        img_path = f"brainrot_images/{safe_name}.png"

        
        # Verifier le cache local d'abord
        if os.path.exists(img_path):
            with image_lock:
                image_cache[brainrot_name] = img_path
            return
        
        # Telecharger l'image
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
        
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        # Sauvegarder dans le cache
        with image_lock:
            image_cache[brainrot_name] = img_path
        
        # Ouvrir l'image (asynchrone)
        try:
            if sys.platform == 'win32':
                os.startfile(img_path)
        except:
            pass
    except:
        pass

def display_cached_image_path(brainrot_name):
    """Affiche le chemin de l'image en cache si disponible."""
    if brainrot_name in image_cache:
        print(f"  [IMAGE EN CACHE] {image_cache[brainrot_name]}")
        return True
    return False

def spawn_brainrot():
    """Spawn d'un brainrot avec gestion asynchrone de l'image."""
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
    
    print(f"SPAWN: {selected['name']} | {selected['rarity']} | {type_selected} | {mutation_selected} => {final_price}$")
    
    # Afficher le chemin en cache si deja telecharge
    if selected.get("image_url"):
        if not display_cached_image_path(selected["name"]):
            print(f"  [IMAGE] Telechargement en arriere-plan...")
            # Telecharger en arriere-plan (ne bloque pas le spawn)
           
            thread = Thread(target=download_image_async, args=(selected["image_url"], selected["name"]), daemon=True)
            thread.start()
    
def simulate_spawns(num_spawns=10):
    """Lance la simulation avec spawns rapides."""
    print("=== SIMULATION DE SPAWN BRAINROT (MODE RAPIDE) ===")
    print(f"Nombre de spawns: {num_spawns}")
    print("")
    
    for i in range(num_spawns):
        spawn_brainrot()
        time.sleep(0.1)  # Delai minimal entre les spawns
    
    print("\n" + "="*70)
    print("Attente de la fin des telechargements d'images...")
    time.sleep(3)  # Attendre la fin des telechargements en arriere-plan
    
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=4)
    
    print(f"Journal exporte dans brainrot_spawn_log.json")
    print(f"Images sauvegardees dans le dossier brainrot_images/")
    print("="*70)

if __name__ == "__main__":
     if os.path.exists("brainrot_images"):
             shutil.rmtree("brainrot_images")  # Supprime tout le dossier et son contenu
    os.mkdir("brainrot_images")
    print(f"MASTER_LIST: {len(MASTER_LIST)} brainrots charges\n")
    simulate_spawns(10)
