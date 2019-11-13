from gestor_bd import gestor_bd
from atencion import atencion
from examen import examen
from consulta import consulta
from datetime import date


class atencion_pool(object):
    __instancia = None
    __atenciones = list()

    def __new__(self, rol):
        if not self.__instancia:
            self.__instancia = super(atencion_pool, self).__new__(self)
            self.__rol = rol
        return self.__instancia

    def set_rol(self, rol):
        self.__rol = rol

    def get_rol(self):
        return self.__rol

    def get_elemento(self):
        if len(self.__atenciones) > 0:
            return self.__atenciones.pop(0)
        else:
            return None
    
    def retornar_elemento(self, elemento):
        if self.__rol == "doctor":
            elemento.reiniciar_consulta()
        elif self.__rol == "enfermero":
            elemento.reiniciar_examen()
        self.__atenciones.append(elemento)

    def crear_examen(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop, _tipox):
        return examen(_base, _fecha, _esatado, _documento, _nombrep, _apellidop, _tipox)

    def crear_consulta(self, _base, _fecha, _esatado, _documento, _nombrep, _apellidop,
                       _especializacion, _nombred, _apellidod, _documentod):

        return consulta(_base, _fecha, _esatado, _documento, _nombrep, _apellidop,
                        _especializacion, _nombred, _apellidod, _documentod)


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
