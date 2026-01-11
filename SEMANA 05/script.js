const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImageBtn");
const deleteImageBtn = document.getElementById("deleteImageBtn");
const gallery = document.getElementById("gallery");

let selectedImage = null;

// Agregar imagen
addImageBtn.addEventListener("click", () => {
    const imageUrl = imageUrlInput.value.trim();

    if (imageUrl === "") {
        alert("Ingrese una URL válida de imagen");
        return;
    }

    const img = document.createElement("img");
    img.src = imageUrl;
    img.alt = "Imagen de la galería";

    // Si la imagen no carga
    img.onerror = () => {
        alert("La imagen no se pudo cargar. Verifique que la URL sea directa a una imagen.");
        img.remove();
    };

    // Seleccionar imagen
    img.addEventListener("click", () => {
        selectImage(img);
    });

    gallery.appendChild(img);
    imageUrlInput.value = "";
});

// Seleccionar imagen
function selectImage(img) {
    const images = document.querySelectorAll(".gallery img");
    images.forEach(image => image.classList.remove("selected"));

    selectedImage = img;
    img.classList.add("selected");
}

// Eliminar imagen seleccionada
deleteImageBtn.addEventListener("click", () => {
    if (!selectedImage) {
        alert("No hay ninguna imagen seleccionada");
        return;
    }

    selectedImage.remove();
    selectedImage = null;
});

// Atajos de teclado
document.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        addImageBtn.click();
    }

    if (event.key === "Delete" && selectedImage) {
        selectedImage.remove();
        selectedImage = null;
    }
});
