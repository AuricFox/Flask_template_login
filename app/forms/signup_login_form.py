from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.models import User

# =========================================================================================
class RegisterForm(FlaskForm):
    '''
    Used for validating User registration
    '''
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=100)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=100)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match."),
        ]
    )

    def validate(self):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        
        user = User.query.filter_by(email=self.email.data).first()
        # Check if the email exists
        if user:
            self.email.errors.append("Email already Exists")
            return False
        # Check if the two passwords are the same (password and confirmation password)
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        
        return True

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