from PIL import Image, ImageDraw
import csv


# Créez une fonction pour identifier et générer les couleurs (ici, vous pouvez définir vos associations de couleurs)
def identifier_couleur(valeur):
    if valeur == "black":
        return (0, 0, 0)  # Noir //
    elif valeur == "red":
        return (255, 0, 0)  # red //
    elif valeur == "yellow":
        return (255, 255, 0)  # yellow //
    elif valeur == "orange":
        return (255, 128, 0)  # orange //
    elif valeur == "brown":
        return (128, 50, 50)  # rouge fonce //
    elif valeur == "green":
        return (0, 100, 0)  # vert fonce //
    elif valeur == "cyan":
        return (0, 170, 200)  # Bleu clair //
    elif valeur == "white":
        return (200, 0, 200)  # violet clair //
    elif valeur == "gray":
        return (70, 70, 70)  # gris //
    elif valeur == "pink":
        return (0, 70, 120)  # Bleu fonce
    elif valeur == "purple":
        return (0, 240, 0)  # vert clair //
    elif valeur == "blue":
        return (90, 0, 90)  # violet fonce //
    # Ajoutez d'autres associations de couleurs selon vos besoins
    else:
        return (255, 255, 255)  # Blanc (couleur par défaut si la valeur n'est pas reconnue)

# Chargez un fichier CSV de votre choix
csv_filename = "bulbi.csv"

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
