from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, Form, SelectField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class SearchForm(FlaskForm):
    title = StringField('Search', name='search', id='search', validators=[DataRequired()])

    submit = SubmitField('Search', id='search')
