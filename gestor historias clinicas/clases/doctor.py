from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario
from atencion_pool import atencion_pool

class doctor(usuario):
    def __init__(self,  _correo, _contra, _base, _nombre, _apellido,
                 _fechan, _ciudad, _direccion, _documento, _especialidad, _nro_cola, _obj):
        usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)
        self.__especialidad = _especialidad
        self.__nro_cola = _nro_cola
        self.__consulta = None
        self.__obcj_pool = _obj

    def get_especialidad(self):
        return self.__especialidad

    def get_nro_cola(self):
        return self.__nro_cola

    def set_especialidad(self, _espec):
        self.__especialidad = _espec

    def set_nro_cola(self, _cola):
        self.__nro_cola = _cola




    def buscar_examenes(self):
        cons = self.__obcj_pool.obtener_primera_posicion()
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes
            """
        )
        for i in temp:
            if cons.get_documento() == i.nro_documento:
                if(i.posicion == 0):
                    return 1

        return 0




    def buscar_consultas(self):
        cons = self.__obcj_pool.obtener_primera_posicion()
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas
            """
        )
        for i in temp:
            if i.nro_cola != self.__nro_cola:
                if cons.get_documento() == i.nro_documento:
                    if i.posicion == 0:
                        return 1

        return 0





    def cambiar_cola(self):
        cont = 0
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                cont = cont + 1
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                if i.posicion == 1:
                    ac = usuario.get_base(self).execute(
                        """
                        update table colas_consultas set posicion = %s
                        where nro_cola = %s and nro_documento = %s
                        """,
                        (cont, self.__nro_cola, i.nro_documento)
                    )
                else:
                    post = i.posicion - 1
                    ac = usuario.get_base(self).execute(
                        """
                        update table colas_consultas set posicion = %s
                        where nro_cola = %s and nro_documento = %s
                        """,
                        (post, self.__nro_cola, i.nro_documento)
                    )
        self.__obcj_pool.cargar_consultas(self.__nro_cola)




    def atender_paciente(self):
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                post = i.posicion - 1
                ac = usuario.get_base(self).execute(
                    """
                    update colas_consultas set posicion = %s
                    where nro_cola = %s and nro_documento = %s
                    """,
                    (post, self.__nro_cola, i.nro_documento)
                )
        self.__obcj_pool.cargar_consultas(self.__nro_cola)
        self.__consulta = self.__obcj_pool.obtener_primera_posicion()
        


    def despachar_paciente(self, _comentario):
        self.ingresar_comentarios(_comentario)
        self.__consulta.cargar_comentarios()
        temp = usuario.get_base(self).execute(
            """
            select * from colas_consultas where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion == 0:
                delp = usuario.get_base(self).execute(
                    """
                    delete from colas_consultas where nro_cola = %s and nro_documento = %s
                    """,
                    (self.__nro_cola, i.nro_documento)
                )
                break
        self.__obcj_pool.cargar_consultas(self.__nro_cola)


    def llamar_paciente(self):
        if(self.buscar_consultas() == 1 or self.buscar_examenes() == 1):
            self.cambiar_cola()
            return 0
        else:
            self.atender_paciente()
            return 1

    def obtener_historia_clinicas(self):
        histo = False
        docu = self.__consulta.get_documento()
        primera_vez = 'este usuario no posee historia clinica'
        temp = usuario.get_base(self).execute(
            """
            select * from paciente_historia where nro_documento = %s
            """,
            ([docu])
        )
        for i in temp:
            if i.id_historia != None:
                histo = True
        if histo == True:
            return self.__consulta.get_historia()
        else:
            return primera_vez

    def ingresar_comentarios(self, _comentario):
        self.__consulta.set_comentario(_comentario)

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


    def agendar_examen(self, _tipo_examen):
        espec = None
        enf = {'nombre': None, 'apellido': None, 'cola': None}
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
            (enf['cola'], self.__consulta.get_documento(), enf['apellido'], self.__consulta.get_apellido_paciente(), enf['nombre'], self.__consulta.get_nombre_paciente(), self.aumentar_posicion_examen(enf['cola']), _tipo_examen)
        )
        temp = usuario.get_base(self).execute(
            """
            insert into paciente_examenes(nro_documento, tipo_examen, estado) values(%s, %s, 'false')
            """,
            (_ndocumento, _tipo_examen)
        )
        temp = usuario.get_base(self).execute(
            """
            insert into paciente_examenes(nro_documento, tipo_examen, estado) values(%s, %s, 'false')
            """,
            (self.__consulta.get_documento(), _tipo_examen)
        )
        self.agendar_consulta_parcial(espec, self.__consulta.get_documento(), self.__consulta.get_nombre_paciente(), self.__consulta.get_apellido_paciente())



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
# c = atencion_pool(a.get_sesion())
# c.cargar_consultas(1)
# b = doctor("aaa@gmail.com", "123", a.get_sesion(), "aaa", "bbbb", "01010", "cali", "cra83c", 1212313, 'general', 1, c)
# bo = False
# while bo == False:
#     if b.llamar_paciente() == 1:
#         bo = True
# print(b.obtener_historia_clinicas())
# b.ingresar_comentarios('primera consulta con el medico general')
# b.despachar_paciente()



        