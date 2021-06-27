from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
db = SQLAlchemy(app)
role=[
    "teacher",
    "student"
]
    
course=[
    "IELTS_level_1",
    "IELTS_level_2",
    "IELTS_level_3",
    "IELTS_level_4",
]
   
class All_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    role=db.Column(db.String(200), nullable=False) #just Teacher and student
    course=db.Column(db.String(200), nullable=True)
    def __init__(self, name, role, course):
        self.name=name
        self.role=role
        self.course=course
    def __repr__(self):
        return  f"user('{self.id}','{self.name}','{self.role}','{self.course}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_name=db.Column(db.String(200), nullable=False)
    def __init__(self, c_name):
        self.c_name=c_name
    def __repr__(self):
        return  f"user('{self.id}','{self.c_name}')"