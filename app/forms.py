from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')


class CategoryEditForm(CategoryForm):
    submit = SubmitField('Update')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Item')


class ItemEditForm(ItemForm):
    category_id = SelectField('Category')
    submit = SubmitField('Update Item Information')


class ConfirmForm(FlaskForm):
    submit = SubmitField('Confirm')
