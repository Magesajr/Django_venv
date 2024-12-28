from wtforms import (SearchField,
SelectField,StringField,DateTimeField,DateField,
SubmitField,TextAreaField,BooleanField,PasswordField,TelField,MultipleFileField,SelectMultipleField)

from wtforms.validators import ValidationError,DataRequired,Length,Email,EqualTo,Optional
from App.models import Ticket,User
from flask_wtf import FlaskForm
import pandas as pd
from datetime import datetime
import os


class UsersForm(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    phonenumber=StringField('phonenumber',validators=[DataRequired()])
    email=StringField('email',validators=[Email(),DataRequired()])
    users_status=SelectField('status',validators=[DataRequired()])

class DateForm(FlaskForm):
    date = DateField('Select a Date', format="%d,%b-%Y",validators=[DataRequired()])
    submit = SubmitField('Submit')