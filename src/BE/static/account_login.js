var api_url = "https://be.magimathicart.hirofine.fr"

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêcher la soumission du formulaire par défaut

        // Récupérer les valeurs du pseudo et du mot de passe
        const pseudo = document.getElementById("name-input").value;
        const password = document.getElementById("password-input").value;

        const userData = {
            pseudo: pseudo,
            passw: password
        };

        // Envoyer une requête au serveur pour vérifier l'authentification
        fetch(api_url + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Rediriger l'utilisateur vers la page de tableau de bord ou une autre page
                    window.location.href = "/";
                } else {
                    // Afficher un message d'erreur
                    alert("Échec de la connexion. Veuillez vérifier vos informations.");
                }
            })
            .catch(error => {
                console.error("Erreur de connexion : " + error);
            });
    });
});