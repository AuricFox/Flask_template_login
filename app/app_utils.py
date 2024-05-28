from flask_login import current_user
import logging, os, re, mimetypes

from app.models.user import User
from app.extensions import db, bcrypt

PATH = os.path.dirname(os.path.abspath(__file__))

# Configure the logging object
logging.basicConfig(
    filename=os.path.join(PATH, '../logs/app.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

LOGGER = logging.getLogger(__name__)

# =========================================================================================
# Error Handling
# =========================================================================================
class InvalidFile(Exception): pass
class FileNotFound(Exception): pass
class InvalidInput(Exception): pass

# =========================================================================================
def sanitize(text:str) -> str:
    '''
    Removes special characters from the string.

    Parameter(s):
        text (str): the string being sanitized

    Output(s):
        str: a sanitized string
    '''
    return re.sub(r'[\\/*?:"<>|]', '_', text)

# =========================================================================================
def verify_file(file:str) -> bool:
    '''
    Verifies input file

    Parameter(s):
        file (str): name of the provided file

    Output(s):
        True if the file is valid, else False
    '''
    try:
        # Replace special characters with underscores
        sanitized_name = re.sub(r'[\\/*?:"<>| ]', '_', file)
        # Remove leading and trailing whitespace
        sanitized_name = sanitized_name.strip()
        # Getting the name of the file without the extension
        sanitized_name = sanitized_name.split('.')[0]

        allowed_mime_types = ['application/json']
        allowed_extensions = ['.json']

        # Get the file's MIME type and extension
        file_mime_type, _ = mimetypes.guess_type(file)
        file_extension = os.path.splitext(file)[1].lower()

        # Check if the file's MIME type or extension is allowed
        if file_mime_type is not None and file_mime_type not in allowed_mime_types:
            LOGGER.error(f'{file} MIME type is not supported! MIME type: {file_mime_type}')
            return False

        if file_extension not in allowed_extensions:
            LOGGER.error(f'{file} extension is not supported! Extension: {file_extension}')
            return False
        
        return True

    except Exception as e:
        LOGGER.error(f"An error occured when validating {file}: {e}")
        return False

# =========================================================================================
def get_user_record(user_id:int=None):
    '''
    Fetches the user(s) info from the database

    Parameter(s):
        user_id (int, default=None): the primary key of the user being queried

    Output(s):
        A list of User objects if user_id is None (all users), else returns a User object containing the user's info
    '''
    try:
        # Get all user info
        if not user_id:
            return User.query.all()

        # Return the queried user's info
        return User.query.filter_by(id=user_id).first()
    
    except Exception as e:
        LOGGER.error(f"An error occurred when retrieving user(s) info: {e}")
        return None

# =========================================================================================
def add_user_record(username:str, email:str, password:str, is_admin:bool=False) -> bool:
    '''
    Adds the user info to the database

    Parameter(s):
        username (str): User's name
        email (str): User's email address
        password (str): User's password
        is_admin (bool, default=False): Whether the user is an admin

    Output(s):
        True if the user data was successfully added, else False
    '''
    try:
        user = User.query.filter_by(email=email).first()
        # Redirect to the sign up page if the email is already taken
        if user:
            LOGGER.warning(f"Email '{email}' is already taken.")
            return False

        # Create new user
        new_user = User(name=username, email=email, password=password, is_admin=is_admin)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        LOGGER.info(f"User '{username}' added successfully.")
        return True

    except Exception as e:
        LOGGER.error(f"An error occurred when adding user info: {e}")
        return False

# =========================================================================================
def update_user_record(user_id:int, username:str=None, email:str=None, password:str=None, is_admin:bool=None) -> bool:
    '''
    Adds the user info to the database

    Parameter(s):
        user_id (int): User's primary key
        username (str, default=None): User's new name
        email (str, default=None): User's new email address
        password (str, default=None): User's new password
        is_admin (bool, default=None): Whether the user should be an admin

    Output(s):
        True if the user data was successfully added, else False
    '''
    try:
        # Check if the record exists
        user = User.query.get(user_id)
        if user is None:
            LOGGER.warning(f"User ID '{user_id}' not found.")
            return False

        if username:
            user.name = username
        if email:
            user.email = email
        if password:
            user.password = bcrypt.generate_password_hash(password)
        if is_admin is not None:
            user.is_admin = is_admin

        # Commit new data to the database
        db.session.commit()

        LOGGER.info(f"User '{user_id}' successfully updated.")
        return True

    except Exception as e:
        LOGGER.error(f"An error occured when updating the user's info: {e}")
        return False

# =========================================================================================
def delete_user_record(user_id:int) -> bool:
    '''
    Deletes user record from the database
    
    Parameter(s):
        user_id (int): the primary key of the user

    Output(s):
        True if the user record is successfully deleted, else False
    '''
    try:
        # Query database for question and delete it
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Delete the row data
            db.session.delete(user)
            db.session.commit()

            LOGGER.info(f"User ID '{user_id}' successfully deleted.")
            return True

        else:
            LOGGER.error(f"User ID '{user_id}' not found.")
            return False
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {e}')
        return False

# =========================================================================================
def get_current_user():
    '''
    Gets the info of the current user that's logged in
    
    Parameter(s): None
    
    Output(s):
        A User object if logged in, else None
    '''
    return current_user if current_user.is_authenticated else None
   
# =========================================================================================
def get_username() -> str:
    '''
    Gets the username of the logged in user
    
    Parameter(s): None
    
    Output(s):
        The name of the user if logged in, else None
    '''
    return current_user.name if current_user.is_authenticated else None