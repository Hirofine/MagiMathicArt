var api_url = "https://be.magimathicart.hirofine.fr"
nav_deco = document.getElementById("nav-deco");
nav_co = document.getElementById("nav-co");
var palettes = [];
const palette_div = document.getElementById("Palettes");
const projet_div = document.getElementById("Projets");
var is_connected = false;
const projet_name_input = document.getElementById("projet-name_input");
const palette_name_input = document.getElementById("palette-name-input")
const colorTable = document.getElementById("palette-display");
const pixelArt = document.getElementById("pixelArt-div");

document.addEventListener("DOMContentLoaded", function () {
    console.log("loaded page");
    fetch(api_url + `/verify-session/`,{
        method: 'GET',
        credentials: 'include'
    })
            .then(response => response.json())
            .then(data => {
               console.log(data);
               console.log(data.data);
               is_connected = data.data;
               update_page(is_connected)
            })
            .catch(error => {
                console.error("Erreur lors de la vérification du pseudo : " + error);
            });
});

async function update_page(is_connected){
    switch(is_connected){
        case true:
            nav_deco.style.display = "none";
            nav_co.style.display = "block";
            var queryString = window.location.search;
            var params = new URLSearchParams(queryString);

            mode = params.get("mode");
            id = params.get("id");
            //mode new
            if(mode == "new"){
                
            }
            if(mode == "edit"){
                projet = await retrieve_user_projets(id);
                display_existing(projet);
                
            }
            break;
        case false:
            nav_deco.style.display = "block";
            nav_co.style.display = "none";
            console.log("case false");
            break;
        default:
            nav_deco.style.display = "block";
            nav_co.style.display = "none";
            console.log("case default");
            break;
       }
}

async function display_existing(projet){
    console.log(projet);
    projet_name_input.value = projet["nom"];
    palette = await retrieve_palette_projet(projet.id);
    display_palette(palette);
    console.log(palette);
    pixelart = await retrieve_pixel_art_projet(projet.id);
    console.log(pixelart);
    display_pixelart(pixelart, palette);
}

function display_pixelart(pixelart, palette){
    art = JSON.parse(pixelart["art"]);
    format = art["format"];
    console.log(format);
    if (format == "square"){
        display_pixelart_square(pixelart, palette)
    }
}

function display_pixelart_square(pixelart, palette){
    dimX = pixelart["dimensionsX"];
    dimY = pixelart["dimensionsY"];
    console.log(dimX, dimY);
    pixels = JSON.parse(pixelart["art"])["pixels"];
    var pixart = [];
    console.log(pixels);
    for (var x=0; x<dimX; x++){
        pixart[x] = [];
        const line = document.createElement("div")
        
        for (var y=0; y<dimY; y++){
            pixart[x][y] = palette["couleurs"][pixels[x * dimY + y][2]].color;
            draw_pixel(pixart[x][y],x,y, line);
        }
        pixelArt.appendChild(line);
    }
    console.log(pixart);
}

function draw_pixel(color,x,y, line) {
    
    const pix = document.createElement("div");
    pix.className = "pixel";
    pix.style.backgroundColor = color;
    pix.id = "pixel-" + x + "-" + y;
    line.appendChild(pix);
    pix.onclick = (event) => {
        //pix.style.backgroundColor = 0;
        console.log("clicked ", pix.id, " my color is ", pix.style.backgroundColor);
    }
}

function display_palette(palette){
    colors_data = palette["couleurs"];
    colors = [];
    colors_data.forEach((col, i) => {
        colors[i] = [col.position, col.color]; 
    })
    console.log(colors);
    paletteName = palette["nom"];
    palette_name_input.value = paletteName;
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
    }
}


async function retrieve_user_projets(id){
    try {
        const response = await fetch(api_url + `/projets/` + id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function retrieve_palette_projet(projet_id){
    try {
        const response = await fetch(api_url + `/palette_full_from_projet/` + id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function retrieve_pixel_art_projet(projet_id){
    try {
        const response = await fetch(api_url + `/pixelart_from_projet/` + id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}