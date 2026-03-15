from flask import Blueprint
register_bp = Blueprint('register', __name__, template_folder='templates')
from . import views