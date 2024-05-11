from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError

from datetime import datetime

class DefaultForm(FlaskForm):
    '''
    NOTE: Change this to better suit your database requirements 

    A default form used for validating default data
    '''
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=50)]
    )
    date = DateField(
        "Date", format='%Y-%m-%d', validators=[Optional()]
    )
    message = TextAreaField(
        "Message", validators=[Optional(), Length(max=1000)]
    )

    # ==============================================================================================================
    def validate_date(self, field):
        """
        Custom validation to check the date format and validity

        Parameter(s):
            field: date field from the submitted form

        Output(s):
            Validation error if the date is not properly formatted
        """
        if field.data:
            try:
                date_str = field.data.strftime('%Y-%m-%d')
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                ValidationError("Invalid date format. Please use YYYY-MM-DD format!")

    # ==============================================================================================================
    def validate_message(self, field):
        """
        Custom validation to check the length of the message

        Parameter(s):
            field: message field from the submitted form

        Output(s):
            Validation error if the message length is out of bounds
        """
        if field.data:
            if len(field.data) > 1000:
                ValidationError("Message should not exceed 1000 characters!")
            if len(field.data) < 0:
                ValidationError("WTF did you do, message has negative characters!")

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(DefaultForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        return True