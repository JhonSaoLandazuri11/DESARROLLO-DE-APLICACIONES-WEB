// ===============================
// Referencias a elementos del DOM
// ===============================
const form = document.getElementById("registForm");

const Nombre = document.getElementById("Nombre");
const Apellidos = document.getElementById("Apellidos");
const Email = document.getElementById("Email");
const Contraseña = document.getElementById("Contraseña");
const Corfirmacion_contraseña = document.getElementById("Corfirmacion_contraseña");
const Descripcion = document.getElementById("Descripcion");

// Botón
const BtnEnviar = document.getElementById("BtnEnviar");

// Mensajes de error
const NombreError = document.getElementById("NombreError");
const ApellidosError = document.getElementById("ApellidosError");
const EmailError = document.getElementById("EmailError");
const ContraseñaError = document.getElementById("ContraseñaError");
const Corfirmacion_contraseñaError = document.getElementById("Corfirmacion_contraseñaError");
const DescripcionError = document.getElementById("DescripcionError");   



// ===============================
// Funciones de estado
// ===============================
function marcarInvalido(input, errorElement, mensaje) {
    input.classList.add("invalid");
    input.classList.remove("valid");
    errorElement.textContent = mensaje;
}

function marcarValido(input, errorElement) {
    input.classList.add("valid");
    input.classList.remove("invalid");
    errorElement.textContent = "";
}

// ===============================
// Validaciones
// ===============================
function validarNombre() {
    const valor = Nombre.value.trim();

    if (valor === "") {
        marcarInvalido(Nombre, NombreError, "El nombre no puede estar vacío");
        BtnEnviar.disabled = true;
        return false;
    }

    if (valor.length < 3) {
        marcarInvalido(Nombre, NombreError, "Mínimo 3 caracteres");
        BtnEnviar.disabled = true;
        return false;
    }

    marcarValido(Nombre, NombreError);
    BtnEnviar.disabled = false;
    return true;
}

function validarApellidos() {
    const valor = Apellidos.value.trim();
    
    if (valor === "") {
        marcarInvalido(Apellidos, ApellidosError, "Los apellidos no pueden estar vacíos");
        BtnEnviar.disabled = true;
        return false;
    }
    if (valor.length < 3) {
        marcarInvalido(Apellidos, ApellidosError, "Mínimo 3 caracteres");
        BtnEnviar.disabled = true;
        return false;
    }   
    marcarValido(Apellidos, ApellidosError);
    BtnEnviar.disabled = false;
    return true;
}

function validarEmail() {
    const valor = Email.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (valor === "") {
        marcarInvalido(Email, EmailError, "El correo no puede estar vacío");
        BtnEnviar.disabled = true;
        return false;
    }

    if (!emailRegex.test(valor)) {
        marcarInvalido(Email, EmailError, "Formato de correo inválido");
        BtnEnviar.disabled = true;
        return false;
    }

    marcarValido(Email, EmailError);
    BtnEnviar.disabled = false;
    return true;
}

function validarConfirmacionContraseña() {
    const contraseñaValor = Contraseña.value;
    const confirmacionValor = Corfirmacion_contraseña.value;

    if (contraseñaValor !== confirmacionValor) {
        marcarInvalido(Corfirmacion_contraseña, Corfirmacion_contraseñaError, "Las contraseñas no coinciden");
        BtnEnviar.disabled = true;
        return false;
    }

    marcarValido(Corfirmacion_contraseña, Corfirmacion_contraseñaError);
    BtnEnviar.disabled = false;
    return true;
}

// ===============================
// Eventos
// ===============================
Nombre.addEventListener("input", validarNombre);
Apellidos.addEventListener("input", validarApellidos);
Email.addEventListener("input", validarEmail);
Corfirmacion_contraseña.addEventListener("input", validarConfirmacionContraseña);

// Evitar envío si hay errores
form.addEventListener("submit", function (e) {
    if (!validarNombre()) {
        e.preventDefault();
    }
});

form.addEventListener("submit", function (e) {
    if (!validarApellidos()) {
        e.preventDefault();
    }
});
form.addEventListener("submit", function (e) {
    if (!validarEmail()) {
        e.preventDefault();
    }       
});
form.addEventListener("submit", function (e) {
    if (!validarConfirmacionContraseña()) {
        e.preventDefault();
    }
});

