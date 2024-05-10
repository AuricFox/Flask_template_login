from flask import render_template
from app.main import bp
from app.app_utils import LOGGER, get_username

# ==============================================================================================================
# Main Pages
# ============================================================================================================== 
@bp.route("/")
@bp.route("/home")
def index():
    '''
    Processes home page

    Parameter(s): None

    Output(s):
        A rendered HTML home page
    '''
    return render_template('index.html', nav_id="home-page", username=get_username())