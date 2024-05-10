from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.models import User

class ProfileForm(FlaskForm):
    '''
    Used for validating User registration and profile information
    '''
    id = HiddenField(
        "ID", validators=[DataRequired()]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=100)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=100)]
    )
    # NOTE: Not currently implemented for registration
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match."),
        ]
    )

    # ==============================================================================================================
    def username_validator(self, field, username:str) -> bool:
        '''
        Validate username to see if it is already registered to another user

        Parameter(s):
            field: username field from the submitted form
            username (str): the current user's name

        Output(s):
            True if the username is not taken, else false
        '''
        if username != field.data:
            return False if User.query.filter_by(name=field.data).first() else True
        
        return True
    
    # ==============================================================================================================
    def email_validator(self, field, email:str) -> bool:
        '''
        Validate email to see if it is already registered to another user

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            True if the email is not taken by another user, else false
        '''
        if email != field.data:
            return False if User.query.filter_by(email=field.data).first() else True
        
        return True

    # ==============================================================================================================
    def validate(self, extra_validators=None) -> bool:
        '''
        Validates the submitted form data
        '''
        initial_validation = super(ProfileForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        user = User.query.filter_by(id=self.id.data).first()
        if not user:
            self.id.errors.append("User ID does not exist!")
            return False

        # Check if the username exists
        if not self.username_validator(field=self.username, username=user.name):
            self.username.errors.append("Username already Exists!")
            return False

        # Check if the email exists
        if not self.email_validator(field=self.email, email=user.email):
            self.email.errors.append("Email already Exists!")
            return False

        # Check if the two passwords are the same (password and confirmation password)
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match!")
            return False

        return True