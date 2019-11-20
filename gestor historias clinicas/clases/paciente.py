from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario

class paciente(usuario):
    def __init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
         usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)

    def obtener_historia_paciente(self):
        lis = list()
        lis2 = list()
        temp = temp = usuario.get_base(self).execute(
            """
            select id_historia, apellido_doctor, apellido_enfermero, 
            comentarios, especialidad, fecha, nombre_doctor, 
            nombre_enfermero, tipo_examen from paciente_historia
            where nro_documento = %s
            """,
            ([self.get_documento()])
        )
        for i in temp:
            lis.append(i.id_historia)
            lis.append(i.fecha)
            lis.append(i.especialidad)
            lis.append(i.tipo_examen)
            lis.append(i.comentarios)
            lis2.append(lis)
            lis = list()
        return lis2
            