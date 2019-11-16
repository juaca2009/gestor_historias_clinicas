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
        


    def despachar_paciente(self):
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
        return self.__consulta.get_historia()

    def ingresar_comentarios(self, _comentario):
        self.__consulta.set_comentario(_comentario)


a = gestor_bd('historias_clinicas')
a.conectar_bd()
c = atencion_pool(a.get_sesion())
c.cargar_consultas(1)
b = doctor("aaa@gmail.com", "123", a.get_sesion(), "aaa", "bbbb", "01010", "cali", "cra83c", 1212313, 'general', 1, c)
bo = False
while bo == False:
    if b.llamar_paciente() == 1:
        bo = True
print(b.obtener_historia_clinicas())
b.ingresar_comentarios('primera consulta con el medico general')
b.despachar_paciente()



        