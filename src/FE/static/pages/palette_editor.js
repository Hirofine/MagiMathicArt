var api_url = "https://be.magimathicart.hirofine.fr"
const colorTable = document.getElementById("palette-display");
const sliders = document.querySelectorAll('.slider');
const colorBox = document.getElementById('color-box');
const selectButton = document.getElementById('validate-color');
const color_editor_div = document.getElementById("color-editor-div");
const addButton = document.getElementById('add-color');
const deleteButton = document.getElementById("delete-color");
const saveButton = document.getElementById("save-palette");
const name_input = document.getElementById("name-input");
var colors = [];
var paletteName = "";
var id = 0;
var mode ="new";

document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le conteneur du tableau  
    //determine mode
    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);

    mode = params.get("mode");
    id = params.get("id");
    //mode new
    if(mode == "new"){
        colors = [[0, "#FFFFFF"]];
        refresh_colors();
    }
    if(mode == "test"){
        colors =[[0,"#ff736e"], [1,"#d30256"], [2,"#d3fa56"],[3,"#da02e6"],[4,"#d1c556"]];
        refresh_colors();
    }
    if(mode == "edit"){
        display_palette(id);
        
    }

    //display les couleurs déjà présente
    


    // Créez un tableau de couleurs

    
    // Parcourez le tableau de couleurs et créez des cases carrées
});

async function display_palette(id){
    palette = await get_palette(id);
    console.log(palette);
    colors_data = palette["couleurs"];
    colors = [];
    colors_data.forEach((col, i) => {
        colors[i] = [col.position, col.color]; 
    })
    console.log(colors);
    paletteName = palette["nom"];
    name_input.value = paletteName;
    refresh_colors();
}

async function get_palette(id){
    try {
        const response = await fetch(api_url + `/palette_full/` + id, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data :", data);
        const palette = data;
        console.log("p1 : ", palette);
        return palette;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }

    
}

function add_color(color){
    colors.push([colors.length, color]);
    refresh_colors();
}

function refresh_colors(){
    colorTable.innerHTML = "";
    colors.forEach(function(color){
        add_square(color);
    });
}

function add_square(color) {
    const square = document.createElement("div");
    square.className = "square";
    square.style.backgroundColor = color[1];
    square.id = "square-" + color[0];
    colorTable.appendChild(square);
    square.onclick = (event) => {
        const allSquares = document.querySelectorAll('.square');
        allSquares.forEach((square) => {
            square.classList.remove('selected');
        });
        square.classList.add("selected");
        color_editor_div.style.display = "block";
    }
}

addButton.onclick = () => {
    add_color("#FFFFFF");

}

sliders.forEach((slider, index) => {
    slider.addEventListener('input', updateColor);
});

function updateColor() {
    const red = sliders[0].value;
    const green = sliders[1].value;
    const blue = sliders[2].value;
    colorBox.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;
}

selectButton.addEventListener("click", function() {
    selectColor();
});


function selectColor(){
    const selectedSquare = document.querySelector('.square.selected');
    var id = selectedSquare.id.split('-')[1];
    couleur = rgbToHex(colorBox.style.backgroundColor);
    colors[id][1] = couleur;
    refresh_colors();

    console.log("Vous avez choisi la couleur :", couleur);
    color_editor_div.style.display = "none";
    selectedSquare.classList.remove('selected');
    color_editor_div.style.display = "none";
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


deleteButton.onclick = () => {
    const selectedSquare = document.querySelector('.square.selected');
    
    if (selectedSquare && colors.length > 1) {
        const squareId = selectedSquare.id;
        delete_color(squareId.split('-')[1]);
        color_editor_div.style.display = "none";
    }
}

function delete_color(place){
    colors.splice(place, 1);
    for(var i=0; i<colors.length; i++){
        colors[i][0] = i;
    }
    refresh_colors();
}


saveButton.onclick = () => {
    
    switch(mode){
        case "test":
            console.log("debut sauvegarde");
            console.log(colors + "");
            break;
        case "new":
            create_new_palette();

            break;
        case "edit":
            save_palette();
            break;
        default:
            break;
    }
}

function save_palette(){
    console.log("id : ", id);
    couleurs_data = [];
    for (var i=0; i<colors.length; i++){
        couleurs_data[i] = { color: colors[i][1], position: i }
    }
    var data = {
        nom: name_input.value,
        couleurs: couleurs_data
    };
    

    console.log(JSON.stringify(data));
    // Configuration de la requête
    var requestOptions = {
        method: 'PUT',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            // Ajoutez d'autres en-têtes si nécessaire
        },
        body: JSON.stringify(data),
    };
    
    // Effectuer la requête
    fetch(api_url + "/palettes_full/" + id, requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
}

function create_new_palette(){
    couleurs_data = [];
    for (var i=0; i<colors.length; i++){
        couleurs_data[i] = { color: colors[i][1], position: i }
    }
    var data = {
        nom: name_input.value,
        couleurs: couleurs_data
    };
    

    console.log(JSON.stringify(data));
    // Configuration de la requête
    var requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            // Ajoutez d'autres en-têtes si nécessaire
        },
        body: JSON.stringify(data),
    };
    
    // Effectuer la requête
    fetch(api_url + "/palettes/", requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
}