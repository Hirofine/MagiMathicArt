from PIL import Image, ImageDraw
import csv
import re

def is_droite(valeur):
    if len(valeur) !=4:
        if valeur == "(d)":
            return True
        else:
            return False
    if valeur[0] != '(' or valeur[3] != ')':
        return False
    if not ('A' <= valeur[1] <= 'H' and 'A' <= valeur[2] <= 'H'):
        return False 
    return True

def is_segment(valeur):
    if len(valeur) !=4:
        return False
    if valeur[0] != '[' or valeur[3] != ']':
        return False
    if not ('A' <= valeur[1] <= 'H' and 'A' <= valeur[2] <= 'H'):
        return False 
    return True

def is_demi_droite(valeur):
    if len(valeur) !=4:
        return False
    if valeur[0] != '[' or valeur[3] != ')':
        return False
    if not ('A' <= valeur[1] <= 'H' and 'A' <= valeur[2] <= 'H'):
        return False 
    return True

def is_frac_sup(valeur):
    # Utilisation d'une expression régulière pour détecter les fractions
    pattern = r'\b(\d{1,3})/(\d{1,3})\b'
    fractions = re.findall(pattern, valeur)
    fractions = [(int(num), int(den)) for num, den in fractions]
    if len(fractions) == 0 :
        return False
    return fractions[0][0] > fractions[0][1]

def is_frac_inf(valeur):
     # Utilisation d'une expression régulière pour détecter les fractions
    pattern = r'\b(\d{1,2})/(\d{1,3})\b'
    fractions = re.findall(pattern, valeur)
    fractions = [(int(num), int(den)) for num, den in fractions]
    if len(fractions) == 0 :
        return False
    return fractions[0][0] < fractions[0][1]

def is_appart(valeur):
    return valeur == "∈"

def is_nb_1000_10000(valeur):
    pattern = r"^\d{4,5}$"
    match = re.match(pattern, valeur)
    return bool(match)

def is_point(valeur):
    pattern = r"([A-H])\((\d+)\)"
    match = re.match(pattern, valeur)
    return bool(match)

def is_nb_100_999(valeur):
    pattern = r"^\d{3}$"
    match = re.match(pattern, valeur)
    return bool(match)

def is_nb_0_99(valeur):
    pattern = r"^\d{1,2}$"
    match = re.match(pattern, valeur)
    return bool(match)

def is_somme_100(valeur):
    pattern = r"^(?:100|\d{1,2}) \+ (?:100|\d{1,2})$"
    match = re.match(pattern, valeur)
    if match:
        n, m = map(int, valeur.split(" + "))
        return n + m == 100
    return False

def is_frac_1(valeur):
     # Utilisation d'une expression régulière pour détecter les fractions
    pattern = r'\b(\d{1,2})/(\d{1,3})\b'
    fractions = re.findall(pattern, valeur)
    fractions = [(int(num), int(den)) for num, den in fractions]
    if len(fractions) == 0 :
        return False
    return fractions[0][0] == fractions[0][1]

def decrypt(valeur):
    if is_droite(valeur):
        return "black"
    elif is_segment(valeur):
        return "yellow"
    elif is_demi_droite(valeur):
        return "orange"
    elif is_frac_sup(valeur):
        return "green"
    elif is_frac_inf(valeur):
        return "red"
    elif is_appart(valeur):
        return "brown"
    elif is_nb_1000_10000(valeur):
        return "gray"
    elif is_point(valeur):
        return "white"
    elif is_nb_100_999(valeur):
        return "pink"
    elif is_nb_0_99(valeur):
        return "blue"
    elif is_somme_100(valeur):
        return "gray"
    elif is_frac_1(valeur):
        return "purple"
    else:
        return "none"

# Créez une fonction pour identifier et générer les couleurs (ici, vous pouvez définir vos associations de couleurs)
def identifier_couleur(valeur):

    d_valeur = decrypt(valeur)

    if d_valeur == "black":
        return (0, 0, 0)  # Noir //
    elif d_valeur == "red":
        return (255, 0, 0)  # red //
    elif d_valeur == "yellow":
        return (255, 255, 0)  # yellow //
    elif d_valeur == "orange":
        return (255, 128, 0)  # orange //
    elif d_valeur == "brown":
        return (128, 50, 50)  # rouge fonce //
    elif d_valeur == "green":
        return (0, 100, 0)  # vert fonce //
    elif d_valeur == "cyan":
        return (0, 170, 200)  # Bleu clair //
    elif d_valeur == "white":
        return (200, 0, 200)  # violet clair //
    elif d_valeur == "gray":
        return (70, 70, 70)  # gris //
    elif d_valeur == "pink":
        return (0, 70, 120)  # Bleu fonce
    elif d_valeur == "purple":
        return (0, 240, 0)  # vert clair //
    elif d_valeur == "blue":
        return (90, 0, 90)  # violet fonce //
    # Ajoutez d'autres associations de couleurs selon vos besoins
    else:
        return (255, 255, 255)  # Blanc (couleur par défaut si la valeur n'est pas reconnue)

# Chargez un fichier CSV de votre choix
csv_filename = "sapin_final.csv"

# Lire le fichier CSV
with open(csv_filename, newline='') as csvfile:
    # Utilisez delimiter pour spécifier le séparateur (dans cet exemple, le point-virgule)
    csvreader = csv.reader(csvfile, delimiter=';')
    data = [list(row) for row in csvreader]

# Taille d'un pixel (modifiable selon vos besoins)
taille_pixel = 20

# Créez une image pour représenter le fichier CSV
largeur = len(data[0]) * taille_pixel
hauteur = len(data) * taille_pixel
image = Image.new("RGB", (largeur, hauteur), "white")
dessin = ImageDraw.Draw(image)

# Parcourez le fichier CSV pour dessiner les pixels
for y, ligne in enumerate(data):
    for x, valeur in enumerate(ligne):
        couleur = identifier_couleur(valeur)
        dessin.rectangle([(x * taille_pixel, y * taille_pixel),
                          ((x + 1) * taille_pixel, (y + 1) * taille_pixel)],
                         fill=couleur)

# Affichez l'image
image.show()