from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.auth import bp

from app.models.models import User
from app.extensions import db, bcrypt
from app.app_utils import LOGGER
from app.app_utils import get_user_record

# ==============================================================================================================
@bp.route("/", methods=['GET', 'POST'])
def index():
    '''
    Renders login/sign-up page

    Parameter(s): None

    Output(s):
        A rendered HTML login/sign-up page
    '''
    return render_template('auth/login.html', nav_id="home-page", sign_up=False)

# ==============================================================================================================
# Login/Log Out Routes
# ==============================================================================================================  
@bp.route("/login", methods=['GET','POST'])
def login():
    '''
    Handles login protocol
    
    Parameter(s): None
    
    Output(s):
        A redirect to a HTML page
    '''
    if request.method == 'GET':
        return render_template('auth/login.html', nav_id="home-page", sign_up=False)

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

# ==============================================================================================================
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

# ==============================================================================================================
# Sign Up Route
# ==============================================================================================================
@bp.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    '''
    Configures sign up page and adds user account

    Parameter(s): None

    Output(s):
        A rendered HTML sign up page
    '''
    if request.method == 'GET':
        return render_template('auth/login.html', nav_id="home-page", sign_up=True)
    
    # Get form fields
    name = request.form.get('name', type=str)
    email = request.form.get('email', type=str)
    password = request.form.get('password', type=str)
    remember = True if request.form.get('remember') else False

    if not (name and email and password):
        flash('Please Enter Required Fields!')
        return redirect(request.referrer or url_for('login.index'))

    user = User.query.filter_by(email=email).first()
    # Redirect to the sign up page if the email is already taken
    if user:
        flash('Email address already exists!')
        return redirect(request.referrer or url_for('login.index'))
    
    # Create new user
    new_user = User(name=name, email=email, password=password)

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()

    login_user(user=new_user, remember=remember)
    return redirect(url_for('main.index'))

# ==============================================================================================================
# Managing User Accounts
# ==============================================================================================================
@bp.route('/manage_users')
def manage_users():
    '''
    NOTE: Remove this function or place restrictions.
    '''
    users = get_user_record()
    return render_template('./auth/manage_users.html', nav_id="manage-user-page", users=users)