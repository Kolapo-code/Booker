from flask import Blueprint

app_views = Blueprint('routes', __name__, url_prefix='/api')

from app.views.sign_up import *
