from gestor_bd import gestor_bd
from cassandra.cluster import Cluster
from usuario import usuario

class paciente(usuario):
    def __init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
         usuario.__init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento)

    def obtener_historia(self):
        temp = self.__base.execute(
            """
            select id_historia, apellido_doctor, apellido_enfermero, 
            comentarios, especialidad, fecha, nombre_doctor, 
            nombre_enfermero, tipo_examen from paciente_historia
            where nro_documento = %s
            """,
            ([usuario.get_documento(self)])
        )
        for i in temp:
            historia_clinica = 'nro historia:' + ' ' + str(i.id_historia)
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'nombre doctor:' + ' ' + i.nombre_doctor
            historia_clinica = self.__historia_clinica + " /n"
            historia_clinica = self.__historia_clinica + 'apellido doctor:' + ' ' + i.apellido_doctor
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'especialidad:' + ' ' + i.especialidad
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'nombre enfermero:' + ' ' + str(i.nombre_enfermero)
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'apellido enfermero:' + ' ' + str(i.apellido_enfermero)
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'fecha:' + ' ' + str(i.fecha)
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'tipo examen:' + ' ' + str(i.tipo_examen)
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + 'comentarios/resultados:' + ' ' + str(i.comentarios) 
            historia_clinica = self.__historia_clinica + '/n'
            historia_clinica = self.__historia_clinica + '====================================================================================================================='