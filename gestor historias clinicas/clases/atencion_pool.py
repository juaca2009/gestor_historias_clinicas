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

    def get_atenciones(self):
        return self.__atenciones
    
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
                cont2 = cont2 + 1
            cont1 = cont1 + 1

    def cargar_examenes(self, _nro_cola):
        temp = self.__base.execute(
            """
            select * from colas_examenes where nro_cola = %s
            """,
            ([_nro_cola])
        )
        for i in temp:
            if i.posicion != None:
                self.__atenciones.append(self.crear_examen(self.__base,i.posicion, i.nro_documento,i.nombre_paciente, i.apellido_paciente, i.tipo_examen))
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
    
    def obtener_atencion(self, _pos):
        return self.__atenciones[_pos]

# a = gestor_bd('historias_clinicas')
# a.conectar_bd()
# b = atencion_pool(a.get_sesion())
# b.cargar_consultas(1)
# c = b.get_atenciones()
# con = 0
# while con < len(c):
#     d = c[con]
#     print(d.get_posicion())
#     con = con + 1

