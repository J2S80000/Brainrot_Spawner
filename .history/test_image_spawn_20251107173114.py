#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test simple du spawn avec affichage d'image
"""
import random
import requests
import os
import sys

from master_list_generated import MASTER_LIST

def test_spawn_with_image():
    """Test un spawn avec image"""
    
    # Selectionner un brainrot aleatoire avec une image
    brainrots_with_images = [b for b in MASTER_LIST if b.get("image_url")]
    
    if not brainrots_with_images:
        print("Aucun brainrot avec image trouvee")
        return
    
    selected = random.choice(brainrots_with_images)
    
    print("=" * 70)
    print(f"BRAINROT SELECTIONNE: {selected['name']}")
    print(f"Rarete: {selected['rarity']}")
    print(f"Poids: {selected['spawn_weight']}")
    print(f"Image URL: {selected['image_url'][:80]}...")
    print("=" * 70)
    
    # Telecharger l'image
    try:
        os.makedirs("brainrot_images", exist_ok=True)
        
        safe_name = "".join(c for c in selected['name'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
        safe_name = safe_name.replace(" ", "_")[:50]
        img_path = f"brainrot_images/{safe_name}.png"
        
        print(f"\nTelechargement de l'image...")
        response = requests.get(selected["image_url"], timeout=5)
        response.raise_for_status()
        
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        print(f"OK Image sauvegardee: {img_path}")
        print(f"Taille: {os.path.getsize(img_path)} bytes")
        
        # Ouvrir l'image
        if sys.platform == 'win32':
            os.startfile(img_path)
            print("OK Image ouverte dans la visionneuse par defaut")
        
    except Exception as e:
        print(f"ERREUR: {e}")

if __name__ == "__main__":
    test_spawn_with_image()
