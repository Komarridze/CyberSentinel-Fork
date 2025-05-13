from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    level = db.Column(db.String(20))
    agent = db.Column(db.String(50))
    message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "agent": self.agent,
            "message": self.message,
        }
        
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50)) # e.g. "admin" or "viewer"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == "admin"