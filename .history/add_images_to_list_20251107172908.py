"""
Script utilitaire pour ajouter les images aux brainrots existants dans master_list_generated.py
"""
import requests
from bs4 import BeautifulSoup
import time

def get_brainrot_image_url(brainrot_name):
    """
    Scrape l'URL de l'image pour un brainrot specifique.
    """
    try:
        # Convertir le nom en URL-compatible
        url_name = brainrot_name.replace(" ", "_")
        page_url = f"https://stealabrainrot.fandom.com/wiki/{url_name}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(page_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher la figure avec l'image
            figure = soup.find('figure', class_='pi-item')
            if figure:
                img = figure.find('img')
                if img and 'src' in img.attrs:
                    img_url = img['src']
                    # Optimiser l'URL
                    if '/revision' in img_url:
                        img_url = img_url.split('/revision')[0]
                    return img_url
            
            # Fallback
            img = soup.find('img', class_='pi-image-thumbnail')
            if img and 'src' in img.attrs:
                return img['src']
    except:
        pass
    
    return None

def update_master_list_with_images():
    """
    Met a jour master_list_generated.py avec les images.
    """
    from master_list_generated import MASTER_LIST
    
    print("RECHERCHE DES IMAGES POUR LES BRAINROTS")
    print("=" * 60)
    
    # Ajouter les images
    for i, brainrot in enumerate(MASTER_LIST, 1):
        if i % 10 == 0:
            print(f"Progression: {i}/{len(MASTER_LIST)}")
        
        name = brainrot['name']
        
        # Sauter si l'image est deja presente
        if brainrot.get('image_url'):
            continue
        
        image_url = get_brainrot_image_url(name)
        if image_url:
            brainrot['image_url'] = image_url
            print(f"  OK {name}")
        else:
            brainrot['image_url'] = None
            print(f"  X {name} (image non trouvee)")
        
        time.sleep(0.2)  # Petit delai pour ne pas surcharger
    
    print("\nMise a jour du fichier master_list_generated.py...")
    
    # Regenerer le fichier
    with open("master_list_generated.py", "w", encoding="utf-8") as f:
        f.write("# Generated Master List for Brainrot Spawn Simulator\n")
        f.write("# Extracted from: https://stealabrainrot.fandom.com/wiki/Category:Brainrots\n\n")
        f.write("MASTER_LIST = [\n")
        for brainrot in MASTER_LIST:
            img_str = f'"{brainrot["image_url"]}"' if brainrot.get('image_url') else "None"
            f.write(f'    {{"name": "{brainrot["name"]}", "rarity": "{brainrot["rarity"]}", "spawn_weight": {brainrot["spawn_weight"]}, "image_url": {img_str}}},\n')
        f.write("]\n")
    
    print("OK Fichier mis a jour!")
    
    # Statistiques
    with_images = sum(1 for b in MASTER_LIST if b.get('image_url'))
    print(f"\nSTATISTIQUES: {with_images}/{len(MASTER_LIST)} brainrots avec images")

if __name__ == "__main__":
    update_master_list_with_images()
