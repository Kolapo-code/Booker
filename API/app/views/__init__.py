from flask import Blueprint

app_views = Blueprint("routes", __name__, url_prefix="/api")

from app.views.administration import *

from app.views.sign_up import *
from app.views.login import *
from app.views.profile import *
from app.views.appointement import *
from app.views.workspace import *
from app.views.review import *
from app.views.reclaim import *
