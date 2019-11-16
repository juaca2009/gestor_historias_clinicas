from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

class recepcionista(usuario):
    def __init__(self,  _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
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