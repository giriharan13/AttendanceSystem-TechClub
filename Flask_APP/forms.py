from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField,BooleanField,DateField
from wtforms.validators import DataRequired,Length,EqualTo
from flask_app.models import Student,Attendance

class LoginForm(FlaskForm):
    email_id = EmailField("Email-ID",validators=[DataRequired(),Length(min=5,max=100)])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=50)])
    submit = SubmitField("Login")


class AttendanceForm(FlaskForm):
    MarkAttendance = SubmitField("Mark Attendance")

class DateFilterForm(FlaskForm):
    dateFilter = DateField("Filter by date",format="%Y-%m-%d")
    filter = SubmitField("Filter")
