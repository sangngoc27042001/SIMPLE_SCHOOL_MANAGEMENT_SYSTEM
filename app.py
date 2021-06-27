from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

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
db.create_all()

@app.route("/")
def index():
    return render_template('index.html',link_css='static/main.css',data=All_user.query.all())

@app.route("/query", methods=['POST', 'GET'])
def query():
    id=int(request.args['id'])
    if id==0:
        return render_template('query.html',link_css='static/main.css', role=role, course=Course.query.all(), id=id)
    elif id==1:
        if request.method == 'POST':
            c = request.form['course']
            teacher=db.session.query(All_user).filter(All_user.course==c).filter(All_user.role==role[0]).all()
            student=db.session.query(All_user).filter(All_user.course==c).filter(All_user.role==role[1]).all()
            return render_template('query.html',link_css='static/main.css',course=c, teacher=teacher, student=student,id=id)
    return redirect("/")

@app.route("/course")
def course():
    return render_template('course.html',link_css='static/main.css', role=role, data=Course.query.all())

@app.route("/add_course",methods=['POST', 'GET'])
def add_course():
    if request.method == 'POST':
        print("hello")
        c = request.form['course']
        print(c)
        a=Course(c)
        db.session.add(a)
        db.session.commit()
    return redirect('/course')

@app.route("/delete_course", methods=['POST', 'GET'])
def delete_course():
    if request.method == 'POST':
        id = cont = request.form['id']
        task_to_delete = Course.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/course')

@app.route("/addform")
def addform():
    return render_template('addform.html',link_css='static/main.css', role=role, course=Course.query.all())

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        c = request.form['course']
        print(course)
        a=All_user(name, role, c)
        db.session.add(a)
        db.session.commit()
    return redirect('/')


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        id = cont = request.form['id']
        task_to_delete = All_user.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

@app.route("/update", methods=['POST', 'GET'])
def update():
    if request.method == 'GET':
        id = request.args.get('id')
        user=All_user.query.get_or_404(id)
        return render_template ('update.html',link_css='static/main.css', user=user,role=role, course=Course.query.all())
    if request.method == 'POST':
        id = request.form['id']
        user = All_user.query.get_or_404(id)
        user.name=request.form['name']
        user.course=request.form['course']
        user.role=request.form['role']
        db.session.commit()
        return redirect('/')
if __name__=="__main__":
    app.run(debug=True)
