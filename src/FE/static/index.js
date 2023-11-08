var api_url = "https://be.magimathicart.hirofine.fr"

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
            })
            .catch(error => {
                console.error("Erreur lors de la vérification du pseudo : " + error);
            });

});