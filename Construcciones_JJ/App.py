from flask import Flask, render_template, url_for, request, redirect, flash
from formulary import ProductoForm
import Inventario.Base_datos as init_db
from Inventario.Inventario import Inventario
from Inventario.productos import Producto
from flask_sqlalchemy import SQLAlchemy
from Inventario.Inventario_persistencia import leer_json, guardar_json, guardar_csv, leer_csv, guardar_txt, leer_txt  
from Inventario.Base_datos import get_connection
from conexion.conexion import get_connection
import os   # ✅ agregado para controlar rutas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

# Inicializar la base de datos y el inventario
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ✅ asegurar que la app trabaje en la carpeta correcta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print("Ruta del proyecto:", BASE_DIR)


# ❗ CORRECCIÓN: ejecutar dentro del contexto de Flask
with app.app_context():
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

#Listar productos con MySQL
@app.route('/productos_mysql')
def productos_mysql():
    try:
        conn = get_connection();
        if conn is None:
            flash('No se pudo conectar a la base de datos', 'danger')
            return redirect(url_for('productos'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, cantidad, descripcion, precio FROM productos")       
        productos_mysql = cursor.fetchall()
        print(productos_mysql)  # Verificar los datos obtenidos
        cursor.close()
        conn.close()    
        return render_template('productos.html', productos=productos_mysql)
    except Exception as e:  
        flash(f'Error al obtener productos: {e}', 'danger')
        return redirect(url_for('productos'))


# ✅ RUTA PARA PERSISTENCIA DE DATOS
@app.route('/datos', methods=['GET', 'POST'])
def mostrar_datos():

    if request.method == 'POST':

        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        descripcion = request.form.get('descripcion')

        # evitar guardar registros vacíos
        if nombre and precio and cantidad and descripcion:

            datos = {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "descripcion": descripcion
            }

            # Guardar en TXT
            guardar_txt(f"{nombre}, {precio}, {cantidad}, {descripcion}")

            # Guardar en JSON
            guardar_json(datos)

            # Guardar en CSV
            guardar_csv(datos)

            flash('Datos guardados correctamente', 'success')

        else:
            flash('Todos los campos son obligatorios', 'danger')

        return redirect(url_for('mostrar_datos'))

    # Leer los datos
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()

    return render_template(
        'datos.html',
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv
    )


#Ruta de conexion a la base de datos en mysql
@app.route('/db_test')
def db_test():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuario")
            result = cursor.fetchall()

            cursor.close()

        return str(result)

    except Exception as e:
        return f"Error al conectar a la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True)