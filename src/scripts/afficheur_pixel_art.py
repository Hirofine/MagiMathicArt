import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

# Fonction pour convertir les coordonnées au format "nombre lettre" en indices de colonne et de ligne
def convertir_coord(coord):
    lettre, nombre = '', ''
    for char in coord:
        if char.isalpha():
            lettre += char
        else:
            nombre += char
    colonne = sum((ord(c) - 64) * (26 ** i) for i, c in enumerate(reversed(lettre)))
    ligne = int(nombre)
    return colonne, ligne

# Charger le fichier XML
arbre = ET.parse("coordonnees.xml")
racine = arbre.getroot()

# Définir une échelle pour agrandir les pixels
echelle = 100  # Augmentez ce nombre pour augmenter la taille des pixels

# Créer une image avec une résolution plus élevée
largeur_base = 35
hauteur_base = 50
largeur = largeur_base * echelle
hauteur = hauteur_base * echelle
image = Image.new("RGB", (largeur, hauteur), "white")
dessin = ImageDraw.Draw(image)

# Parcourir les éléments XML pour dessiner le pixel art
for categorie in racine:
    coordonnees = categorie.text.split(", ")
    for coord in coordonnees:
        colonne, ligne = convertir_coord(coord)
        # Dessiner un carré de couleur en fonction de la catégorie
        if categorie.tag == "N":
            couleur = (0, 0, 0)  # Noir
        elif categorie.tag == "O":
            couleur = (255, 128, 0)  # Orange
        elif categorie.tag == "J":
            couleur = (255, 255, 0)  # Jaune
        elif categorie.tag == "G":
            couleur = (128, 128, 128)  # Vert
        elif categorie.tag == "GF":
            couleur = (64, 64, 64)  # Bleu
        elif categorie.tag == "F":
            couleur = (128, 64, 0)  # Bleu
        elif categorie.tag == "V":
            couleur = (30, 150, 64)  # Bleu
        # Dessiner un carré à la position ajustée par l'échelle
        dessin.rectangle([(colonne * echelle, ligne * echelle),
                          ((colonne + 1) * echelle, (ligne + 1) * echelle)],
                         fill=couleur)

# Afficher l'image avec une échelle d'affichage
image = image.resize((largeur, hauteur))  # Redimensionner l'image pour affichage
image.show()
