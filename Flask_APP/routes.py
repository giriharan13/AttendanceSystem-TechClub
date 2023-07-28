from datetime import datetime,timezone

from flask import render_template,url_for,flash,redirect,Response
from flask_app import app,VideoCamera,login_manager,db
from flask_app.forms import LoginForm,AttendanceForm,DateFilterForm
import face_recog.FRmain as fr
import cv2
from flask_login import current_user,logout_user,login_user,login_required
from flask_app.models import Student,Admin,Attendance
from sqlalchemy import  func ,Date


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if(form.validate_on_submit()):
        student = Student.query.filter_by(email_id=form.email_id.data).first()
        print("hello")
        if (student and student.password==form.password.data):
            login_user(student)
            flash(f"green : Successfully logged in as {student.name}")
            return redirect(url_for("home", form=form,role=current_user.get_role()))
        else:
            flash("red : Doesnt exist or Invalid password")
    return render_template("login.html",title="login",form=form)

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if(form.validate_on_submit()):
        admin = Admin.query.filter_by(email_id=form.email_id.data).first()
        print("hello")
        if (admin and admin.password==form.password.data):
            login_user(admin)
            flash(f"green : Successfully logged in as {admin.name}")
            return redirect(url_for("home", form=form,role=current_user.get_role()))
        else:
            flash("red : Doesnt exist or Invalid password")
    return render_template("adminlogin.html",title="adminlogin",form=form)

@app.route("/logout")
def logout():
    if(current_user.get_role()=="STUDENT"):
        logout_user()
        return redirect(url_for("login"))
    else:
        logout_user()
        return redirect(url_for("adminlogin"))

@login_manager.user_loader
def load_user(reg):
    #print(email_id+"lpdpd")
    if(len(reg)==12):
        return Student.query.filter_by(register_number=reg).first()
    else:
        return Admin.query.filter_by(id_number=reg).first()

def checkForToday():
    records = Attendance.query.filter(Attendance.register_number == current_user.register_number)
    for record in records:
        if(record.date.date()==datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None).date()):
            print(record.date.date(),datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None))
            return 1
    return 0

@app.route("/home",methods=["GET","POST"])
@login_required
def home():
    form = AttendanceForm()
    filterform = DateFilterForm()
    attendance = checkForToday() if current_user.get_role() == "STUDENT" else None
    if(form.MarkAttendance.data and form.validate_on_submit()):
        return redirect(url_for("scanpage",form=form))
    if(filterform.validate_on_submit()):
        today_date = filterform.dateFilter.data
        return render_template("home.html", form=form, user=current_user, attendance=attendance,
                               todayDate=today_date, allAttendance=Attendance, allStudents=Student,
                               func=func, Date=Date, dateFilterForm=filterform)
    '''func.cast(allAttendance.date,Date)==todayDate,'''
    return render_template("home.html",form=form,user=current_user,attendance=attendance,todayDate=datetime.utcnow().date(),allAttendance= Attendance,allStudents=Student,func=func,Date=Date,dateFilterForm=filterform)


@app.route("/student/<int:register_number>",methods=["GET","POST"])
@login_required
def student(register_number):
    if(current_user.get_role()=="STUDENT"):
        flash("you are not allowed to access this page")
        return redirect(url_for("home"))
    else:
        stud = Student.query.get_or_404(register_number)
        return render_template("student.html",student=stud)


frame = None
def gen(camera):
    while True:
        global frame
        frame,jpg = camera.get_frame()
        '''res = fr.validate(frame)
        ret,out = cv2.imencode('.jpg',res)
        out = out.tobytes()'''
        yield(b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n'+jpg+b'\r\n\r\n')

@app.route("/scanpage",methods=["GET","POST"])
def scanpage():
    form = AttendanceForm()
    if(form.validate_on_submit()):
        info = fr.validate(frame,datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None).date())
        print(info)
        if(info[2]==False):
            flash("red : Picture detected.Please don't cheat")
        elif(info[3]==current_user.register_number):
            update(info[0])
        else:
            flash("red : Face did not match! Try again")
        print(dir(current_user))
        return redirect(url_for("home",form=form))
    return render_template("scanpage.html",form=form)

@app.route("/video_feed",methods=["GET","POST"])
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def update(frm):
    #res = fr.validate(frame,str(datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None).date()))
    ret, out = cv2.imencode('.jpg', frm)
    out = out.tobytes()
    attrec = Attendance(status=True,image=out,register_number=current_user.register_number,date=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None))
    db.session.add(attrec)
    db.session.commit()

@app.route("/result_feed",methods=["GET","POST"])
def result_feed():
    out = None
    records = Attendance.query.filter(Attendance.register_number==current_user.register_number)
    for record in records:
        if(record.date.date()==datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None).date()):
            out = record.image
            break;
    return Response(b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n'+(out)+b'\r\n\r\n',
                    mimetype='multipart/x-mixed-replace; boundary=frame')
