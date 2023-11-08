document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le conteneur du tableau
    const colorTable = document.getElementById("palette-display");

    // Créez un tableau de couleurs
    const colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"];

    // Parcourez le tableau de couleurs et créez des cases carrées
    colors.forEach(function(color) {
        const square = document.createElement("div");
        square.className = "square";
        square.style.backgroundColor = color;
        colorTable.appendChild(square);
    });
});

const sliders = document.querySelectorAll('.slider');
const colorBox = document.getElementById('color-box');
const selectButton = document.getElementById('select-color');

selectButton.addEventListener("click", selectColor);


sliders.forEach((slider, index) => {
    slider.addEventListener('input', updateColor);
});

function selectColor(){
    couleur = rgbToHex(colorBox.style.backgroundColor);
    console.log("Vous avez choisi la couleur :", couleur);
}

function updateColor() {
    const red = sliders[0].value;
    const green = sliders[1].value;
    const blue = sliders[2].value;
    colorBox.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;
}

function rgbToHex(rgb){
    const parts = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);

    if (!parts) {
        return rgb; // Si la chaîne n'est pas un format RGB valide, retournez-la telle quelle
    }

    // Extrait les valeurs R, G et B
    const red = parseInt(parts[1]);
    const green = parseInt(parts[2]);
    const blue = parseInt(parts[3]);

    // Convertit les valeurs en format hexadécimal
    const redHex = red.toString(16).padStart(2, '0');
    const greenHex = green.toString(16).padStart(2, '0');
    const blueHex = blue.toString(16).padStart(2, '0');

    // Combine les valeurs hexadécimales pour former la couleur en format #RRGGBB
    const hexColor = `#${redHex}${greenHex}${blueHex}`;

    return hexColor;
}