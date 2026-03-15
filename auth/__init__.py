from flask import Blueprint
# Khởi tạo Blueprint 'auth' với url_prefix để namespacing
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
# Nạp các view để gắn route vào blueprint
from . import views