from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length

class DefaultForm(FlaskForm):
    '''
    NOTE: Change this to better suit your database requirements 

    A default form used for validating default data
    '''
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=6, max=50)]
    )
    date = DateField(
        "Date"
    )
    message = StringField(
        "Message"
    )