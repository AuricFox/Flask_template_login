from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required

from app.admin import bp
from app.models.user import User

from app.forms.base_form import UserForm
from app.app_utils import LOGGER, get_current_user, get_user_record
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
    try:
        admin = get_current_user()
        # Check if the current user has admin privileges
        if not admin.is_admin:
            return render_template('404.html'), 404

        users = get_user_record()
        return render_template('./admin/manage_users.html', nav_id="manage-user-page", users=users, username=admin.username)

    except Exception as e:
        LOGGER.error(f"An error occurred when accessing admin page: {e}")
        return redirect(url_for('main.index'))

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
    try:
        admin = get_current_user()
        # Check if the current user has admin privileges
        if not admin.is_admin:
            return render_template('404.html'), 404

        # Get the data upon the first instance of the key
        user = get_user_record(user_id=id)
        return render_template('./admin/view_user.html', nav_id="home-page", user=user, username=admin.username)
    
    except Exception as e:
        LOGGER.error(f"An error occurred when viewing info on user {id}: {e}")
        return render_template('404.html'), 404

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
        admin = get_current_user()
        # Check if the user has admin access
        if not admin.is_admin:
            return render_template('404.html'), 404
        
        user = User.query.get(id)
        # Check if the user record exists
        if user is None:
            return render_template('404.html'), 404
        
        form = UserForm(form=request.form)
        if form.validate_on_submit():

            if form.username.data:
                user.username = form.username.data
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

    return render_template('./admin/edit_user.html', nav_id="home-page", user=user, username=admin.username, form=form)

# ==============================================================================================================
@bp.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    '''
    Deletes the user's profile from the database

    Parameter(s):
        id (int): the queried user's primary key

    Output(s):
        None, redirects to the manage page
    '''
    try:
        admin = get_current_user()
        if not admin.is_admin:
            return render_template('404.html'), 404
        
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
        flash("Failed to delete user record!")
    
    return redirect(url_for('admin.index'))