from flask import Flask,render_template,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm,PaymentForm

app=Flask(__name__)
app.config['SECRET_KEY']='c5c321bb470b4b11b98346a4f7223005'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)
from models import User,Post

  
posts = [ { 'Author':'Magesajr',
          'title':'first post',
        'content':'testing flask',
          'date':'july,26 2023'},
          
         { 'Author':'sam',
          'title':'first post',
        'content':'testing blog',
          'date':'july,27 2023'}]
          
@app.route('/')
def HOME():
  return render_template('home.html',posts=posts)

@app.route('/about')
def about():
  return render_template('about.html',title='About')

@app.route('/register',methods=['GET',"POST"])
def register():
  form=RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for { form.name.data}!','success')
    return redirect(url_for('about'))
  return render_template('register.html',title='register',form=form)
  
@app.route('/login')
def login():
  form=LoginForm()
  return render_template('login.html',title='login',form=form)
  
@app.route('/payment',methods=['GET','POST'])
def payment():
  form=PaymentForm()
  if form.validate_on_submit():
    flash(f'your success full paid{ form.name.data}!','success')
    return redirect(url_for('register'))
  return render_template('payment.html',title='payment',form=form)
  

if __name__=='__main__':
    app.run(debug=True)