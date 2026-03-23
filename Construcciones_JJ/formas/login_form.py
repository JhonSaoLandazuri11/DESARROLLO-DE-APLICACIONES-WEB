from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = EmailField(
        'Correo electrónico',
        validators=[
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido")
        ]
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, message="Mínimo 6 caracteres")
        ]
    )
    
    submit = SubmitField('Iniciar sesión')