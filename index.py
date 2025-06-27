import random
from collections import Counter, defaultdict
import csv

# Syllabes variées pour créer des noms divins
SYLLABES = [
    "ar", "ze", "no", "ka", "mi", "ru", "ta", "lo", "pha", "ix", "dra", "the",
    "mor", "yn", "ul", "sa", "va", "shi", "kor", "bel", "ny", "xar", "val", "eir",
    "qu", "an", "thur", "zel", "ir", "is", "ly", "ros", "vor", "mek", "nea", "thu",
    "rah", "or", "ien", "laz", "kra", "nim", "sol", "vyn", "eth", "nys", "zan", "tal"
]

DOMAINES = ["guerre", "amour", "mer", "ciel", "mort", "terre", "feu", "sagesse", "chaos", "rêves"]
TRAITS = [
    "sage", "colérique", "fière", "jaloux", "mystique", "impulsif", "calculateur",
    "créatif", "ténébreux", "lumineux", "audacieux", "déterminé", "rancunier",
    "charismatique", "vaniteux", "généreux", "introverti", "extravagant",
    "méfiant", "endurant", "curieux", "loyal", "indépendant", "têtu",
    "romantique", "mélancolique", "ambitieux", "timide", "brave", "naïf",
    "optimiste", "pessimiste", "calme", "agressif", "passionné", "réfléchi",
    "ironique", "vif", "mystérieux", "impitoyable", "doux", "dramatique",
    "dévoué", "orgueilleux", "insouciant", "inflexible", "joueur", "perseverant",
    "sarcastique", "jaloux", "affectueux", "endurant", "romantique", "fiable",
    "énergique", "sérieux", "spirituel", "manipulateur", "patient", "autoritaire",
    "impulsif", "rêveur", "tempétueux", "calme", "mystique", "observateur",
    "aventurier", "pragmatique", "protecteur", "sage", "sympathique", "méditatif",
    "travailleur", "méthodique", "égoïste", "brillant", "fragile", "endurant",
    "inspirant", "loyal", "réservé", "audacieux", "sanguin", "perspicace",
    "charmeur", "malicieux", "noble", "sensible", "taciturne", "veillant",
    "furtif", "vigilant", "courageux", "éloquent", "magnanime", "excentrique",
    "visionnaire", "débonnaire", "impassible", "farouche", "lumineux", "rugueux"
]

# Liste de tuples : (nom, genre, mythologie)
DIEUX_INITIAUX = [
    ("Zeus", ["dieu"], "Grecque", "ciel"),
    ("Hera", ["déesse"], "Grecque", "amour"),
    ("Odin", ["dieu"], "Nordique", "sagesse"),
    ("Freya", ["déesse"], "Nordique", "amour"),
    ("Loki", ["dieu", "déesse"], "Nordique", "chaos"),
    ("Ra", ["dieu"], "Égyptienne", "soleil"),
    ("Isis", ["déesse"], "Égyptienne", "magie"),
    ("Quetzalcoatl", ["dieu"], "Aztèque", "savoir"),
    ("Tlazolteotl", ["déesse"], "Aztèque", "péché"),
    ("Shiva", ["dieu"], "Hindoue", "destruction"),
    ("Parvati", ["déesse"], "Hindoue", "fertilité")
]

# Classe Dieu
class Dieu:
    def __init__(self, nom, genre, domaine, puissance, traits, mythologie, parents=None):
        self.nom = nom
        if isinstance(genre, list):
            self.genre = genre
        else:
            self.genre = [genre]
        self.domaine = domaine
        self.puissance = puissance
        self.traits = traits
        self.parents = parents
        self.mythologie = mythologie

    def get_genre_texte(self):
        if len(self.genre) == 1:
            return self.genre[0]
        else:
            return "/".join(self.genre)

    def __str__(self):
        lineage = f" (enfant de {self.parents[0].nom} et {self.parents[1].nom})" if self.parents else ""
        return f"{self.nom} {self.get_genre_texte()}, {self.domaine}, puissance: {self.puissance}, traits: {', '.join(self.traits)}{lineage}"

# Générateur de nom syllabique
def generer_nom_syllabique():
    return ''.join(random.choices(SYLLABES, k=random.randint(2, 4))).capitalize()

def generer_nom_unique(deja_utilises):
    while True:
        nom = generer_nom_syllabique()
        if nom not in deja_utilises:
            deja_utilises.add(nom)
            return nom

# Génère des dieux de base
def creer_dieux_initiaux():
    dieux = []
    for nom, genre, mythologie, domaine in DIEUX_INITIAUX:
        puissance = 1000
        traits = random.sample(TRAITS, 2)
        dieux.append(Dieu(nom, genre, domaine, puissance, traits, mythologie=mythologie))
    return dieux


# Reproduction
def reproduction(p1, p2, noms_utilises):
    nom = generer_nom_unique(noms_utilises)

    p1_changeant = len(p1.genre) > 1
    p2_changeant = len(p2.genre) > 1

    if p1_changeant and p2_changeant:
        proba_changeant = 0.5
    elif p1_changeant or p2_changeant:
        proba_changeant = 0.2
    else:
        proba_changeant = 0.0

    if random.random() < proba_changeant:
        # enfant héritant du genre changeant (on mélange les genres des parents changeants)
        genres_possibles = []
        if p1_changeant:
            genres_possibles += p1.genre
        if p2_changeant:
            genres_possibles += p2.genre
        genres_possibles = list(set(genres_possibles))
        genre = genres_possibles  # multi-genre
    else:
        # enfant avec genre simple
        genres_possibles = list(set(p1.genre + p2.genre))
        genre = [random.choice(genres_possibles)]


    domaine = random.choice([p1.domaine, p2.domaine, random.choice(DOMAINES)])
    base = (p1.puissance + p2.puissance) / 2
    facteur = random.uniform(0.9, 1.10)  # entre 90% et 110%
    puissance = max(10,int(base * facteur))
    traits = list(set(random.sample(p1.traits + p2.traits + random.sample(TRAITS, 2), 3)))
    mythologie = random.choice([p1.mythologie, p2.mythologie])
    return Dieu(nom, genre, domaine, puissance, traits, mythologie, parents=(p1, p2))

# Simule une génération
def simuler_une_generation(premiere_gen, numero_generation, noms_utilises):
    enfants = []
    couples = []
    for i, a in enumerate(premiere_gen):
        for b in premiere_gen[i+1:]:
            # Simple condition d'exclusion de même dieu et genres non identiques en liste
            if set(a.genre).isdisjoint(set(b.genre)):
                couples.append((a, b))
    random.shuffle(couples)
    for i in range(0, len(couples), 2):
        if i + 1 < len(couples):
            enfant = reproduction(couples[i][0], couples[i][1], noms_utilises)
            enfants.append(enfant)
    afficher_generation(enfants, numero_generation)  # <-- affichage propre ici
    print(f"Nombre d'enfants créés cette génération : {len(enfants)}")
    
    puissances = [d.puissance for d in enfants] if enfants else [0]
    moyenne = sum(puissances) / len(puissances) if enfants else 0

    return enfants, {
        'generation': numero_generation,
        'nombre_dieux': len(enfants),
        'puissance_moyenne': moyenne
    }

def afficher_generation(generation, numero):
    print(f"\n=== Génération {numero} ===")
    for dieu in generation:
        print(f"• [{dieu.mythologie}] {dieu.nom} [{dieu.get_genre_texte()}], {dieu.domaine}, puissance: {dieu.puissance}")
        if dieu.parents:
            print(f"  ↳ Enfant de {dieu.parents[0].nom} & {dieu.parents[1].nom}")
        else:
            print(f"  ↳ Dieu initial")
        print(f"  ↳ Mythologie : {dieu.mythologie}")
        print(f"  ↳ Traits : {', '.join(dieu.traits)}")


# Programme principal interactif
def lancer_simulation():
    panthéon = creer_dieux_initiaux()
    generation_actuelle = panthéon[:]
    noms_utilises = set(d.nom for d in panthéon)
    afficher_generation(generation_actuelle, 0)
    
    statistiques_generations = []
    generation = 1
    while True:
        reponse = input(f"\nGénérer génération {generation} ? (o/n ou chiffre pour +ieurs) > ").lower().strip()
        if reponse == "n":
            exporter_pantheon_csv(panthéon)
            break
        elif reponse.isdigit():
            for _ in range(int(reponse)):
                print(f"\n==== Génération {generation} ====")
                enfants, stats = simuler_une_generation(generation_actuelle, generation, noms_utilises)
                statistiques_generations.append(stats)
                generation_actuelle = enfants
                panthéon.extend(generation_actuelle)
                generation += 1
        else:
            print(f"\n==== Génération {generation} ====")
            enfants, stats = simuler_une_generation(generation_actuelle, generation, noms_utilises)
            statistiques_generations.append(stats)
            generation_actuelle = enfants
            panthéon.extend(generation_actuelle)
            generation += 1
    afficher_statistiques(panthéon)
    print("\n=== Evolution de la puissance moyenne et nombre de dieux par génération ===")
    for stat in statistiques_generations:
        print(f"  Génération {stat['generation']}: {stat['nombre_dieux']} dieux, puissance moyenne {stat['puissance_moyenne']:.2f}")

    print("\nSimulation terminée. Total de dieux créés :", len(panthéon))

def afficher_statistiques(pantheon):
    print("\n=== Statistiques finales ===")

    print(f"Nombre total de dieux créés : {len(pantheon)}")

    # Répartition par mythologie
    mythos = Counter(d.mythologie for d in pantheon)
    print("\nRépartition par mythologie (nombre de dieux et puissance moyenne):")
    for myth, count in mythos.items():
        puissances_mytho = [d.puissance for d in pantheon if d.mythologie == myth]
        moyenne_mytho = sum(puissances_mytho) / len(puissances_mytho)
        print(f"  - {myth} : {count}  dieux, puissance moyenne {moyenne_mytho:.2f}")

    plus_prolifique = mythos.most_common(1)[0]
    print(f"La mythologie la plus prolifique est {plus_prolifique[0]} avec {plus_prolifique[1]} dieux.")


    # Répartition par genre
    genre_counter = Counter()
    for d in pantheon:
        for g in d.genre:
            genre_counter[g] += 1
    print("\nRépartition par genre :")
    for g, count in genre_counter.items():
        print(f"  - {g} : {count}")
    multi_genres = sum(1 for d in pantheon if len(d.genre) > 1)
    print(f"Nombre de dieux avec genre changeant (multi-genres) : {multi_genres}")


    # Répartition par domaine
    domaines = Counter(d.domaine for d in pantheon)
    top10_domaines = domaines.most_common(10)
    print("\nTop 10 des domaines les plus fréquents :")
    for dom, count in top10_domaines:
        print(f"  - {dom} : {count}")

    # Statistiques de puissance
    puissances = [d.puissance for d in pantheon]
    moyenne = sum(puissances) / len(puissances)
    print(f"\nPuissance moyenne : {moyenne:.2f}")
    print(f"Puissance maximale : {max(puissances)}")
    print(f"Puissance minimale : {min(puissances)}")

    # Top 5 dieux les plus puissants
    top10_dieux = sorted(pantheon, key=lambda d: d.puissance, reverse=True)[:10]
    print("\nTop 10 des dieux les plus puissants :")
    for d in top10_dieux:
        print(f"  - {d.nom} ({d.puissance}) [{d.mythologie}]")

    compteur_traits = Counter()
    for d in pantheon:
        compteur_traits.update(d.traits)
    top10_traits = compteur_traits.most_common(10)
    print("\nTop 10 des traits les plus fréquents :")
    for trait, count in top10_traits:
        print(f"  - {trait} : {count}")

def exporter_pantheon_csv(pantheon, nom_fichier="pantheon.csv"):
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        writer.writerow(["Nom", "Genre", "Domaine", "Puissance", "Traits", "Mythologie", "Parents"])
        for d in pantheon:
            parents = f"{d.parents[0].nom} & {d.parents[1].nom}" if d.parents else "N/A"
            writer.writerow([d.nom, "/".join(d.genre), d.domaine, d.puissance, ", ".join(d.traits), d.mythologie, parents])
    print(f"Données exportées dans {nom_fichier}")

# Lancer
if __name__ == "__main__":
    lancer_simulation()
