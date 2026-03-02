from flask import Flask, render_template, url_for, request, redirect, flash
from formulary import ProductoForm
import Inventario.Base_datos as init_db
from Inventario.Inventario import Inventario
from Inventario.productos import Producto

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

init_db.init_db()
inventario = Inventario()
inventario.cargar_productos()


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')


@app.route('/contactos')
def contactos():
    return render_template('contactos.html')


@app.route('/quienes')
def quienes():
    return render_template('quienes.html')


# ✅ LISTAR PRODUCTOS
@app.route("/productos")
def productos():
    inventario.cargar_productos()
    productos = inventario.productos.values()
    return render_template("productos.html", productos=productos)


# ✅ CREAR PRODUCTO
@app.route("/productos/nuevo", methods=["GET", "POST"])
def producto_nuevo():
    form = ProductoForm()

    if form.validate_on_submit():
        inventario.agregar_producto(
            form.nombre.data,
            form.precio.data,
            form.cantidad.data,
            form.descripcion.data
        )
        flash("Producto creado correctamente", "success")
        return redirect(url_for("productos"))

    return render_template("producto_form.html", form=form)


# ✅ LISTA ALTERNA (SE MANTIENE)
@app.route("/productos/lista")
def listar_productos():
    inventario.cargar_productos()
    productos = inventario.productos.values()
    return render_template("productos/productos.html", productos=productos)


# ✅ EDITAR PRODUCTO
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    inventario.cargar_productos()
    producto = inventario.productos.get(id)

    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos'))

    form = ProductoForm(obj=producto)

    if form.validate_on_submit():
        inventario.editar_producto(
            id,
            form.nombre.data,
            form.precio.data,
            form.cantidad.data,
            form.descripcion.data
        )
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos'))

    return render_template("producto_form.html", form=form, editar=True)


# ✅ ELIMINAR PRODUCTO
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    inventario.eliminar_producto(id)
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos'))


if __name__ == '__main__':
    app.run(debug=True)