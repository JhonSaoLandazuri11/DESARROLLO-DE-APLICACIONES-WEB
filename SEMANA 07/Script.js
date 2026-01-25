// Arreglo de productos
const productos = [
    { id: 1, nombre: "Coca-Cola", precio: 0.50, descripcion: "Bebida refrescante" },
    { id: 2, nombre: "Galletas Oreo", precio: 1, descripcion: "Galletas sabor chocolate" },
    { id: 3, nombre: "Chocolate Galak", precio: 0.75, descripcion: "Chocolate con leche" }
];

// Referencias al DOM
const listaProductos = document.getElementById("Listadoproductos");
const btnAgregarProducto = document.getElementById("Btnproducto");

// Función para renderizar productos
function renderizarProductos() {
    listaProductos.innerHTML = ""; // Limpia la lista

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.textContent = `${producto.nombre} - $${producto.precio} | ${producto.descripcion}`;
        listaProductos.appendChild(li);
    });
}

// Función para agregar un nuevo producto
function agregarProducto() {
    const nombre = prompt("Ingrese el nombre del producto:");
    const precio = parseFloat(prompt("Ingrese el precio del producto:"));
    const descripcion = prompt("Ingrese la descripción del producto:");

    if (nombre && !isNaN(precio) && descripcion) {
        const nuevoProducto = {
            id: productos.length + 1,
            nombre,
            precio,
            descripcion
        };
        productos.push(nuevoProducto);
        renderizarProductos();
    } else {
        alert("Datos inválidos. Intente nuevamente.");
    }
}

// Eventos
document.addEventListener("DOMContentLoaded", renderizarProductos);
btnAgregarProducto.addEventListener("click", agregarProducto);
