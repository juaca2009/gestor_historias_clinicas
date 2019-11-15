from gestor_bd import gestor_bd
from atencion import atencion
from examen import examen
from consulta import consulta
from datetime import date


class atencion_pool(object):
    __instancia = None
    __atenciones = list()

    def __new__(self, _base):
        if not self.__instancia:
            self.__instancia = super(atencion_pool, self).__new__(self)
            self.__base = _base
        return self.__instancia

    def get_elemento(self):
        if len(self.__atenciones) > 0:
            return self.__atenciones.pop(0)
        else:
            return None
    
    def crear_examen(self, _base, _posicion, _documento, _nombrep, _apellidop, _tipox):
        return examen(_base, _posicion, _documento, _nombrep, _apellidop, _tipox)

    def crear_consulta(self, _base, _posicion, _documento, _nombrep, _apellidop,
                       _especializacion, _nombred, _apellidod):

        return consulta(_base, _posicion, _documento, _nombrep, _apellidop,
                        _especializacion, _nombred, _apellidod)

    def organizar_atenciones(self):
        cont1 = 0
        cont2 = 0
        max1 = len(self.__atenciones)
        max2 = len(self.__atenciones) - 1
        while cont1 < max1:
            while cont2 < max2:
                temp1 = self.__atenciones[cont2]
                temp2 = self.__atenciones[cont2+1]
                if temp1.get_posicion() > temp2.get_posicion():
                    self.__atenciones[cont2] = temp2
                    self.__atenciones[cont2+1] = temp1

    def cargar_examenes(self, _nro_cola):
        temp = self.__base.execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([_nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                self.__atenciones.append(self.crear_examen(self.__base,i._posicion, i.nro_documento,i.nombre_paciente, i.apellido_paciente, i.tipo_examen))
        self.organizar_atenciones()

    def cargar_consultas(self, _nro_cola):
        temp = self.__base.execute(
            """
            select * from colas_consultas where nro_cola = %s
            """,
            ([_nro_cola])
        )
        for i in temp:
             if i.posicion != None:
                 self.__atenciones.append(self.crear_consulta(self.__base, i.posicion, i.nro_documento, i.nombre_paciente, i.apellido_paciente, i.especialidad, i.nombre_doctor, i.apellido_doctor))
        self.organizar_atenciones()

    def obtener_primera_posicion(self):
        return self.__atenciones[0] 

# a = gestor_bd('historias_clinicas')
# a.conectar_bd()
# b = atencion_pool("enfermero")
# ex = b.get_elemento()
# if ex == None:
#     print("sin examenes, creando uno")
#     ex = b.crear_examen(a.get_sesion(), date.today(), 0, 12234, "cami", "hernan", "endoscopia")
# print(ex.get_apellido_paciente())

# b.retornar_elemento(ex)

# ex = b.get_elemento()
# if ex == None:
#     print("sin examenes, creando uno")
# print("dando elemento")

# print(ex.get_apellido_paciente())
