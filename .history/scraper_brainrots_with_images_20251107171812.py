import requests
from bs4 import BeautifulSoup
import json
import re
import time
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

WIKI_URL = "https://stealabrainrot.fandom.com/wiki/Category:Brainrots"
WIKI_BASE = "https://stealabrainrot.fandom.com"

def scrape_brainrot_image(brainrot_name):
    """
    Scrape l'image d'un brainrot spécifique depuis sa page wiki.
    """
    try:
        # Convertir le nom en URL-compatible
        url_name = brainrot_name.replace(" ", "_")
        page_url = f"{WIKI_BASE}/wiki/{url_name}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(page_url, headers=headers, timeout=5)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher l'image principale (généralement dans la figure)
            figure = soup.find('figure', class_='pi-item')
            if figure:
                img = figure.find('img')
                if img and 'src' in img.attrs:
                    img_url = img['src']
                    # Prendre la version de meilleure qualité
                    img_url = img_url.split('/revision')[0] if '/revision' in img_url else img_url
                    return img_url
            
            # Fallback: chercher n'importe quelle image
            img = soup.find('img', class_='pi-image-thumbnail')
            if img and 'src' in img.attrs:
                return img['src']
                
    except Exception as e:
        pass
    
    return None

def scrape_brainrots_from_wiki():
    """
    Scrape dynamiquement la liste complète des brainrots avec images.
    """
    try:
        print("🔄 Scraping du wiki Fandom en cours...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        brainrot_data = []
        limit = 500
        offset = 0
        
        api_url = "https://stealabrainrot.fandom.com/api/v1/Articles/List"
        
        print("  📡 Requête vers l'API Fandom...")
        response = requests.get(api_url, headers=headers, params={
            'category': 'Brainrots',
            'limit': limit,
            'offset': offset
        }, timeout=15)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        data = response.json()
        
        if 'items' in data:
            for item in data['items']:
                if 'title' in item:
                    title = item['title']
                    # Filtrer les fichiers multimédias et pages système
                    if not any(exclude in title for exclude in 
                              ['webp', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'File:',
                               'User', 'Talk:', 'Special:', 'Help:', 'Category:', '.jpg', '.png']):
                        brainrot_data.append({
                            'name': title,
                            'image_url': None  # À remplir ultérieurement
                        })
        
        print(f"✅ {len(brainrot_data)} brainrots trouvés!")
        print("📸 Extraction des images en cours... (cela peut prendre du temps)")
        
        # Extraire les images (limiter pour performance)
        for i, brainrot in enumerate(brainrot_data, 1):
            if i % 10 == 0:
                print(f"  [{i}/{len(brainrot_data)}] Traitement des images...")
            
            image_url = scrape_brainrot_image(brainrot['name'])
            if image_url:
                brainrot['image_url'] = image_url
            
            time.sleep(0.1)  # Petit délai pour ne pas surcharger le serveur
        
        return brainrot_data
        
    except Exception as e:
        print(f"❌ Erreur lors du scraping: {e}")
        print("📌 Utilisation de la liste par défaut...")
        return get_default_brainrots()

def get_default_brainrots():
    """
    Liste par défaut en cas d'échec du scraping.
    """
    defaults = [
        "1x1x1x1", "67", "Admin Lucky Block", "Agarrini La Palini", "Alessio",
        "Anpali Babel", "Antonio", "Aquanut", "Avocadini Antilopini", "Avocadini Guffo",
        "Avocadorilla", "Ballerina Cappuccina", "Ballerino Lololo", "Bambini Crostini",
    ]
    return [{"name": name, "image_url": None} for name in defaults]

def generate_master_list_with_images():
    """
    Génère la MASTER_LIST avec images.
    """
    brainrot_data = scrape_brainrots_from_wiki()
    
    master_list = []
    
    for i, brainrot in enumerate(brainrot_data):
        name = brainrot['name']
        image_url = brainrot['image_url']
        
        # Distribution des raretés
        if i < len(brainrot_data) * 0.35:
            rarity = "Common"
            spawn_weight = 40
        elif i < len(brainrot_data) * 0.55:
            rarity = "Rare"
            spawn_weight = 25
        elif i < len(brainrot_data) * 0.75:
            rarity = "Epic"
            spawn_weight = 15
        elif i < len(brainrot_data) * 0.90:
            rarity = "Legendary"
            spawn_weight = 10
        else:
            rarity = "God"
            spawn_weight = 5
        
        brainrot_entry = {
            "name": name,
            "rarity": rarity,
            "spawn_weight": spawn_weight,
            "image_url": image_url
        }
        master_list.append(brainrot_entry)
    
    return master_list

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATEUR DE MASTER LIST - BRAINROT SIMULATOR")
    print("=" * 60)
    
    master_list = generate_master_list_with_images()
    
    print(f"\n OK Total brainrots generés: {len(master_list)}")
    print(f"\n DISTRIBUTION PAR RARETE:")
    
    rarity_counts = {}
    for rarity in ["Common", "Rare", "Epic", "Legendary", "God"]:
        count = sum(1 for b in master_list if b["rarity"] == rarity)
        rarity_counts[rarity] = count
        percentage = (count / len(master_list)) * 100
        print(f"  {rarity:12} | {count:3} items | {percentage:6.2f}%")
    
    print(f"\n PREMIERS BRAINROTS (avec images):")
    for i, brainrot in enumerate(master_list[:5], 1):
        has_img = "OUI" if brainrot['image_url'] else "NON"
        print(f"  {i}. {brainrot['name']:30} | {brainrot['rarity']:10} | Image: {has_img}")
    
    # Export en JSON
    with open("master_list.json", "w", encoding="utf-8") as f:
        json.dump(master_list, f, ensure_ascii=False, indent=2)
    
    # Générer le fichier Python
    with open("master_list_generated.py", "w", encoding="utf-8") as f:
        f.write("# Generated Master List for Brainrot Spawn Simulator\n")
        f.write("# Extracted from: https://stealabrainrot.fandom.com/wiki/Category:Brainrots\n\n")
        f.write("MASTER_LIST = [\n")
        for brainrot in master_list:
            img_str = f'"{brainrot["image_url"]}"' if brainrot["image_url"] else "None"
            f.write(f'    {{"name": "{brainrot["name"]}", "rarity": "{brainrot["rarity"]}", "spawn_weight": {brainrot["spawn_weight"]}, "image_url": {img_str}}},\n')
        f.write("]\n")
    
    print("\n FICHIERS GENERÉS:")
    print("  - master_list.json")
    print("  - master_list_generated.py")
    print("\n EXTRACTION COMPLETE!")
    print("=" * 60)
