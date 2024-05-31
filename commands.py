from getpass import getpass
import unittest, click
from datetime import datetime

from flask.cli import FlaskGroup

import app
from app.extensions import db
from app.models.user import User
from app.models.default import Default_Model

cli = FlaskGroup(app)

# ==============================================================================================================
# TEST COMMANDS
# ==============================================================================================================
@cli.command("test")
def test():
    '''
    Runs all the unit tests
    '''
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ==============================================================================================================
@cli.command("test_routes")
@click.argument('file_name', required=False)
def test_routes(file_name):
    '''
    Runs the unit tests for routes
    '''
    if not file_name:
        tests = unittest.TestLoader().discover("tests/test_routes")
    elif file_name == 'defualt':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_defualt_routes.py")
    elif file_name == 'login':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_login_routes.py")
    elif file_name == 'profile':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_profile_routes.py")
    elif file_name == 'register':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_register_routes.py")
    elif file_name == 'user':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_user_routes.py")
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ==============================================================================================================
@cli.command("test_forms")
@click.argument('file_name', required=False)
def test_forms(file_name):
    '''
    Runs the unit tests for forms
    '''
    if not file_name:
        tests = unittest.TestLoader().discover("tests/test_forms")
    elif file_name == 'defualt':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_defualt_form.py")
    elif file_name == 'login':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_login_form.py")
    elif file_name == 'profile':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_profile_form.py")
    elif file_name == 'register':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_register_form.py")
    elif file_name == 'user':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_user_form.py")
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ==============================================================================================================
# INPUT COMMANDS
# ==============================================================================================================
@cli.command("add_admin")
def add_admin():
    '''
    Adds an admin account to the database
    
    Parameter(s):
        username (str): account user's name
        email (str): email address of the user
        password (str): account password
        confirm (str): confirmation password

    Output(s):
        A message if the data was successfully added or not
    '''
    username = input("Enter a Username: ")
    if not username:
        print("Username is required!")
        return 1

    email = input("Enter an Email Address: ")
    if not email:
        print("Email is required!")
        return 1
    
    password = getpass("Enter a Password: ")
    confirm = getpass("Confirm Password: ") 
    if password != confirm:
        print("Passwords do not match!")
        return 1
    
    try:
        user = User(username=username, email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print(f"Admin account successfully added!")

    except Exception as e:
        print(f"An error occurred when adding admin account: {e}")
# ==============================================================================================================
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
        data = Default_Model(name=name, date=date_str, message=message)
        db.session.add(data)
        db.session.commit()
        print(f"Record successfully added!")

    except Exception as e:
        print(f"An error occurred when adding data: {e}")


if __name__ == "__main__":
    cli()