
document.addEventListener("DOMContentLoaded", () => {

    const estado = document.getElementById("estado-sistema");

    if (!estado) {
        return;
    }

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
    const search = document.getElementById("donation-search");
    const statusFilter = document.getElementById("donation-status-filter");
    const categoryFilter = document.getElementById("donation-category-filter");
    const dateFrom = document.getElementById("donation-date-from");
    const dateTo = document.getElementById("donation-date-to");
    const clearButton = document.getElementById("clear-donation-filters");
    const cards = Array.from(document.querySelectorAll(".admin-donation-card"));
    const emptyResult = document.getElementById("no-search-results");
    const countLabel = document.getElementById("donation-filter-count");

    if (!search || cards.length === 0) return;

    function applyFilters() {
        const query = search.value.trim().toLocaleLowerCase();
        const status = statusFilter ? statusFilter.value : "";
        const category = categoryFilter ? categoryFilter.value : "";
        const from = dateFrom ? dateFrom.value : "";
        const to = dateTo ? dateTo.value : "";
        let visibleCount = 0;

        cards.forEach((card) => {
            const matchesSearch = (card.dataset.search || "").toLocaleLowerCase().includes(query);
            const matchesStatus = !status || card.dataset.status === status;
            const categories = (card.dataset.categories || "").trim().split(/\\s+/);
            const matchesCategory = !category || categories.includes(category);
            const date = card.dataset.date || "";
            const matchesFrom = !from || date >= from;
            const matchesTo = !to || date <= to;
            const visible = matchesSearch && matchesStatus && matchesCategory && matchesFrom && matchesTo;

            card.hidden = !visible;
            if (visible) visibleCount += 1;
        });

        if (emptyResult) emptyResult.hidden = visibleCount > 0;
        if (countLabel) countLabel.textContent = `Mostrando ${visibleCount} de ${cards.length} donación(es).`;
    }

    [search, statusFilter, categoryFilter, dateFrom, dateTo].forEach((control) => {
        if (control) control.addEventListener("input", applyFilters);
        if (control && control.tagName === "SELECT") control.addEventListener("change", applyFilters);
    });

    if (clearButton) {
        clearButton.addEventListener("click", () => {
            search.value = "";
            if (statusFilter) statusFilter.value = "";
            if (categoryFilter) categoryFilter.value = "";
            if (dateFrom) dateFrom.value = "";
            if (dateTo) dateTo.value = "";
            applyFilters();
        });
    }

    applyFilters();
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


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("donation-form");
    const feedback = document.getElementById("donation-feedback");

    if (!form || !feedback) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = form.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        const materiales = Array.from(form.querySelectorAll(".material-item"), (item) => ({
            material: item.querySelector('[name="material"]').value.trim(),
            categoria: item.querySelector('[name="categoria"]').value,
            cantidad: Number(item.querySelector('[name="cantidad"]').value),
            condicion: item.querySelector('[name="condicion"]').value
        }));
        const datos = {
            donante: form.elements.donante.value.trim(),
            telefono: form.elements.telefono.value.trim(),
            correo: form.elements.correo.value.trim(),
            observaciones: form.elements.observaciones.value.trim(),
            materiales
        };

        feedback.hidden = true;
        feedback.className = "form-feedback";
        submitButton.disabled = true;
        submitButton.textContent = "Guardando…";

        try {
            const response = await fetch("/api/donaciones", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datos)
            });
            const result = await response.json();
            if (!response.ok || !result.correcto) {
                throw new Error(result.mensaje || "No se pudo registrar la donación.");
            }

            feedback.textContent = `${result.mensaje} Código: ${result.donacion.id}`;
            feedback.classList.add("is-success");
            feedback.hidden = false;
            form.reset();
            const container = document.getElementById("materials-container");
            container.querySelectorAll(".material-item").forEach((item, index) => {
                if (index > 0) item.remove();
            });
            const removeButton = container.querySelector(".remove-material");
            if (removeButton) removeButton.disabled = true;
        } catch (error) {
            feedback.textContent = error.message || "No se pudo conectar con el servidor.";
            feedback.classList.add("is-error");
            feedback.hidden = false;
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
});
