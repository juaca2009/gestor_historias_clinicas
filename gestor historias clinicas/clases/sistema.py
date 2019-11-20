from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from administrador import administrador
from atencion_pool import atencion_pool
from doctor import doctor
from empresa import empresa
from enfermero import enfermero
from paciente import paciente
from recepcionista import recepcionista
from validate_email import validate_email
from datetime import date

class sistema(object):
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



#metodos administrador
    def verificar_correo(self, _correo):
        return validate_email(_correo, verify=True)



    def agregar_paciente(self, _nombre, _apellido, _fechan, _ciudad, _direccion,
                         _tdocumento, _ndocumento, _ntelefono, _correo):
        if _nombre != None and _apellido != None and _fechan != None and _ciudad != None and _direccion != None and _tdocumento != None and _ndocumento  != None and _ntelefono != None and _correo != None:
            if type(_nombre) is str and type(_apellido) is str and type(_ciudad) is str and type(_direccion) is str and type(_tdocumento) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__admin.agregar_paciente(_nombre, _apellido, _fechan, _ciudad, _direccion,
                                                  _tdocumento, _ndocumento, _ntelefono, _correo)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0


    def agregar_recepcionista(self, _nombre, _apellido, _fechan, _ciudad, _direccion, 
                              _tdocumento, _ndocumento, _ntelefono, _correo):
        if _nombre != None and _apellido != None and _fechan != None and _ciudad != None and _direccion != None and _tdocumento != None and _ndocumento  != None and _ntelefono != None and _correo != None:
            if type(_nombre) is str and type(_apellido) is str and type(_ciudad) is str and type(_direccion) is str and type(_tdocumento) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__admin.agregar_recepcionista(_nombre, _apellido, _fechan, _ciudad, _direccion,
                                                       _tdocumento, _ndocumento, _ntelefono, _correo)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0

    
    def agregar_enfermero(self, _nombre, _apellido, _fechan, _ciudad, _direccion, 
                          _tdocumento, _ndocumento, _ntelefono, _correo):
        if _nombre != None and _apellido != None and _fechan != None and _ciudad != None and _direccion != None and _tdocumento != None and _ndocumento  != None and _ntelefono != None and _correo != None:
            if type(_nombre) is str and type(_apellido) is str and type(_ciudad) is str and type(_direccion) is str and type(_tdocumento) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__admin.agregar_enfermero(_nombre, _apellido, _fechan, _ciudad, _direccion,
                                                   _tdocumento, _ndocumento, _ntelefono, _correo)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0


    def agregar_doctor(self, _nombre, _apellido, _fechan, _ciudad, _direccion, 
                       _tdocumento, _ndocumento, _ntelefono, _correo,  _celular, _especialidad):
        if _nombre != None and _apellido != None and _fechan != None and _ciudad != None and _direccion != None and _tdocumento != None and _ndocumento  != None and _ntelefono != None and _correo != None and _celular != None and _especialidad != None:
            if type(_nombre) is str and type(_apellido) is str and type(_ciudad) is str and type(_direccion) is str and type(_tdocumento) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str and type(_celular) is int and type(_especialidad) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__admin.agregar_doctor(_nombre, _apellido, _fechan, _ciudad, _direccion,
                                                   _tdocumento, _ndocumento, _ntelefono, _correo, _celular, _especialidad)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0


    def agregar_empresa(self, _correo, _nombre, _ciudad, _direccion, _ndocumento, _ntelefono):
        if _nombre != None and _ciudad != None and _direccion != None and _ndocumento  != None and _ntelefono != None and _correo != None:
            if type(_nombre) is str and type(_ciudad) is str and type(_direccion) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__admin.agregar_empresa(_correo, _nombre, _ciudad, _direccion,
                                                   'nit', _ndocumento, _ntelefono)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0



    def asignar_examen(self, _tipo_examen, _documento):
        existe = False
        examen = False
        if _tipo_examen != None and _documento !=None:
            if type(_tipo_examen) is str and type(_documento) is int:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login
                    """
                )
                for i in temp:
                    if i.nro_documento == _documento and i.rol == 'enfermero':
                        existe = True
                temp = self.__base.get_sesion().execute(
                    """
                    select * from asignacion_examenes
                    """
                )
                for i in temp:
                    if i.tipo_examen == _tipo_examen:
                        examen = True
                if existe == True and examen == True:
                    self.__admin.asignar_examen(_tipo_examen, _documento)
                    return 1
                else:
                    return 0
            else:
                return 0
        return 0











#metodos generales
    def iniciar_sesion(self, _correo, _contrasena):
        if (_correo != None and _contrasena != None):
            if type(_correo) is str and type(_contrasena) is str:
                rol = None
                documento = None
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login
                    """
                )
                for i in temp:
                    if i.correo == _correo and i.contrasena == _contrasena:
                        rol = i.rol
                        documento = i.nro_documento
                        break
                if rol != None and documento != None:
                    if rol == 'administrador':
                        self.iniciar_administrador(documento, _correo, _contrasena)
                        return 1
                    elif rol == 'recepcionista':
                        self.iniciar_recepcionista(documento, _correo, _contrasena)
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
                else:
                    return 0
            else:
                return 0

        else:
            return 0



    def iniciar_administrador(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(

            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            where rol = 'administrador' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__admin = administrador(_correo, _contra, self.__base.get_sesion(), i.nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, _documento)

    def iniciar_recepcionista(self,  _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            where rol = 'recepcionista' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__recepcionista = recepcionista(_correo, _contra, self.__base.get_sesion(), i.nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, _documento)

    
    def iniciar_empresa(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, ciudad, direccion from rol_usuario
            where rol = 'empresa' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__empresa = empresa(_correo, _contra, self.__base.get_sesion(), i.nombre, None, None, i.ciudad, i.direccion, _documento)


    def iniciar_paciente(self, _documento, _correo, _contra):
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            where rol = 'paciente' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:            
            self.__paciente = paciente(_correo, _contra, self.__base.get_sesion(), i.nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, _documento)
    

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
            self.__atention_pool.cargar_consultas(i.nro_cola)
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion, especialidad from rol_usuario
            where rol = 'doctor' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__doctor = doctor(_correo, _contra, self.__base.get_sesion(), i.nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, _documento, i.especialidad, cola, self.__atention_pool)
        


    def iniciar_enfermero(self,  _documento, _correo, _contra):
        cola = None
        temp = self.__base.get_sesion().execute(
            """
            select * from asignacion_examenes
            """
        )
        for i in temp:
            if i.id_enfermero == _documento:
                cola = i.nro_cola
        
        temp = self.__base.get_sesion().execute(
            """
            select nombre, apellidos, fecha_nacimiento, ciudad, direccion from rol_usuario
            where rol = 'enfermero' and nro_documento = %s
            """,
            ([_documento])
        )
        for i in temp:
            self.__enfermero = enfermero(_correo, _contra, self.__base.get_sesion(), i.nombre, i.apellidos, i.fecha_nacimiento, i.ciudad, i.direccion, _documento, cola, self.__atention_pool, None)
        if (cola != None):
            self.__enfermero.set_asignacion(True)
        else:
            self.__enfermero.set_asignacion(False)

    def get_asignacion_examenes(self):
        lis = list()
        lis2 = list()
        temp = self.__base.get_sesion().execute(
            """
            select * from asignacion_examenes
            """
        )
        for i in temp:
            lis.append(i.tipo_examen)
            lis.append(i.id_enfermero)
            lis.append(i.apellido)
            lis.append(i.nombre)
            lis2.append(lis)
            lis = list()
        return lis2














#metodos empresa
    def registrar_paciente(self, _nombre, _apellido, _fechan, _ciudad, _direccion,
                            _tdocumento, _ndocumento, _ntelefono, _correo):
        if _nombre != None and _apellido != None and _fechan != None and _ciudad != None and _direccion != None and _tdocumento != None and _ndocumento  != None and _ntelefono != None and _correo != None:
            if type(_nombre) is str and type(_apellido) is str and type(_ciudad) is str and type(_direccion) is str and type(_tdocumento) is str and type(_ndocumento) is int and type(_ntelefono) is int and type(_correo) is str:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento != None:
                        return 0 
                if self.verificar_correo(_correo) == True:
                    self.__empresa.registrar_paciente(_nombre, _apellido, _fechan, _ciudad, _direccion,
                                                  _tdocumento, _ndocumento, _ntelefono, _correo)
                    return 1
                return 0
            else:
                return 0
        else:
            return 0

    
    def agendar_consulta_general_empresa(self, _ndocumento):
        existe = False
        if _ndocumento != None:
            if type(_ndocumento) is int:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento == _ndocumento and i.rol == 'paciente':
                        existe = True
                if existe == True:
                    self.__empresa.agendar_consulta_general(_ndocumento)
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    def agendar_examen_empresa(self, _tipo_examen, _ndocumento):
        existe = False
        examen = False
        if _tipo_examen != None and _ndocumento != None:
            if type(_tipo_examen) is str and type(_ndocumento) is int:
                temp = self.__base.get_sesion().execute(
                    """
                    select * from login where nro_documento = %s
                    """,
                    ([_ndocumento])
                )
                for i in temp:
                    if i.nro_documento == _ndocumento and i.rol == 'paciente':
                        existe = True
                temp = self.__base.get_sesion().execute(
                    """
                    select * from asignacion_examenes where tipo_examen = %s
                    """,
                    ([_tipo_examen])
                )
                for i in temp:
                    if i.tipo_examen != None:
                        examen = True
                if existe == True and examen == True:
                    self.__empresa.agendar_examen(_tipo_examen, _ndocumento)
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0













#metodos enfermero
    def llamar_paciente_enfermero(self):
        cola = False
        if(self.__enfermero.get_asignacion() == True):
            temp = self.__base.get_sesion().execute(
                """
                select max(posicion) from colas_examenes where nro_cola = %s
                """,
                ([self.__enfermero.get_nro_cola()])
            )
            for i in temp:
                if i[0] != None:
                    cola = True
            if cola == True:
                return self.__enfermero.llamar_paciente()
            else:
                return 0
        else:
            return 0

    def mostrar_historia_enfermero(self):
        return self.__enfermero.obtener_historia_clinicas()

    def despachar_paciente_enfermero(self, _comentario):
        if _comentario != None:
            if type(_comentario) is str:

                self.__enfermero.despachar_paciente(_comentario)
                return 1
            else:
                return 0
        else:
            return 0 




#metodos doctor
    def llamar_paciente_doctor(self):
        cola = False
        temp = self.__base.get_sesion().execute(

            """
            select max(posicion) from colas_consultas where nro_cola = %s
            """,
            ([self.__doctor.get_nro_cola()])
        )
        for i in temp:
            if i[0] != None:
                cola = True
        if cola == True:
            return self.__doctor.llamar_paciente()
        else:
            return 0



    def despachar_paciente_doctor(self):
        self.__doctor.despachar_paciente()


    def mostrar_historia_doctor(self):
        return self.__doctor.obtener_historia_clinicas()

    def agendar_examen_doctor(self, _tipo_examen):
        examen = False
        if type(_tipo_examen) is str:
            temp = self.__base.get_sesion().execute(
                """
                select * from asignacion_examenes where tipo_examen = %s
                """,
                ([_tipo_examen])
            )
            for i in temp:
                if i.tipo_examen != None:
                    examen = True
            if examen == True:
                self.__doctor.agendar_examen(_tipo_examen)
                return 1
            else:
                return 0
        else:
            return 0
        

    def ingresar_comentario(self, _comentario):
        if _comentario != None or _comentario != '':
            if type(_comentario) is str:
                self.__doctor.ingresar_comentarios(_comentario)
                return 1
            else:
                return 0
        else:
            return 0











# a = sistema()
# print(a.get_asignacion_examenes())
# a.iniciar_sesion('camia177@gmail.com', '2sd44f6h')
# print(a.llamar_paciente_doctor())
# print(a.agendar_examen_doctor('urodinamia'))
# print(a.despachar_paciente_doctor('sano, pero no me convence'))
#b = date(1997, 1, 23)
#a.iniciar_sesion('luis.oviedolutkens@gmail.com', 'mqouq7c4')
#a.agendar_examen_empresa('endoscopia', 1286456)
#print(a.llamar_paciente_enfermero())
#print(a.mostrar_historia_enfermero())
#print(a.despachar_paciente_enfermero('uretra sana'))




        

