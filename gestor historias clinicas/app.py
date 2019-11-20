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
            return redirect(url_for('recepcionista_m'))
        elif sis.iniciar_sesion(correo, contra) == 3:
            session['user'] = request.form["correo"]
            return redirect(url_for('empresa_m'))
        elif sis.iniciar_sesion(correo, contra) == 4:
            session['user'] = request.form["correo"]
        elif sis.iniciar_sesion(correo, contra) == 5:
            session['user'] = request.form["correo"]
            return redirect(url_for('doctor_m'))
        elif sis.iniciar_sesion(correo, contra) == 6:
            session['user'] = request.form["correo"]
            return redirect(url_for('enfermero_m'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html")











#rutas admin
@app.route("/admin")
def admin_m():
    if g.user:
        return render_template("admin.html")
    return redirect(url_for('login'))


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

@app.route("/salir_ad", methods = ["POST"])
def salir_ad():
    global sis
    if g.user:
        return redirect(url_for('admin_m'))


@app.route("/asig_examenes", methods = ["GET", "POST"])
def asig_examenes():
    global sis
    if g.user:
        if request.method == "POST":
            if sis.asignar_examen(str(request.form["examen"]), str(request.form["documento"])) == 1:
               return redirect(url_for('asig_examenes'))
            else:
                return redirect(url_for('admin_m'))
        return render_template("asignar_examen.html")



@app.route("/reg_recepcionista", methods = ["GET", "POST"])
def reg_recepcionista():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            if fecha != '':
                print(fecha)
                dt = datetime.strptime(fecha, '%Y-%m-%d')
                d = dt.date()
                tele = int(str(request.form["telefono"]))
                docu = int(str(request.form["documento"]))
                if sis.agregar_recepcionista(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                    return redirect(url_for('admin_m'))
                else:
                    return redirect(url_for('reg_recepcionista'))
            else:
                return redirect(url_for('reg_recepcionista'))
        return render_template("R_recepcionista.html")

@app.route("/reg_enfermero", methods = ["GET", "POST"])
def reg_enfermero():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            if fecha != '':
                dt = datetime.strptime(fecha, '%Y-%m-%d')
                d = dt.date()
                tele = int(str(request.form["telefono"]))
                docu = int(str(request.form["documento"]))
                if sis.agregar_enfermero(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                    return redirect(url_for('admin_m'))
                else:
                    return redirect(url_for('reg_enfermero'))
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
            if fecha != '':
                dt = datetime.strptime(fecha, '%Y-%m-%d')
                d = dt.date()
                cel = int(str(request.form["celular"]))
                tele = int(str(request.form["telefono"]))
                docu = int(str(request.form["documento"]))
                if sis.agregar_doctor(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"]), cel, str(request.form["especialidad"])) == 1:
                    return redirect(url_for('admin_m'))
                else:
                    return redirect(url_for('reg_doctor'))
            else:
                return redirect(url_for('reg_doctor'))
        return render_template("R_doctor.html")

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










#rutas doctor
@app.route("/doctor_m", methods = ["GET", "POST"])
def doctor_m():
    global sis
    if g.user:
        if request.method == "POST":
            if sis.llamar_paciente_doctor() == 1:
                return redirect(url_for('atender'))
            else:
                redirect(url_for('doctor_m'))
        return render_template("doctor.html")


@app.route("/atender", methods = ["GET", "POST"])
def atender():
    global sis
    if g.user:
        if request.method == "POST":
            come = str(request.form["comentario"])
            if sis.ingresar_comentario(come) == 1:
                return redirect(url_for('agendar_examen'))
            else:
                return redirect(url_for('atender'))
        his = sis.mostrar_historia_doctor()
        return render_template("atencion.html", historias = his)

@app.route("/agendar_examen", methods = ["GET", "POST"])
def agendar_examen():
    global sis
    exam = None
    if g.user:
        if request.method == "POST":
            exam = str(request.form["examen_doctor"])
            if exam == None or exam == '':
                sis.despachar_paciente_doctor()
                return redirect(url_for('doctor_m'))
            else:
                if sis.agendar_examen_doctor(exam) == 1:
                    sis.despachar_paciente_doctor()
                    return redirect(url_for('doctor_m'))
                else:
                    return redirect(url_for('agendar_examen'))
        return render_template("examen_doctor.html")




#rutas enfermero
@app.route("/enfermero_m", methods = ["GET", "POST"])
def enfermero_m():
    global sis
    if g.user:
        if request.method == "POST":
            if sis.llamar_paciente_enfermero() == 1:
                return redirect(url_for('atender_examen'))
            else:
                redirect(url_for('enfermero_m'))
        return render_template("enfermero.html")


@app.route("/atender_examen",  methods = ["GET", "POST"])
def atender_examen():
    global sis
    if g.user:
        if request.method == "POST":
            come = str(request.form["resultado"])
            if sis.ingresar_resultado(come) == 1:
                sis.despachar_paciente_enfermero()
                return redirect(url_for('enfermero_m'))
            else:
                return redirect(url_for('atender_examen'))
        his = sis.mostrar_historia_enfermero()
        return render_template("atencion_examen.html", historias = his)









#metodos empresa
@app.route("/empresa_m")
def empresa_m():
    global sis
    if g.user:
        return render_template("empresa.html")
    return redirect(url_for('login'))

@app.route("/empre_paciente", methods = ["POST"])
def empre_paciente():
    global sis
    if g.user:
        return redirect(url_for('regi_paciente'))

@app.route("/empre_consulta", methods = ["POST"])
def empre_cconsulta():
    global sis
    if g.user:
        return redirect(url_for('consu_general'))

@app.route("/empre_examen", methods = ["POST"])
def empre_examen():
    global sis
    if g.user:
        return redirect(url_for('exam_empre'))

@app.route("/regi_paciente", methods = ["GET", "POST"])
def regi_paciente():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            if fecha != '':
                dt = datetime.strptime(fecha, '%Y-%m-%d')
                d = dt.date()
                tele = int(str(request.form["telefono"]))
                docu = int(str(request.form["documento"]))
                if sis.registrar_paciente(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                    return redirect(url_for('empresa_m'))
                else:
                    return redirect(url_for('regi_paciente'))
            else:
                return redirect(url_for('regi_paciente'))
        return render_template("R_paciente.html")


@app.route("/consu_general", methods = ["GET", "POST"])
def consu_general():
    global sis
    if g.user:
        if request.method == "POST":
            docus = str(request.form["consulta_empresa"])
            if docus != '':
                docu = int(docus)
                if sis.agendar_consulta_general_empresa(docu) == 1:
                    return redirect(url_for('empresa_m'))
                else:
                    return redirect(url_for('consu_general'))
            else:
                return redirect(url_for('consu_general'))
        return render_template("consulta_empresa.html")


@app.route("/exam_empre", methods = ["GET", "POST"])
def exam_empre():
    global sis
    if g.user:
        if request.method == "POST":
            ex = str(request.form["examen"])
            docus = str(request.form["documento"])
            if ex != '' and docu != '':
                docu = int(docus)
                if sis.agendar_examen_empresa(ex, docu) == 1:
                    return redirect(url_for('empresa_m'))
                else:
                    return redirect(url_for('exam_empre'))
            else:
                return redirect(url_for('exam_empre'))
        return render_template("examen_empresa.html")






@app.route("/recepcionista_m")
def recepcionista_m():
    global sis
    if g.user:
        return render_template("recepcionista.html")
    return redirect(url_for('login'))

@app.route("/recep_paciente", methods = ["POST"])
def recep_paciente():
    global sis
    if g.user:
        return redirect(url_for('regil_paciente'))

@app.route("/recep_consulta", methods = ["POST"])
def recep_consulta():
    global sis
    if g.user:
        return redirect(url_for('consul_general'))

@app.route("/regil_paciente", methods = ["GET", "POST"])
def regil_paciente():
    global sis
    if g.user:
        if request.method == "POST":
            fecha = str(request.form["fecha_nacimiento"])
            if fecha != '':
                dt = datetime.strptime(fecha, '%Y-%m-%d')
                d = dt.date()
                tele = int(str(request.form["telefono"]))
                docu = int(str(request.form["documento"]))
                if sis.registrar_paciente(str(request.form["nombre"]), str(request.form["apellido"]), d, str(request.form["ciudad"]), str(request.form["direccion"]), str(request.form["tipo_documento"]), docu, tele, str(request.form["correo"])) == 1:
                    return redirect(url_for('recepcionista_m'))
                else:
                    return redirect(url_for('regil_paciente'))
            else:
                return redirect(url_for('regil_paciente'))
        return render_template("R_paciente2.html")

@app.route("/consul_general", methods = ["GET", "POST"])
def consul_general():
    global sis
    if g.user:
        if request.method == "POST":
            docus = str(request.form["consulta_empresa"])
            if docus != '':
                docu = int(docus)
                if sis.agendar_consulta_general_empresa(docu) == 1:
                    return redirect(url_for('recepcionista_m'))
                else:
                    return redirect(url_for('consul_general'))
            else:
                return redirect(url_for('consul_general'))
        return render_template("consulta_recep.html")







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