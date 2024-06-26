# Flask Template with Login

A Flask template used for starting web projects that supports user registration and login. It provides basic navigation for main pages, sub pages, and a side bar for related topics. The database is maintained using SQLAlchemy which currently supports a default table called Models and a User table.

![Home Page](home_page.jpg "Home Page")

## Getting Started

To get started, follow these steps:

1. **Clone the Repository:**
    ```
    git clone https://github.com/AuricFox/Flask_template_login.git
    ```

2. **Navigate to the Project Directory:**
    ```
    cd Flask_template_login
    ```

3. **Setup Environment:**  
    Windows:
    ```
    pip install virtualenv  
    virtualenv env
    .\env\Scripts\activate
    ```  

    macOS:
    ```
    pip install virtualenv  
    virtualenv env
    source env/bin/activate
    ```    

    NOTE: Remaining steps are done in the activated environment.

4. **Install Dependencies:**
    ```
    pip install Flask Flask-Login Flask-Bcrypt FLask-WTF Flask-SQLAlchemy Flask-Testing python-dotenv
    ```
    * **Flask:** a python framework for building web applications.
    * **Flask-Login:** provides user session management for Flask such as logging in or out.
    * **Flask-Bcrypt:** a Flask extension for hashing passwords.
    * **Flask-WTF:** an extension that handles forms and CSRF tokens.
    * **Flask-SQLAlchemy:** a Flask extension that simplifies database queries and management.
    * **Flask-Testing:** an extension that provides unit testing utilities for Flask.
    * **Python-Dotenv:** allows use of environment variables in python projects.

## Running Server
```
python wsgi.py
```

The server will start running, and you can access the application by navigating to `http://localhost:5000` in your web browser.

## Export Secret Key and Database URI
Note: Use `set` for windows and `export` for macOS.
```
set SECRET_KEY="your secret key"
set DATABASE_URI="postgresql://username:password@host:port/database_name"
```

Check if the Secret Key was set:
```
echo %SECRET_KEY%  # Windows
```
```
echo $SECRET_KEY   # Unix-like
```

## Adding an Admin Account From the Terminal

To add an admin account execute the following command from the base directory:

```
python commands.py add_admin
```

You will be prompted to add a Username, email, and password.


## Running Tests

All the test scripts are located it the `tests` directory. They enable you to test the routes, models, and user inputs. To run the tests, 
execute the following command in the terminal from the base directory:

```
python commands.py test
```

You should see all the tests being executed followed by the number of tests run and the status. Form and Route test can be run individually 
by executing one of the following commands:
```
python commands.py test_forms
```
```
python commands.py test_routes
```

## File Structure

NOTE: All non-relavent files like `__pycache__` and env files have been removed from the file tree. Image files 
have also been removed to reduce clutter.

```
.
Flask_template_login
├───app
│   ├───admin
│   │   ├───__init__.py
|   |   └───routes.py
│   ├───auth
│   │   ├───__init__.py
|   |   └───routes.py
│   ├───forms
│   │   ├───default_form.py
│   │   ├───login_form.py
│   │   ├───profile_form.py
│   │   ├───register_form.py
|   |   └───user_form.py
│   ├───main
│   │   ├───__init__.py
|   |   └───routes.py
│   ├───manage
│   │   ├───__init__.py
|   |   └───routes.py
│   ├───models
│   │   ├───default.py
│   │   └───user.py
│   ├───profile
│   │   ├───__init__.py
|   |   └───routes.py
│   ├───static
│   │   ├───css
|   |   |   ├───base.css
|   |   |   └───login.css
│   │   ├───images
│   │   │   └───icons
|   |   |       └───...
│   │   └───js
|   |       └───base.js
│   ├───templates
|   |    ├───admin
|   |    |   ├───edit_user.html
|   |    |   ├───manage_users.html
|   |    |   └───view_user.html
|   |    ├───auth
|   |    |   └───login.html
│   |    ├───manage
|   |    |   ├───add.html
|   |    |   ├───edit.html
|   |    |   ├───manage.html
|   |    |   └───view.html
│   |    ├───profile
|   |    |   ├───edit_profile.html
|   |    |   └───view_profile.html
|   |    ├───404.html
|   |    ├───base.html
|   |    └───index.html
|   ├───__init__.py
|   ├───app_utils.py
|   └───extensions.py
├───data
|   ├───app_test.db
|   └───app.db
├───env
│   └───...
├───logs
|   └───app.log
├───tests
|   └───...
├───.gitignore
├───commands.py
├───config.py
├───LICENSE
├───README.md
└───wsgi.py
```

## Directories

- **forms**: Contains the FlaskWTF form classes used to verify data submittions.
- **models**: Maintians separation of SQLAlchemy models for large applications. As projects grow, more database tables may be added and more models will need to be wriiten. Splitting the models into individual files will help with management and maintenance.
- **static**: Contains all the css, js, and image files which are stored in their corresponding directory.
- **templates**: Maintains the organization of the HTML files that provide structure for the web pages.
- **data**: Contains the database and any other possible data management files such as JSON files.
- **logs**: Stores the logging information of the application. Logs info, warnings, and errors as they arise.
- **tests**: Contains all the test cases for the application.
- **other**: Any remaining directories (main, etc.) manages the applications blueprints and routes. These enable the end-user to navigate the 
application or website.

## Files

- **commands.py**: Enables command-line entries for adding accounts and data.
- **config.py**: Configuration file for the Flask application that manages the settings. It configures the `secret key`, `SQLAlchemy database URI`, and more.
- **wsgi.py**: A mediator between the web server and Python web application. Runs the overall application.
- **extensions.py**: Manages the flask extensions like SQLAlchemy.

## Database Info

### Current Database Schema:

**User**  
|**id**|name   |email   |password |created_on |is_admin |
|:-----:|:----:|:------:|:-------:|:---------:|:-------:|

- **Primary Key:** id 
- All feilds are none nullable

**Models**  
|**id**|name   |date   |message |
|:-----:|:----:|:-----:|:------:|

- **Primary Key:** id 

### Data Type(s):

- **Integer**: integer column
- **String**: string column with fixed length
- **Text**: string column with variable length
- **Boolean**: boolean column
- **Float**: floating point column
- **Numeric**: numeric column with fixed-point precision
- **DateTime**: datetime column
- **Date**: date column
- **Time**: time column
- **Interval**: time interval column
- **JSON**: JSON column (support limited)
- **Enum**: enumerated values column

### Parameter(s):
- **primary_key (bool)**: indicates the variable is a primary key
- **nullable (bool)**: indicates if the value can be null or not
- **length (int)**: length of a string column
- **precision (int)**: total number of digits that can be stored in a column (before and after the decimal point)
- **scale (int)**: number of digits that can be store to the right of the decimal point
- **unique (bool)**: states whether a column must have unique values
- **default (int)**: specifies a default value for a column
- **autoincrement (bool)**: specifies whether a column should auto-increment its vlaue
- **index (bool)**: indecates wheater a index should be created for the column
- **Check (function)**: checks contraint for the column's values
- **server_deault (str)**: specifies a server-side default value for the column

Example:
```
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, db.CheckConstraint('length(name) > 0'))
    cost = db.Column(db.Numeric(precision=10, scale=2))
    code = db.Column(db.String(50), unique=True)
    score = db.Column(db.Integer, default=0)
```

### Creating Tables

The tables have not yet been added to the database and need to be created.

1. Open the Flask shell to create a table:  
```
flask shell
```

2. Run the folling code to create the table:  
```
from app.extensions import db
from app.models.user import User
from app.models.default import Default_Model
db.create_all()
```

3. To Update or Delete tables:
```
db.drop_all()
db.create_all()
```

4. Run the following code to exit:  
```
exit()
```

## Helpful Resources
- [How To Structure a Large Flask Application with Flask Blueprints and Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy)
- [Demystifying Flask’s “Application Factory”](https://hackersandslackers.com/flask-application-factory/)  
- [User Session Data with Flask-Session & Redis](https://hackersandslackers.com/flask-user-sessions-and-redis/)  
- [Configuring Your Flask App](https://hackersandslackers.com/configure-flask-applications/)  
- [Configuration Handling](https://flask.palletsprojects.com/en/3.0.x/config/#configuration-handling)
- [How to Set Up Basic User Authentication in a Flask App](https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.
