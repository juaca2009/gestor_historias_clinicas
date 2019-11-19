from flask import Flask, render_template, request, redirect, session, g, url_for
import os
from clases.sistema import sistema

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "historias_clinicas"
sis = sistema()

@app.route("/", methods = ["GET", "POST"])
def login():
    global sis
    if request.method == "POST":
        session.pop('user', None)
        correo = str(request.form["correo"])
        contra = str(request.form["contra"])
        if sis.iniciar_sesion(correo, contra) == 1:
            session['user'] = request.form["correo"]
            return redirect(url_for('admin_m'))
        elif sis.iniciar_sesion(correo, contra) == 2:
            session['user'] = request.form["correo"]
        elif sis.iniciar_sesion(correo, contra) == 3:
            session['user'] = request.form["correo"]
        elif sis.iniciar_sesion(correo, contra) == 4:
            session['user'] = request.form["correo"]
        elif sis.iniciar_sesion(correo, contra) == 5:
            session['user'] = request.form["correo"]
        elif sis.iniciar_sesion(correo, contra) == 6:
            session['user'] = request.form["correo"]
        else:
            return redirect(url_for('login'))
    return render_template("login.html")











#rutas admin
@app.route("/admin")
def admin_m():
    if g.user:
        return render_template("admin.html")
    return redirect(url_for('login'))

@app.route("/paciente", methods = ["POST"])
def paciente():
    global sis
    if g.user:
        if request.method == "POST":
            return redirect(url_for('reg_paciente'))

@app.route("/recepcionista", methods = ["POST"])
def recepcionista():
    global sis
    if g.user:
        return redirect(url_for('reg_recepcionista'))
        

@app.route("/enfermero", methods = ["POST"])
def enfermero():
    global sis 
    if g.user:
        return redirect(url_for('reg_enfermero'))
        

@app.route("/doctor", methods = ["POST"])
def doctor():
    global sis 
    if g.user:
        return redirect(url_for('reg_doctor'))
        
    
@app.route("/empresa", methods = ["POST"])
def empresa():
    global sis 
    if g.user:
        return redirect(url_for('reg_empresa'))


@app.route("/reg_recepcionista", methods = ["GET", "POST"])
def reg_recepcionista():
    global sis
    if g.user:
        return render_template("R_recepcionista.html")

@app.route("/reg_enfermero", methods = ["GET", "POST"])
def reg_enfermero():
    global sis
    if g.user:
        return render_template("R_enfermero.html")

@app.route("/reg_doctor", methods = ["GET", "POST"])
def reg_doctor():
    global sis
    if g.user:
        return render_template("R_doctor.html")

@app.route("/reg_paciente", methods = ["GET", "POST"])
def reg_paciente():
    global sis
    if g.user:
        return render_template("R_paciente.html")

@app.route("/reg_empresa", methods = ["GET", "POST"])
def reg_empresa():
    global sis
    if g.user:
        return render_template("R_empresa.html")
















#generales
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route("/drop")
def drop():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)