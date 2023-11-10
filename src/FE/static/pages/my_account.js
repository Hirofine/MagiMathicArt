var api_url = "https://be.magimathicart.hirofine.fr"
nav_deco = document.getElementById("nav-deco");
nav_co = document.getElementById("nav-co");
var palettes = [];
const palette_div = document.getElementById("Palettes");
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
            const palettes = await retrieve_user_palettes();
            palettes.forEach(function(palette){
                display_palette(palette);
            });
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

function display_palette(palette){
    var palette_button = document.createElement("button");
    palette_button.innerHTML = palette.nom;
    palette_button.addEventListener("click", function(){
        window.location.href = "./palette_editor?mode=edit&id=" + palette.id;
    })
    palette_div.appendChild(palette_button)
    console.log(palette);
}