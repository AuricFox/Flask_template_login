from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import bp

from app.models.models import User
from app.extensions import db, bcrypt
from app.app_utils import LOGGER

from app.forms.register_form import RegisterForm
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
        return redirect(request.referrer or url_for('main.index'))
    
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
    # Redirect to the calling page or home page if the user is logged in
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('main.index'))
    # Render the login page
    if request.method == 'GET':
        return render_template('auth/login.html', nav_id="home-page", sign_up=False)
    
    # Get form data and varify contents
    form = LoginForm(request.form)
    if not form.validate_on_submit():
        return render_template('auth/login.html', nav_id="home-page", sign_up=False, form=form)
    
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=form.username.data).first()

    # Check if the user exists and if the hashed passwords match
    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
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
    form = RegisterForm(request.form)
    remember = True if request.form.get('remember') else False

    if not form.validate_on_submit():
        return render_template('auth/login.html', nav_id="home-page", sign_up=True, form=form)
    
    # Create new user
    new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()

    login_user(user=new_user, remember=remember)
    return redirect(url_for('main.index'))