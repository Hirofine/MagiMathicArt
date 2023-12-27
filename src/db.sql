-- Table des Utilisateurs
CREATE TABLE Users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pseudo VARCHAR(255) NOT NULL,
  passw VARCHAR(255) NOT NULL,
  token VARCHAR(255),
  tokenExpi DATETIME,
  tokenSalt VARCHAR(255)
);

-- Table des Projets
CREATE TABLE Projets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  description TEXT
  -- Autres colonnes de projet
);

-- Table des Couleurs
CREATE TABLE Couleurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    color VARCHAR(7) UNIQUE NOT NULL -- Code hexadécimal de la couleur
);

-- Table des Palettes
CREATE TABLE Palettes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
    -- D'autres colonnes pour les informations de la palette
);

-- Table des Images
CREATE TABLE Images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  description TEXT,
  image BLOB
  -- Autres colonnes d'image
);

-- Table des Pixel Arts
CREATE TABLE PixelArts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  description TEXT,
  dimensionsX INT,
  dimensionsY INT,
  art TEXT -- Stockez ici les données de pixel art
  -- Autres colonnes de pixel art
);

-- Table des Réponses
CREATE TABLE Reponses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  description TEXT,
  ennonce TEXT,
  fonction TEXT, 
  genre TEXT
  -- Stockez ici les fonctions ou données de réponse
  -- Autres colonnes de réponse
);

-- Table d'Association entre Palette et Couleur
CREATE TABLE AssoPaletteCouleur (
  id INT AUTO_INCREMENT PRIMARY KEY,
  palette_id INT,
  couleur_id INT,
  position INT,
  UNIQUE (palette_id, couleur_id, position),
  FOREIGN KEY (palette_id) REFERENCES Palettes(id),
  FOREIGN KEY (couleur_id) REFERENCES Couleurs(id)
);

-- Table d'Association entre Palette et Reponse pour un projet donné
CREATE TABLE AssoProjetPaletteReponse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projet_id INT,
    palette_id INT,
    reponse_id INT,
    position INT,
    UNIQUE (projet_id, palette_id, reponse_id),
    FOREIGN KEY (projet_id) REFERENCES Projets(id),
    FOREIGN KEY (palette_id) REFERENCES Palettes(id),
    FOREIGN KEY (reponse_id) REFERENCES Reponses(id)
);

-- Table d'Association entre Projets et Images
CREATE TABLE AssoProjetImage (
  id INT AUTO_INCREMENT PRIMARY KEY,
  projet_id INT,
  image_id INT,
  coordX INT,
  coordY INT,
  opacite INT,
  dimX INT,
  dimY INT,
  UNIQUE (projet_id, image_id),
  FOREIGN KEY (projet_id) REFERENCES Projets(id),
  FOREIGN KEY (image_id) REFERENCES Images(id)
);

-- Table d'Association entre Projets et Réponses
CREATE TABLE AssoProjetReponse (
  id INT AUTO_INCREMENT PRIMARY KEY,
  projet_id INT,
  reponse_id INT,
  UNIQUE (projet_id, reponse_id),
  FOREIGN KEY (projet_id) REFERENCES Projets(id),
  FOREIGN KEY (reponse_id) REFERENCES Reponses(id)
);

-- Table d'Association entre Projet et Palette
CREATE TABLE AssoProjetPalette (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projet_id INT,
    palette_id INT,
    UNIQUE (projet_id, palette_id),
    FOREIGN KEY (projet_id) REFERENCES Projets(id),
    FOREIGN KEY (palette_id) REFERENCES Palettes(id)
);

-- Table d'Association entre Projets et PixelArts
CREATE TABLE AssoProjetPixelArt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projet_id INT,
    pixelart_id INT,
    UNIQUE (projet_id, pixelart_id),
    FOREIGN KEY (projet_id) REFERENCES Projets(id),
    FOREIGN KEY (pixelart_id) REFERENCES PixelArts(id)
);

-- Table d'Association entre Users et Projets
CREATE TABLE AssoUserProjet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    projet_id INT,
    UNIQUE (user_id, projet_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (projet_id) REFERENCES Projets(id)
);

-- Table d'Association entre Users et Palettes
CREATE TABLE AssoUserPalette (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    palette_id INT,
    UNIQUE (user_id, palette_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (palette_id) REFERENCES Palettes(id)
);

-- Table d'Association entre Users et Images
CREATE TABLE AssoUserImage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image_id INT,
    UNIQUE (user_id, image_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (image_id) REFERENCES Images(id)
);

CREATE TABLE AssoUserReponse(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reponse_id INT,
    UNIQUE (user_id, reponse_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (reponse_id) REFERENCES Reponses(id)
);

CREATE TABLE AssoUserPixelArt(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    pixelart_id INT,
    UNIQUE (user_id, pixelart_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (pixelart_id) REFERENCES PixelArts(id)
);


