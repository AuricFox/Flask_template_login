from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.auth import bp

from app.models.models import User
from app.extensions import db, bcrypt
from app.app_utils import LOGGER

# ====================================================================
@bp.route("/", methods=['GET', 'POST'])
def index():
    '''
    Renders login/sign-up page

    Parameter(s): None

    Output(s):
        A rendered HTML login/sign-up page
    '''
    return render_template('login/login.html', nav_id="home-page", sign_up=False)

# ====================================================================
# Login/Log Out Routes
# ====================================================================  
@bp.route("/login", methods=['GET','POST'])
def login():
    '''
    Handles login protocol
    
    Parameter(s): None
    
    Output(s):
        A redirect to a HTML page
    '''
    if request.method == 'GET':
        return render_template('login/login.html', nav_id="home-page", sign_up=False)

    name = request.form.get('name', type=str)
    password = request.form.get('password', type=str)
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    # Check if the user exists
    if not user or not bcrypt.check_password_hash(user.password, password):
        flash('Incorrect username or password!')
        return redirect(url_for('auth.index'))
    
    login_user(user=user, remember=remember)
    return redirect(url_for('main.index'))

# ====================================================================
@bp.route("/log_out")
@login_required
def log_out():
    '''
    Logs user out of their account

    Parameter(s): 
        User must be logged in

    Output(s):
        Redirects to the home page
    '''
    logout_user()
    return redirect(url_for('main.index'))

# ====================================================================
# Sign Up Route
# ====================================================================
@bp.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    '''
    Configures sign up page

    Parameter(s): None

    Output(s):
        A rendered HTML sign up page
    '''
    if request.method == 'GET':
        return render_template('login/login.html', nav_id="home-page", sign_up=True)
    
    # Get form fields
    name = request.form.get('name', type=str)
    email = request.form.get('email', type=str)
    password = request.form.get('password', type=str)

    user = User.query.filter_by(email=email).first()
    # Redirect to the sign up page if the email is already taken
    if user:
        flash('Email address already exists!')
        return redirect(url_for('login.index'))
    
    # Create new user
    new_user = User(name=name, email=email, password=password)

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.index'))

# ====================================================================
# Managing User Accounts
# ====================================================================
@bp.route('/manage_users')
def manage_users():
    users = User.query.all()
    return render_template('./manage_users/manage_users.html', nav_id="manage-page", users=users)

# ==============================================================================================================
@bp.route('/view_user/<int:id>')
def view_user(id):
    '''
    Retrieves the queried data from the database for viewing

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the view page
    '''
    # Get the data upon the first instance of the key
    user = User.query.filter_by(id=id).first()
    return render_template('./manage_users/view_user.html', nav_id="manage-page", user=user)

# ==============================================================================================================
@bp.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    '''
    Retrieves the queried data from the database for editing

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the edit page
    '''
    # Get the data upon the first instance of the key
    user = User.query.filter_by(id=id).first()
    return render_template('./manage_users/edit_user.html', nav_id="manage-page", user=user)

# ==============================================================================================================

@bp.route('/update_info/<int:id>', methods=['POST'])
def update_info(id):
    '''
    Processes the new data and updates the database
    
    Parameter(s): 
        id (int): the primary key of the record being updated

    Output(s):
        None, redirects to the manage page
    '''
    try:
        # Check if the record exists
        user = User.query.get(id)

        if user is None:
            raise ValueError("Record not found.")

        # Get all the form fields
        updated_name = request.form.get('name', type=str)
        updated_email = request.form.get('email')
        updated_password = request.form.get('password', type=str)

        if updated_name:
            user.name = updated_name
        if updated_email:
            user.email = updated_email
        if updated_password:
            user.password = bcrypt.generate_password_hash(updated_password)

        # Commit new data to the database
        db.session.commit()

    except ValueError as e:
        LOGGER.error(f'Error updating record: {e}')
        flash("Error: Invalid input.", "error")

    except Exception as e:
        LOGGER.error(f'An error occurred when updating record: {e}')
        flash("Error: Something went wrong.", "error")

    return redirect(url_for('auth.manage_users'))

# ==============================================================================================================
@bp.route("/delete/<int:id>")
def delete(id):
    '''
    Deletes the queried data from the database and redirects to manage page

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the manage page
    '''
    try:
        # Query database for question and delete it
        user = User.query.filter_by(id=id).first()

        if user:
            # Delete the row data
            db.session.delete(user)
            db.session.commit()
            LOGGER.info(f'Record deleted:\n{user}')
            flash("Successfully deleted record!", "error")
        else:
            LOGGER.error(f'An error occurred when deleting record: {e}')
            flash("Failed to delete record", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {str(e)}')
    
    return redirect(url_for('auth.manage_users'))