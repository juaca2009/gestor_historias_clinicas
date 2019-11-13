# coding=UTF-8
from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class administrador(usuario):
    def __init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
        usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)




    def agregar_paciente(self, _nombre, _apellido, _fechan, _ciudad, _direccion,
                         _tdocumento, _ndocumento, _ntelefono, _correo):
        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono, tipo_documento)
            values ("paciente", %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _apellido, _ciudad, _direccion, _fechan, _nombre, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, "paciente")




    def agregar_recepcionista(self, _nombre, _apellido, _fechan, _ciudad, _direccion, 
                              _tdocumento, _ndocumento, _ntelefono, _correo):
        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono, tipo_documento)
            values ("recepcionista", %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _apellido, _ciudad, _direccion, _fechan, _nombre, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, "recepcionista")




    def agregar_enfermero(self,  _nombre, _apellido, _fechan, _ciudad, _direccion, 
                          _tdocumento, _ndocumento, _ntelefono, _correo):
        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono, tipo_documento)
            values ("enfermero", %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _apellido, _ciudad, _direccion, _fechan, _nombre, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, "enfermero")




    def agregar_doctor(self,  _nombre, _apellido, _fechan, _ciudad, _direccion, 
                       _tdocumento, _ndocumento, _ntelefono, _correo, _tipo_examen, _celular, _especialidad):

        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, apellidos, ciudad, direccion, 
            especialidad, fecha_nacimiento, nombre, numero_cel, telefono, tipo_documento)
            values ("doctor", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _apellido, _ciudad, _direccion, _especialidad, _fechan, _nombre, _celular, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, "doctor")
        self.asiganar_consulta(_especialidad, _nombre, _apellido, _ndocumento)




    def agregar_empresa(self, _nombre, _ciudad, _direccion,  _tdocumento, _ndocumento, _ntelefono):
        temp = usuario.get_base(self).execute(
            """
            insert into rol_usuario(rol, nro_documento, ciudad, direccion, 
            nombre, telefono, tipo_documento)
            values ("empresa", %s, %s, %s, %s, %s, %s)
            """,
            (_ndocumento, _ciudad, _direccion, _nombre, _ntelefono, _tdocumento)
        )
        contra_temp = self.crear_contrasena()
        self.enviar_contrasena(_correo, contra_temp)
        self.insertar_login(_correo, contra_temp, _ndocumento, "empresa")




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




    def asignar_examen(self, _tipo_examen, _nombree, _apellidoe, _documento, _cola):
       
        temp = usuario.get_base(self).execute(
            """
            insert into asignacion_examenes(tipo_examen, apellido, id_enfermero, nombre, nro_cola)
            values (%s, %s, %s, %s, %s)
            """,
            (_tipo_examen, _apellidoe, _documento, _nombree, _cola)
        )




    def asiganar_consulta(self, _especialidad, _nombree, _apellidoe, _documento):
         temp = usuario.get_base(self).execute(
            """
            insert into asignacion_consultas(nro_documento, apellido_doctor, especialidad, nombre_doctor, nro_cola)
            values (%s, %s, %s, %s, %s)
            """,
            (_tipo_examen, _apellidoe, _documento, _nombree, _cola, self.aumentar_consulta())
        )




    def aumentar_consulta(self):
        max_cola =  None
        temp = usuario.get_base(self).execute(
            """
            select max(nro_cola) from asignacion_examenes
            """
        )
        for i in temp:
            max_cola = i[0]
        if max_cola == None:
            return 1
        else:
            return max_cola + 1




    def obtener_informacion_paciente(self, _ndocumento):
        datos = {
            'nombre': None, 'apellido': None, 'ciudad': None, 'direccion': None, 'fecha': None, 'telefono': None
        }
        temp = usuario.get_base(self).execute(
            """
            select apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono from rol_usuario
            where rol = 'paciente' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            datos['nombre'] = i.nombre
            datos['apellido'] = i.apellidos
            datos['ciudad'] = i.ciudad
            datos['direccion'] = i.direccion
            datos['fecha'] = i.fecha_nacimiento
            datos['telefono'] = i.telefono
        return datos




    def obtener_informacion_recepcionista(self,  _ndocumento):
        datos = {
            'nombre': None, 'apellido': None, 'ciudad': None, 'direccion': None, 'fecha': None, 'telefono': None
        }
        temp = usuario.get_base(self).execute(
            """
            select apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono from rol_usuario
            where rol = 'recepcionista' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            datos['nombre'] = i.nombre
            datos['apellido'] = i.apellidos
            datos['ciudad'] = i.ciudad
            datos['direccion'] = i.direccion
            datos['fecha'] = i.fecha_nacimiento
            datos['telefono'] = i.telefono
        return datos




    def obtener_informacion_enfermero(self, _ndocumento):
        datos = {
            'nombre': None, 'apellido': None, 'ciudad': None, 'direccion': None, 'fecha': None, 'telefono': None
        }
        temp = usuario.get_base(self).execute(
            """
            select apellidos, ciudad, direccion, 
            fecha_nacimiento, nombre, telefono from rol_usuario
            where rol = 'enfermero' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            datos['nombre'] = i.nombre
            datos['apellido'] = i.apellidos
            datos['ciudad'] = i.ciudad
            datos['direccion'] = i.direccion
            datos['fecha'] = i.fecha_nacimiento
            datos['telefono'] = i.telefono
        return datos




    def obtener_informacion_doctor(self, _ndocumento):
        datos = {
            'nombre': None, 'apellido': None, 'ciudad': None, 'direccion': None, 
            'fecha': None, 'telefono': None, 'especialidad': None,'celular': None
        }
        temp = usuario.get_base(self).execute(
            """
            select apellidos, ciudad, direccion, especialidad, fecha_nacimiento, 
            nombre, numero_cel, telefono from rol_usuario
            where rol = 'doctor' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            datos['nombre'] = i.nombre
            datos['apellido'] = i.apellidos
            datos['ciudad'] = i.ciudad
            datos['direccion'] = i.direccion
            datos['fecha'] = i.fecha_nacimiento
            datos['telefono'] = i.telefono
            datos['especialidad'] = i.especialidad
            datos['celular'] = i.numero_cel
        return datos




    def obtener_informacion_empresa(self, _ndocumento):
        datos = {
            'nombre': None, 'ciudad': None, 'direccion': None,'telefono': None
        }
        temp = usuario.get_base(self).execute(
            """
            select ciudad, direccion, nombre, telefono from rol_usuario
            where rol = 'paciente' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            datos['nombre'] = i.nombre
            datos['ciudad'] = i.ciudad
            datos['direccion'] = i.direccion
            datos['telefono'] = i.telefono
        return datos




    def actualizar_datos_paciente(self, _datosn, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            update rol_usuario 
            set apellidos = %s, ciudad = %s, direccion = %s, 
            nombre = %s, telefono = %s
            where rol = 'paciente' and nro_documento = %s
            """,
            (_datosn['apellido'], _datosn['ciudad'], _datosn['direccion'], _datosn['nombre'], _datosn['telefono'], _ndocumento)
        )




    def actualizar_datos_recepcionista(self, _datosn, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            update rol_usuario 
            set apellidos = %s, ciudad = %s, direccion = %s, 
            nombre = %s, telefono = %s
            where rol = 'recepcionista' and nro_documento = %s
            """,
            (_datosn['apellido'], _datosn['ciudad'], _datosn['direccion'], _datosn['nombre'], _datosn['telefono'], _ndocumento)
        )




    def actualizar_datos_enfermero(self, _datosn, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            update rol_usuario 
            set apellidos = %s, ciudad = %s, direccion = %s, 
            nombre = %s, telefono = %s
            where rol = 'enfermero' and nro_documento = %s
            """,
            (_datosn['apellido'], _datosn['ciudad'], _datosn['direccion'], _datosn['nombre'], _datosn['telefono'], _ndocumento)
        )
        
        temp = usuario.get_base(self).execute(
            """
            select * from asignacion_examenes
            """
        )
        for i in temp:
            if i.id_enfermero == _ndocumento:
                temp = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes
                    set apellido = %s, nombre = %s
                    where tipo_examen = %s
                    """,
                    (_datosn['apellido'], _datosn['nombre'], i.tipo_examen)
                )




    def actualizar_datos_doctor(self, _datosn, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            update rol_usuario 
            set apellidos = %s, ciudad = %s, direccion = %s, especialidad = %s, 
            nombre = %s, numero_cel = %s, telefono = %s
            where rol = 'doctor' and nro_documento = %s
            """,
            (_datosn['apellido'], _datosn['ciudad'], _datosn['direccion'], _datosn['especialidad'],
            _datosn['nombre'], _datosn['celular'], _datosn['telefono'], _ndocumento)
        )




    def cambiar_examenesi(self, _ndocumento, _examen, tnombre, tapellido):
        texa = None
        temp = usuario.get_base(self).execute(
            """
            select * from asignacion_examenes
            """
        )
        for i in temp:
            if i.id_enfermero == _ndocumento:
                texa = i.tipo_examen

        temp = usuario.get_base(self).execute(
            """
            select * from asignacion_examenes
            """
        )
        for y in temp:
            if y.tipo_examen == _examen:
                bb = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes 
                    set nombre = %s, apellido = %s, id_enfermero = %s
                    where tipo_examen = %s
                    """,
                    (y.nombre, y.apellido, y.id_enfermero, texa)
                )
                bb = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes 
                    set nombre = %s, apellido = %s, id_enfermero = %s
                    where tipo_examen = %s
                    """,
                    (tnombre, tapellido, _ndocumento, _examen)
                )
    



    def cambiar_examenesme(self, _ndocumento, _examen, tnombre, tapellido):
        temp = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes 
                    set nombre = %s, apellido = %s, id_enfermero = %s
                    where tipo_examen = %s
                    """,
                    (tnombre, tapellido, _ndocumento, _examen)
                )




    def cambiar_examenesma(self, _ndocumento, _examen, tnombre, tapellido):
        texa = None
        temp = usuario.get_base(self).execute(
            """
            select * from asignacion_examenes
            """
        )
        for i in temp:
            if i.nro_documento == _ndocumento:
                texa = i.tipo_examen
        
        temp = usuario.get_base(self).execute(
            """
            select * from asignacion_examenes
            """
        )
        for y in temp:
            if y.tipo_examen == _examen:
                bb = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes 
                    set nombre = %s, apellido = %s, id_enfermero = %s
                    where tipo_examen = %s
                    """,
                    (tnombre, tapellido, _ndocumento, _examen)
                )
                bb = usuario.get_base(self).execute(
                    """
                    update asignacion_examenes 
                    set nombre = %s, apellido = %s, id_enfermero = %s
                    where tipo_examen = %s
                    """,
                    (None, None, None, texa)
                )




    def cambiar_examen(self, _ndocumento, _examen):
        nombret = None
        apellidot = None
        enf = None
        exa = None
        temp = usuario.get_base(self).execute(
            """
            select nombre, apellidos from rol_usuario where rol = 'enfermero' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        for i in temp:
            nombret = i.nombre
            apellidot = i.apellidos
        temp = usuario.get_base(self).execute(
            """
            select count(nro_documento) from rol_usuario where rol = 'enfermero'
            """
        )
        for i in temp:
            enf = i[0]
        temp = usuario.get_base(self).execute(
            """
            select count(tipo_examen) from asignacion_examenes
            """
        )
        for i in temp:
            exa = i[0]

        if enf == exa:
            self.cambiar_examenesi(_ndocumento, _examen, nombret, apellidot)
        elif exa < enf:
            self.cambiar_examenesme(_ndocumento, _examen, nombret, apellidot)
        else:
            self.cambiar_examenesma(_ndocumento, _examen, nombret, apellidot)
        





    def actualizar_datos_empresa(self, _datons, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            update rol_usuario 
            set ciudad = %s, direccion = %s, nombre = %s telefono = %s
            where rol = 'empresa' and nro_documento = %s
            """,
            (_datosn['ciudad'], _datosn['direccion'], _datosn['nombre'], _datosn['telefono'], _ndocumento)
        )




    def eliminar_paciente(self, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            delete from rol_usuario where rol = 'paciente' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        temp = usuario.get_base(self).execute(
            """
            delete from login where nro_documento = %s
            """,
            ([_ndocumento])
        )
    



    def eliminar_recepcionista(self, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            delete from rol_usuario where rol = 'recepcionista' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        temp = usuario.get_base(self).execute(
            """
            delete from login where nro_documento = %s
            """,
            ([_ndocumento])
        )




    def eliminar_enfermero(self, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            delete from rol_usuario where rol = 'enfermero' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        temp = usuario.get_base(self).execute(
            """
            delete from login where nro_documento = %s
            """,
            ([_ndocumento])
        )




    def eliminar_doctor(self, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            delete from rol_usuario where rol = 'doctor' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        temp = usuario.get_base(self).execute(
            """
            delete from login where nro_documento = %s
            """,
            ([_ndocumento])
        )




    def eliminar_empresa(self, _ndocumento):
        temp = usuario.get_base(self).execute(
            """
            delete from rol_usuario where rol = 'empresa' and nro_documento = %s
            """,
            ([_ndocumento])
        )
        temp = usuario.get_base(self).execute(
            """
            delete from login where nro_documento = %s
            """,
            ([_ndocumento])
        )




a = gestor_bd('historias_clinicas')
a.conectar_bd()
b = administrador("aaa@gmail.com", "123", a.get_sesion(), "aaa", "bbbb", "01010", "cali", "cra83c", 1212313)
b.cambiar_examen(16001462, 'urodinamia')




