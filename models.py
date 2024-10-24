from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone

db = SQLAlchemy()
bcrypt = Bcrypt()
class  User(db.Model):
    __tablename__='users'
    
    user_id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password =db.Column(db.Text,nullable = False) 
    email =db.Column(db.String(50), nullable = False, unique = True)
    first_name=db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)


    def __repr__(self):
      return f"<User {self.username}>"
    

    @classmethod 
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username = username, password = hashed_utf8)
   
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        
class  Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id=db.Column(db.Integer,primary_key = True, autoincrement = True)
    title=db.Column(db.String(100),nullable =False,  )
    content=db.Column(db.Text, nullable = False, )
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now(timezone.utc))
    username=db.Column(db.String(20),db.ForeignKey('users.username'),nullable =False)

    user = db.relationship('User', backref= 'feedbacks')