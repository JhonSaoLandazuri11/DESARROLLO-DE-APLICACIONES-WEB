function mostrarAlerta() {
    const alerta = document.getElementById("alertaBootstrap");
    alerta.classList.remove("d-none");

    setTimeout(() => {
        alerta.classList.add("d-none");
    }, 4000);
}

document.getElementById("formulario").addEventListener("submit", function (e) {
    e.preventDefault();

    let nombre = document.getElementById("nombre").value.trim();
    let correo = document.getElementById("correo").value.trim();
    let mensaje = document.getElementById("mensaje").value.trim();

    let valido = true;

    document.getElementById("errorNombre").textContent = "";
    document.getElementById("errorCorreo").textContent = "";
    document.getElementById("errorMensaje").textContent = "";

    if (nombre === "") {
        document.getElementById("errorNombre").textContent = "El nombre es obligatorio";
        valido = false;
    }

    if (correo === "") {
        document.getElementById("errorCorreo").textContent = "El correo es obligatorio";
        valido = false;
    }

    if (mensaje === "") {
        document.getElementById("errorMensaje").textContent = "El mensaje es obligatorio";
        valido = false;
    }

    if (valido) {
        mostrarAlerta();
        document.getElementById("formulario").reset();
    }
});
