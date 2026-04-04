from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class ServicioForm(FlaskForm):
    nombre = StringField('Nombre del servicio', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    submit = SubmitField('Guardar')