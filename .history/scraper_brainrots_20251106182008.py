import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

# URL du wiki
WIKI_URL = "https://stealabrainrot.fandom.com/wiki/Category:Brainrots"

def scrape_brainrots_from_wiki():
    """
    Scrape dynamiquement la liste des brainrots depuis le wiki Fandom.
    """
    try:
        print("🔄 Scraping du wiki Fandom en cours...")
        
        # Headers pour éviter les blocages
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(WIKI_URL, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Méthode 1: Extraire les liens des brainrots
        brainrot_names = []
        
        # Chercher les liens dans les sections de liste (structure de Fandom)
        # Les liens sont généralement dans des balises <a> avec href=/wiki/
        all_links = soup.find_all('a', href=re.compile(r'^/wiki/'))
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Filtrer les noms valides
            if href.startswith('/wiki/') and text and len(text) > 0:
                # Exclure les pages système et spéciales
                if not any(exclude in href for exclude in 
                          ['Category:', 'File:', 'User', 'Talk:', 'Special:', 'Help:']):
                    # Exclure les textes trop courts ou spéciaux
                    if len(text) > 1 and text not in ['Fandom', 'Community', 'Discuss']:
                        brainrot_names.append(text)
        
        # Dédupliquer et trier
        brainrot_names = sorted(list(set(brainrot_names)))
        
        print(f"✅ {len(brainrot_names)} brainrots trouvés!")
        
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
    master_list = generate_master_list()
    
    # Affichage pour vérification
    print(f"✅ Total brainrots générés: {len(master_list)}")
    print(f"\n📊 Distribution par rareté:")
    for rarity in ["Common", "Rare", "Epic", "Legendary", "God"]:
        count = sum(1 for b in master_list if b["rarity"] == rarity)
        print(f"  {rarity}: {count}")
    
    # Export en JSON pour vérification
    with open("master_list.json", "w", encoding="utf-8") as f:
        json.dump(master_list, f, ensure_ascii=False, indent=2)
    
    print("\n💾 Master list exportée dans 'master_list.json'")
