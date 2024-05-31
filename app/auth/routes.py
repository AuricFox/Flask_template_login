from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import bp

from app.models.user import User
from app.extensions import db, bcrypt
from app.app_utils import LOGGER

from app.forms.base_form import RegisterForm
from app.forms.login_form import LoginForm

# ==============================================================================================================
@bp.route("/", methods=['GET', 'POST'])
def index():
    '''
    Renders login/sign-up page

    Parameter(s): None

    Output(s):
        A HTML login/sign-up page if the user is not logged in, else redirects to the home page or calling page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return redirect(url_for('auth.login'))

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
    try:
        # Redirect to the calling page or home page if the user is logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        # Get form data and varify contents
        login_form = LoginForm(request.form)
        if login_form.validate_on_submit():

            user = User.query.filter_by(username=login_form.username.data).first()

            # Check if the user exists and if the hashed passwords match
            if user and bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user=user)
                return redirect(url_for('main.index'))
        
            flash('Invalid username or password!', 'login_error')
    
    except Exception as e:
        LOGGER.error(f"An error occurred when logging in: {e}")
        flash("Login Failed!", "login_error")

    register_form = RegisterForm(request.form)
    return render_template('auth/login.html', nav_id="home-page", sign_up=False, login_form=login_form, register_form=register_form)

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
    try:
        # Redirect to the calling page or home page if the user is logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        # Get form fields
        register_form = RegisterForm()

        # Process data if valid
        if register_form.validate_on_submit():
            # Create new user
            new_user = User(
                username=register_form.username.data, 
                email=register_form.email.data, 
                password=register_form.password.data
            )

            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()

            login_user(user=new_user)
            return redirect(url_for('main.index'))
    
    except Exception as e:
        LOGGER.error(f"An error occurred when registering account: {e}")
        flash("Failed to register account!", "register_error")
    
    # Form is not submitted yet or validation failed, render sign-up page
    login_form = LoginForm()
    return render_template('auth/login.html', nav_id="home-page", sign_up=True, register_form=register_form, login_form=login_form)