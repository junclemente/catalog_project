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
    description = TextAreaField('Description')
    submit = SubmitField('Add Category')

# class CategoryForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     description = TextAreaField('Description')


# class CategoryAddForm(CategoryForm):


class CategoryEditForm(CategoryForm):
    submit = SubmitField('Edit Category')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add')


# class ItemAddForm(ItemForm):


class ItemEditForm(ItemForm):
    category_id = SelectField('Category')
    submit = SubmitField('Edit')


class ConfirmForm(FlaskForm):
    submit = SubmitField('Confirm')
