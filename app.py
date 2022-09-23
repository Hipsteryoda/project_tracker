#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    notes = db.Column(db.String(1000))
    created = db.Column(db.DateTime)
    progress = db.Column(db.Boolean)
    # progress = db.Column(db.String(60))


@app.route('/')
def home():
    project_list = Projects.query.all()
    return render_template('base.html', project_list=project_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("projectname")
    notes = request.form.get("notes")
    created = datetime.now()
    new_project = Projects(title=title, notes=notes, created=created, progress=False)
    # makes sure that the project title isn't blank
    if new_project.title != '':
        db.session.add(new_project)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:project_id>")
def update(project_id):
    project = Projects.query.filter_by(id=project_id).first()
    project.progress = not project.progress

    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:project_id>")
def delete(project_id):
    project = Projects.query.filter_by(id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)