var api_url = "https://be.magimathicart.hirofine.fr"

document.addEventListener("DOMContentLoaded", function () {
    // Sélectionnez les éléments du formulaire
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("name-input");
    const passwordInput = document.getElementById("password-input");
    const confirmPasswordInput = document.getElementById("re-password-input");
    const submit_button = document.getElementById("submit-button");
    const availabilityMessage = document.getElementById("availability-message");


    usernameInput.addEventListener("blur", function () {
        const pseudo = usernameInput.value;

        // Envoyer une requête au serveur pour vérifier la disponibilité du pseudo
        fetch(api_url + `/check-pseudo/?pseudo=${pseudo}`)
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    availabilityMessage.textContent = "Pseudo disponible";
                    availabilityMessage.style.color = "green";
                    submit_button.disabled = false;
                } else {
                    availabilityMessage.textContent = "Pseudo déjà pris";
                    availabilityMessage.style.color = "red";
                    submit_button.disabled = true;
                }
            })
            .catch(error => {
                console.error("Erreur lors de la vérification du pseudo : " + error);
            });
    });

    // Ajoutez un écouteur d'événement pour la soumission du formulaire
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêchez la soumission du formulaire par défaut

        // Récupérez les données du formulaire
        const pseudo = usernameInput.value;
        const passw = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Effectuez des vérifications côté client (par exemple, vérification de mots de passe)
        if (passw !== confirmPassword) {
            // Les mots de passe ne correspondent pas, affichez un message d'erreur
            errorContainer.innerText = "Les mots de passe ne correspondent pas.";
        } else {
        // Créez une requête HTTP POST
        
        const userData = {
            pseudo: pseudo,
            passw: passw
        };

        fetch(api_url + "/register/", {
            method: "POST",
            body: JSON.stringify(userData),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            // Gérez la réponse du serveur backend (par exemple, affichez un message de réussite ou d'erreur)
            // Utilisation :
            const sessionToken = getCookie('session');

            if (sessionToken) {
                // Le cookie session_token existe, vous pouvez effectuer des opérations avec le token.
                console.log(`Session Token: ${sessionToken}`);
            } else {
                // Le cookie session_token n'existe pas.
                console.log("Le cookie de session n'a pas été trouvé.");
            }
        })
        .catch(error => {
            console.log(error)
            // Gérez les erreurs (par exemple, problème de connectivité avec le serveur)
        });
    }
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

