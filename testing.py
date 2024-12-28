from time import time,sleep 
from functools import wraps
from datetime import datetime
import  os
from itsdangerous.url_safe import URLSafeTimedSerializer as s
import requests as r
from requests.auth import  HTTPBasicAuth as Hb
from azampay import Azampay as A 
import json
import pandas as pd                                                                                                                                                                                                                                                                                    


url='https://authenticator-sandbox.azampay.co.tz/AppRegistration/GenerateToken'                   
base='https://sandbox.azampay.co.tz/azampay/mno/checkout'                                         
clid=os.environ.get('CLID')                                                         
token=os.environ.get('TOKEN')                                                       
cskey=''

data={
        "appName":'magesaapp',
        "clientId":clid,
        "clientSecret":cskey
}



#SAM=A(app_name=data['appName'],client_id=clid,client_secret=cskey,sandbox=True)


def payment_token(phonenumber):
    serial=s(phonenumber,salt='payment')
    token=serial.dumps({'payment':'paid ticket'})
    return token

def verify_payment_token(t,max_age:int,salt='payment'):
    serial=s('mamasam')
    try:
        token=serial.loads(t,max_age,salt=salt)['payment']
    except:
        return 'expired or valid token'
    return token



available=[i for i in range(1,201)]
taken_seat=[]

def seat_choice(number):
    if number in available:
        available.remove(number)
    else:
        print('seat number is Taken')
    return number

def check_seats():
    number=int(input('choose your available seats:'))
    seat=seat_choice(number=number)
    if seat not in taken_seat:
        taken_seat.append(seat)
        print('taken seats',taken_seat)


def measure(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        t=time()
        func(*args,**kwargs)
        print(func.__name__,'took:',time()-t)
    return wrapper

def mex_result(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        result=func(*args,**kwargs)
        if result >100:
            print(f'Too big ({result})')
    return wrapper


@measure
@mex_result
def cube(n):
    return n**3

n=1

safari_times=[i for i in range(10,19)]
s=datetime(2024,9,1)
e=datetime(2025,12,31)
g=pd.date_range(s,e)

df=pd.DataFrame(g)

def dates():
    D=[]
    for d in df[0].to_list():
        D.append(d.__format__('%b,%d-%Y'))
    print(D)


def times():
    D=[]
    for i in safari_times:
        dates=datetime(year=2024,month=9,day=1,hour=i,minute=30)
        D.append(dates.__format__('%H:%M'))
    print(D)

# token=payment_token('mamasam')
dates()
