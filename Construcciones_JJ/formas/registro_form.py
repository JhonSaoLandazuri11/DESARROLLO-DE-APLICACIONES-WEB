from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ClienteForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=3, max=100)
        ]
    )

    apellido = StringField(
        'Apellido',
        validators=[
            DataRequired(message="El apellido es obligatorio"),
            Length(min=3, max=100)
        ]
    )

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