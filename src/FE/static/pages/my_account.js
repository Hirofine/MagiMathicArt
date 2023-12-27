//var api_url = "https://be.magimathicart.hirofine.fr"
var api_url = "http://localhost:8001";
nav_deco = document.getElementById("nav-deco");
nav_co = document.getElementById("nav-co");
var palettes = [];
const palette_div = document.getElementById("Palettes");
const projet_div = document.getElementById("Projets");
const reponse_div = document.getElementById("Ennonces")
var is_connected = false;
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
            display_pals();
            display_projs();
            display_reps();
            console.log("case true");
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

async function retrieve_user_palettes() {
    try {
        const response = await fetch(api_url + `/palette_from_user/`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data :", data);
        const palette_list = data["palettes"];
        console.log("p1 : ", palette_list);
        return palette_list;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function retrieve_user_projets() {
    try {
        const response = await fetch(api_url + `/projet_from_user/`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data :", data);
        const projet_list = data["projets"];
        console.log("p1 : ", projet_list);
        return projet_list;
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
        console.log("data :", data);
        const reponse_list = data["reponses"];
        
        return reponse_list;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

async function display_pals(){
    const palettes = await retrieve_user_palettes();
    palettes.forEach(function(palette){
        display_palette(palette);
    });
    var new_palette_button = document.createElement("button");
    new_palette_button.innerHTML = "Nouvelle Palette";
    new_palette_button.addEventListener("click", function(){
        window.location.href = "./palette_editor?mode=new&id=0";
    })
    palette_div.appendChild(new_palette_button)
}

async function display_projs(){
    const projets = await retrieve_user_projets();
    projets.forEach(function(projet){
        display_projet(projet);
    });
    var new_projet_button = document.createElement("button");
    new_projet_button.innerHTML = "Nouveau Projet";
    new_projet_button.addEventListener("click", function(){
        window.location.href = "./editeur?mode=new&id=0";
    })
    projet_div.appendChild(new_projet_button)
}

async function display_reps(){
    const reponses = await retrieve_user_reponses();
    reponses.forEach(function(reponse){
        display_reponse(reponse);
    });
    var new_reponse_button = document.createElement("button");
    new_reponse_button.innerHTML = "Nouvel Énnoncé";
    new_reponse_button.addEventListener("click", function(){
        window.location.href = "./reponse_editeur?mode=new&id=0";
    })
    reponse_div.appendChild(new_reponse_button)
}

function display_palette(palette){
    var palette_button = document.createElement("button");
    palette_button.innerHTML = palette.nom;
    palette_button.addEventListener("click", function(){
        window.location.href = "./palette_editor?mode=edit&id=" + palette.id;
    })
    palette_div.appendChild(palette_button)
    console.log(palette);
}

function display_projet(projet){
    var projet_button = document.createElement("button");
    projet_button.innerHTML = projet.nom;
    projet_button.addEventListener("click", function(){
        window.location.href = "./editeur?mode=edit&id=" + projet.id;
    })
    projet_div.appendChild(projet_button)
    console.log(projet);
}

function display_reponse(reponse){
    var reponse_button = document.createElement("button");
    reponse_button.innerHTML = reponse.nom;
    reponse_button.addEventListener("click", function(){
        window.location.href = "./reponse_editeur?mode=edit&id=" + reponse.id;
    })
    reponse_div.appendChild(reponse_button)
    console.log(reponse);
}