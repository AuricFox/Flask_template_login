from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required

from app.admin import bp
from app.models.models import User

from app.forms.user_form import UserForm
from app.app_utils import LOGGER, curr_user, get_user_record
from app.extensions import bcrypt, db

# ==============================================================================================================
# Managing User Accounts
# ==============================================================================================================
@bp.route('/')
@login_required
def index():
    '''
    Consrtucts a dashboard for managing users

    Parameter(s):
        Current user must be logged in and have admin privileges

    Output(s):
        A HTML template with all the registered users
    '''
    admin = curr_user()
    # Check if the current user has admin privileges
    if not admin.is_admin:
        return redirect(url_for('main.index'))

    users = get_user_record()
    return render_template('./admin/manage_users.html', nav_id="manage-user-page", users=users, username=admin.name)

# ==============================================================================================================
@bp.route('/view_user/<int:id>')
@login_required
def view_user(id):
    '''
    Retrieves the users profile info

    Parameter(s):
        id (int): the queried user's primary key

    Output(s):
        Redirects to the home page if id is None, else redirects to the user's profile page
    '''
    admin = curr_user()
    # Check if the current user has admin privileges
    if not admin.is_admin:
        return redirect(url_for('main.index'))
    
    user = get_user_record(user_id=id)
    
    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=user_id)
    return render_template('./admin/view_user.html', nav_id="home-page", user=user, username=admin.name)

# ==============================================================================================================
@bp.route('/update_user/<int:id>', methods=['GET','POST'])
@login_required
def update_user(id):
    '''
    Processes the new data and updates the database
    
    Parameter(s): 
        id (int): the queried user's primary key

    Output(s):
        None, redirects to the manage page
    '''
    try:
        admin = curr_user()
        # Check if the user has admin access
        if not admin.is_admin:
            return redirect(url_for('main.index'))
        
        user = User.query.get(id)
        # Check if the user record exists
        if user is None:
            raise Exception(f"User ID '{id}' not found.")
        
        form = UserForm(form=request.form)
        if form.validate_on_submit():

            if form.username.data:
                user.name = form.username.data
            if form.email.data:
                user.email = form.email.data
            if form.password.data:
                user.password = bcrypt.generate_password_hash(form.password.data)
            if form.is_admin.data is not None:
                user.is_admin = form.is_admin.data

            # Commit new data to the database
            db.session.commit()
            
            flash("Updated Successfully!")
            return redirect(url_for('admin.index'))

    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        LOGGER.error(f"An error occurred when updating user record: {e}")
        flash("Failed to update record!", "error")

    return render_template('./admin/edit_user.html', nav_id="home-page", user=user, username=admin.name, form=form)

# ==============================================================================================================
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    '''
    Deletes the user's profile from the database

    Parameter(s):
        id (int): the queried user's primary key

    Output(s):
        None, redirects to the manage page
    '''
    try:
        admin = curr_user()
        if not admin.is_admin:
            return redirect(url_for('auth.index'))
        
        # Query database for question and delete it
        user = User.query.filter_by(id=id).first()

        if user:
            # Delete the row data
            db.session.delete(user)
            db.session.commit()

            LOGGER.info(f"User ID '{id}' successfully deleted.")
            flash("User record successfully deleted!")
            
    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        LOGGER.error(f"An Error occured when deleting the record: {str(e)}")
    
    return redirect(url_for('admin.index'))