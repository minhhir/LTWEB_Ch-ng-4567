
from flask import Blueprint
scores_bp = Blueprint('scores', __name__, url_prefix='/scores')
from . import views