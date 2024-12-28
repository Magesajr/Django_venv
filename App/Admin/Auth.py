from flask import g
from flask_httpauth import HTTPBasicAuth
from App import db
from App.utils import (generate_token,send_token,digest_token,send_reset_token)
from App.models import User
from datetime import datetime
auth=HTTPBasicAuth()
import secrets

token =generate_token(3)
login_token=token['token']
pin=token['pin']

@auth.verify_password
def verify_password(email,token):
    if email=='':
        return False
    user=User.query.filter_by(email=email).first()
    t=user.generate_token()
    if not user:
        return False
    g.current_user=user
    return False



