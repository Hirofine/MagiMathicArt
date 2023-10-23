import pandas as pd
import xml.etree.ElementTree as ET

# Fonction pour trier les coordonnées par lettre puis par nombre
def trier_coord(coord):
    def cle_tri(coordonnee):
        lettre, nombre = '', ''
        for char in coordonnee:
            if char.isalpha():
                lettre += char
            else:
                nombre += char
        return (int(nombre), lettre)

    return sorted(coord, key=cle_tri)

# Fonction pour convertir un indice de colonne en lettre (A, B, C...)
def convertir_en_lettre(indice):
    lettre = ""
    while indice > 0:
        indice, reste = divmod(indice - 1, 26)
        lettre = chr(65 + reste) + lettre
    return lettre

# Spécifiez le chemin complet de votre fichier CSV
fichier_csv = "CITROUILLE.csv"

# Chargez le fichier CSV dans un DataFrame
data_frame = pd.read_csv(fichier_csv, sep=';', header=None)  # Spécifiez le délimiteur

# Créez un dictionnaire pour stocker les coordonnées
coordonnees = {
    "N": set(),
    "O": set(),
    "J": set(),
    "G": set(),
    "GF": set(),
    "F": set(),
    "V": set()
}

# Parcourez les lignes du DataFrame
for index, row in data_frame.iterrows():
    for col_name, cell_value in row.items():
        if cell_value in ["N", "O", "J", "G", "GF", "F", "V"]:
            colonne = data_frame.columns.get_loc(col_name) + 1
            coord = f"{convertir_en_lettre(colonne)}{index + 1}"
            coordonnees[cell_value].add(coord)

# Triez les coordonnées
for categorie, coord in coordonnees.items():
    if coord:
        coordonnees[categorie] = trier_coord(coord)

# Affichez les coordonnées triées
for categorie, coord in coordonnees.items():
    if coord:
        print(f"{categorie}: {'; '.join(coord)}")

# Créez un élément racine pour le fichier XML
racine = ET.Element("coordonnees")

# Ajoutez les coordonnées triées au fichier XML
for categorie, coord in coordonnees.items():
    if coord:
        cat_elem = ET.SubElement(racine, categorie)
        cat_elem.text = ", ".join(coord)

# Créez un objet ElementTree et enregistrez le fichier XML
arbre = ET.ElementTree(racine)
arbre.write("coordonnees.xml", encoding="utf-8", xml_declaration=True)

print("Données exportées avec succès vers coordonnees.xml")
