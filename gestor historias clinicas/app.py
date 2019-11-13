from flask import Flask, render_template, request, redirect, session, g, url_for
from flask_sqlalchemy import SQLAlchemy
import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

class usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(50))
    contra = db.Column(db.String(8))

""" new_usuario = usuarios(correo = "juaca2009@gmail.com", contra = "12345er")
new_usuario2 = usuarios(correo = "mimi512@gmail.com", contra = "mimi123")
db.session.add(new_usuario2)
db.session.add(new_usuario)
db.session.commit() """

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        session.pop('user', None)
        user = usuarios.query.filter_by(correo = request.form["usuario"]).first()
        if user and (user.contra == request.form["contrasena"]):
            session['user'] = request.form["usuario"]
            return redirect(url_for('protected'))
    return render_template("index.html")

@app.route("/protected")
def protected():
    if g.user:
        return render_template("protected.html")
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route("/drop")
def drop():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)