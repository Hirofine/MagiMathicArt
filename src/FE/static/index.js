//var api_url = "https://be.magimathicart.hirofine.fr"
var api_url = "http://localhost:8001";
nav_deco = document.getElementById("nav-deco");
nav_co = document.getElementById("nav-co");

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

function update_page(is_connected){
    switch(is_connected){
        case true:
            nav_deco.style.display = "none";
            nav_co.style.display = "block";
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