#Formulario del Producto

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired(), length(min=2, max=100)])
    cantidad = IntegerField('Cantidad del Producto', validators=[DataRequired(), NumberRange(min=0)])   
    descripcion = TextAreaField('Descripción del Producto', validators=[DataRequired(), length(min=10, max=500)])
    precio = IntegerField('Precio del Producto', validators=[DataRequired(), NumberRange(min=0.00)])
    submit = SubmitField('Agregar Producto')    




