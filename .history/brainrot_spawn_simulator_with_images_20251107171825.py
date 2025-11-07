import random
import time
import json
import pandas as pd
from PIL import Image
from io import BytesIO
import requests
import urllib.request

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
    Affiche l'image du brainrot dans le terminal.
    """
    if not image_url:
        return
    
    try:
        # Telecharger l'image
        response = requests.get(image_url, timeout=5)
        img = Image.open(BytesIO(response.content))
        
        # Redimensionner pour le terminal (petit pour ne pas trop encombrer)
        img.thumbnail((60, 40), Image.Resampling.LANCZOS)
        
        # Convertir en ASCII art simplifie
        from PIL import ImageDraw
        pixels = list(img.convert('L').getdata())
        width, height = img.size
        
        ascii_chars = "@%#*+=-:. "
        
        print("\n" + "=" * 70)
        print(f"BRAINROT: {brainrot_name}")
        print("=" * 70)
        
        for i in range(height):
            for j in range(width):
                pixel = pixels[i * width + j]
                char_index = pixel * len(ascii_chars) // 256
                print(ascii_chars[min(char_index, len(ascii_chars) - 1)], end='')
            print()
        print("=" * 70 + "\n")
        
    except Exception as e:
        # Fallback: afficher un lien
        print(f"\n[IMAGE] {brainrot_name}: {image_url}\n")

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
