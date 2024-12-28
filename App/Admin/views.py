from flask import( url_for,redirect,render_template,
                  flash,send_from_directory,
                  current_app,abort,request,g)
from flask_login import (current_user,
login_required,login_user,logout_user)
from App.models import Ticket,Seats,User
from .import admin
from .forms import UsersForm,DateForm
from datetime import datetime
import os  
import pandas as pd

@admin.route('/Home',methods=['GET','POST'])
def home():
    flash('Welcome to Admin page','info')
    return render_template('admin/home.html')

@admin.route('/tickets',methods=['GET','POST'])
def tickets():
    flash('All tickets of Today','info')
    tickets=Ticket.query.all()
    return render_template('admin/tickets_page.html',tickets=tickets)


@admin.route('/users',methods=['GET','POST'])
def users():
    form=UsersForm()
    flash('Users Site','info')
    users=User.query.all()
    names,phonenumbers,emails=[],[],[]
    for user in users:
        names.append(user.name)
        phonenumbers.append(user.phonenumber)
        emails.append(user.email)
    df={'names':names,'emails':emails,'phonenumbers':phonenumbers}
    table=pd.DataFrame(df).to_html(classes='table table-striped',render_links=True,justify='center')
    return render_template('admin/users_page.html',users=users,form=form,table=table)

@admin.route('date/')
def index():
    form = DateForm()
    if form.validate_on_submit():
        selected_date = form.date.data
        return f'Selected Date: {selected_date}'
    return render_template('admin/index.html', form=form)