from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.auth import bp

from app.models.models import User
from app.extensions import db, bcrypt
from app.app_utils import LOGGER, curr_user, get_user_record, update_user_record, delete_user_record

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
    admin = curr_user().is_admin
    # Check if the current user has admin privileges
    if not admin:
        return redirect(request.referrer or url_for('main.home'))

    users = get_user_record()
    return render_template('./admin/manage_users.html', nav_id="manage-user-page", users=users)

# ==============================================================================================================
@bp.route('/view_user')
@login_required
def view_user():
    '''
    Retrieves the users profile info

    Parameter(s):
        User must be logged in

    Output(s):
        Redirects to the home page if id is None, else redirects to the user's profile page
    '''
    user = curr_user()
    if not user:
        return redirect(request.referrer or url_for('main.index'))
    
    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=user_id)
    return render_template('./profile/view_profile.html', nav_id="home-page", user=user, username=user.name)

# ==============================================================================================================
@bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    '''
    Retrieves the queried data from the database for editing

    Parameter(s):
        User must be logged in

    Output(s):
        Redirects to the edit page if id is not None, else redirects to referrer or home page
    '''
    user = curr_user()
    if not user:
        return redirect(request.referrer or url_for('auth.index'))

    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=id)
    return render_template('./profile/edit_profile.html', nav_id="home-page", user=user, username=user.name)

# ==============================================================================================================
@bp.route('/update_user', methods=['POST'])
@login_required
def update_user():
    '''
    Processes the new data and updates the database
    
    Parameter(s): 
        id (int): the primary key of the record being updated

    Output(s):
        None, redirects to the manage page
    '''
    try:
        user_id = curr_user().id
        if not user_id:
            return redirect(request.referrer or url_for('auth.index'))
    
        # Get all the form fields
        name = request.form.get('name', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)

        status = update_user_record(user_id=user_id, username=name, email=email, password=password)

        if status:
            flash("Update Successful!", "success")
        else:
            raise Exception("Update failed")        

    except Exception as e:
        LOGGER.error(f'An error occurred when updating record: {e}')
        flash("Failed to update record!", "error")

    return redirect(url_for('auth.manage_users'))

# ==============================================================================================================
@bp.route("/delete_user")
@login_required
def delete_user():
    '''
    Deletes the user's profile from the database

    Parameter(s):
        User must be logged in

    Output(s):
        None, redirects to the manage page
    '''
    try:
        user_id = curr_user().id
        if not user_id:
            return redirect(request.referrer or url_for('auth.index'))
        
        # Query database for question and delete it
        status = delete_user_record(user_id=user_id)

        if status:
            flash("Successfully deleted record!", "success")
        else:
            flash("Failed to delete record", "error")
            raise Exception("Deletion failed")
            
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {str(e)}')
    
    return redirect(url_for('auth.manage_users'))