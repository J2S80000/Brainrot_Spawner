import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

# URL du wiki
WIKI_URL = "https://stealabrainrot.fandom.com/wiki/Category:Brainrots"

def scrape_brainrots_from_wiki():
    """
    Scrape dynamiquement la liste complète des brainrots depuis le wiki Fandom.
    Utilise l'API Fandom pour obtenir les membres de la catégorie.
    """
    try:
        print("🔄 Scraping du wiki Fandom en cours (API method)...")
        
        # Headers pour éviter les blocages
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Méthode 1: Essayer avec l'API Fandom Query Service
        brainrot_names = set()
        limit = 500  # Augmenter la limite pour capturer tous les brainrots
        offset = 0
        
        # Récupérer tous les membres de la catégorie via l'API
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
                    # Filtrer les fichiers multimédias
                    if not any(ext in title.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.mp4', '.webm']):
                        brainrot_names.add(title)
            print(f"  ✅ API: {len(brainrot_names)} brainrots trouvés!")
        
        # Vérifier s'il y a une pagination
        if len(brainrot_names) >= limit - 10:
            print("  ⚠️  Limite API atteinte, vérification de la pagination...")
            offset = limit
            response = requests.get(api_url, headers=headers, params={
                'category': 'Brainrots',
                'limit': limit,
                'offset': offset
            }, timeout=15)
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                for item in data['items']:
                    if 'title' in item:
                        brainrot_names.add(item['title'])
                print(f"  ✅ API (page 2): +{len(data['items'])} brainrots!")
        
        # Méthode 2: Si pas assez de résultats, scraper la page directement
        if len(brainrot_names) < 150:
            print("  📄 Scraping HTML fallback...")
            response = requests.get("https://stealabrainrot.fandom.com/wiki/Category:Brainrots", 
                                   headers=headers, timeout=15)
            response.encoding = 'utf-8'
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les liens dans les sections de liste
            all_links = soup.find_all('a', href=re.compile(r'^/wiki/'))
            
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if href.startswith('/wiki/') and text and len(text) > 1:
                    exclude_patterns = [
                        'Category:', 'File:', 'User', 'Talk:', 'Special:', 'Help:',
                        '/Gallery', 'Gallery', 'blog', 'User_blog', 'Discuss',
                        'Community', 'Fandom', 'WIKI', 'Edit', 'Sign', 'View'
                    ]
                    
                    should_exclude = any(pattern in href or pattern in text for pattern in exclude_patterns)
                    
                    if not should_exclude:
                        clean_text = re.sub(r'\s*\(\d+\)\s*$', '', text).strip()
                        
                        if len(clean_text) > 1 and clean_text not in ['', 'View', 'Edit', 'NEXT']:
                            brainrot_names.add(clean_text)
            
            print(f"  ✅ HTML Scraping: {len(brainrot_names)} brainrots trouvés!")
        
        # Dédupliquer et trier
        brainrot_names = sorted(list(brainrot_names))
        
        print(f"\n✅ Total final: {len(brainrot_names)} brainrots extraits!")
        
        return brainrot_names
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        print("📌 Utilisation de la liste par défaut...")
        return get_default_brainrots()

def get_default_brainrots():
    """
    Liste par défaut en cas d'échec du scraping.
    """
    return [
        "1x1x1x1", "67", "Admin Lucky Block", "Agarrini La Palini", "Alessio",
        "Anpali Babel", "Antonio", "Aquanut", "Avocadini Antilopini", "Avocadini Guffo",
        "Avocadorilla", "Ballerina Cappuccina", "Ballerino Lololo", "Bambini Crostini",
        "Bambu Bambu Sahur", "Bananita Dolphinita", "Bananito Bandito", "Bandito Axolito",
        "Bandito Bobritto", "Belula Beluga", "Bisonte Giuppitere", "Blackhole Goat",
        "Blueberrinni Octopusini", "Bombardini Tortinii", "Bombardiro Crocodilo",
        "Bombombini Gusini", "Boneca Ambalabu", "Brainrot God Lucky Block",
        "Brasilini Berimbini", "Brr Brr Patapim", "Brr es Teh Patipum",
        "Brri Brri Bicus Dicus Bombicus", "Bruto Gialutto", "Buho De Fuego",
        "Bulbito Bandito Traktorito", "Burbaloni Luliloli", "Burguro And Fryuro",
        "Burrito Bandito", "Cacasito Satalito", "Cachorrito Melonito", "Cacto Hipopotamo",
        "Capi Taco", "Capitano Moby", "Cappuccino Assassino", "Cappuccino Clownino",
        "Caramello Filtrello", "Carloo", "Carrotini Brainini", "Cavallo Virtuoso",
        "Celularcini Viciosini", "Chachechi", "Chef Crabracadabra", "Chicleteira Bicicleteira",
        "Chicleteirina Bicicleteirina", "Chihuanini Taconini", "Chillin Chili",
        "Chimpanzini Bananini", "Chimpanzini Spiderini", "Chipso and Queso",
        "Cocofanto Elefanto", "Cocosini Mama", "Combinasions", "Corn Corn Corn Sahur",
        "Crabbo Limonetta", "Developini Braziliaspidini", "Dragon Cannelloni", "Dug dug dug",
        "Dul Dul Dul", "Elefanto Frigo", "Esok Sekolah", "Espresso Signora", "Eviledon",
        "Extinct Ballerina", "Extinct Matteo", "Extinct Tralalero", "Fluriflura",
        "Fragola La La La", "Frankentteo", "Frigo Camelo", "Frio Ninja", "Frogato Pirato",
        "Ganganzelli Trulala", "Gangster Footera", "Garama and Madundung", "Gattatino Neonino",
        "Gattatino Nyanino", "Gattito Tacoto", "Girafa Celestre", "Glorbo Fruttodrillo",
        "Gorillo Subwoofero", "Gorillo Watermelondrillo", "Graipuss Medussi",
        "Guerriro Digitale", "Headless Horseman", "Jacko Jack Jack", "Job Job Job Sahur",
        "John Pork", "Karker Sahur", "Karkerkar Kurkur", "Ketchuru and Musturu",
        "Ketupat Kepat", "Krupuk Pagi Pagi", "La Cucaracha", "La Extinct Grande",
        "La Grande Combinasion", "La Karkerkar Combinasion", "La Sahur Combinasion",
        "La Secret Combinasion", "La Spooky Grande", "La Supreme Combinasion",
        "La Taco Combinasion", "La Vacca Jacko Linterino", "La Vacca Saturno Saturnita",
        "Las Cappuchinas", "Las Sis", "Las Tralaleritas", "Las Vaquitas Saturnitas",
        "Lerulerulerule", "Limited Stock Brainrots", "Lionel Cactuseli", "Lirilì Larilà",
        "Los 67", "Los Bombinitos", "Los Bros", "Los Chicleteiras", "Los Combinasionas",
        "Los Crocodillitos", "Los Hotspotsitos", "Los Jobcitos", "Los Karkeritos",
        "Los Matteos", "Los Mobilis", "Los Noobinis", "Los Nooo My Hotspotsitos",
        "Los Orcalitos", "Los Primos", "Los Spyderinis", "Los Tacoritas", "Los Tipi Tacos",
        "Los Tortus", "Los Tralaleritos", "Los Tungtungtungcitos", "Magi Ribbitini",
        "Malame Amarele", "Mangolini Parrocini", "Mariachi Corazoni",
        "Mastodontico Telepiedone", "Matteo", "Meowl", "Mieteteira Bicicleteira",
        "Money Money Puggy", "Mummio Rappitto", "Mythic Lucky Block", "Noo my Candy",
        "Noo my examine", "Noobini Pizzanini", "Nooo My Hotspot", "Nuclearo Dinossauro",
        "Odin Din Din Dun", "Orangutini Ananassini", "Orcalero Orcala", "Orcalita Orcala",
        "Pakrahmatmamat", "Pakrahmatmatina", "Pandaccini Bananini", "Penguino Cocosino",
        "Perochello Lemonchello", "Perrito Burrito", "Pi Pi Watermelon", "Piccione Macchina",
        "Piccionetta Machina", "Pinealotto Fruttarino", "Pipi Avocado", "Pipi Corni",
        "Pipi Kiwi", "Pipi Potato", "Pop Pop Pop Pop Sahur", "Pot Hotspot", "Pot Pumpkin",
        "Quackula", "Quesadilla Crocodila", "Quesadillo Vampiro", "Quivioli Ameleonni",
        "Raccooni Jandelini", "Rhino Helicopterino", "Rhino Toasterino", "Salad fish master",
        "Salamino Penguino", "Sammyni Spyderini", "Secret Lucky Block", "Sigma Boy",
        "Sigma Girl", "Strawberry Elephant"
    ]

def generate_master_list():
    """
    Génère la MASTER_LIST avec les brainrots du wiki.
    Assigne des raretés et des spawn_weights en fonction de la position.
    """
    # Extraire dynamiquement les brainrots du wiki
    brainrot_names = scrape_brainrots_from_wiki()
    
    master_list = []
    
    for i, name in enumerate(brainrot_names):
        # Distribution des raretés (peut être ajustée selon vos besoins)
        if i < len(brainrot_names) * 0.35:  # 35% = Common
            rarity = "Common"
            spawn_weight = 40
        elif i < len(brainrot_names) * 0.55:  # 20% = Rare
            rarity = "Rare"
            spawn_weight = 25
        elif i < len(brainrot_names) * 0.75:  # 20% = Epic
            rarity = "Epic"
            spawn_weight = 15
        elif i < len(brainrot_names) * 0.90:  # 15% = Legendary
            rarity = "Legendary"
            spawn_weight = 10
        else:  # 10% = God
            rarity = "God"
            spawn_weight = 5
        
        brainrot = {
            "name": name,
            "rarity": rarity,
            "spawn_weight": spawn_weight
        }
        master_list.append(brainrot)
    
    return master_list

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 GÉNÉRATEUR DE MASTER LIST - BRAINROT SIMULATOR")
    print("=" * 60)
    
    master_list = generate_master_list()
    
    # Affichage pour vérification
    print(f"\n✅ Total brainrots générés: {len(master_list)}")
    print(f"\n📊 Distribution par rareté:")
    
    rarity_counts = {}
    for rarity in ["Common", "Rare", "Epic", "Legendary", "God"]:
        count = sum(1 for b in master_list if b["rarity"] == rarity)
        rarity_counts[rarity] = count
        percentage = (count / len(master_list)) * 100
        print(f"  {rarity:12} | {count:3} items | {percentage:6.2f}%")
    
    print(f"\n📋 Premiers brainrots (exemples):")
    for i, brainrot in enumerate(master_list[:5], 1):
        print(f"  {i}. {brainrot['name']:30} | {brainrot['rarity']:10} | Poids: {brainrot['spawn_weight']}")
    
    print(f"\n📋 Derniers brainrots (exemples):")
    for i, brainrot in enumerate(master_list[-5:], len(master_list)-4):
        print(f"  {i}. {brainrot['name']:30} | {brainrot['rarity']:10} | Poids: {brainrot['spawn_weight']}")
    
    # Export en JSON pour vérification
    with open("master_list.json", "w", encoding="utf-8") as f:
        json.dump(master_list, f, ensure_ascii=False, indent=2)
    
    # Générer aussi un fichier Python directement utilisable
    with open("master_list_generated.py", "w", encoding="utf-8") as f:
        f.write("# Generated Master List for Brainrot Spawn Simulator\n")
        f.write("# Extracted from: https://stealabrainrot.fandom.com/wiki/Category:Brainrots\n\n")
        f.write("MASTER_LIST = [\n")
        for brainrot in master_list:
            f.write(f'    {{"name": "{brainrot["name"]}", "rarity": "{brainrot["rarity"]}", "spawn_weight": {brainrot["spawn_weight"]}}},\n')
        f.write("]\n")
    
    print("\n💾 Fichiers générés:")
    print("  - master_list.json")
    print("  - master_list_generated.py")
    print("\n✨ Extraction complète!")
    print("=" * 60)