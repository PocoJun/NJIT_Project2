# models.py
import flask_sqlalchemy
from app import db

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    message_id = db.Column(db.Integer, db.ForeignKey('user_info.id')) #add message Id user
    
    def __init__(self, a, b):
        self.message = a
        self.message_id = b

        
    def __repr__(self):
        return (
            '<message: %s>' % self.message,
            '<message_id: %s>' % self.message_id
            )
        

# user information database(email, user, picture)
class user_info(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000), unique=True)
    user = db.Column(db.String(1000), unique=True)
    picture = db.Column(db.String(1000), unique=True)
    
    def __init__(self, a, b, c):
        
        self.email = a
        self.user = b
        self.picture = c

        
    def __repr__(self):
        
        return {
            
            '<email: %s>' % self.email,
            '<user: %s>' % self.user,
            '<picture: %s>' % self.picture
            
            }
