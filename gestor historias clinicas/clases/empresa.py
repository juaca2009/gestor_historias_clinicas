# coding=UTF-8
from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

class empresa(usuario):
    def __init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
        usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)
    
    def crear_contrasena(self):
        letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        contador = 0
        contrasena = ''
        while contador < 8:
            temp = randint(0,1)
            if temp == 0:
                contrasena = contrasena + letras[randint(0,25)]
            else:
                contrasena = contrasena + numeros[randint(0,9)]
            contador = contador + 1
        return contrasena

    def enviar_contrasena(self, correo_dest, contrasena):
        msg = MIMEMultipart()
        mensaje = 'su cuenta ha sido creada correctamente, para iniciar sesion en el sistema su contrasena es: ' + contrasena
        contra = 'gestor123'
        msg['from'] = 'gestor.historias.clinicas@gmail.com'
        msg['to'] = correo_dest
        msg['Subject'] = 'envio contraseña'
        msg.attach(MIMEText(mensaje, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], contra)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def insertar_login(self, _correo, _constra, _documento, _rol):
        temp = usuario.get_base(self).execute(
            """
            insert into login(nro_documento, contrasena, correo, rol)
            values (%s, %s, %s, %s)
            """,
            (_documento, _constra, _correo, _rol)
        )

    def registrar_paciente(self, _nombre, _apellido, _fechan, _ciudad, _direccion,
                        _tdocumento, _ndocumento, _ntelefono, _correo):
        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono, tipo_documento)
            values ('paciente', %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _apellido, _ciudad, _direccion, _fechan, _nombre, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, 'paciente')

    def aumentar_posicion_consulta(self, _nro_cola):
        maxc = None
        temp = usuario.get_base(self).execute(
            """
            select max(posicion) from colas_consultas where nro_cola = %s
            """,
            ([_nro_cola])
        )
        for i in temp:
            maxc = i[0]
        if maxc == None:
            return 1
        else:
            return maxc + 1
    
    def aumentar_posicion_examen(self, _nro_cola):
        maxc = None
        temp = usuario.get_base(self).execute(
            """
            select max(posicion) from colas_examenes where nro_cola = %s
            """,
            ([_nro_cola])
        )
        for i in temp:
            maxc = i[0]
        if maxc == None:
            return 1
        else:
            return maxc + 1

    def agendar_consulta_general(self, _ndocumento):
        nombre = None
        apellido = None
        medicos = list()
        temp = usuario.get_base(self).execute(
            """
            select nombre, apellidos from rol_usuario where rol = 'paciente' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            nombre = i.nombre
            apellido = i.apellidos
        temp = usuario.get_base(self).execute(
            """
            select nombre_doctor, apellido_doctor, especialidad, nro_cola from asignacion_consultas 
            """
        )
        for i in temp:
            dic = {'nombre': None, 'apellido': None, 'nro_cola': None}
            if i.especialidad == 'general':
                dic['nombre'] = i.nombre_doctor
                dic['apellido'] = i.apellido_doctor
                dic['nro_cola'] = i.nro_cola
                medicos.append(dic)
        if len(medicos) == 1:
            mec = medicos[0]
            temp = usuario.get_base(self).execute(
                """
                insert into colas_consultas(nro_cola, nro_documento, apellido_doctor, apellido_paciente,
                especialidad, nombre_doctor, nombre_paciente, posicion)
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (mec['nro_cola'], _ndocumento, mec['apellido'], apellido, 'general', mec['nombre'], nombre, self.aumentar_posicion_consulta(mec['nro_cola']))
            )
        else:
            num = randint(0,len(medicos)-1)
            mec = medicos[num]
            temp = usuario.get_base(self).execute(
                """
                insert into colas_consultas(nro_cola, nro_documento, apellido_doctor, apellido_paciente,
                especialidad, nombre_doctor, nombre_paciente, posicion)
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (mec['nro_cola'], _ndocumento, mec['apellido'], apellido, 'general', mec['nombre'], nombre, self.aumentar_posicion_consulta(mec['nro_cola']))
            )

    def agendar_examen(self, _tipo_examen, _ndocumento):
        nombre = None
        apellido = None
        espec = None
        enf = {'nombre': None, 'apellido': None, 'cola': None}
        temp = usuario.get_base(self).execute(
            """
            select nombre, apellidos from rol_usuario where rol = 'paciente' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            nombre = i.nombre
            apellido = i.apellidos
        temp = usuario.get_base(self).execute(
            """
            select * from especializacion_examenes
            """
        )
        for i in temp:
            if i.tipo_examen == _tipo_examen:
                espec = i.especializacion
        temp = usuario.get_base(self).execute(
            """
            select nro_cola, apellido, nombre from asignacion_examenes where tipo_examen = %s
            """,
            ([_tipo_examen])
        )
        for i in temp:
            enf['nombre'] = i.nombre
            enf['apellido'] = i.apellido
            enf['cola'] = i.nro_cola
        temp = usuario.get_base(self).execute(
            """
            insert into colas_examenes(nro_cola, nro_documento, apellido_enfermero, 
            apellido_paciente, nombre_enfermero, nombre_paciente, posicion, tipo_examen)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (enf['cola'], _ndocumento, enf['apellido'], apellido, enf['nombre'], nombre, self.aumentar_posicion_examen(enf['cola']), _tipo_examen)
        )
        temp = usuario.get_base(self).execute(
            """
            insert into paciente_examenes(nro_documento, tipo_examen, estado) values(%s, %s, 'false')
            """,
            (_ndocumento, _tipo_examen)
        )
        self.agendar_consulta_parcial(espec, _ndocumento, nombre, apellido)

    def agendar_consulta_parcial(self, _especialidad, _ndocumento, _nombrep, _apellidop):
        medicos = list()
        temp = usuario.get_base(self).execute(
            """
            select nombre_doctor, apellido_doctor, especialidad, nro_cola from asignacion_consultas 
            """
        )
        for i in temp:
            dic = {'nombre': None, 'apellido': None, 'nro_cola': None}
            if i.especialidad == _especialidad:
                dic['nombre'] = i.nombre_doctor
                dic['apellido'] = i.apellido_doctor
                dic['nro_cola'] = i.nro_cola
                medicos.append(dic)
        if self.verificar_paciente(_especialidad, _ndocumento) == 0:
            if len(medicos) == 1:
                mec = medicos[0]
                temp = usuario.get_base(self).execute(
                    """
                    insert into colas_consultas(nro_cola, nro_documento, apellido_doctor, apellido_paciente,
                    especialidad, nombre_doctor, nombre_paciente, posicion)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (mec['nro_cola'], _ndocumento, mec['apellido'], _apellidop, _especialidad, mec['nombre'], _nombrep, None)
                )
            else:
                num = randint(0,len(medicos)-1)
                mec = medicos[num]
                temp = usuario.get_base(self).execute(
                    """
                    insert into colas_consultas(nro_cola, nro_documento, apellido_doctor, apellido_paciente,
                    especialidad, nombre_doctor, nombre_paciente, posicion)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (mec['nro_cola'], _ndocumento, mec['apellido'], _apellidop, 'general', mec['nombre'], _nombrep, None)
                )
        

    def verificar_paciente(self, _especialidad, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas
            """
        )
        for i in temp:
            if _ndocumento == i.nro_documento and _especialidad == i.especialidad:
                return 1
        return 0

# a = gestor_bd('historias_clinicas')
# a.conectar_bd()
# b = empresa("aaa@gmail.com", "123", a.get_sesion(), "aaa", "bbbb", "01010", "cali", "cra83c", 1212313)
# b.agendar_examen('endoscopia' ,11441089, 'camilon', 'hernandez')