import random
import time
import json
import requests
import os
import sys
import threading
from threading import Thread
from pathlib import Path

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
download_stats = {"success": 0, "failed": 0, "cache": 0, "errors": []}

def sanitize_filename(name):
    """Convertit un nom en nom de fichier valide."""
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    return safe_name.replace(" ", "_")[:50]

def fix_image_url(url):
    """Corrige les URLs d'images invalides."""
    if not url:
        return None
    
    # Remplacer les anciens domaines par le bon CDN Wikia
    url = url.replace("stealabr/", "stealabrainrot/")
    
    return url

def download_image_async(image_url, brainrot_name, retry_count=2):
    """Telecharge l'image en arriere-plan avec retry et diagnostic."""
    if not image_url or not brainrot_name:
        return
    
    # Fixer l'URL
    image_url = fix_image_url(image_url)
    
    try:
        os.makedirs("brainrot_images", exist_ok=True)
        safe_name = sanitize_filename(brainrot_name)
        img_path = f"brainrot_images/{safe_name}.png"
        
        # Verifier le cache local d'abord
        if os.path.exists(img_path):
            with image_lock:
                image_cache[brainrot_name] = img_path
                download_stats["cache"] += 1
            print(f"    └─ [CACHE HIT] {img_path}")
            return
        
        # Essayer de telecharger avec retry
        for attempt in range(retry_count):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                print(f"    └─ [DOWNLOAD] Tentative {attempt + 1}/{retry_count}: {brainrot_name}")
                
                response = requests.get(image_url, headers=headers, timeout=10, allow_redirects=True)
                response.raise_for_status()
                
                # Verifier que c'est bien une image
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type:
                    if attempt < retry_count - 1:
                        print(f"       └─ Type invalide: {content_type}, retry...")
                        time.sleep(0.5)
                        continue
                    else:
                        with image_lock:
                            download_stats["failed"] += 1
                            download_stats["errors"].append(f"{brainrot_name}: Type invalide ({content_type})")
                        print(f"       └─ ERREUR: Type de contenu invalide")
                        return
                
                # Sauvegarder l'image
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                
                # Sauvegarder dans le cache
                with image_lock:
                    image_cache[brainrot_name] = img_path
                    download_stats["success"] += 1
                
                print(f"       └─ OK: {len(response.content)} bytes sauvegarde")
                
                # Ouvrir l'image (asynchrone)
                try:
                    if sys.platform == 'win32':
                        os.startfile(img_path)
                except:
                    pass
                
                return
                
            except requests.exceptions.Timeout:
                if attempt < retry_count - 1:
                    print(f"       └─ Timeout, retry...")
                    time.sleep(0.5)
                else:
                    with image_lock:
                        download_stats["failed"] += 1
                        download_stats["errors"].append(f"{brainrot_name}: Timeout")
                    print(f"       └─ ERREUR: Timeout")
                    
            except requests.exceptions.ConnectionError as e:
                if attempt < retry_count - 1:
                    print(f"       └─ Erreur de connexion, retry...")
                    time.sleep(0.5)
                else:
                    with image_lock:
                        download_stats["failed"] += 1
                        download_stats["errors"].append(f"{brainrot_name}: {str(e)[:50]}")
                    print(f"       └─ ERREUR: Connexion refusee")
                    
            except Exception as e:
                if attempt < retry_count - 1:
                    print(f"       └─ Erreur: {str(e)[:50]}, retry...")
                    time.sleep(0.5)
                else:
                    with image_lock:
                        download_stats["failed"] += 1
                        download_stats["errors"].append(f"{brainrot_name}: {str(e)[:50]}")
                    print(f"       └─ ERREUR: {str(e)[:50]}")
        
    except Exception as e:
        with image_lock:
            download_stats["failed"] += 1
            download_stats["errors"].append(f"{brainrot_name}: {str(e)[:50]}")
        print(f"    └─ ERREUR CRITIQUE: {str(e)[:50]}")

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
    
    print(f"✓ SPAWN: {selected['name']:30} | {selected['rarity']:10} | {type_selected:8} | {mutation_selected:7} => {final_price:8.0f}$", end="")
    
    # Telecharger l'image en arriere-plan
    if selected.get("image_url"):
        if selected["name"] not in image_cache:
            print()
            # Telecharger en arriere-plan (ne bloque pas le spawn)
            thread = Thread(target=download_image_async, args=(selected["image_url"], selected["name"]), daemon=True)
            thread.start()
        else:
            print(" [CACHED]")
    else:
        print(" [NO_URL]")
    
def simulate_spawns(num_spawns=10):
    """Lance la simulation avec spawns rapides."""
    print("\n" + "="*100)
    print("BRAINROT SPAWN SIMULATOR - MODE RAPIDE AVEC DIAGNOSTIC")
    print("="*100)
    print(f"MASTER_LIST: {len(MASTER_LIST)} brainrots charges")
    print(f"Spawning {num_spawns} brainrots...\n")
    
    # IMPORTANT: Ne pas supprimer le dossier!
    os.makedirs("brainrot_images", exist_ok=True)
    
    for i in range(num_spawns):
        spawn_brainrot()
        time.sleep(0.2)
    
    print("\n" + "="*100)
    print("Attente de la fin des telechargements en arriere-plan (10 secondes)...")
    time.sleep(10)
    
    print("\n" + "="*100)
    print("STATISTIQUES DE TELECHARGEMENT:")
    print(f"  ✓ Reussis: {download_stats['success']}")
    print(f"  ◆ En cache: {download_stats['cache']}")
    print(f"  ✗ Echoues: {download_stats['failed']}")
    
    if download_stats['errors']:
        print("\nDETAILS DES ERREURS:")
        for error in download_stats['errors'][:10]:  # Afficher les 10 premieres erreurs
            print(f"  - {error}")
    
    print("="*100)
    
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=4)
    
    print(f"\n✓ Log exporte: brainrot_spawn_log.json")
    print(f"✓ Images sauvegardees dans: brainrot_images/")
    
    # Afficher les fichiers telecharges
    if os.path.exists("brainrot_images"):
        files = os.listdir("brainrot_images")
        print(f"✓ {len(files)} fichiers dans brainrot_images/")
        if files:
            print(f"  Exemples: {', '.join(files[:3])}")

if __name__ == "__main__":
    simulate_spawns(10)
