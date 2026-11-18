
document.addEventListener("DOMContentLoaded", () => {

    const estado = document.getElementById("estado-sistema");

    // Consultar el estado del backend
    fetch("/api/estado")

        .then(response => {

            if (!response.ok) {
                throw new Error("Error de conexión");
            }

            return response.json();

        })

        .then(data => {

            estado.textContent =
                "Sistema conectado correctamente: " +
                data.proyecto;

            console.log("Respuesta del servidor:", data);

        })

        .catch(error => {

            estado.textContent =
                "No se pudo conectar con el servidor.";

            console.error("Error:", error);

        });

});


document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("materials-container");
    const addButton = document.getElementById("add-material");

    if (!container || !addButton) {
        return;
    }

    function updateRemoveButtons() {
        const items = container.querySelectorAll(".material-item");

        items.forEach((item) => {
            const removeButton = item.querySelector(".remove-material");
            removeButton.disabled = items.length === 1;
        });
    }

    addButton.addEventListener("click", () => {
        const firstItem = container.querySelector(".material-item");
        const newItem = firstItem.cloneNode(true);

        newItem.querySelectorAll("input").forEach((input) => {
            input.value = "";
        });

        newItem.querySelectorAll("select").forEach((select) => {
            select.selectedIndex = 0;
        });

        container.appendChild(newItem);
        updateRemoveButtons();
    });

    container.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-material")) {
            event.target.closest(".material-item").remove();
            updateRemoveButtons();
        }
    });

    updateRemoveButtons();
});
