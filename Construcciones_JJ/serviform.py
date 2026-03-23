# formulario de servicios

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ServicioForm(FlaskForm):

    descripcion = StringField(
        'Descripción del servicio',
        validators=[DataRequired(), Length(min=5, max=500)]
    )

    costo = DecimalField(
        'Costo',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )

    fecha_inicio = DateField(
        'Fecha de inicio',
        validators=[Optional()]
    )

    fecha_fin = DateField(
        'Fecha de finalización',
        validators=[Optional()]
    )

    estado = StringField(
        'Estado',
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    id_cliente = IntegerField(
        'ID Cliente',
        validators=[DataRequired(), NumberRange(min=1)]
    )

    submit = SubmitField('Guardar Servicio')


