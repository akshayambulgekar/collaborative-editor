# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from .config import Config
from .models import db
from .routes.auth import auth_bp
from .routes.document import doc_bp
from .sockets.document_socket import init_sockets

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(doc_bp, url_prefix='/doc')
    init_sockets(socketio)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app, socketio