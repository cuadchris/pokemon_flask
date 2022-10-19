from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class GetPoke(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Retrieve PoKémon')