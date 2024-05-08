from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.models import User

class RegisterForm(FlaskForm):
    '''
    Used for validating User registration
    '''
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=100)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=100)]
    )
    '''
    confirm = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match."),
        ]
    )
    '''
    # ==============================================================================================================
    def email_validator(self, field):
        '''
        Validate email to see if it is already registered

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            True if the email is not taken, else false
        '''
        return False if User.query.filter_by(email=field.data).first() else True

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
    
        # Check if the email exists
        if not self.email_validator(self.email):
            self.email.errors.append("Email already Exists")
            return False
        
        # Check if the two passwords are the same (password and confirmation password)
        '''
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        '''
        
        return True