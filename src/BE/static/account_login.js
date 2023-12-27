//var api_url = "https://be.magimathicart.hirofine.fr"
var api_url = "http://localhost:8001";

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("name-input");
    const passwordInput = document.getElementById("password-input");
    const submit_button = document.getElementById("submit-button");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêchez la soumission du formulaire par défaut

        // Récupérez les données du formulaire
        const pseudo = usernameInput.value;
        const passw = passwordInput.value;

     
        const userData = {
            pseudo: pseudo,
            passw: passw
        };

        fetch(api_url + "/login/", {
            method: "POST",
            body: JSON.stringify(userData),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data["message"] == "Connexion réussie"){
                window.location.href = "https://magimathicart.hirofine.fr";
            }else{
                console.log("c'est la merder");
            }
            
            
        })
        .catch(error => {
            console.log(error)
            // Gérez les erreurs (par exemple, problème de connectivité avec le serveur)
        });
    
    });
});