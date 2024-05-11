from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

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
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match."),
        ]
    )

    # ==============================================================================================================
    def validate_username(self, field):
        '''
        Validates the username to see if it is registered to another user or not

        Parameter(s):
            field: username field from the submitted form

        Output(s):
            Raises validation error if the username is taken by another user
        '''
        existing_user = User.query.filter(User.id != self.id.data, User.name == field.data).first()
        if existing_user:
            raise ValidationError("Username already exists!")

    # ==============================================================================================================
    def validate_email(self, field):
        '''
        Validate the user's email to see if it is registered to another user or not

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            Raises a validation error if the email is taken by another user
        '''
        existing_user = User.query.filter(User.id != self.id.data, User.email == field.data).first()
        if existing_user:
            raise ValidationError("Email address already exists!")
        
    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(ProfileForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        user = User.query.filter_by(id=self.id.data).first()
        if not user:
            self.id.errors.append("Invalid user ID!")
            return False

        # Check if the two passwords are the same (password and confirmation password)
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match!")
            return False

        return True