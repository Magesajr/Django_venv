from flask import( url_for,redirect,render_template,
                  flash,send_from_directory,
                  current_app,abort,request,g)
from flask_login import (current_user,
login_required,login_user,logout_user)
from .form import (TicketForm,
PaymentForm,LinkForm,
DownloadForm,GetTicketForm,
SeatForm,UserRegisterForm,LoginForm,SubmitToken,
SendPayForm,PayTokenForm,UserProfileForm)
from flask_httpauth import HTTPBasicAuth
from App import db
from App.utils import (convert,send_email,Payment,
generate_token,send_token,digest_token,send_reset_token)
from App.models import Ticket,Seats,User
from .import tickets
from .Auth import auth
from datetime import datetime
import os  


@tickets.route('/token',methods=['GET','POST'])

def token():
    form=SubmitToken()
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    flash('token for login it only valid within 30s','warning')
    if form.validate_on_submit():
        global token
        token=generate_token(3)
        login_token=token['token']
        send_token(form.email.data,'LOGIN TOKEN','MagesaJR',token=login_token)
        return redirect(url_for('.login'))
    return render_template('tickets/token.html',form=form)


@tickets.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    form = UserRegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        phone=form.phonenumber.data
        password=form.password.data
        user=User(name=name,
                      email=email,phonenumber=phone,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.process'))
    return render_template('tickets/process.html',form=form,date=datetime.utcnow())


@tickets.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if digest_token(token=token['pin'],user=form.token.data,max_age=60):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('.process'))
        else:
            flash('invalid or expired token generate another token','warning')
            return redirect(url_for('.home'))
    return render_template('tickets/process.html',form=form,date=datetime.utcnow())

@tickets.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.token'))

@tickets.route('/reset_pass',methods=['GET','POST'])
def reset_pass():
    form = SendPayForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        payment_token=user.generate_token()
        send_reset_token(email,'PAYMENT TOKEN','OnlineTickets@gmail.com',payment_token,user=user)
    return render_template('tickets/process.html',form=form,date=datetime.utcnow())

@tickets.route('/verify_token/<token>',methods=['GET','POST'])
def verify_token(token):
    form = PayTokenForm()
    user=User.verify_token(token,max_age=600)
    if user is None:
        flash('invalid or expired token','info')
        return redirect(url_for('.reset_pass'))
    return render_template('tickets/process.html',form=form,date=datetime.utcnow())


@tickets.route('/home',methods=['GET','POST'])
def home():
    flash('Welcome to Our Online Ticket Services','warning')
    return render_template('tickets/home.html')


def display():
    seat=Seats.query.all()
    a=[]
    for seats in seat:
        if seats.available_seats:
            a.append(seats.available_seats+'>>free')
        if seats.available_seats==None and seats.taken_seat:
            a.append(seats.taken_seat)
    return a

@tickets.route('/processing',methods=['GET','POST'])
@login_required
def process():
    form = TicketForm()
    if form.validate_on_submit():
        seat=form.seat_number.data
        start=form.start_point.data
        end=form.destination.data
        date_journey=form.date_journey.data
        Seat=Seats(taken_seat=seat)
        Seat_a=Seats.query.filter_by(available_seats=seat).first()
        client=Ticket(seat_number=seat,
                      start_point=start,destination=end,date=date_journey,
                      derpeture_time=form.departure_time.data,user=current_user)
        db.session.add(client)
        db.session.add(Seat)
        db.session.delete(Seat_a)
        db.session.commit()
    return render_template('tickets/process.html',form=form,date=datetime.utcnow(),a=display())


@tickets.route('/payment/',methods=['GET','POST'])
def payment():
    form=PaymentForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        table=user.tickets.all()
        flash('Your ticket is ready choose your payment Methods','info')
        return render_template('tickets/tiket.html',table=table)
    if current_user.is_authenticated:
            form.email.data=current_user.email
    return render_template('tickets/payment.html',form=form,date=datetime.utcnow())

@tickets.route('/payment_generation',methods=['GET','POST'])
def links():
    form=LinkForm()
    user=current_user
    tickets_no=user.tickets.count()
    if form.validate_on_submit:
        provider=form.provider.data
    return render_template('tickets/generation.html',form=form,
                           date=datetime.utcnow(),link=Payment('tigopesa',tickets_no,20000))


@tickets.route('/Account',methods=['GET','POST'])
@login_required
def Account():
    form=UserProfileForm()
    flash(f'welcome {current_user.name}','success')
    user=current_user
    if form.validate_on_submit():
        User(name=form.name.data,
                  email=form.email.data,
                  phonenumber=form.phonenumber.data)
        db.session.commit()
    form.name.data=current_user.name    
    form.phonenumber.data=current_user.phonenumber    
    form.email.data=current_user.email    
    return render_template('tickets/account.html',form=form)


@tickets.route('/download/',methods=['GET','POST'])
@login_required
def download():
    form=DownloadForm()
    folder=current_app.config['UPLOAD_FOLDER']
    if form.validate_on_submit():
        try:
            return send_from_directory(folder,form.ticket.data,as_attachment=True)
        except:FileNotFoundError
        abort(404)
    return  render_template('tickets/Download.html',form=form)


@tickets.route('/seats/',methods=['GET','POST'])
def seats():
    form=SeatForm()
    seat=Seats.query.all()
    a=[]
    for seats in seat:
        if seats.available_seats:
            a.append(seats.available_seats+'>>free')
        if seats.available_seats==None and seats.taken_seat:
            a.append(seats.taken_seat)
    return  render_template('tickets/seats.html',form=form,a=a)



@tickets.route('/verify_ticket/',methods=['GET','POST'])
@login_required
def verify():
    form=GetTicketForm()
    folder=current_app.config['UPLOAD_FOLDER']
    tickets=current_user.tickets.all()
    t_nu=current_user.tickets.count()
    file=[]
    convets=[]
    if form.validate_on_submit():
        if tickets:
            for user in tickets:
                # ticket_file=os.path.join(folder,'ticket.txt')
                #send_email(user.email,'VERIFY YOUR TICKECT',current_app.config['MAIL_USERNAME'],user=user)
                File=f'''passenger\'s name:{current_user.name}
    phonenumber:{current_user.phonenumber}
    email:{current_user.email}
    From:{user.start_point}
    destination:{user.destination}
    seat number:{user.seat_number}
    Date:{user.date.__format__('%b,%d~%Y')}
    Derpeture time:{user.derpeture_time}'''
                file.append(File)
            for i in range(t_nu):
                with open(os.path.join(folder,'ticket'+str(i)+'.txt'),'x') as f:
                    f.write(file[i])
                    f.close()
                # sam=open(os.path.join(folder,'ticket'+str(i)+'.txt'),'r')
                # convets.append(sam)
                # convert(convets[i],i=i)
            flash(f'Download Your ticket','primary')
            return redirect(url_for('.download'))
    return  render_template('tickets/Download.html',form=form)
