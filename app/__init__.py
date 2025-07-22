from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from app.models import db
import os

# db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Use psycopg directly in the DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgresql://', 'postgresql+psycopg://')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'options': '-c timezone=UTC'
        }
    }

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, async_mode='gevent')
    csrf.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.document import doc_bp
    from app.routes.home import home_bp
    from app.sockets.document_socket import register_socket_handlers

    from app.models.user import User  # Import User model
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    socketio.init_app(app, async_mode='gevent')
    csrf.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(doc_bp, url_prefix='/doc')
    app.register_blueprint(home_bp)
    register_socket_handlers(socketio)

    with app.app_context():
        db.create_all()

    return app, socketio