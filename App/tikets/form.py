from wtforms import (SearchField,
SelectField,StringField,DateField,
SubmitField,TextAreaField,BooleanField,PasswordField,TelField,MultipleFileField,SelectMultipleField)

from wtforms.validators import ValidationError,DataRequired,Length,Email,EqualTo,Optional
from App.models import Ticket,User
from flask_wtf import FlaskForm
import pandas as pd
from datetime import datetime
import os


places={
    'coast':'Dar-es-salaam Tanga Mtwara Lindi Mafia'.split(),
    'central':'Dodoma Morogoro Singida Shinyanga'.split(),
    'lakezone':'Mwanza Mara Simiyu Geita Kagera'.split(),
    'sourthen':'Mbeya Songea Njombe Iringa'.split(),
    'western':'Kigoma Tabora Katavi Sumbawanga'.split()
    }

seats={'A':'A1(Asile) A2(Window)  A3(Asile) A4(middle) A5(window)'.split(),
    'B':'B1(Asile) B2(Window)  B3(Asile) B4(middle) B5(window)'.split(),
    'C':'C1(Asile) C2(Window)  C3(Asile) C4(middle) C5(window)'.split(),
    'D':'D1(Asile) D2(Window)  D3(Asile) D4(middle) D5(window)'.split(),
    'F':'F1(Asile) F2(Window)  F3(Asile) F4(middle) F5(window)'.split()
    }


folder='/mnt/c/Users/kebby/Desktop/ubuntu/LINUX/Django/App/Uploads'
choices=[f for f in os.listdir(folder)]
fares=pd.DataFrame(columns=places.keys())

safari_times=[i for i in range(10,19)]
def times():
    D=[]
    for i in safari_times:
        dates=datetime(year=2024,month=9,day=1,hour=i,minute=30)
        D.append(dates.__format__('%H:%M %p'))
    return D 

s=datetime(2024,9,1)
e=datetime(2025,12,31)
g=pd.date_range(s,e)

df=pd.DataFrame(g)

def dates():
    D=[]
    for d in df[0].to_list():
        D.append(d.__format__('%b,%d-%Y'))
    return D


class UserProfileForm(FlaskForm):
    name=StringField('Passenger\'s Name',validators=[DataRequired()])
    email=StringField('Email Address',validators=[Email()])
    phonenumber=StringField('phonenumber',validators=[DataRequired()],default='+255')
    National_id=StringField('National ID',validators=[DataRequired()],default='birthyear-..-..')
    register=SubmitField('Update')

class UserRegisterForm(FlaskForm):
    name=StringField('Passenger\'s Name',validators=[DataRequired()])
    email=StringField('Email Address',validators=[Email()])
    phonenumber=StringField('phonenumber',validators=[DataRequired()],default='+255')
    password=PasswordField('password',validators=[DataRequired()])
    register=SubmitField('Register')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Taken')
    
    def validate_phonenumber(self,phonenumber):
            phone = phonenumber.data
            if not phone.startswith('0') and not  phone.startswith('+255'):
                raise ValidationError('Phone number must starts with +255 or 0 (country\'s code)')

class LoginForm(FlaskForm):
    email=StringField('Email Address',validators=[Email()])
    token=StringField('token',validators=[DataRequired()],description='enter your token')
    # confirm_password=PasswordField('confirm password',validators=[EqualTo('password')])
    # confirm_password=PasswordField('confirm password',validators=[EqualTo('password')])
    remember=BooleanField('Remember Me')
    login=SubmitField('Login')

class SubmitToken(FlaskForm):
    email=StringField('Email',validators=[Optional()])
    phonenumber=TelField('phonenumber',validators=[Optional()],default='+255',description='fill either your email or phonenumber')
    submit=SubmitField('send token')
    
    def validate_phonenumber(self,phonenumber):
            phone = phonenumber.data
            if not phone.startswith('0') and not  phone.startswith('+255'):
                raise ValidationError('Phone number must starts with +255 or 0 (country\'s code)')


class TicketForm(FlaskForm):
    start_point=SelectField('Journey starting point',validators=[DataRequired()],choices=places)
    destination=SelectField('End of the Journey',validators=[DataRequired()],choices=places)
    seat_number=SelectField('choose Your seat',validators=[DataRequired()],choices=seats)
    date_journey=DateField('Date of the Journey',validators=[DataRequired()],
                             default=datetime.utcnow(),format='%b~%d~%Y',
                             description='Fill in month,date Year for your Journey')
    departure_time=SelectField('Derpeture time',validators=[DataRequired()],choices=times())
    disc=TextAreaField('Description',validators=[Optional()])
    submit=SubmitField('See Your Ticket')


class PaymentForm(FlaskForm):
    email=StringField('enter Your email',validators=[DataRequired()],description='Enter  your email to see Your Tiket')
    submit=SubmitField('See Your Ticket')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'This email ({email.data})  is not registered')

class SendPayForm(FlaskForm):
    email=StringField('enter Your email',validators=[DataRequired()],description='Enter your email to send  your payment token')
    submit=SubmitField('Send Payment token')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'This email ({email.data})  is not registered')

class PayTokenForm(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    phonenumber=TelField('Phonenumber',validators=[DataRequired()])
    Amount=StringField('Amount',validators=[DataRequired(),Length(min=3)],description='Amount must exceed 999 tsh')
    tickets=MultipleFileField('Choose a ticket to pay',[DataRequired()])
    submit=SubmitField('Pay')


class DownloadForm(FlaskForm):
    ticket=SelectField('File',validators=[DataRequired()],
                       description='Download your pdf ticket',
                       choices=choices)
    sumit=SubmitField('Download')


class GetTicketForm(FlaskForm):
    email=StringField('Search',validators=[DataRequired()],
                       description='Search your Ticket by Email')
    sumit=SubmitField('Submit')

class LinkForm(FlaskForm):
    provider=StringField('choose your network provider',validators=[DataRequired()],
                       description='Tigopesa Airtel Mpesa')
    submit=SubmitField('Pay')


class SeatForm(FlaskForm):
    sumit=SubmitField('A')
    sumi=SubmitField('A')
    summ=SubmitField('A')
    mit=SubmitField('A')
    mi=SubmitField('A')
