import random
import time
import json
import pandas as pd

# === LISTE MAÎTRESSE DES OBJETS BRAINROT ===
MASTER_LIST = [
    {"name": "1x1x1x1", "rarity": "Common", "spawn_weight": 40},
    {"name": "67", "rarity": "Common", "spawn_weight": 40},
    {"name": "Admin Lucky Block", "rarity": "Common", "spawn_weight": 40},
    {"name": "Agarrini La Palini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Alessio", "rarity": "Common", "spawn_weight": 40},
    {"name": "Anpali Babel", "rarity": "Common", "spawn_weight": 40},
    {"name": "Antonio", "rarity": "Common", "spawn_weight": 40},
    {"name": "Aquanut", "rarity": "Common", "spawn_weight": 40},
    {"name": "Avocadini Antilopini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Avocadini Guffo", "rarity": "Common", "spawn_weight": 40},
    {"name": "Avocadorilla", "rarity": "Common", "spawn_weight": 40},
    {"name": "Ballerina Cappuccina", "rarity": "Common", "spawn_weight": 40},
    {"name": "Ballerino Lololo", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bambini Crostini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bambu Bambu Sahur", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bananita Dolphinita", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bananito Bandito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bandito Axolito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bandito Bobritto", "rarity": "Common", "spawn_weight": 40},
    {"name": "Belula Beluga", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bisonte Giuppitere", "rarity": "Common", "spawn_weight": 40},
    {"name": "Blackhole Goat", "rarity": "Common", "spawn_weight": 40},
    {"name": "Blueberrinni Octopusini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bombardini Tortinii", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bombardiro Crocodilo", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bombombini Gusini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Boneca Ambalabu", "rarity": "Common", "spawn_weight": 40},
    {"name": "Brainrot God Lucky Block", "rarity": "Common", "spawn_weight": 40},
    {"name": "Brasilini Berimbini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Brr Brr Patapim", "rarity": "Common", "spawn_weight": 40},
    {"name": "Brr es Teh Patipum", "rarity": "Common", "spawn_weight": 40},
    {"name": "Brri Brri Bicus Dicus Bombicus", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bruto Gialutto", "rarity": "Common", "spawn_weight": 40},
    {"name": "Buho De Fuego", "rarity": "Common", "spawn_weight": 40},
    {"name": "Bulbito Bandito Traktorito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Burbaloni Luliloli", "rarity": "Common", "spawn_weight": 40},
    {"name": "Burguro And Fryuro", "rarity": "Common", "spawn_weight": 40},
    {"name": "Burrito Bandito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cacasito Satalito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cachorrito Melonito", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cacto Hipopotamo", "rarity": "Common", "spawn_weight": 40},
    {"name": "Capi Taco", "rarity": "Common", "spawn_weight": 40},
    {"name": "Capitano Moby", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cappuccino Assassino", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cappuccino Clownino", "rarity": "Common", "spawn_weight": 40},
    {"name": "Caramello Filtrello", "rarity": "Common", "spawn_weight": 40},
    {"name": "Carloo", "rarity": "Common", "spawn_weight": 40},
    {"name": "Carrotini Brainini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Cavallo Virtuoso", "rarity": "Common", "spawn_weight": 40},
    {"name": "Celularcini Viciosini", "rarity": "Common", "spawn_weight": 40},
    {"name": "Chachechi", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chef Crabracadabra", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chicleteira Bicicleteira", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chicleteirina Bicicleteirina", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chihuanini Taconini", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chillin Chili", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chimpanzini Bananini", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chimpanzini Spiderini", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Chipso and Queso", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Cocofanto Elefanto", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Cocosini Mama", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Combinasions", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Corn Corn Corn Sahur", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Crabbo Limonetta", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Developini Braziliaspidini", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Dragon Cannelloni", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Dug dug dug", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Dul Dul Dul", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Elefanto Frigo", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Esok Sekolah", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Espresso Signora", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Eviledon", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Extinct Ballerina", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Extinct Matteo", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Extinct Tralalero", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Fluriflura", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Fragola La La La", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Frankentteo", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Frigo Camelo", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Frio Ninja", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Frogato Pirato", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Ganganzelli Trulala", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Gangster Footera", "rarity": "Rare", "spawn_weight": 25},
    {"name": "Garama and Madundung", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Gattatino Neonino", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Gattatino Nyanino", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Gattito Tacoto", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Girafa Celestre", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Glorbo Fruttodrillo", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Gorillo Subwoofero", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Gorillo Watermelondrillo", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Graipuss Medussi", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Guerriro Digitale", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Headless Horseman", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Jacko Jack Jack", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Job Job Job Sahur", "rarity": "Epic", "spawn_weight": 15},
    {"name": "John Pork", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Karker Sahur", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Karkerkar Kurkur", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Ketchuru and Musturu", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Ketupat Kepat", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Krupuk Pagi Pagi", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Cucaracha", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Extinct Grande", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Grande Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Karkerkar Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Sahur Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Secret Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Spooky Grande", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Supreme Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Taco Combinasion", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Vacca Jacko Linterino", "rarity": "Epic", "spawn_weight": 15},
    {"name": "La Vacca Saturno Saturnita", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Las Cappuchinas", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Las Sis", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Las Tralaleritas", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Las Vaquitas Saturnitas", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Lerulerulerule", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Limited Stock Brainrots", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Lionel Cactuseli", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Lirilì Larilà", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Los 67", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Los Bombinitos", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Los Bros", "rarity": "Epic", "spawn_weight": 15},
    {"name": "Los Chicleteiras", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Combinasionas", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Crocodillitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Hotspotsitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Jobcitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Karkeritos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Matteos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Mobilis", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Noobinis", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Nooo My Hotspotsitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Orcalitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Primos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Spyderinis", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Tacoritas", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Tipi Tacos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Tortus", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Tralaleritos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Los Tungtungtungcitos", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Magi Ribbitini", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Malame Amarele", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mangolini Parrocini", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mariachi Corazoni", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mastodontico Telepiedone", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Matteo", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Meowl", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mieteteira Bicicleteira", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Money Money Puggy", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mummio Rappitto", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Mythic Lucky Block", "rarity": "Legendary", "spawn_weight": 10},
    {"name": "Noo my Candy", "rarity": "God", "spawn_weight": 5},
    {"name": "Noo my examine", "rarity": "God", "spawn_weight": 5},
    {"name": "Noobini Pizzanini", "rarity": "God", "spawn_weight": 5},
    {"name": "Nooo My Hotspot", "rarity": "God", "spawn_weight": 5},
    {"name": "Nuclearo Dinossauro", "rarity": "God", "spawn_weight": 5},
    {"name": "Odin Din Din Dun", "rarity": "God", "spawn_weight": 5},
    {"name": "Orangutini Ananassini", "rarity": "God", "spawn_weight": 5},
    {"name": "Orcalero Orcala", "rarity": "God", "spawn_weight": 5},
    {"name": "Orcalita Orcala", "rarity": "God", "spawn_weight": 5},
    {"name": "Pakrahmatmamat", "rarity": "God", "spawn_weight": 5},
    {"name": "Pakrahmatmatina", "rarity": "God", "spawn_weight": 5},
    {"name": "Pandaccini Bananini", "rarity": "God", "spawn_weight": 5},
    {"name": "Penguino Cocosino", "rarity": "God", "spawn_weight": 5},
    {"name": "Perochello Lemonchello", "rarity": "God", "spawn_weight": 5},
    {"name": "Perrito Burrito", "rarity": "God", "spawn_weight": 5},
    {"name": "Pi Pi Watermelon", "rarity": "God", "spawn_weight": 5},
    {"name": "Piccione Macchina", "rarity": "God", "spawn_weight": 5},
    {"name": "Piccionetta Machina", "rarity": "God", "spawn_weight": 5},
    {"name": "Pinealotto Fruttarino", "rarity": "God", "spawn_weight": 5},
    {"name": "Pipi Avocado", "rarity": "God", "spawn_weight": 5},
    {"name": "Pipi Corni", "rarity": "God", "spawn_weight": 5},
    {"name": "Pipi Kiwi", "rarity": "God", "spawn_weight": 5},
    {"name": "Pipi Potato", "rarity": "God", "spawn_weight": 5},
    {"name": "Pop Pop Pop Pop Sahur", "rarity": "God", "spawn_weight": 5},
    {"name": "Pot Hotspot", "rarity": "God", "spawn_weight": 5},
    {"name": "Pot Pumpkin", "rarity": "God", "spawn_weight": 5},
    {"name": "Quackula", "rarity": "God", "spawn_weight": 5},
    {"name": "Quesadilla Crocodila", "rarity": "God", "spawn_weight": 5},
    {"name": "Quesadillo Vampiro", "rarity": "God", "spawn_weight": 5},
    {"name": "Quivioli Ameleonni", "rarity": "God", "spawn_weight": 5},
    {"name": "Raccooni Jandelini", "rarity": "God", "spawn_weight": 5},
    {"name": "Rhino Helicopterino", "rarity": "God", "spawn_weight": 5},
    {"name": "Rhino Toasterino", "rarity": "God", "spawn_weight": 5},
    {"name": "Salad fish master", "rarity": "God", "spawn_weight": 5},
    {"name": "Salamino Penguino", "rarity": "God", "spawn_weight": 5},
    {"name": "Sammyni Spyderini", "rarity": "God", "spawn_weight": 5},
    {"name": "Secret Lucky Block", "rarity": "God", "spawn_weight": 5},
    {"name": "Sigma Boy", "rarity": "God", "spawn_weight": 5},
    {"name": "Sigma Girl", "rarity": "God", "spawn_weight": 5},
    {"name": "Strawberry Elephant", "rarity": "God", "spawn_weight": 5},
]

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
TYPE_WEIGHTS = [80, 15, 5]  # pour random.choices

MUTATION_MULTIPLIERS = {"None": 1.0, "Minor": 1.2, "Major": 1.6, "Mythic": 2.0}
MUTATION_WEIGHTS = [70, 20, 8, 2]

# === JOURNAL DE SPAWN ===
spawn_log = []

# === FONCTION DE SPAWN ===
def spawn_brainrot():
    # Sélection pondérée de l’objet
    selected = random.choices(MASTER_LIST, weights=[b["spawn_weight"] for b in MASTER_LIST], k=1)[0]
    
    # Sélection du type et mutation (également pondérée)
    type_selected = random.choices(list(TYPE_MULTIPLIERS.keys()), weights=TYPE_WEIGHTS, k=1)[0]
    mutation_selected = random.choices(list(MUTATION_MULTIPLIERS.keys()), weights=MUTATION_WEIGHTS, k=1)[0]
    
    # Calcul du prix
    base_value = RARITY_VALUES[selected["rarity"]]
    final_price = base_value * TYPE_MULTIPLIERS[type_selected] * MUTATION_MULTIPLIERS[mutation_selected]
    final_price = round(final_price, 2)
    
    # Enregistrement
    spawn_info = {
        "name": selected["name"],
        "rarity": selected["rarity"],
        "type": type_selected,
        "mutation": mutation_selected,
        "price": final_price
    }
    spawn_log.append(spawn_info)
    
    # Affichage en temps réel
    print(f"🧠 {selected['name']} | {selected['rarity']} | {type_selected} | {mutation_selected} → 💰 {final_price}$")
    
# === BOUCLE DE SIMULATION ===
def simulate_spawns(duration_seconds=20):
    print("=== Simulation de Spawn Brainrot ===")
    num_spawns = duration_seconds // 2  # toutes les 2 secondes
    for _ in range(num_spawns):
        spawn_brainrot()
        time.sleep(2)
    
    # Export JSON
    with open("brainrot_spawn_log.json", "w", encoding="utf-8") as f:
        json.dump(spawn_log, f, ensure_ascii=False, indent=4)
    print("\n✅ Journal exporté dans brainrot_spawn_log.json")

# === LANCEMENT ===
if __name__ == "__main__":
    simulate_spawns(20)
