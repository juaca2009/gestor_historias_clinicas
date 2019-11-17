from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario
from atencion_pool import atencion_pool

class enfermero(usuario):
    def __init__(self,  _correo, _contra, _base, _nombre, _apellido,
                 _fechan, _ciudad, _direccion, _documento, _nro_cola, _obj, _asignacion):
        usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)
        self.__nro_cola = _nro_cola
        self.__consulta = None
        self.__obcj_pool = _obj
        self.__asignacion = _asignacion
    
    def get_nro_cola(self):
        return self.__nro_cola

    def get_asignacion(self):
        return self.__asignacion

    def set_nro_cola(self, _cola):
        self.__nro_cola = _cola

    def set_asignacion(self, _asig):
        self.__asignacion = _asig

    def buscar_examenes(self):
        cons = self.__obcj_pool.obtener_primera_posicion()
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes
            """
        )
        for i in temp:
            if i.nro_cola != self.__nro_cola:
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
                if cons.get_documento() == i.nro_documento:
                    if i.posicion == 0:
                        return 1

        return 0


    def cambiar_cola(self):
        cont = 0
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                cont = cont + 1
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                if i.posicion == 1:
                    ac = usuario.get_base(self).execute(
                        """
                        update table colas_examenes set posicion = %s
                        where nro_cola = %s and nro_documento = %s
                        """,
                        (cont, self.__nro_cola, i.nro_documento)
                    )
                else:
                    post = i.posicion - 1
                    ac = usuario.get_base(self).execute(
                        """
                        update table colas_examenes set posicion = %s
                        where nro_cola = %s and nro_documento = %s
                        """,
                        (post, self.__nro_cola, i.nro_documento)
                    )
        self.__obcj_pool.cargar_examenes(self.__nro_cola)


    def atender_paciente(self):
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                post = i.posicion - 1
                ac = usuario.get_base(self).execute(
                    """
                    update colas_examenes set posicion = %s
                    where nro_cola = %s and nro_documento = %s
                    """,
                    (post, self.__nro_cola, i.nro_documento)
                )
        self.__obcj_pool.cargar_examenes(self.__nro_cola)
        self.__consulta = self.__obcj_pool.obtener_primera_posicion()


    def despachar_paciente(self):
        self.confirmar_examen()
        self.__consulta.cargar_comentarios()
        temp = usuario.get_base(self).execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([self.__nro_cola])
        )
        for i in temp:
            if i.posicion == 0:
                delp = usuario.get_base(self).execute(
                    """
                    delete from colas_examenes where nro_cola = %s and nro_documento = %s
                    """,
                    (self.__nro_cola, i.nro_documento)
                )
                break
        self.__obcj_pool.cargar_examenes(self.__nro_cola)


    def llamar_paciente(self):
        if(self.buscar_consultas() == 1 or self.buscar_examenes() == 1):
            self.cambiar_cola()
            return 0
        else:
            self.atender_paciente()
            return 1

    def obtener_historia_clinicas(self):
        return self.__consulta.get_historia()

    def ingresar_comentarios(self, _comentario):
        self.__consulta.set_comentario(_comentario)

    def confirmar_examen(self):
        temp = usuario.get_base(self).execute(
            """
            update paciente_examenes set estado = 'true'
            where nro_documento = %s and tipo_examen = %s
            """,
            (self.__consulta.get_documento(), self.__consulta.get_tipo_examen())
        )

    
    def verificar_dependencias(self):
        espc = None
        dependencias = list()
        examenes = list()
        temp = usuario.get_base(self).execute(
            """
            select especializacion, tipo_examen from  especializacion_examenes
            """
        )
        for i in temp:
            if i.tipo_examen == self.__consulta.get_tipo_examen():
                espc = i.especializacion

        temp = usuario.get_base(self).execute(
            """
            select tipo_examen from  especializacion_examenes where  especializacion %s 
            """,
            ([espc])
        )
        for i in temp:
            dependencias.append(i)

        temp = usuario.get_base(self).execute(
            """
            select * from paciente_examenes where nro_documento = %s
            """,
            ([self.__consulta.get_documento()])
        )
        for i in temp:
            if i.tipo_examen in dependencias:
                examenes.append(i.estado)

        if examenes.count('true') == len(examenes):
            temp = usuario.get_base(self).execute(
                """
                select * from colas_consultas
                """
            )
            for i in temp:
                if self.__consulta.get_documento() == i.nro_documento and espc == i.especialidad:
                    ac = usuario.get_base(self).execute(
                        """
                        update colas_consultas set posicion = %s
                        where nro_cola = %s and nro_documento = %s
                        """,
                        (self.aumentar_posicion_consulta(i._nro_cola), i.nro_cola, self.__consulta.get_documento())
                    )


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


        

    