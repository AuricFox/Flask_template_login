from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user

from app.profile import bp
from app.app_utils import LOGGER, get_current_user, update_user_record, delete_user_record
from app.forms.base_form import ProfileForm

# ==============================================================================================================
# User Profile Pages
# ============================================================================================================== 
@bp.route('/')
@login_required
def index():
    '''
    Retrieves the users profile info

    Parameter(s):
        User must be logged in

    Output(s):
        Redirects to the home page if  is None, else redirects to the user's profile page
    '''
    user = get_current_user()
    # Check if the user is logged in
    if not user:
        return redirect(url_for('auth.index'))
    
    # Get the data upon the first instance of the key
    #user = get_user_record(user_id=user_id)
    return render_template('./profile/view_profile.html', nav_id="home-page", user=user, username=user.username)

# ==============================================================================================================
@bp.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    '''
    Updates the users credentials
    
    Parameter(s): 
        User must be logged in

    Output(s):
        An html page for editing profile info if logged in or post fails, else redirects to login page
    '''
    try:
        user = get_current_user()
        if not user:
            return redirect(url_for('auth.index'))
    
        form = ProfileForm(form=request.form)
        # Check Form validation
        if form.validate_on_submit():

            status = update_user_record(
                user_id=user.id, 
                username=form.username.data, 
                email=form.email.data, 
                password=form.password.data
            )

            # Check if the profile was successfully updated
            if status:
                flash("Update Successful!", "success")
                return redirect(url_for('profile.index'))
            else:
                raise Exception("Update failed")        

    except Exception as e:
        LOGGER.error(f'An error occurred when updating record: {e}')
        flash("Failed to update record!", "error")
        
    return render_template('./profile/edit_profile.html', nav_id="home-page", user=user, username=user.username, form=form)

# ==============================================================================================================
@bp.route("/delete_profile")
@login_required
def delete_profile():
    '''
    Deletes the user's profile from the database

    Parameter(s):
        User must be logged in

    Output(s):
        None, redirects to the manage page
    '''
    try:
        user = get_current_user()
        if not user:
            return redirect(url_for('auth.index'))
        
        # Query database for question and delete it
        status = delete_user_record(user_id=user.id)

        if status:
            logout_user()
            flash("Profile deleted successfully!", "success")
            return redirect(url_for('main.index'))
        else:
            raise Exception("Deletion failed")
            
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {str(e)}')
        flash("Failed to delete profile!", "error")
    
    return redirect(url_for('profile.index'))