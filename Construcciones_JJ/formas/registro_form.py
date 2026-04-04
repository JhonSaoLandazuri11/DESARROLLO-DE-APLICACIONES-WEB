from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ClienteForm(FlaskForm):
    nombres = StringField(
        'Nombres',
        validators=[DataRequired(message="El nombre es obligatorio")]
    )

    direccion = StringField(
        'Dirección',
        validators=[DataRequired(message="La dirección es obligatoria")]
    )

    telefono = StringField(
        'Teléfono',
        validators=[DataRequired(message="El teléfono es obligatorio")]
    )

    email = EmailField(
        'Correo electrónico',
        validators=[
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido")
        ]
    )

    cedula = StringField(
        'Cédula',
        validators=[DataRequired(message="La cédula es obligatoria")]
    )

    tipo_identificacion = SelectField(
        'Tipo de identificación',
        choices=[('cedula', 'Cédula'), ('ruc', 'RUC')]
    )

    tipo_cliente = SelectField(
        'Tipo de cliente',
        choices=[('normal', 'Normal'), ('vip', 'VIP')]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, message="Mínimo 6 caracteres")
        ]
    )

    submit = SubmitField('Registrarse')
    telefono = StringField(
        'Teléfono',
        validators=[
            DataRequired(message="El teléfono es obligatorio"),
            Length(min=7, max=15)
        ]
    )

    email = EmailField(
        'Correo electrónico',
        validators=[
            DataRequired(message="El correo es obligatorio"),
            Email(message="Correo inválido")
        ]
    )

    submit = SubmitField('Guardar cliente')