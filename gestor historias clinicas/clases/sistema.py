from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from administrador import administrador
from atencion_pool import atencion_pool
from doctor import doctor
from empresa import empresa
from enfermero import enfermero
from paciente import paciente
from recepcionista import recepcionista

class sistema():
    __instancia = None
    def __new__(self):
        if not self.__instancia:
            self.__instancia = super(sistema, self).__new__(self)
            self.__base = gestor_bd('historias_clinicas')
            self.__base.conectar_bd()
            self.__atention_pool = atencion_pool(self.__base.get_sesion())
            self.__admin = None
            self.__doctor = None
            self.__enfermero = None
            self.__paciente = None
            self.__recepcionista = None
            self.__empresa = None
        return self.__instancia

    
    def iniciar_sesion(self, _correo, _contrasena):
        if (_correo != None or _contrasena != None):
            if type(_correo) is str and type(_contrasena) is str:
                rol = None
                documento = None
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login
                    """
                )
                for i in temp:
                    if i.correo == _correo and i._contrasena == _contrasena:
                        rol = i.rol
                        documento = i.nro_documento
                        break
                if rol != None and documento != None:
                    if rol == 'administrador':
                        self.iniciar_administrador(documento, _correo, _contrasena)
                        return 1
                    elif rol == 'recepcionista':
                        self.iniciar_recepcionista(documento, _correo, _contrasena):
                        return 2
                    elif rol == 'empresa':
                        self.iniciar_empresa(documento, _correo, _contrasena)
                        return 3
                    elif rol == 'paciente':
                        self.iniciar_paciente(documento, _correo, _contrasena)
                        return 4
                    elif rol == 'doctor':
                        self.iniciar_doctor(documento, _correo, _contrasena)
                        return 5
                    else:
                        self.iniciar_enfermero(documento, _correo, _contrasena)
                        return 6



    def iniciar_administrador(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(

            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            whrere rol = 'administrador' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__admin = administrador(_correo, _contra, self.__base.get_sesion(), i._nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, documento)

    def iniciar_recepcionista(self,  _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            whrere rol = 'recepcionista' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__recepcionista = recepcionista(_correo, _contra, self.__base.get_sesion(), i._nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, documento)

    
    def iniciar_empresa(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, ciudad, direccion from rol_usuario
            whrere rol = 'empresa' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__empresa = empresa(_correo, _contra, self.__base.get_sesion(), i._nombre, None, None, i.ciudad, i.direccion, documento)


    def iniciar_paciente(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            whrere rol = 'paciente' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:            
            self.__paciente = paciente(_correo, _contra, self.__base.get_sesion(), i._nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, documento)
    

    def iniciar_doctor(self,  _documento, _correo, _contra):
        cola = None
        temp = self.__base.get_sesion().execute(
            """
            select nro_cola from asignacion_consultas where nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            cola = i.nro_cola
            self.__atention_pool.cargar_consultas(i._nro_cola)
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion, especialidad from rol_usuario
            whrere rol = 'doctor' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__doctor = doctor(correo, _contra, self.__base.get_sesion(), i._nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, documento, i.especialidad, cola, self.__atention_pool)
        


    def iniciar_enfermero(self,  _documento, _correo, _contra):
        cola = None
        temp = self.__base.get_sesion().execute(
            """
            select * from asignacion_examenes
            """,
            ([_documento])
        )
        for i in temp:
            if i.id_enfermero == _documento:
                cola = i.nro_cola
        
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            whrere rol = 'enfermero' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__enfermero = enfermero(_correo, _contra, self.__base.get_sesion(), i._nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, documento, cola, self.__atention_pool, None)
        if (cola != None):
            self.__enfermero.set_asignacion(True)
        else:
            self.__enfermero.set_asignacion(False)


a = sistema()

        

