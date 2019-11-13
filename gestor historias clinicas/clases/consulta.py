from atencion import atencion
from gestor_bd import gestor_bd
from datetime import date
from cassandra.cluster import Cluster

class consulta(atencion):
    def __init__(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop,
                 _especializacion, _nombred, _apellidod, _documentod):
        atencion.__init__(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop)
        self.__especializacion =_especializacion
        self.__nombre_doctor = _nombred
        self.__apellido_doctor = _apellidod
        self.__documento_doctor =  _documentod
        self.__comentario = None
    
    def get_especializacion(self):
        return self.__especializacion

    def get_nombre_doctor(self):
        return self.__nombre_doctor

    def get_apellido_doctor(self):
        return self.__apellido_doctor

    def get_documento_doctor(self):
        return self.__documento_doctor

    def get_comentario(self):
        return self.__comentario

    def set_comentario(self, _comentario):
        self.__comentario = _comentario

    def cargar_comentarios(self):
        temp = atencion.get_base(self).execute(
            """
            insert into paciente_historia(nro_documento, id_historia, apellido_doctor, comentarios, especialidad, fecha, nombre_doctor)
            values (%s, %s, %s, %s, %s, %s, %s)
            """,
            (atencion.get_documento(self), atencion.aumentar_id_historias(self), self.get_apellido_doctor(), self.get_comentario(), self.get_especializacion(), date.today(), self.get_nombre_doctor())
        )

    def reiniciar_consulta(self):
        self.__apellido_doctor = None
        self.__documento_doctor = None
        self.__nombre_doctor = None
        self.__especializacion = None
        self.__comentario = None
        atencion.set_apellido_paciente(self, None)
        atencion.set_documento(self, None)
        atencion.set_estado(self, None)
        atencion.set_fecha(self, None)
        atencion.set_historia(self, None)
        atencion.set_id(self, None)
        atencion.set_nombre_paciente(self, None)


#a = gestor_bd('historias_clinicas')
#a.conectar_bd()
#b = consulta(a.get_sesion(), date.today(), 0, 12234, "cami", "hernan", "aaa", "camila", "acevedo", 1212121)
# print(b.get_apellido_paciente())
# b.reiniciar_consulta()
# print(b.get_apellido_paciente())
# b.cargar_comentarios()