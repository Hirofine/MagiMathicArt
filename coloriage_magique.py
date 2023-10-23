import csv
import random


def gen_droite(n):
    valeurs = []
    for _ in range(n):
        lettre1 = random.choice("ABCDEFGH")
        lettre2 = random.choice("ABCDEFGH")
        while lettre2 == lettre1:  # Assurez-vous que les lettres sont différentes
            lettre2 = random.choice("ABCDEFGH")
        valeur = f"({lettre1}{lettre2})"
        valeurs.append(valeur)
    valeurs.append("(d)")
    return valeurs

def gen_segment(n):
    valeurs = []
    for _ in range(n):
        lettre1 = random.choice("ABCDEFGH")
        lettre2 = random.choice("ABCDEFGH")
        while lettre2 == lettre1:  # Assurez-vous que les lettres sont différentes
            lettre2 = random.choice("ABCDEFGH")
        valeur = f"[{lettre1}{lettre2}]"
        valeurs.append(valeur)
    return valeurs

def gen_demi_droite(n):
    valeurs = []
    for _ in range(n):
        lettre1 = random.choice("ABCDEFGH")
        lettre2 = random.choice("ABCDEFGH")
        while lettre2 == lettre1:  # Assurez-vous que les lettres sont différentes
            lettre2 = random.choice("ABCDEFGH")
        valeur = f"[{lettre1}{lettre2})"
        valeurs.append(valeur)
    return valeurs

def gen_appart(n):
    return ["∈"]

def gen_point(n):
    valeurs = []
    for _ in range(n):
        lettre1 = random.choice("ABCDEFGH")
        nombre = random.randint(0,50)
        valeur = f"{lettre1}({nombre})"
        valeurs.append(valeur)
    return valeurs

def gen_frac_inf(n):
    fractions = []
    for _ in range(n):
        a = random.randint(0, 99)  # Numérateur aléatoire de 0 à 99
        b = random.randint(a + 1, 100)  # Dénominateur aléatoire de 1 à 100
        fraction = f"{a}/{b}"
        fractions.append(fraction)
    return fractions

def gen_frac_1(n):
    fractions = []
    for _ in range(n):
        a = random.randint(1, 100)  # Numérateur aléatoire de 0 à 99
        fraction = f"{a}/{a}"
        fractions.append(fraction)
    return fractions

def gen_nb_0_100(n):
    fractions = []
    for _ in range(n):
        a = random.randint(0, 99)  # Numérateur aléatoire de 0 à 99
        fraction = f"{a}"
        fractions.append(fraction)
    return fractions

def gen_nb_1001_10000(n):
    fractions = []
    for _ in range(n):
        a = random.randint(1000, 10000)  # Numérateur aléatoire de 0 à 99
        fraction = f"{a}"
        fractions.append(fraction)
    return fractions

def gen_nb_101_1000(n):
    fractions = []
    for _ in range(n):
        a = random.randint(100, 999)  # Numérateur aléatoire de 0 à 99
        fraction = f"{a}"
        fractions.append(fraction)
    return fractions

def gen_somme_100(n):
    fractions = []
    for _ in range(n):
        a = random.randint(0, 100)  # Numérateur aléatoire de 0 à 99
        b = 100 - a
        fraction = f"{a} + {b}"
        fractions.append(fraction)
    return fractions

def gen_frac_sup(n):
    fractions = []
    for _ in range(n):
        a = random.randint(0, 99)  # Numérateur aléatoire de 0 à 99
        b = random.randint(a + 1, 100)  # Dénominateur aléatoire de 1 à 100
        fraction = f"{b}/{a}"
        fractions.append(fraction)
    return fractions

# Définir des tableaux de valeurs pour chaque couleur
valeurs_couleurs = {
    "black": gen_droite(50),
    "yellow": gen_segment(50),
    "orange": gen_demi_droite(50),
    "purple": gen_frac_1(50),
    "red": gen_frac_inf(50),
    "green": gen_frac_sup(50),
    "brown": gen_appart(50),
    "white": gen_point(50),
    "pink": gen_nb_101_1000(50),
    "cyan": gen_nb_0_100(50),
    "gray": gen_nb_1001_10000(50),
    "blue": gen_nb_0_100(50)
}



# Ouvrir le fichier CSV en lecture
with open('sapin.csv', 'r', newline='') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv, delimiter=';')
    lignes = list(lecteur_csv)

# Fonction pour remplacer les couleurs par des valeurs aléatoires
def remplacer_couleurs(ligne):
    for i in range(len(ligne)):
        if ligne[i] in valeurs_couleurs:
            couleur = ligne[i]
            nouvelle_valeur = random.choice(valeurs_couleurs[couleur])
            ligne[i] = nouvelle_valeur

# Modifier les couleurs dans chaque ligne
for ligne in lignes:
    remplacer_couleurs(ligne)

# Sauvegarder les modifications dans un nouveau fichier CSV
with open('image_modifiee.csv', 'w', newline='') as fichier_csv_modifie:
    ecrivain_csv = csv.writer(fichier_csv_modifie, delimiter=';')
    ecrivain_csv.writerows(lignes)

print("Modification terminée. Le fichier 'image_modifiee.csv' a été créé avec les couleurs modifiées.")