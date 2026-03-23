from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ServicioForm(FlaskForm):

    descripcion = StringField(
        'Descripción',
        validators=[DataRequired(message="La descripción es obligatoria")]
    )

    costo = DecimalField(
        'Costo del servicio',
        validators=[DataRequired(message="El costo es obligatorio")]
    )

    fecha_inicio = DateField(
        'Fecha de inicio',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    fecha_fin = DateField(
        'Fecha de finalización',
        format='%Y-%m-%d'
    )

    estado = SelectField(
        'Estado',
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_proceso', 'En proceso'),
            ('finalizado', 'Finalizado')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Guardar servicio')