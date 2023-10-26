import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import xml.etree.ElementTree as ET

# Variables globales
largeur_grille = 50
hauteur_grille = 50
grille = [["" for _ in range(largeur_grille)] for _ in range(hauteur_grille)]
couleur_actuelle = "black"  # Couleur par défaut pour dessiner
taille_pixel = 13  # Taille d'un pixel en pixels
alpha = 255
step = 10
pos_image = [0,0]
step_image = 5
step_zoom = 0.01
image_transparente = None
image = None

# Fonction pour mettre à jour la couleur actuelle
def choisir_couleur(nouvelle_couleur):
    global couleur_actuelle
    couleur_actuelle = nouvelle_couleur

def refresh_pixels():
    for y in range(hauteur_grille):
        for x in range(largeur_grille):
            couleur = grille[y][x]
            if couleur:
                canvas.create_rectangle(x * taille_pixel, y * taille_pixel, (x + 1) * taille_pixel, (y + 1) * taille_pixel, fill=couleur)
            

def draw_grid():
    # Dessiner un cadrillage (lignes verticales)
    for i in range(1, largeur_grille):
        canvas.create_line(i * taille_pixel, 0, i * taille_pixel, hauteur_grille * taille_pixel, fill="gray")
    # Dessiner un cadrillage (lignes horizontales)
    for j in range(1, hauteur_grille):
        canvas.create_line(0, j * taille_pixel, largeur_grille * taille_pixel, j * taille_pixel, fill="gray")

# Fonction pour dessiner un pixel de la couleur actuelle
def dessiner_pixel(event):
    x, y = event.x // taille_pixel, event.y // taille_pixel
    grille[y][x] = couleur_actuelle
    canvas.create_rectangle(x * taille_pixel, y * taille_pixel, (x + 1) * taille_pixel, (y + 1) * taille_pixel, fill=couleur_actuelle)
    

# Fonction pour importer une image et la rendre transparente
def importer_image():
    global image
    global image_transparente
    fichier_image = filedialog.askopenfilename(filetypes=[("Fichiers image", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm *.pbm")])
    if fichier_image:
        image = Image.open(fichier_image).convert('RGBA')
        if image.mode != 'RGBA':
            image.convert('RGBA')
        print_image()
        
def redimensionner_image(image, facteur):
    # Redimensionner l'image en fonction du facteur donné
    nouvelle_largeur = int(image.width * facteur)
    nouvelle_hauteur = int(image.height * facteur)
    image_redimensionnee = image.resize((nouvelle_largeur, nouvelle_hauteur))
    return image_redimensionnee

def print_image():
    global image
    global image_transparente
    global pos_image
    print("affichage de l'image alpha:", alpha)
    
    # Appliquer la transparence à l'image
    image_alpha = Image.new('RGBA', image.size, (255, 255, 255, alpha))
    print(image)
    if image.mode != 'RGBA':
        image.convert('RGBA')
    print(image_alpha)
    image_with_alpha = Image.alpha_composite(image_alpha, image)
    
    image_transparente = ImageTk.PhotoImage(image=image_with_alpha)  # Utilisez PhotoImage pour charger l'image avec transparence
    canvas.create_image(pos_image[0], pos_image[1], anchor="nw", image=image_transparente)
    draw_grid()
    refresh_pixels()
    

def change_alpha(mode):
    global alpha
    global image
    if image.mode != 'RGBA':
        image.convert('RGBA')
    donnees_pixel = list(image.getdata())

    # Modifier la valeur alpha de chaque pixel
    nouvelle_donnees_pixel = []
    alpha = alpha - (step * mode)  # Valeur alpha souhaitée (0-255)
    if alpha < 0:
        alpha = 0
    if alpha > 255:
        alpha = 255

    for pixel in donnees_pixel:

        r, g, b = pixel[:3]  # R, G, B, Alpha
        nouvelle_donnees_pixel.append((r, g, b, alpha))
    
    print("nouvelle valeur de alpha:", alpha)

    # Appliquez les nouvelles données de pixel à l'image
    image.putdata(nouvelle_donnees_pixel)
    print_image()

# Fonction pour exporter la grille vers un fichier CSV
def exporter_csv():
    with open("pixel_art.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for ligne in grille:
            writer.writerow(ligne)

# Fonction pour exporter la grille vers un fichier XML
def exporter_xml():
    racine = ET.Element("coordonnees")
    for ligne in grille:
        categorie = ET.Element("N")
        coordonnees = [str(i + 1) for i, couleur in enumerate(ligne) if couleur == "black"]
        categorie.text = ", ".join(coordonnees)
        racine.append(categorie)
    arbre = ET.ElementTree(racine)
    arbre.write("pixel_art.xml", encoding="utf-8", xml_declaration=True)

#gestion des touches
def appuyer_sur_a(event):
    change_alpha(1)

def appuyer_sur_z(event):
    change_alpha(-1)

def appuyer_sur_q(event):
    global image
    global step_zoom
    image = redimensionner_image(image, 1-step_zoom)
    print_image()
    
def appuyer_sur_s(event):
    global image
    global step_zoom
    image = redimensionner_image(image, 1 + step_zoom)
    print_image()

def move_image(mode):
    print("move image")
    global image
    if image != None:
        global pos_image
        global step_image
        if mode == 2:
            pos_image = [pos_image[0] - step_image, pos_image[1]]
        if mode == 3:
            pos_image = [pos_image[0] + step_image, pos_image[1]]
        if mode == 0:
            pos_image = [pos_image[0], pos_image[1] - step_image]
        if mode == 1:
            pos_image = [pos_image[0], pos_image[1] + step_image]
        
        print_image()

def move_image_u(event):
    move_image(0)

def move_image_d(event):
    move_image(1)

def move_image_l(event):
    move_image(2)

def move_image_r(event):
    move_image(3)

# Création de la fenêtre
fenetre = tk.Tk()
fenetre.title("Éditeur de Pixel Art")

# Création de la toile pour dessiner
canvas = tk.Canvas(fenetre, width=largeur_grille * taille_pixel, height=hauteur_grille * taille_pixel)
canvas.bind("<Button-1>", dessiner_pixel)
canvas.pack()
draw_grid()

# Palette de couleurs
couleurs = ["black", "white", "red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "gray", "cyan"]
for couleur in couleurs:
    couleur_button = tk.Button(fenetre, text=couleur, bg=couleur, command=lambda c=couleur: choisir_couleur(c))
    couleur_button.pack(side="left")

# Boutons pour importer l'image
importer_image_button = tk.Button(fenetre, text="Importer Image", command=importer_image)
importer_image_button.pack()

# Boutons pour exporter le dessin
exporter_csv_button = tk.Button(fenetre, text="Exporter vers CSV", command=exporter_csv)
exporter_csv_button.pack()
exporter_xml_button = tk.Button(fenetre, text="Exporter vers XML", command=exporter_xml)
exporter_xml_button.pack()

# Lie la fonction "appuyer_sur_a" à l'événement "<KeyPress-a>"
fenetre.bind("<KeyPress-a>", appuyer_sur_a)
fenetre.bind("<KeyPress-z>", appuyer_sur_z)
fenetre.bind("<KeyPress-q>", appuyer_sur_q)
fenetre.bind("<KeyPress-s>", appuyer_sur_s)

fenetre.bind("<KeyPress-t>", move_image_u)
fenetre.bind("<KeyPress-g>", move_image_d)
fenetre.bind("<KeyPress-f>", move_image_l)
fenetre.bind("<KeyPress-h>", move_image_r)

# Bouton pour quitter
quitter_button = tk.Button(fenetre, text="Quitter", command=fenetre.quit)
quitter_button.pack()

fenetre.mainloop()
