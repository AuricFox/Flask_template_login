from flask import render_template, url_for, redirect, request, flash
from app.manage import bp
from app.extensions import db
from app.models.models import Models
from app.app_utils import LOGGER, sanitize, username

from datetime import datetime

# Routes for pages associated with manage page

@bp.route('/')
def index():
    data = Models.query.all()
    return render_template('./manage/manage.html', nav_id="manage-page", data=data, username=username())

# ==============================================================================================================
@bp.route('/view/<int:id>')
def view(id):
    '''
    Retrieves the queried data from the database for viewing

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the view page
    '''
    # Get the data upon the first instance of the key
    data = Models.query.filter_by(id=id).first()
    return render_template('./manage/view.html', nav_id="manage-page", data=data, username=username())

# ==============================================================================================================
@bp.route('/add')
def add():
    '''
    Generates add new data page

    Parameter(s): None

    Output(s):
        returns add.html page
    '''
    return render_template('./manage/add.html', nav_id="add-page", username=username())

# ==============================================================================================================
@bp.route('/add_info', methods=['POST'])
def add_info():
    '''
    Processes the new data and adds it to the database
    
    Parameter(s): None

    Output(s):
        None, redirects to the manage page
    '''
    try:
        # Get all the form fields
        name = sanitize(request.form.get('name', type=str))
        date_str = request.form.get('date')
        message = request.form.get('message', type=str)

        if not (name and date_str):
            raise ValueError("Name and Date fields are required.")
        
        # Convert date string to datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Adding and commit new data to the database
        new_info = Models(name=name, date=date, message=message)
        db.session.add(new_info)
        db.session.commit()

    except ValueError as e:
        LOGGER.error(f'Error adding new info: {e}')
        flash("Error: Invalid input.", "error")

    except Exception as e:
        LOGGER.error(f'An error occurred when adding the new info: {e}')
        flash("Error: Something went wrong.", "error")

    return redirect(url_for('manage.index'))

# ==============================================================================================================
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    '''
    Retrieves the queried data from the database for editing

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the edit page
    '''
    # Get the data upon the first instance of the key
    data = Models.query.filter_by(id=id).first()
    return render_template('./manage/edit.html', nav_id="manage-page", data=data, username=username())

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
        data = Models.query.get(id)

        if data is None:
            raise ValueError("Record not found.")

        # Get all the form fields
        updated_name = sanitize(request.form.get('name', type=str))
        updated_date_str = request.form.get('date')
        updated_message = request.form.get('message', type=str)
        
        # Parse and validate the updated date
        if updated_date_str:
            updated_date = datetime.strptime(updated_date_str, '%Y-%m-%d').date()
            data.date = updated_date

        if updated_name:
            data.name = updated_name
        if updated_message:
            data.message = updated_message

        # Commit new data to the database
        db.session.commit()

    except ValueError as e:
        LOGGER.error(f'Error updating record: {e}')
        flash("Error: Invalid input.", "error")

    except Exception as e:
        LOGGER.error(f'An error occurred when updating record: {e}')
        flash("Error: Something went wrong.", "error")

    return redirect(url_for('manage.index'))

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
        data = Models.query.filter_by(id=id).first()

        if data:
            # Delete the row data
            db.session.delete(data)
            db.session.commit()
            LOGGER.info(f'Record deleted:\n{data}')
            flash("Successfully deleted record!", "error")
        else:
            LOGGER.error(f'An error occurred when deleting record: {e}')
            flash("Failed to delete record", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the record: {str(e)}')
    
    return redirect(url_for('manage.index'))