from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import Optional, Length

from app.models.models import User

class UserForm(FlaskForm):
    '''
    Used for validating User credentials for admin functionality
    '''
    username = StringField(
        "Username", validators=[Optional(), Length(min=6, max=100)]
    )
    email = EmailField(
        "Email", validators=[Optional(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[Optional(), Length(min=8, max=100)]
    )
    is_admin = BooleanField(
        "Admin Privileges", validators=[Optional()]
    )

    # ==============================================================================================================
    def email_validator(self, field):
        '''
        Validate email to see if it is registered

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            True if the email is registered, else false
        '''
        return True if User.query.filter_by(email=field.data).first() else False

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(UserForm, self).validate(extra_validators)
        if not initial_validation:
            return False
    
        # Check if the email exists
        if not self.email_validator(self.email):
            self.email.errors.append("Invalid Email")
            return False
        
        return True