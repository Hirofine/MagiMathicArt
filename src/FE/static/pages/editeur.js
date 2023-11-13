var api_url = "https://be.magimathicart.hirofine.fr"
nav_deco = document.getElementById("nav-deco");
nav_co = document.getElementById("nav-co");
var palettes = [];
const palette_div = document.getElementById("Palettes");
const projet_div = document.getElementById("Projets");
var is_connected = false;
const projet_name_input = document.getElementById("projet-name-input");
var palette_name_input = document.getElementById("palette-name-input")
const colorTable = document.getElementById("palette-display");
const pixelArt_div = document.getElementById("pixelArt-div");

const dimX_input = document.getElementById("dimX-input");
const dimY_input = document.getElementById("dimY-input");
const valider_dimension_button = document.getElementById("validate-dimensions")
const save_button = document.getElementById("sauvegarder-button");

var dimX;
var dimY;

var pixart = [];

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


valider_dimension_button.addEventListener("click", function(){
    resize_pixel_art(dimX_input.value, dimY_input.value);
    
});

save_button.addEventListener("click", function(){
    save_projet();
})

function resize_pixel_art(new_dimX, new_dimY){
    console.log("resize to ", new_dimX, " by ", new_dimY);
    var new_pix = []
    for (var x=0; x<new_dimX; x++){
        new_pix[x] = [];
        for (var y=0; y<new_dimY; y++){
            if (x < dimX && y < dimY){
                new_pix[x][y] = pixart[x][y];
            }else{
                new_pix[x][y] = "#ffffff";
            }
            
        }
    }
    pixart = new_pix;
    display_pixelart_square();
}

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
                a = await update_palette_selector();
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

async function update_palette_selector(){
    pals = await retrieve_palette_user();
    palettes = pals["palettes"];
    palettes.forEach(function(palette){
        var opt = document.createElement("option");
        opt.value = palette["id"];
        opt.innerHTML = palette["nom"];
        palette_name_input.appendChild(opt);
    });
    return 1;
}

async function display_existing(projet){
    console.log(projet);
    projet_name_input.value = projet["nom"];
    var palette = await retrieve_palette_projet(projet.id);
    console.log(palette);
    palette_name_input.value = palette["id"];
    display_palette(palette);
    console.log(palette);
    var pixelart = await retrieve_pixel_art_projet(projet.id);
    console.log(pixelart);
    display_pixelart(pixelart, palette);
}

function load_pixel_art(pixelart, palette){
    dimX = pixelart["dimensionsX"];
    dimY = pixelart["dimensionsY"];

    dimX_input.value = dimX;
    dimY_input.value = dimY;

    console.log(dimX, dimY);
    pixels = JSON.parse(pixelart["art"])["pixels"];
    pixart = [];
    console.log(pixels);
    for (var x=0; x<dimX; x++){
        pixart[x] = [];
        const line = document.createElement("div")
        
        for (var y=0; y<dimY; y++){
            pixart[x][y] = palette["couleurs"][pixels[x * dimY + y][2]].color;
        }
    }
}

function display_pixelart(pixelart, palette){
    
    art = JSON.parse(pixelart["art"]);
    format = art["format"];
    console.log(format);
    load_pixel_art(pixelart, palette);
    if (format == "square"){
        display_pixelart_square()
    }
}

function display_pixelart_square(){
    dimX = dimX_input.value;
    dimY = dimY_input.value;
    pixelArt_div.innerHTML = "";
    for (var x=0; x<dimX; x++){
        const line = document.createElement("div")
        for (var y=0; y<dimY; y++){
            draw_pixel(pixart[x][y],x,y, line);
        }
        pixelArt_div.appendChild(line);
    }
    console.log(pixart);
}

function draw_pixel(color,x,y, line) {
    
    const pix = document.createElement("div");
    pix.className = "pixel";
    pix.style.backgroundColor = color;
    pix.id = "pixel-" + x + "-" + y;
    line.appendChild(pix);
    pix.onmousemove = (event) => {
        //pix.style.backgroundColor = 0;
        console.log("mousemove");
        if(event.buttons === 1){
            console.log("clicked ", pix.id, " my color is ", pix.style.backgroundColor);
            change_color(x,y, pix);
        }
    }
}

function change_color(x,y, pix){
    color = document.querySelector('.square.selected');
    pix.style.backgroundColor = color.style.backgroundColor;
    console.log("change color ", pix, color);
}

function display_palette(palette){
    colors_data = palette["couleurs"];
    colors = [];
    colors_data.forEach((col, i) => {
        colors[i] = [col.position, col.color]; 
    })
    console.log(colors);
    paletteName = palette["nom"];
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

async function retrieve_palette_user(projet_id){
    try {
        const response = await fetch(api_url + '/palette_from_user/', {
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

function save_projet(){

}