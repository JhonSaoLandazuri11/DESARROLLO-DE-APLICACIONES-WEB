from flask import Flask, render_template, request, redirect, url_for, flash
from models.db import db
from models.cliente import Cliente

from servicios.cliente_servicio import *
from servicios.servicio_servicio import *
from servicios.factura_servicio import *
from servicios.pago_servicio import *

from formas.login_form import LoginForm
from formas.registro_form import RegistroForm
from formas.servicio_form import ServicioForm

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Sistema_factura'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# =========================
# 🔐 LOGIN
# =========================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))


# =========================
# 🔐 AUTENTICACIÓN
# =========================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)

        crear_cliente(
            form.nombre.data,
            form.apellido.data,
            form.telefono.data,
            form.email.data,
            password_hash
        )

        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))

    return render_template('auth/registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        cliente = obtener_cliente_por_email(form.email.data)

        if cliente and check_password_hash(cliente.password, form.password.data):
            login_user(cliente)
            flash('Bienvenido', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


# =========================
# 🏠 PÁGINAS
# =========================

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/contactos')
def contactos():
    return render_template('contactos.html')


@app.route('/quienes')
def quienes():
    return render_template('quienes.html')


@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')


# =========================
# 🧩 SERVICIOS (CRUD)
# =========================

@app.route('/servicios')
@login_required
def listar_servicios():
    servicios = obtener_servicios()
    return render_template('servicios/listar.html', servicios=servicios)


@app.route('/servicios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_servicio():
    form = ServicioForm()

    if form.validate_on_submit():
        crear_servicio(
            form.descripcion.data,
            form.costo.data,
            form.fecha_inicio.data,
            form.fecha_fin.data,
            form.estado.data,
            form.id_cliente.data
        )
        flash('Servicio creado correctamente', 'success')
        return redirect(url_for('listar_servicios'))

    return render_template('servicios/formulario.html', form=form)


@app.route('/servicios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_servicio_route(id):
    eliminar_servicio(id)
    flash('Servicio eliminado', 'warning')
    return redirect(url_for('listar_servicios'))


# =========================
# 🧾 FACTURAS
# =========================

@app.route('/facturas')
@login_required
def listar_facturas():
    facturas = obtener_facturas()
    return render_template('facturas/listar.html', facturas=facturas)


# =========================
# 💳 PAGOS
# =========================

@app.route('/pagos')
@login_required
def listar_pagos():
    pagos = obtener_pagos()
    return render_template('pagos/listar.html', pagos=pagos)


# =========================
# 🚀 RUN
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)