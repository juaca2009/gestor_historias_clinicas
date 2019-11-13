from atencion import atencion
from gestor_bd import gestor_bd
from datetime import date
from cassandra.cluster import Cluster

class examen(atencion):
    def __init__(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop, _tipox):
        atencion.__init__(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop)
        self.__resultados = None
        self.__tipo_examen = _tipox

    def set_resultados(self, _resultado):
        self.__resultados = _resultado
    
    def set_tipo_examen(self, _tipox):
        self.__tipo_examen = _tipox

    def get_resultados(self):
        return self.__resultados

    def get_tipo_examen(self):
        return self.__tipo_examen

    def cargar_resultados(self):
        temp = atencion.get_base(self).execute(
            """
            select nombre, apellido  from asignacion_examenes 
            where tipo_examen = %s
            """,
            ([self.get_tipo_examen()])
        )
        for i in temp:
            nombre_enf = i.nombre
            apellido_enf = i.apellido

        temp = atencion.get_base(self).execute(
            """
            insert into paciente_historia(nro_documento, id_historia, apellido_enfermero, comentarios, fecha, nombre_enfermero, tipo_examen)
            values (%s, %s, %s, %s, %s, %s, %s)
            """,
            (atencion.get_documento(self), atencion.aumentar_id_historias(self), apellido_enf, self.get_resultados(), date.today(), nombre_enf, self.get_tipo_examen())
        )

    def reiniciar_examen(self):
        self.__resultados = None
        self.__tipo_examen = None
        atencion.set_apellido_paciente(self, None)
        atencion.set_documento(self, None)
        atencion.set_estado(self, None)
        atencion.set_fecha(self, None)
        atencion.set_historia(self, None)
        atencion.set_id(self, None)
        atencion.set_nombre_paciente(self, None)

# a = gestor_bd('historias_clinicas')
# a.conectar_bd()
# b = examen(a.get_sesion(), date.today(), 0, 12234, "cami", "hernan", "endoscopia")
# b.cargar_resultados()