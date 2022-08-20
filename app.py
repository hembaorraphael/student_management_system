import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# func helper from sqlalchemy.sql give access to raw SQL functions
# its good for setting default date,time when a record is created
from sqlalchemy.sql import func

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:root@localhost:5432/student_mgt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Student system management Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f"<Student {self.firstname}>"


@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)


@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        email = request.form["email"]
        age = int(request.form["age"])
        bio = request.form["bio"]

        student = Student(
            firstname=fname, lastname=lname, email=email, age=age, bio=bio
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

#decorator with a url variable  section student_id of type int
@app.route("/<int:student_id>/")
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("student.html", student=student)


@app.route("/<int:student_id>/edit/", methods=("GET", "POST"))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        bio = request.form["bio"]
        age = int(request.form["age"])
        email = request.form["email"]

        student.firstname = fname
        student.lastname = lname
        student.age = age
        student.email = email
        student.bio = bio

        db.session.add(student)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", student=student)


# python decorator that accepts only post request
@app.post("/<int:student_id>/delete/")
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("index"))
