from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class AdminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[Length(max=255)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Submit')

class AdminPlayerForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    level = IntegerField('Level', validators=[DataRequired()])
    ads_disabled = BooleanField('Ads Disabled')
    donation = DecimalField('Donation', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=255)])
    price = DecimalField('Price', validators=[DataRequired()])
    purchasable = BooleanField('Purchasable')
    submit = SubmitField('Submit')

class AdminAchievementForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')

class AdminInventoryForm(FlaskForm):
    player_id = IntegerField('Player ID', validators=[DataRequired()])
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminRecordForm(FlaskForm):
    player_id = IntegerField('Player ID', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Submit')

 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    purchasable = BooleanField('Purchasable')
    effect = StringField('Effect', validators=[DataRequired()])  # Новое поле для эффекта предмета
    submit = SubmitField('Add Item')
