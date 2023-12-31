//var api_url = "https://be.magimathicart.hirofine.fr";
var api_url = "http://localhost:8001";
const nav_deco = document.getElementById("nav-deco");
const nav_co = document.getElementById("nav-co");
var palettes = [];
const palette_div = document.getElementById("Palettes");
const projet_div = document.getElementById("Projets");
var is_connected = false;
const projet_name_input = document.getElementById("projet-name-input");
const projet_desc_input = document.getElementById("projet-desc-input");
const pixelart_name_input = document.getElementById("pixelart-name-input");
const pixelart_desc_input = document.getElementById("pixelart-desc-input");
var palette_name_input = document.getElementById("palette-name-input")
const colorTable = document.getElementById("palette-display");
const pixelArt_div = document.getElementById("pixelArt-div");

const dimX_input = document.getElementById("dimX-input");
const dimY_input = document.getElementById("dimY-input");
const valider_dimension_button = document.getElementById("validate-dimensions")
const save_button = document.getElementById("sauvegarder-button");

const ennonce_div = document.getElementById("ennonce-div");
const av_reponse_div = document.getElementById("available-ennonce");
const as_reponse_div = document.getElementById("associated-ennonce");

const exp_png_btn = document.getElementById("export-png-button");


var pixelart;
var palette;
var dimX;
var dimY;

var pixart = [];
var projet_id = 0;
var av_reponses = [];
var as_reponses = [];
var as_pa_reponses = [];
var asso_reponse_empl = [];

document.addEventListener("DOMContentLoaded", function () {
    //console.log("loaded page");
    fetch(api_url + `/verify-session/`,{
        method: 'GET',
        credentials: 'include'
    })
            .then(response => response.json())
            .then(data => {
               //console.log(data);
               //console.log(data.data);
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

exp_png_btn.addEventListener("click", async function(){
    var imageData = await load_png_export();

    console.log("imageData : ", imageData);
    const blob = new Blob([imageData], { type: 'image/png' });
    const imageUrl = URL.createObjectURL(blob);

    const imgElement = document.createElement('img');
    imgElement.src = imageUrl;

    // Ajouter l'image à un élément existant dans votre page HTML (par exemple, un élément avec l'ID "image-container")
    const imageContainer = document.getElementById('image-container');
    imageContainer.appendChild(imgElement);

    // Créer un lien invisible pour déclencher le téléchargement
    const downloadLink = document.createElement("a");
    downloadLink.href = imageUrl;
    downloadLink.download = "nom_de_votre_image.png"; // Nom du fichier à télécharger
    downloadLink.style.display = "none";

    // Ajouter le lien à la page et déclencher le téléchargement
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink); 
})

async function load_png_export(){
    try {    
        const response = await fetch(api_url + `/export_png/` + projet_id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const blob = await response.blob();

        return blob;
        //var data = await response.json();
        //return response;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

save_button.addEventListener("click", async function(){
    switch(mode){
        case "edit":
            save_projet();
            break;
        case "new":
            pr = await create_projet();
            window.location.href = "./editeur?mode=edit&id=" + pr["id"];
    }
    
})

palette_name_input.addEventListener("change", async function(){
    palette = await update_palette();
    //console.log(palette);
    display_palette(palette);
    display_pixelart(pixelart, palette);
    display_available_reponses(palette);
    display_associated_reponses(palette);
})

function resize_pixel_art(new_dimX, new_dimY){
    //console.log("resize to ", new_dimX, " by ", new_dimY);
    var new_pix = []
    for (var y=0; y<new_dimY; y++){
        new_pix[y] = [];
        for (var x=0; x<new_dimX; x++){
            if (x < dimX && y < dimY){
                new_pix[y][x] = pixart[y][x];
            }else{
                new_pix[y][x] = ["#ffffff", -1];
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
            projet_id = params.get("id");
            //mode new
            if(mode == "new"){
                palette = await update_palette_selector();
                create_new_projet(palette);
            }
            if(mode == "edit"){
                a = await update_palette_selector();
                projet = await retrieve_user_projets(projet_id);
                palette = await retrieve_palette_projet(projet.id);
                av_reponses = await retrieve_user_reponses();
                as_reponses = await retrieve_asso_projet_reponse(projet_id);
                asso_reponse_empl = await retrieve_asso_projet_palette_reponse_from_projet(projet_id);
                // remove ids for easier saving later on
                asso_reponse_empl.forEach((asso, i) => {
                    asso_reponse_empl[i] = {"reponse_id": asso["reponse_id"],
                                            "position": asso["position"],
                                            "projet_id": asso["projet_id"],
                                            "palette_id": asso["palette_id"]};
                })
                display_existing(projet);
                
            }
            break;
        case false:
            nav_deco.style.display = "block";
            nav_co.style.display = "none";
            //console.log("case false");
            break;
        default:
            nav_deco.style.display = "block";
            nav_co.style.display = "none";
            //console.log("case default");
            break;
       }
}

async function create_new_projet(palette){
    projet_name_input.value = "Nouveau Projet";
    projet_desc_input.value = "Nouveau Projet";

    pixelart_name_input.value = "Nouveau Dessin";
    pixelart_desc_input.value = "Dessin du projet ...";

    dimX = 20;
    dimY = 20;
    dimX_input.value = dimX;
    dimY_input.value = dimY;

    palette_name_input.value = palette["id"];
    p_full = await retrieve_palette_id(palette["id"])
    //console.log(p_full);
    display_palette(p_full);

    var new_pix = [];
    for (var y=0; y<dimY; y++){
        new_pix[y] = [];
        for (var x=0; x<dimX; x++){
            new_pix[y][x] = ["#ffffff", -1];
        }
    }
    pixart = new_pix;
    resize_pixel_art(dimX, dimY);
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
    return palettes[0];
}

async function display_existing(projet){
    //console.log(projet);
    projet_name_input.value = projet["nom"];
    projet_desc_input.value = projet["description"];
    
    //console.log(palette);
    palette_name_input.value = palette["id"];
    display_palette(palette);
    //console.log(palette);
    pixelart = await retrieve_pixel_art_projet(projet.id);
    //console.log(pixelart);
    display_pixelart(pixelart, palette);
    display_available_reponses(palette);
    display_associated_reponses(palette);
}

function display_available_reponses(palette){
    av_reponse_div.innerHTML = "";
    console.log("palette : ", palette);
    console.log("av_rep  : ", av_reponses);
    console.log("as_rep : ", as_reponses);
    console.log("asso_rep_empl : ", asso_reponse_empl);
    av_reponses.forEach((rep) => {
        const div_av_rep = document.createElement("div");
        const lab_av_rep = document.createElement("label");
        const che_av_rep = document.createElement("input");
        che_av_rep.setAttribute("type", "checkbox");
        lab_av_rep.innerHTML = rep["nom"];
        const associa = as_reponses.some((asRep) => asRep["id"] === rep["id"]);
        var test = false;
        if (associa){
            test = asso_reponse_empl.some((asRep) => asRep["reponse_id"] === rep["id"] && asRep["palette_id"] === palette["id"]);
        }
        console.log(rep);
        console.log("found association : ", associa);
        if (test){
            che_av_rep.checked = true;
        }else{
            che_av_rep.checked = false;
        }

        che_av_rep.onchange = (event) => {
            //console.log("selection changed");
           // var  index = av_reponse_div.indexOf(che_av_rep);
            if(!che_av_rep.checked){
                //console.log(rep);
                var index = av_reponses.indexOf(rep);
                //console.log("index : ", index);
                var index_ass = asso_reponse_empl.indexOf(asso_reponse_empl.find((asso) => asso["palette_id"] === palette["id"] && asso["reponse_id"] === rep["id"]));
                as_reponses.splice(index, 1);
                asso_reponse_empl.splice(index_ass,1);
                
            }
            if(che_av_rep.checked){
                var index = av_reponses.indexOf(rep);
                if (!as_reponses.find((as_rep) => as_rep["id"] === rep["id"])){
                    as_reponses.splice(index, 0, rep);
                }
                asso_reponse_empl.splice(index, 0, {"projet_id": projet["id"],
                                                    "reponse_id" : rep["id"],
                                                    "palette_id" : palette["id"],
                                                    "position" : -1});
            }
            display_associated_reponses(palette);
        }

        div_av_rep.appendChild(lab_av_rep);
        div_av_rep.appendChild(che_av_rep);
        av_reponse_div.appendChild(div_av_rep); 
    });
}

function display_associated_reponses(palette){
    as_reponse_div.innerHTML = "";
    console.log("as_rep  =", as_reponses);
    console.log("palette : ", palette);
    console.log("asso_empl : ", asso_reponse_empl);
    var as_pal_asso = as_reponses.filter(element => {
        asso_pal = asso_reponse_empl.find((asso) => (asso["reponse_id"] === element["id"] && asso["palette_id"] === palette["id"]));
        if (asso_pal == null){
            return false;
        }
        console.log("test : ", asso_pal["palette_id"] , palette["id"]);
        return asso_pal["palette_id"] === palette["id"]; 
    })
    console.log(as_pal_asso);
    as_pal_asso.forEach((rep, i) => {
        const div_as_rep = document.createElement("div");
        const lab_as_rep = document.createElement("label");
        const color_div = document.createElement("div");
        lab_as_rep.innerHTML = rep["nom"];
        //console.log("rep en cours: ", rep);
        var emplacement = asso_reponse_empl.find((asso) => asso["reponse_id"] === rep["id"] && asso["palette_id"] === palette["id"]);
        var empl_index = asso_reponse_empl.indexOf(emplacement);
        //console.log("pos : ", emplacement);
        var color = "#FFFFFF";
        if (emplacement != null){
            var position = emplacement["position"];
            if(position >= 0){
                color = palette["couleurs"][position]["color"];
            }
            
        }
        color_div.style.backgroundColor = color;
        color_div.className = "square";
        color_div.onclick = (event) => {
            const allPaletteDisplay = document.querySelectorAll(".palette_display");
            //console.log("allpale : ", allPaletteDisplay);
            allPaletteDisplay.forEach((pal) => {
                pal.remove();
            });
            open_palette_selector(rep, color_div, div_as_rep, empl_index, palette);
        }
        div_as_rep.appendChild(lab_as_rep);
        div_as_rep.appendChild(color_div);
        as_reponse_div.appendChild(div_as_rep);
    });
}

function open_palette_selector(rep, color_div, div_as_rep, indice, palette){
    //console.log("truc, ", div_as_rep);
    const palette_div = document.createElement("div");
    palette_div.className = "palette_display";
    colors_data = palette["couleurs"];
    colors = [];
    colors_data.forEach((col, i) => {
        colors[i] = [col.position, col.color]; 
    })
    //console.log(colors);
    paletteName = palette["nom"];
    palette_div.innerHTML = "";
    colors.forEach(function(color, i){
        const square = document.createElement("div");
        square.className = "square";
        if (asso_reponse_empl[indice] != null && i == asso_reponse_empl[indice]["position"]){
            square.classList.add("selected");
        }
        square.style.backgroundColor = color[1];
        square.id = "square-" + color[0];
        palette_div.appendChild(square);
        square.onclick = (event) => {
            if (asso_reponse_empl[indice] == null){
                asso_reponse_empl[indice] = {"reponse_id": rep["id"],
                                                "position": 0,
                                                "projet_id": parseInt(projet_id),
                                                "palette_id": palette["id"]};
            }
            asso_reponse_empl[indice]["position"] = parseInt(square.id.split("-")[1]);
            color_div.style.backgroundColor = colors[square.id.split("-")[1]][1];
            const allPaletteDisplay = document.querySelectorAll(".palette_display");
            //console.log("allpale : ", allPaletteDisplay);
            allPaletteDisplay.forEach((pal) => {
                pal.remove();
            });
        }
    });
    div_as_rep.appendChild(palette_div);
}

function load_pixel_art(pixelart, palette){
    dimX = pixelart["dimensionsX"];
    dimY = pixelart["dimensionsY"];

    dimX_input.value = dimX;
    dimY_input.value = dimY;
    pixelart_name_input.value = pixelart["nom"];
    pixelart_desc_input.value = pixelart["description"];

    //console.log(dimX, dimY);
    pixels = JSON.parse(pixelart["art"])["pixels"];
    pixart = [];
    //console.log(pixels);
    for (var y=0; y<dimY; y++){
        pixart[y] = [];
        const line = document.createElement("div")
        
        for (var x=0; x<dimX; x++){
            indice = pixels[x * dimY + y][2];
            couleur = "#ffffff";
            if (indice != -1){
                couleur = palette["couleurs"][indice].color;
            }
            
            pixart[y][x] = [couleur, indice];
        }
    }
}

function display_pixelart(pixelart, palette){
    
    art = JSON.parse(pixelart["art"]);
    format = art["format"];
    //console.log(format);
    load_pixel_art(pixelart, palette);
    if (format == "square"){
        display_pixelart_square()
    }
}

function display_pixelart_square(){
    dimX = dimX_input.value;
    dimY = dimY_input.value;
    pixelArt_div.innerHTML = "";
    pixelArt_div.style.display = "flex";
    pixelArt_div.style.flexDirection = "column";
    for (var y=0; y<dimY; y++){
        const line = document.createElement("div")
        line.style.border = "0";
        line.style.padding = "0";
        line.style.fontSize = "0px";
        for (var x=0; x<dimX; x++){
            draw_pixel(pixart[y][x][0],x,y, line);

        }
        pixelArt_div.appendChild(line);
    }
    //console.log(pixart);
}

function draw_pixel(color,x,y, line) {
    
    const pix = document.createElement("div");
    pix.className = "pixel";
    pix.style.backgroundColor = color;
    pix.id = "pixel-" + x + "-" + y;
    line.appendChild(pix);
    pix.onmousemove = (event) => {
        //pix.style.backgroundColor = 0;
        //console.log("mousemove");
        if(event.buttons === 1){
            //console.log("clicked ", pix.id, " my color is ", pix.style.backgroundColor);
            change_color(x,y, pix);
        }
    }
    pix.onclick = (event) => {
        change_color(x,y, pix);
    }
}

function change_color(x,y, pix){
    color = document.querySelector('.square.selected');
    pix.style.backgroundColor = color.style.backgroundColor;
    params = pix.id.split("-");
    x = params[1];
    y = params[2];
    pixart[y][x][0] = color.style.backgroundColor;
    pixart[y][x][1] = color.id.split("-")[1];
    //console.log("change color ", pix, color);
}

function display_palette(palette){
    colors_data = palette["couleurs"];
    colors = [];
    colors_data.forEach((col, i) => {
        colors[i] = [col.position, col.color]; 
    })
    //console.log(colors);
    paletteName = palette["nom"];
    refresh_colors();
}

function refresh_colors(){
    colorTable.innerHTML = "";
    colors.forEach(function(color, i){
        add_square(color, i);
    });
}

function add_square(color, i) {
    const square = document.createElement("div");
    square.className = "square";
    if (i == 0){square.classList.add("selected");}
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

async function update_palette(){
    try {
        const id = palette_name_input.value;
        const response = await fetch(api_url + `/palette_full/` + id, {
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
        const response = await fetch(api_url + `/palette_full_from_projet/` + projet_id, {
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

async function retrieve_palette_user(){
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

async function retrieve_palette_id(palette_id){
    try {
        const response = await fetch(api_url + '/palette_full/' + palette_id, {
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
        const response = await fetch(api_url + `/pixelart_from_projet/` + projet_id, {
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

async function create_projet(){
    var data = {
        nom: projet_name_input.value,
        description: projet_desc_input.value
    };
    

    //console.log(JSON.stringify(data));
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
    try{
        response = await fetch(api_url + "/projets/", requestOptions) ;
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        projet_id = data.id;
    
        a = await create_projet_palette();
        b = await create_pixel_art();
        c = await create_asso_projet_pixelart(projet_id, b["id"]);
        return data;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
    
    
}

async function save_projet(){
    
    var data = {
        nom: projet_name_input.value,
        description: projet_desc_input.value
    };
    

    //console.log(JSON.stringify(data));
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
    fetch(api_url + "/projets/" + projet_id, requestOptions)
        .then(response => response.json())
        .then(data => {
            //console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
    
    save_palette();
    save_pixel_art();
    save_association();
}

async function create_projet_palette(){
    var data = {
        projet_id: projet_id,
        palette_id: palette_name_input.value
    };
    

    //console.log(JSON.stringify(data));
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
    try{
        response = await fetch(api_url + "/assoprojetpalette/", requestOptions) ;
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

async function save_palette(){
    var data = {
        projet_id: projet_id,
        palette_id: palette_name_input.value
    };
    

    //console.log(JSON.stringify(data));
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
    fetch(api_url + "/assoprojetpalette_from_projet/" + projet_id, requestOptions)
        .then(response => response.json())
        .then(data => {
            //console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
}

async function save_association(){
    //console.log("----------------------------------", as_reponses);

    var data = {
        assos : asso_reponse_empl
    }
    console.log(JSON.stringify(data));
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
    fetch(api_url + "/assoprojetpalettereponse_collec/", requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
    //console.log(data);
}

async function create_pixel_art(){
    var data = {
        nom: pixelart_name_input.value,
        description: pixelart_desc_input.value,
        dimensionsX: dimX,
        dimensionsY: dimY,
        art: pixart_to_string(),
    };
    

    //console.log(JSON.stringify(data));
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
    try{
        response = await fetch(api_url + "/pixelarts/", requestOptions) ;
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

async function save_pixel_art(){
    var data = {
        nom: pixelart_name_input.value,
        description: pixelart_desc_input.value,
        dimensionsX: dimX,
        dimensionsY: dimY,
        art: pixart_to_string(),
    };
    

    //console.log(JSON.stringify(data));
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
    fetch(api_url + "/pixelarts_from_projet/" + projet_id, requestOptions)
        .then(response => response.json())
        .then(data => {
            //console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });
}

async function create_asso_projet_pixelart(proj_id, pixart_id){
    var data = {
        projet_id: proj_id,
        pixelart_id: pixart_id
    };
    

    //console.log(JSON.stringify(data));
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
    try{
        response = await fetch(api_url + "/assoprojetpixelart/", requestOptions) ;
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

function pixart_to_string(){
    pix = [];
    for(var y=0; y<dimY; y++){
    
        for (var x=0; x<dimX; x++){
            pix[x*dimY + y] = [x, y, pixart[y][x][1]];
        }
    }
    data = {
        format:"square",
        pixels: pix
    }

    return JSON.stringify(data);
}

function load_asso_projet_palette_reponse(){
    //console.log("thingy");
}


async function retrieve_asso_projet_reponse(projet_id){
    try {
        const response = await fetch(api_url + `/reponses_from_projet/` + projet_id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data["reponses"];
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function retrieve_user_reponses(){
    try {
        const response = await fetch(api_url + `/reponse_from_user/`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data["reponses"];
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function retrieve_asso_projet_palette_reponse_from_projet(projet_id){
    try {
        const response = await fetch(api_url + `/assoprojetpalettereponse_from_projet/` + projet_id, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data["assos"];
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

