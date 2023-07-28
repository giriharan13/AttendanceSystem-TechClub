from flask_app import db
from datetime import datetime,timezone
from flask_login import UserMixin

class Student(db.Model,UserMixin):
    register_number = db.Column(db.String(12),primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email_id = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),default="rmkec@123")

    attendance_records = db.relationship("Attendance",backref="student",lazy=True)

    def __repr__(self):
        return f'{self.name} {self.register_number} {self.email_id} {self.password}'

    def get_id(self):
        return self.register_number

    def get_role(self):
        return "STUDENT"

class Admin(db.Model,UserMixin):
    id_number = db.Column(db.String(10),primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email_id = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),default="admin@rmkec")

    def __repr__(self):
        return f'{self.name} {self.id_number} {self.email_id} {self.password}'

    def get_id(self):
        return self.id_number

    def get_role(self):
        return "ADMIN"

class Attendance(db.Model):
    date = db.Column(db.DateTime,default=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None))
    status = db.Column(db.Boolean,default=False)
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.LargeBinary)
    register_number = db.Column(db.String(12),db.ForeignKey("student.register_number"),nullable=False)

    def __repr__(self):
        return f"{self.register_number} {self.date} {self.id} "




