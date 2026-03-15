from flask import Blueprint
articles_bp = Blueprint('articles', __name__, url_prefix='/articles')
from . import views