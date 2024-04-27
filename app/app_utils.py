from flask_login import current_user
import logging, os, re, mimetypes

from app.models.models import User
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
def verify_file(file:str):
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
def view_user(user_id:int=None):
    '''
    Fetches the user(s) info from the database

    Parameter(s):
        user_id (int, default=None): the primary key of the user being queried

    Output(s):
        A dictionary list if user_id is None, else returns a dictionary containing the user's info
    '''
    # Get all user info
    if not user_id:
        return User.query.all()
    
    # Return the queried user's info
    return User.query.filter_by(id=user_id).first()

# =========================================================================================
def add_user(username:str, email:str, password:str, is_admin:bool=False) -> bool:
    '''
    Adds the user info to the database

    Parameter(s):

    Output(s):
        True if the user data was successfully added, else False
    '''

# =========================================================================================
def update_user(user_id:int, name:str=None, email:str=None, password:str=None, is_admin:bool=None) -> bool:
    '''
    Adds the user info to the database

    Parameter(s):

    Output(s):
        True if the user data was successfully added, else False
    '''
    try:
        # Check if the record exists
        user = User.query.get(user_id)
        if user is None: 
            return False

        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = bcrypt.generate_password_hash(password)
        if is_admin:
            user.is_admin = is_admin

        # Commit new data to the database
        db.session.commit()

    except Exception as e:
        LOGGER.error(f"An error occured when updating the user's info: {e}")
        return False
    
    return True
 
# =========================================================================================
def username() -> str:
    '''
    Gets the username of the logged in user
    
    Parameter(s): None
    
    Output(s):
        The name of the user if logged in, else None
    '''
    return current_user.name if current_user.is_authenticated else None

# =========================================================================================
def is_admin() -> bool:
    '''
    Get the admin status of the logged in user
    
    Parameter(s): None
    
    Output(s):
        True is the logged in user is an admin, alse False
    '''
    return current_user.is_admin if current_user.is_authenticated else False