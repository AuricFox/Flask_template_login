import getpass, unittest
from datetime import datetime

from flask.cli import FlaskGroup

import app
from app.extensions import db
from app.models.models import Models

cli = FlaskGroup(app)

@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
    
@cli.command("add_data")
def add_data():
    '''
    Adds the user input data to the default database
    
    Parameter(s):
        name (str): a name associated with the data
        date (str): a date formatted as YYYY/MM/DD
        message (str): a message associated with the data

    Output(s):
        A message if the data was successfully added or not
    '''
    name = input("Enter a name: ")
    date_str = input("Enter a date (YYYY-MM-DD): ")
    message = input("Enter a message: ")

    if not name:
        print("Name is required!")
        return 1
    
    if not date_str:
        print("Date is required!")
        return 1
    else:
        date_str = datetime.strptime(date_str, '%Y-%m-%d')
    
    try:
        data = Models(name=name, date=date_str, message=message)
        db.session.add(data)
        db.session.commit()
        print(f"Record successfully added!")

    except Exception as e:
        print(f"Couldn't add data: {e}")
    
if __name__ == "__main__":
    cli()