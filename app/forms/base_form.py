from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Optional, Length, ValidationError, EqualTo

from app.models.user import User

class BaseUserForm(FlaskForm):
    '''
    Used for validating User credentials
    '''
    id = HiddenField(
        "ID", validators=[Optional()]
    )
    username = StringField(
        "Username", validators=[Optional(), Length(min=6, max=100)]
    )
    email = EmailField(
        "Email", validators=[Optional(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[Optional(), Length(min=8, max=100)]
    )
    confirm = PasswordField(
        "Confirm Password", validators=[Optional(), Length(min=8, max=100)]
    )

    # ==============================================================================================================
    def validate_id(self, field):
        '''
        Validates the ID to see if it is valid

        Parameter(s):
            field: id field from the submitted form

        Output(s):
            Raises validation error if the ID is invalid
        '''
        if field.data:
            user = User.query.filter_by(id=self.id.data).first()
            if not user:
                raise ValidationError("Invalid user ID!")

    # ==============================================================================================================
    def validate_username(self, field):
        '''
        Validates the username to see if it is registered to another user or not

        Parameter(s):
            field: username field from the submitted form

        Output(s):
            Raises validation error if the username is taken by another user
        '''
        if field.data:
            existing_user = User.query.filter(User.id != self.id.data, User.username == field.data).first()
            if existing_user:
                raise ValidationError("Username already exists!")

    # ==============================================================================================================
    def validate_email(self, field):
        '''
        Validate the user's email to see if it is registered to another user or not
        NOTE: This function only checks for basic email inputs in the database not real emails

        Parameter(s):
            field: email field from the submitted form

        Output(s):
            Raises a validation error if the email is taken by another user
        '''
        if field.data:
            existing_user = User.query.filter(User.id != self.id.data, User.email == field.data).first()
            if existing_user:
                raise ValidationError("Email address already exists!")

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        
        initial_validation = super(BaseUserForm, self).validate(extra_validators)
        if not initial_validation:
            return False

        if self.id.data:
            try:
                self.validate_id(self.id)
            except Exception as e:
                self.id.errors.append(str(e))
                return False
        
        # Validate username if it exists
        if self.username.data:
            try:
                self.validate_username(self.username)
            except ValidationError as e:
                self.username.errors.append(str(e))
                return False
        
        # Validate email if it exists
        if self.email.data:
            try:
                self.validate_email(self.email)
            except ValidationError as e:
                self.email.errors.append(str(e))
                return False
        
        if self.password.data or self.confirm.data:
            # Check if a password was enetered
            if not self.password.data:
                self.password.errors.append("Password is required!")
                return False
            
            # Check if a confirmation password was enetered
            if not self.confirm.data:
                self.confirm.errors.append("Confirm password is required!")
                return False

            # Check if the two passwords are the same (password and confirmation password)
            if self.password.data != self.confirm.data:
                self.confirm.errors.append("Passwords must match!")
                return False
        
        return True
# ==============================================================================================================
class ProfileForm(BaseUserForm):
    '''
    Used for validating profile information
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
# ==============================================================================================================
class RegisterForm(BaseUserForm):
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
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
# ==============================================================================================================
class UserForm(BaseUserForm):
    '''
    Used for validating User credentials for admin functionality
    '''
    id = HiddenField(
        "ID", validators=[DataRequired()]
    )
    is_admin = BooleanField(
        "Admin Privileges", validators=[Optional()]
    )