var api_url = "https://be.magimathicart.hirofine.fr"
const nav_deco = document.getElementById("nav-deco");
const nav_co = document.getElementById("nav-co");

const nom_input = document.getElementById("nom-input");
const description_input = document.getElementById("description-input");
const ennonce_input = document.getElementById("ennonce-input");
const genre_select = document.getElementById("genre-select");

const add_perso_div = document.getElementById("add-perso-div");
const add_quest_field = document.getElementById("add-quest-field");
const add_quest_button = document.getElementById("add-quest-button");
const quest_div = document.getElementById("quest-div");

const add_fonct_div = document.getElementById("add-fonct-div");
const fonct_select = document.getElementById("fonction-select")

const enregistrer_button = document.getElementById("enregistrer-button");

var mode = "new";
var id = 0;

var reponse = {};
var questions = [];

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
               update_page(data.data)
            })
            .catch(error => {
                console.error("Erreur lors de la vérification du pseudo : " + error);
            });

});

genre_select.addEventListener("change", function (){
    console.log("change genre to ", genre_select.value);
    switch(genre_select.value){
        case "perso":
        default:
            add_perso_div.style.display = "block";
            add_fonct_div.style.display = "none";
            break;
        case "fonct":
            add_perso_div.style.display = "none";
            add_fonct_div.style.display = "block";
            break;
        
    }
});

add_quest_button.addEventListener("click", function(){
    add_question(add_quest_field.value);
    add_quest_field.value = "";
});

enregistrer_button.addEventListener("click", async function(){
    switch(mode){
        case "edit":
            a = await save_reponse();
            break;
        case "new":
            id = await create_reponse();
            window.location.href = "./reponse_editeur?mode=edit&id=" + id;
            break;
        default:
            break;
    }
   
});

function update_page(is_connected){
    switch(is_connected){
        case true:
            nav_deco.style.display = "none";
            nav_co.style.display = "block";

            handle_params();

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

async function handle_params(){
    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);
    var m = params.get("mode");
    var i = params.get("id");
    mode = m!=null?m:"new"; // defaults to "new"
    id = i!=null?i:0;       // defaults to 0

    switch(mode){
        case "edit":
            a = await load_reponse();
            if (a == null){
                console.log("erreur ?")
            }
            display_reponse();
        
            break;
        case "new":


            break;
        default:
            break;
    }

}

async function load_reponse(){
    try {
        const response = await fetch(api_url + `/reponses/` + id, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data :", data);
        reponse = data;
        return reponse;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
}

function display_reponse(){
    nom_input.value = reponse["nom"];
    description_input.value = reponse["description"];
    ennonce_input.value = reponse["ennonce"];
    genre_select.value = reponse["genre"];
    switch (reponse["genre"]){
        case "perso":
            questions = JSON.parse(reponse["fonction"]);
            draw_questions();
            break;
        case "fonct":
            break;
        default:
            break;
    }
    
}

function add_question(quest){
    questions.push(quest);
    draw_question(questions.length - 1)
}

function draw_question(id){
    const question_div = document.createElement("div");
    const question_text = document.createElement("input");
    question_text.value = questions[id];

    question_text.addEventListener("blur", function(){
        const parentDiv = remove_button.parentNode;
        const index = Array.from(parentDiv.parentNode.children).indexOf(parentDiv);
        questions[index] = question_text.value;
    });
    
    const remove_button = document.createElement("button");
    remove_button.innerHTML = "X";
    remove_button.addEventListener("click", function(){
        const parentDiv = remove_button.parentNode;
        const index = Array.from(parentDiv.parentNode.children).indexOf(parentDiv); 
        questions.splice(index, 1);
        parentDiv.remove(); 
    })
    question_div.appendChild(question_text);
    question_div.appendChild(remove_button);

    quest_div.appendChild(question_div);
    
}

function draw_questions(){
    quest_div.innerHTML = "";
    for (var i=0;i<questions.length; i++){
        draw_question(i);
    }
}

async function save_reponse(){
    data = {
        nom: nom_input.value,
        description: description_input.value,
        ennonce: ennonce_input.value,
        genre: genre_select.value,
        fonction: JSON.stringify(questions)
    }

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
    fetch(api_url + "/reponses/" + id, requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log('Réponse de l\'API:', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête:', error);
        });

}

async function create_reponse(){
    data = {
        nom: nom_input.value,
        description: description_input.value,
        ennonce: ennonce_input.value,
        genre: genre_select.value,
        fonction: JSON.stringify(questions)
    }
        
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
        
    try {
        const response = await fetch(api_url + "/reponses/", requestOptions)
    
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
            
        const data = await response.json()
        console.log('Réponse de l\'API:', data);
        id = data.id;
        return data.id;
    } catch (error) {
        console.error("Erreur lors de la vérification du pseudo : " + error);
        return []; // Retourne une liste vide en cas d'erreur
    }
    
        // Effectuer la requête
        
    
}