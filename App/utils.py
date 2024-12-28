from App.models import  Ticket,Routes,User
from flask_mail import Message,Mail
from flask import url_for,render_template
#from fpdf import FPDF
import os,time
import secrets
from App.config import Config
from itsdangerous.url_safe import URLSafeTimedSerializer as s
from azampay import Azampay
from fpdf import FPDF

pd=FPDF('p','mm','Letter')

p=Config.UPLOAD_FOLDER

def convert(file,i):
    pd.add_page(orientation='portrait')
    for text in file:
        pd.set_font('Arial','B')
        pd.multi_cell(0,10,text)
    pd.output(os.path.join(p,'ticket'+str(i)+'.pdf'))

def generate_token(i):
    token=secrets.token_hex(i)
    t=s(token,salt='token')
    pin=t.dumps({'token':token})
    return {'token':token,'pin':pin}

def digest_token(token,user,max_age=int,**kwargs):
    t=s(user)
    try:
        key=t.loads(token,max_age,salt='token')['token']
    except:
        return False
    return secrets.compare_digest(key,user)

def send_token(to,subject,sender,token,**kwargs):
    mail=Mail()
    msg=Message(subject,recipients=[to],sender=sender)
    msg.body = f'''This is Your token:{token} use it to login to your account
it only valid within 30s    '''
    mail.send(msg)

def send_reset_token(to,subject,sender,token,**kwargs):
    mail=Mail()
    msg=Message(subject,recipients=[to],sender=sender)
    msg.body = f'''Click this link: {url_for("tickets.verify_token",token=token,_external=True)} use it to login to your account
it only valid within 10 minutes'''
    mail.send(msg)


def send_email(to,subject,sender,**kwargs):
    mail=Mail()
    user=User.query.filter_by(email=to).first()
    msg=Message(subject,recipients=[to],sender=sender)
    msg.body = render_template('emails/email_message.txt',user=user)
    msg.html = render_template('emails/send_email.html',user=user)
    msg.attach(os.path.join(p,'ticket0.txt'))
    mail.send(msg)


#AzamPay Payment Functions
app_name=Config.app_name
app_id=Config.app_id
client_secret=Config.client_secret

def Payment(provider,t_no,fare):
    azam=Azampay(app_name=app_name,client_id=app_id,client_secret=client_secret)
    link=azam.generate_payment_link(amount=t_no*fare,external_id='testing',provider=provider)
    data=link['data']
    return data