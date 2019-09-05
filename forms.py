from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, NumberRange

class Initial(FlaskForm):
    selection = RadioField(label='Select Upload to upload/download resumes from the link(Sharepoint) or Skills to ', choices=[('Up/Down', 'Up/Down'), ('Skills','Skills')], validators=[DataRequired()])
    submit = SubmitField('Submit')

#class up_down(FlaskForm):
    
class Skills(FlaskForm):
    skills = StringField('Enter Required Skill Sets', validators=[DataRequired()])
    submit = SubmitField('Submit')