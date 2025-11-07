import random
import time
import json
import pandas as pd
import requests
import webbrowser
import os
from pathlib import Path

# Importer la MASTER_LIST generee dynamiquement par le scraper
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

def display_brainrot_image(image_url, brainrot_name):
    """
    Telecharge et affiche l'image du brainrot.
    """
    if not image_url:
        print(f"[INFO] Pas d'image disponible pour {brainrot_name}")
        return
    
    try:
        # Creer un dossier pour les images
        os.makedirs("brainrot_images", exist_ok=True)
        
        # Generer un nom de fichier valide
        safe_name = "".join(c for c in brainrot_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        safe_name = safe_name.replace(" ", "_")[:50]
        
        img_path = f"brainrot_images/{safe_name}.png"
        
        # Telecharger l'image
        print(f"  Telechargement de l'image... ({image_url[:60]}...)")
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
        
        # Sauvegarder l'image
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  Image sauvegardee: {img_path}")
        
        # Ouvrir l'image avec le programme par defaut
        try:
            if os.name == 'nt':  # Windows
                os.startfile(img_path)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{img_path}"')
        except Exception as e:
            print(f"  Impossible d'ouvrir l'image automatiquement")
        
    except Exception as e:
        print(f"  Erreur lors du telechargement: {str(e)}")
        print(f"  Lien direct: {image_url}")

def spawn_brainrot():
    """Fonction de spawn avec affichage de l'image"""
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
    
    # Afficher l'image si disponible
    if selected.get("image_url"):
        display_brainrot_image(selected["image_url"], selected["name"])
    
    # Affichage texte
    print(f"SPAWN: {selected['name']} | {selected['rarity']} | {type_selected} | {mutation_selected} => {final_price}$")
def simulate_spawns(duration_seconds=20):
    print("=== SIMULATION DE SPAWN BRAINROT ===")
    num_spawns = duration_seconds // 2
    for _ in range(num_spawns):
        spawn_brainrot()
        time.sleep(2)
    
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=4)
    print("\n OK JOURNAL EXPORTE dans brainrot_spawn_log.json")

if __name__ == "__main__":
    print(f"OK MASTER_LIST: {len(MASTER_LIST)} brainrots charges")
    simulate_spawns(20)
