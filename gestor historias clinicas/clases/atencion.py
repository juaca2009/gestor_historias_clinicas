from gestor_bd import gestor_bd
from cassandra.cluster import Cluster

class atencion(object):
    def __init__(self, ba, fe, esta, doc, nom, ape):
        self.__id_consulta = 0
        self.__fecha = fe
        self.__estado = esta
        self.__documento = doc
        self.__nombre_paciente = nom
        self.__apellido_paciente = ape
        self.__historia_clinica = None
        self.__base = ba
    
    def set_id(self, id):
        self.__id_consulta = id
    
    def set_fecha(self, fec):
        self.__fecha  = fec

    def set_estado(self, esta):
        self.__estado = esta
    
    def set_nombre_paciente(self, nom):
        self.__nombre_paciente = nom

    def set_apellido_paciente(self, ape):
        self.__apellido_paciente = ape

    def set_historia(self, his):
        self.__historia_clinica = his

    def set_documento(self, docu):
        self.__documento = docu

    def get_base(self):
        return self.__base

    def get_id(self):
        return self.__id_consulta

    def get_fecha(self):
        return self.__fecha
    
    def get_estado(self):
        return self.__estado

    def get_nombre_paciente(self):
        return self.__nombre_paciente

    def get_apellido_paciente(self):
        return self.__apellido_paciente

    def get_historia(self):
        return self.__historia_clinica

    def get_documento(self):
        return self.__documento

    def obtener_historia_clinina(self):
        temp = self.__base.execute(
            """
            select id_historia, apellido_doctor, apellido_enfermero, 
            comentarios, especialidad, fecha, nombre_doctor, 
            nombre_enfermero, tipo_examen from paciente_historia
            where nro_documento = %s
            """,
            ([self.get_documento()])
        )
        for i in temp:
            self.__historia_clinica = 'nro historia:' + ' ' + str(i.id_historia)
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'nombre doctor:' + ' ' + i.nombre_doctor
            self.__historia_clinica = self.__historia_clinica + " /n"
            self.__historia_clinica = self.__historia_clinica + 'apellido doctor:' + ' ' + i.apellido_doctor
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'especialidad:' + ' ' + i.especialidad
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'nombre enfermero:' + ' ' + str(i.nombre_enfermero)
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'apellido enfermero:' + ' ' + str(i.apellido_enfermero)
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'fecha:' + ' ' + str(i.fecha)
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'tipo examen:' + ' ' + str(i.tipo_examen)
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + 'comentarios/resultados:' + ' ' + str(i.comentarios) 
            self.__historia_clinica = self.__historia_clinica + '/n'
            self.__historia_clinica = self.__historia_clinica + '====================================================================================================================='



    def aumentar_id_historias(self):
        tmax = self.__base.execute(
            """
            select max(id_historia) as max from paciente_historia 
            where nro_documento = %s
            """,
            ([self.get_documento()])
        )
        for i in tmax:
            temp = i[0]
        if temp == None:
            return 1
        else:
            return temp + 1



# a = gestor_bd('historias_clinicas')
# a.conectar_bd()
# b = atencion(a.get_sesion())
# b.set_documento(12234)
# print(b.aumentar_id_historias())