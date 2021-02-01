from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    category = RadioField('Category', validators=[DataRequired()])
    submit = SubmitField('Search')

