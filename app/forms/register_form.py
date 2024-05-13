from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.models import User

class RegisterForm(FlaskForm):
    '''
    Used for validating User registration and profile information
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
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match."),
        ]
    )
    # ==============================================================================================================
    def validate_username(self, field):
        '''
        Validate username to see if it is already registered to another user

        Parameter(s):
            field: username field from the submitted form

        Output(s):
            Raises a validation error if the username is register to another user
        '''
        user = User.query.filter_by(name=field.data).first()
        if user:
            raise ValidationError("Username is taken!")

    # ==============================================================================================================
    def validate_email(self, field):
        '''
        Validate email to see if it is already registered to another user

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            Raises a validation error if the email is register to another user
        '''
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email is taken!")

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        # Check if the two passwords are the same (password and confirmation password)
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match!")
            return False
        
        return True