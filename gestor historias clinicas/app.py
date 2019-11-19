from flask import Flask, render_template, request, redirect, session, g, url_for
import os
from clases.sistema import sistema
from datetime import datetime

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

@app.route("/asignar", methods = ["POST"])
def asignar():
    global sis
    if g.user:
        return redirect(url_for('asig_examenes'))


@app.route("/asig_examenes", methods = ["GET", "POST"])
def asig_examenes():
    global sis
    if g.user:
        exa = sis.get_asignacion_examenes()
        return render_template("asignar_examen.html", exam = exa)



@app.route("/reg_recepcionista", methods = ["GET", "POST"])
def reg_recepcionista():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            dt = datetime.strptime(fecha, '%Y-%m-%d')
            d = dt.date()
            tele = int(str(request.form["telefono"]))
            docu = int(str(request.form["documento"]))
            if sis.agregar_recepcionista(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                return redirect(url_for('admin_m'))
            else:
                return redirect(url_for('reg_recepcionista'))
        return render_template("R_recepcionista.html")

@app.route("/reg_enfermero", methods = ["GET", "POST"])
def reg_enfermero():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            dt = datetime.strptime(fecha, '%Y-%m-%d')
            d = dt.date()
            tele = int(str(request.form["telefono"]))
            docu = int(str(request.form["documento"]))
            if sis.agregar_enfermero(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                return redirect(url_for('admin_m'))
            else:
                return redirect(url_for('reg_enfermero'))
        return render_template("R_enfermero.html")

@app.route("/reg_doctor", methods = ["GET", "POST"])
def reg_doctor():
    global sis
    fecha = None
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            dt = datetime.strptime(fecha, '%Y-%m-%d')
            d = dt.date()
            cel = int(str(request.form["celular"]))
            tele = int(str(request.form["telefono"]))
            docu = int(str(request.form["documento"]))
            if sis.agregar_doctor(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"]), cel, str(request.form["especialidad"])) == 1:
                return redirect(url_for('admin_m'))
            else:
                return redirect(url_for('reg_doctor'))
        return render_template("R_doctor.html")

@app.route("/reg_paciente", methods = ["GET", "POST"])
def reg_paciente():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            dt = datetime.strptime(fecha, '%Y-%m-%d')
            d = dt.date()
            tele = int(str(request.form["telefono"]))
            docu = int(str(request.form["documento"]))
            if sis.agregar_paciente(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                return redirect(url_for('admin_m'))
            else:
                return redirect(url_for('reg_paciente'))
        return render_template("R_paciente.html")

@app.route("/reg_empresa", methods = ["GET", "POST"])
def reg_empresa():
    global sis
    if g.user:
        if request.method == "POST":
            tele = int(str(request.form["telefono"]))
            docu = int(str(request.form["documento"]))
            if sis.agregar_empresa(str(request.form["correo"]), str(request.form["nombre"]), str(request.form["ciudad"]), str(request.form["direccion"]), docu, tele) == 1:
                return redirect(url_for('admin_m'))
            else:
                return redirect(url_for('reg_empresa'))
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