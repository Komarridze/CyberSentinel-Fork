from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

socketio = SocketIO()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Loads your configuration class
    
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    
    # Initialize extensions
    socketio.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from .routes import main_bp
    from .auth import auth_bp
    from .chat import chat_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
