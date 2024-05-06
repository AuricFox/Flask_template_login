from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length

from app.models.models import User

# =========================================================================================
class LoginForm(FlaskForm):
    '''
    Used for validating User login
    '''
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=100)]
    )