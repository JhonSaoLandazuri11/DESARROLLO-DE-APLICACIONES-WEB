import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_file
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import UserMixin
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from MySQLdb.cursors import DictCursor

from modelos.db import db
from modelos.cliente import Clientes

from servicios.servicio_servicio import obtener_servicios, guardar_servicio, obtener_servicios, actualizar_servicio, eliminar_servicio
from servicios.cliente_servicio import listar_clientes, obtener_cliente, guardar_cliente, actualizar_cliente_db, eliminar_cliente_db, obtener_cliente_por_email, crear_cliente
from servicios.servicio_servicio import *
from servicios.factura_servicio import guardar_factura, obtener_factura


from servicios.pago_servicio import *

from formas.login_form import LoginForm
from formas.registro_form import ClienteForm
from formas.servicio_form import ServicioForm 
from servicios.empresa_servicio import listar_empresas
from servicios.servicio_servicio import obtener_servicios, guardar_servicio





from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import io
from datetime import datetime

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================
app.config['SECRET_KEY'] = 'mi_clave_secreta'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'servicios_m_mecanica'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db.init_app(app)

# =========================
# LOGIN MANAGER
# =========================
# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# -------------------------------
# User loader (OBLIGATORIO)
# -------------------------------
@login_manager.user_loader
def load_user(user_id):
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (user_id,))
    cliente = cursor.fetchone()

    if cliente:
        return Clientes(
            id_cliente=cliente.get('id_cliente'),
            nombres=cliente.get('nombres'),
            direccion=cliente.get('direccion'),
            telefono=cliente.get('telefono'),
            email=cliente.get('email'),
            cedula=cliente.get('cedula'),
            tipo_identificacion=cliente.get('tipo_identificacion'),
            tipo_cliente=cliente.get('tipo_cliente')
        )
    return None


# -------------------------------
# Context processor (opcional)
# -------------------------------
@app.context_processor
def inject_user():
    return dict(current_user=current_user)
# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        cliente = obtener_cliente_por_email(form.email.data)

        if cliente:
            if check_password_hash(cliente['password'], form.password.data):

                user = Clientes(
                    id_cliente=cliente.get('id_cliente'),
                    nombres=cliente.get('nombres'),
                    direccion=cliente.get('direccion'),
                    telefono=cliente.get('telefono'),
                    email=cliente.get('email'),
                    cedula=cliente.get('cedula'),
                    tipo_identificacion=cliente.get('tipo_identificacion'),
                    tipo_cliente=cliente.get('tipo_cliente')
                )

                login_user(user)
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('clientes'))
            else:
                flash('Contraseña incorrecta', 'danger')
        else:
            flash('Correo no registrado', 'danger')

    return render_template('auth/login.html', form=form)

# =========================
# LOGOUT
# =========================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

# =========================
# REGISTRO
# =========================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = ClienteForm()

    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)

        crear_cliente(
            form.nombres.data,
            form.direccion.data,
            form.telefono.data,
            form.email.data,
            form.cedula.data,
            form.tipo_identificacion.data,
            form.tipo_cliente.data,
            password_hash
        )

        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))

    return render_template('auth/registro.html', form=form)

# =========================
# PÁGINAS PRINCIPALES
# =========================
@app.route('/')
def inicio():
    return render_template('productos/index.html')

@app.route('/contactos')
def contactos():
    return render_template('productos/contactos.html')

@app.route('/quienes')
def quienes():
    return render_template('productos/quienes.html')

@app.route('/proyectos')
def proyectos():
    return render_template('productos/proyectos.html')

# =========================
# CLIENTES
# =========================
@app.route('/clientes')
@login_required
def clientes():
    lista = listar_clientes()
    return render_template('clientes/listar_clientes.html', clientes=lista)

@app.route('/clientes/registrar', methods=['GET', 'POST'])
@login_required
def registrar_cliente():
    if request.method == 'POST':
        guardar_cliente(
            request.form['nombres'],
            request.form['direccion'],
            request.form['telefono'],
            request.form['email'],
            request.form['cedula'],
            request.form['tipo_identificacion'],
            request.form['tipo_cliente']
        )
        flash('Cliente guardado correctamente', 'success')
        return redirect(url_for('clientes'))

    return render_template('clientes/registrar_cliente.html')

@app.route('/clientes/editar/<int:id>')
@login_required
def editar_cliente(id):
    cliente = obtener_cliente(id)
    return render_template('clientes/editar_cliente.html', cliente=cliente)

@app.route('/clientes/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar_cliente_route(id):
    actualizar_cliente_db(
        id,
        request.form['nombres'],
        request.form['direccion'],
        request.form['telefono'],
        request.form['email'],
        request.form['cedula'],
        request.form['tipo_identificacion'],
        request.form['tipo_cliente']
    )
    flash('Cliente actualizado', 'info')
    return redirect(url_for('clientes'))
@app.route('/cliente/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    if request.method == 'POST':
        nombres = request.form['nombres']
        cedula = request.form['cedula']
        tipo_identificacion = request.form['tipo_identificacion']
        tipo_cliente = request.form['tipo_cliente']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']

        cursor = db.connection.cursor()
        cursor.execute("""
            INSERT INTO cliente 
            (nombres, cedula, tipo_identificacion, tipo_cliente, telefono, email, direccion)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (nombres, cedula, tipo_identificacion, tipo_cliente, telefono, email, direccion))

        db.connection.commit()

        flash('Cliente agregado correctamente', 'success')
        return redirect(url_for('clientes'))

    return render_template('clientes/registrar_cliente.html')

@app.route('/clientes/eliminar/<int:id>')
@login_required
def eliminar_cliente_route(id):
    eliminar_cliente_db(id)
    flash('Cliente eliminado correctamente', 'warning')
    return redirect(url_for('clientes'))

# =========================
# SERVICIOS
# =========================

@app.route('/servicios')
@login_required
def listar_servicios():
    servicios = obtener_servicios()
    print(servicios)  # Para depuración
    return render_template('Servicios/listar.html', servicios=servicios)

@app.route('/servicio/nuevo', methods=['GET', 'POST'])
@login_required
def registrar_servicio():
    # 🔹 Cargar clientes y empresas siempre para el formulario
    clientes = listar_clientes()
    empresas = listar_empresas()

    if request.method == 'POST':
        tipo_identificacion = request.form.get('tipo_identificacion', '').strip()
        tipo_servicio = request.form.get('tipo_servicio', '').strip()
        estado_servicio = request.form.get('estado_servicio', '').strip()
        costo_estimado = request.form.get('costo_estimado', '').strip()
        fecha_solicitud = request.form.get('fecha_solicitud', '').strip()
        fecha_estimada = request.form.get('fecha_estimada', '').strip()
        fecha_inicio = request.form.get('fecha_inicio', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        RUC_empresa = request.form.get('RUC_empresa', '').strip()
        id_cliente = request.form.get('id_cliente', '').strip()

        print("FORMULARIO:", request.form)
        print("ID_CLIENTE RECIBIDO:", id_cliente)

        # 🔹 VALIDACIONES
        if not id_cliente:
            flash('Debe seleccionar un cliente', 'danger')
            return render_template('Servicios/registrar.html', clientes=clientes, empresas=empresas)

        if not RUC_empresa:
            flash('Debe seleccionar una empresa', 'danger')
            return render_template('Servicios/registrar.html', clientes=clientes, empresas=empresas)

        try:
            id_cliente = int(id_cliente)
        except ValueError:
            flash('Cliente inválido', 'danger')
            return render_template('Servicios/registrar.html', clientes=clientes, empresas=empresas)

        # 🔹 GUARDAR SERVICIO
        guardar_servicio(
            tipo_identificacion,
            tipo_servicio,
            estado_servicio,
            costo_estimado,
            fecha_solicitud,
            fecha_estimada,
            fecha_inicio,
            descripcion,
            RUC_empresa,
            id_cliente
        )

        flash('Servicio registrado correctamente', 'success')
        return redirect(url_for('listar_servicios'))

    # 🔹 GET: mostrar formulario
    return render_template('Servicios/registrar.html', clientes=clientes, empresas=empresas)


@app.route('/servicio/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_servicio(id):
    servicio = obtener_servicio(id)  # <- CORRECCIÓN

    if request.method == 'POST':
        tipo_identificacion = request.form['Tipo_Identificacion']
        tipo_servicio = request.form['Tipo_Servicio']
        estado_servicio = request.form['Estado_Servicio']
        costo_estimado = request.form['Costo_Estimado']
        fecha_solicitud = request.form['Fecha_Solicitud']
        fecha_estimada = request.form['Fecha_Estimada']
        fecha_inicio = request.form['fecha_inicio']
        descripcion = request.form['descripcion']
        RUC_empresa = request.form['RUC_empresa']
        id_cliente = request.form['id_cliente']

        actualizar_servicio(
            id,
            tipo_identificacion,
            tipo_servicio,
            estado_servicio,
            costo_estimado,
            fecha_solicitud,
            fecha_estimada,
            fecha_inicio,
            descripcion,
            RUC_empresa,
            id_cliente
        )

        flash('Servicio actualizado correctamente', 'info')
        return redirect(url_for('listar_servicios'))

    clientes = listar_clientes()
    return render_template('Servicios/editar.html', servicio=servicio, clientes=clientes)

    

# Obtener todos los servicios
def obtener_servicios():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT 
            s.id_servicio,
            s.Tipo_Identificacion AS tipo_identificacion,
            s.Tipo_servicio AS tipo_servicio,
            s.Estado_Servicio AS estado_servicio,
            s.Costo_estimado AS costo_estimado,
            s.Fecha_solicitud AS fecha_solicitud,
            s.Fecha_estimada AS fecha_estimada,
            s.Fecha_inicio AS fecha_inicio,
            s.Descripcion AS descripcion,
            s.RUC_empresa AS ruc_empresa,
            s.id_cliente,
            c.nombres AS cliente_nombre
        FROM servicio s
        JOIN cliente c ON s.id_cliente = c.id_cliente
    """)
    return cursor.fetchall()


# Obtener un solo servicio por id
def obtener_servicio(id):
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT 
            s.id_servicio,
            s.Tipo_Identificacion AS tipo_identificacion,
            s.Tipo_servicio AS tipo_servicio,
            s.Estado_Servicio AS estado_servicio,
            s.Costo_estimado AS costo_estimado,
            s.Fecha_solicitud AS fecha_solicitud,
            s.Fecha_estimada AS fecha_estimada,
            s.Fecha_inicio AS fecha_inicio,
            s.Descripcion AS descripcion,
            s.RUC_empresa AS ruc_empresa,
            s.id_cliente,
            c.nombres AS cliente_nombre
        FROM servicio s
        JOIN cliente c ON s.id_cliente = c.id_cliente
        WHERE s.id_servicio = %s
    """, (id,))
    return cursor.fetchone()

def guardar_factura(numero, subtotal, descuento, iva, total,
                   forma_pago, estado_pago, id_servicio, id_cliente):

    cursor = db.connection.cursor()

    cursor.execute("""
        INSERT INTO factura 
        (Numero_factura, Sub_total, Descuento, IVA, Total_pago,
         Forma_pago, Estado_pago, id_servicio, id_cliente)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (numero, subtotal, descuento, iva, total,
          forma_pago, estado_pago, id_servicio, id_cliente))

    db.connection.commit()


@app.route('/servicio/eliminar/<int:id>')
@login_required
def eliminar_servicio_route(id):
    cursor = db.connection.cursor()  # 🔹 Definir cursor
    cursor.execute("UPDATE servicio SET Estado_Servicio = 0 WHERE id_servicio = %s", (id,))
    db.connection.commit()
    flash("Servicio desactivado correctamente.", "success")
    return redirect(url_for('listar_servicios'))

#Factura
@app.route('/facturas')
@login_required
def listar_facturas():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
    SELECT 
        f.Id_factura,
        f.Numero_factura,
        f.Fecha_emision,
        f.Total_pago,
        f.Forma_pago,
        f.Estado_pago,
        c.nombres,
        s.tipo_servicio
    FROM factura f
    INNER JOIN cliente c ON f.Id_cliente = c.id_cliente
    INNER JOIN servicio s ON f.Id_servicio = s.id_servicio
    ORDER BY f.Id_factura DESC
    """)
    facturas = cursor.fetchall()
    return render_template('factura/listar.html', facturas=facturas)


@app.route('/factura/nueva', methods=['GET','POST'])
@login_required
def nueva_factura():
    cursor = db.connection.cursor(DictCursor)
    
    # 🔹 Traer todos los clientes y servicios desde la base
    cursor.execute("SELECT * FROM cliente ORDER BY nombres")
    clientes = cursor.fetchall()
    
    cursor.execute("SELECT * FROM servicio ORDER BY tipo_servicio")
    servicios = cursor.fetchall()

    if request.method == 'POST':
        # 🔹 Recibir datos del formulario
        numero = request.form.get('numero')
        id_cliente = request.form.get('Id_cliente')
        id_servicio = request.form.get('Id_servicio')
        subtotal = float(request.form.get('Sub_total', 0))
        descuento = float(request.form.get('Descuento', 0))
        iva = float(request.form.get('IVA', 0))
        total = float(request.form.get('Total_pago', 0))
        forma_pago = request.form.get('forma_pago')
        estado_pago = request.form.get('estado_pago')

        # Validar campos
        if not numero or not id_cliente or not id_servicio:
            flash('Complete todos los campos obligatorios', 'danger')
            return redirect(request.url)

        # 🔹 Guardar en la base de datos
        guardar_factura(
            numero, subtotal, descuento, iva, total,
            forma_pago, estado_pago, id_servicio, id_cliente
        )

        flash('Factura creada correctamente', 'success')
        return redirect(url_for('listar_facturas'))

    # 🔹 Renderizar formulario con todos los clientes y servicios
    return render_template('factura/nueva.html', clientes=clientes, servicios=servicios)

@app.route('/factura/eliminar/<int:id>', methods=['GET'])
@login_required
def eliminar_factura(id):
    cursor = db.connection.cursor()
    try:
        cursor.execute("DELETE FROM factura WHERE Id_factura = %s", (id,))
        db.connection.commit()
        flash('Factura eliminada correctamente', 'success')
    except Exception as e:
        db.connection.rollback()
        flash(f'Error al eliminar la factura: {e}', 'danger')
    return redirect(url_for('listar_facturas'))

# ------------------------
# Función para generar PDF
# ------------------------
def generar_pdf_factura(factura):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Encabezado ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-50, factura['empresa']['nombre'])
    c.setFont("Helvetica", 10)
    c.drawString(50, height-65, f"RUC: {factura['empresa']['ruc']}")
    c.drawString(50, height-80, f"Dirección: {factura['empresa']['direccion']}")
    c.drawString(50, height-95, f"Tel: {factura['empresa']['telefono']}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, height-50, f"Factura N°: {factura['numero']}")
    c.drawString(400, height-65, f"Fecha: {factura['fecha']}")

    # --- Datos del Cliente ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height-130, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height-145, f"Nombre: {factura['cliente']['nombre']}")
    c.drawString(50, height-160, f"RUC/CI: {factura['cliente']['ruc']}")
    c.drawString(50, height-175, f"Dirección: {factura['cliente']['direccion']}")

    # --- Tabla de items ---
    data = [["Cant.", "Descripción", "Precio Unitario", "Subtotal"]]
    for item in factura['items']:
        data.append([
            item['cantidad'],
            item['descripcion'],
            f"${item['precio']:.2f}",
            f"${item['subtotal']:.2f}"
        ])

    table = Table(data, colWidths=[50, 300, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height-350)

    # --- Totales ---
    total_y = height-370-len(factura['items'])*20
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(480, total_y, f"Subtotal: ${factura['totales']['subtotal']:.2f}")
    c.drawRightString(480, total_y-15, f"IVA: ${factura['totales']['iva']:.2f}")
    c.drawRightString(480, total_y-30, f"Total: ${factura['totales']['total']:.2f}")

    # --- Pie de página legal ---
    c.setFont("Helvetica", 8)
    c.drawString(50, 50, "Factura autorizada por el SRI. Conserve este documento según normativa vigente.")

    c.save()
    buffer.seek(0)
    return buffer

# ------------------------
# Ruta Flask para descargar PDF
# ------------------------
@app.route('/factura/<int:id>')
def factura_pdf(id):
    # Simulación: Obtener factura de la base de datos
    factura = {
        "numero": f"001-001-{id:06}",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "empresa": {
            "nombre": "Construcciones JJ",
            "ruc": "0999999999001",
            "direccion": "Av. Principal #123, Quito",
            "telefono": "0999999999"
        },
        "cliente": {
            "nombre": "Juan Pérez",
            "ruc": "1712345678",
            "direccion": "Calle Secundaria #456"
        },
        "items": [
            {"cantidad": 2, "descripcion": "Servicio de construcción", "precio": 120.00, "subtotal": 240.00},
            {"cantidad": 1, "descripcion": "Materiales", "precio": 50.00, "subtotal": 50.00}
        ],
        "totales": {"subtotal": 290.00, "iva": 34.80, "total": 324.80}
    }

    pdf_buffer = generar_pdf_factura(factura)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"factura_{id}.pdf", mimetype='application/pdf')

# ------------------------
# Ejecutar app
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)

# =========================
# PRUEBA CONEXIÓN
# =========================
@app.route('/test_db')
def test_db():
    cursor = db.connection.cursor()
    cursor.execute("SELECT 1")
    return "Conexión OK"

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)