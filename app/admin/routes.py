from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.admin import bp

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
    admin = curr_user()
    # Check if the current user has admin privileges
    if not admin.is_admin:
        return redirect(request.referrer or url_for('main.index'))

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
        return redirect(request.referrer or url_for('main.index'))
    
    user = get_user_record(user_id=id)
    
    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=user_id)
    return render_template('./admin/view_user.html', nav_id="home-page", user=user, username=admin.name)

# ==============================================================================================================
@bp.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    '''
    Retrieves the queried data from the database for editing

    Parameter(s):
        User must be logged in

    Output(s):
        Redirects to the edit page if id is not None, else redirects to referrer or home page
    '''
    admin = curr_user()
    # Check if the current user has admin privileges
    if not admin.is_admin:
        return redirect(request.referrer or url_for('main.index'))
    
    user = get_user_record(user_id=id)

    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=id)
    return render_template('./admin/edit_user.html', nav_id="home-page", user=user, username=admin.name)

# ==============================================================================================================
@bp.route('/update_user/<int:id>', methods=['POST'])
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
        if not admin.is_admin:
            return redirect(request.referrer or url_for('main.index'))
    
        # Get all the form fields
        name = request.form.get('name', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)

        status = update_user_record(user_id=id, username=name, email=email, password=password)

        if status:
            flash("Update Successful!", "success")
        else:
            raise Exception("Update failed")        

    except Exception as e:
        LOGGER.error(f'An error occurred when updating record: {e}')
        flash("Failed to update record!", "error")

    return redirect(url_for('admin.index'))

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
            return redirect(request.referrer or url_for('auth.index'))
        
        # Query database for question and delete it
        status = delete_user_record(user_id=id)

        if status:
            flash("Successfully deleted record!", "success")
        else:
            flash("Failed to delete record", "error")
            raise Exception("Deletion failed")
            
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {str(e)}')
    
    return redirect(url_for('admin.index'))