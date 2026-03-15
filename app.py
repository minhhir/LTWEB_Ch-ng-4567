from flask import Flask, render_template
from auth import auth_bp
from articles import articles_bp
from scores import scores_bp
from products import products_bp
from register import register_bp
from cart import cart_bp
from admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '@HoangNangMinh11112005'

    app.register_blueprint(auth_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(scores_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)
    @app.route('/')
    def index():
        return render_template('base.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5050)