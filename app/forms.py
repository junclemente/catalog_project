from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Category')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    maker = StringField('Make', validators=[DataRequired()])
    model_year = StringField('Year')
    description = TextAreaField('Description')
    price = StringField('Price')
    submit = SubmitField('Add')


class ConfirmForm(FlaskForm):
    submit = SubmitField('Confirm')
