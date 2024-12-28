from App import db,manager
from datetime  import datetime
from flask import current_app
from faker import Faker 
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as serializer
from flask_login import UserMixin

@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),unique=True)
    phonenumber=db.Column(db.String(20))
    tickets=db.relationship('Ticket',backref='user',lazy='dynamic')
    role=db.relationship('Roles',backref='user',lazy='dynamic')
    password_hash=db.Column(db.String(200))


    @property
    def password(self):
        raise AttributeError('Password is not readable')
        
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
   
    def generate_token(self,salt='token'):
        s=serializer(current_app.config['SECRET_KEY'],salt=salt)
        sam=s.dumps({'user_id':self.id})
        return sam
    
    @staticmethod
    def verify_token(token,max_age=int):
        s=serializer(current_app.config['SECRET_KEY'])
        try:
            sam=s.loads(token,max_age,salt='token')['user_id']
        except:
            return None
        return User.query.get(sam)
    # @staticmethod
    # def fakeusers(count=5):
    #     fake=Faker()
    #     i=0
    #     while i < count:
    #         user=User(
    #             name=fake.user_name(),
    #             email=fake.email(),
    #             phonenumber=fake.phone_number()
    #         )
    #         db.session.add(user)
    #         try:
    #             db.session.commit()
    #             i+=1
    #         except IntegrityError:
    #             db.session.rollback()

    def __repr__(self):
        return f"User<<'{self.name}','{self.email}','{self.phonenumber}'>>"

class Ticket(db.Model):
    __tablename__='ticket'
    id=db.Column(db.Integer,primary_key=True)
    ticket_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    start_point=db.Column(db.String(20),nullable=False)
    destination=db.Column(db.String(20),nullable=False)
    seat_number=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    derpeture_time=db.Column(db.String(20))
    places=db.relationship('Routes',backref='place',lazy='dynamic')
    

    #ticket assigment permissions
    

    def __repr__(self):
        return f"Ticket('{self.ticket_id}','{self.start_point}','{self.destination}','{self.date}')"


class Routes(db.Model):
    __tablename__='routes'

    Route_id=db.Column(db.Integer,db.ForeignKey('ticket.ticket_id'),primary_key=True)
    name=db.Column(db.String(20))
    distance=db.Column(db.String(20))
    discription=db.Column(db.String(20))


class Roles(db.Model):
    __tablename__='roles'

    id=db.Column(db.Integer,primary_key=True)
    ticket_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    name=db.Column(db.String(20))
    Permit=db.Column(db.Integer)


class Seats(db.Model):
    __tablename__='seats'
    id=db.Column(db.Integer,primary_key=True)
    available_seats=db.Column(db.String(200))
    taken_seat=db.Column(db.String(200))
    
    @staticmethod
    def adding_seats():
        seats={'A':'seat A1(Asile) A2(Window)  A3(Asile) A4(middle) A5(window)'.split(),
    'B':'seat B1(Asile) B2(Window)  B3(Asile) B4(middle) B5(window)'.split(),
    'C':'seat C1(Asile) C2(Window)  C3(Asile) C4(middle) C5(window)'.split(),
    'D':'seat D1(Asile) D2(Window)  D3(Asile) D4(middle) D5(window)'.split(),
    'F':'seat F1(Asile) F2(Window)  F3(Asile) F4(middle) F5(window)'.split()
    }
        
        for seat in seats['A']:
            s=Seats.query.filter_by(available_seats=seat).first()
            if s is None:
                s=Seats(available_seats=seat)
            db.session.add(s)
        for seat in seats['B']:
            s=Seats.query.filter_by(available_seats=seat).first()
            if s is None:
                s=Seats(available_seats=seat)
            db.session.add(s)
        for seat in seats['C']:
            s=Seats.query.filter_by(available_seats=seat).first()
            if s is None:
                s=Seats(available_seats=seat)
            db.session.add(s)
        for seat in seats['D']:
            s=Seats.query.filter_by(available_seats=seat).first()
            if s is None:
                s=Seats(available_seats=seat)
            db.session.add(s)
        for seat in seats['F']:
            s=Seats.query.filter_by(available_seats=seat).first()
            if s is None:
                s=Seats(available_seats=seat)
            db.session.add(s)
        db.session.commit()   
    
    @staticmethod
    def clear_seats(seats):
        db.session.delete(seats)
        db.session.commit()

    def __repr__(self):
        return f'Seats("{self.available_seats}")'


class Permissions:
    paid=1
    scanner=2
    Admin=4

