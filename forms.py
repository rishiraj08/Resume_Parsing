from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, NumberRange

class Initial(FlaskForm):
    skills = StringField('Skills', validators=[DataRequired()])
    submit = SubmitField('Submit')
