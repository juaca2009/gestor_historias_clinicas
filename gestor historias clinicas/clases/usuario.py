from gestor_bd import gestor_bd
from cassandra.cluster import Cluster

class usuario(object):
    def __init__(self, _correo, _contra, _base, _nombre, _apellido, _fechan, _ciudad, _direccion, _documento):
        self.__correo = _correo
        self.__contrasena = _contra
        self.__base = _base
        self.__nombre = _nombre
        self.__apellido = _apellido
        self.__fecha_nacimiento = _fechan
        self.__ciudad = _ciudad
        self.__direccion = _direccion
        self.__documento = _documento

    def get_correo(self):
        return self.__correo

    def get_documento(self):
        return self.__documento

    def get_contrasena(self):
        return self.__contrasena

    def get_apellido(self):
        return self.__apellido

    def get_nombre(self):
        return self.__nombre

    def get_nacimiento(self):
        return self.__fecha_nacimiento

    def get_ciudad(self):
        return self.__ciudad

    def get_direccion(self):
        return self.__direccion

    def get_base(self):
        return self.__base

    def set_correo(self, _correo):
        self.__correo = _correo

    def set_contrasena(self, _contra):
        self.__contrasena = _contra

    def set_documento(self, _documento):
        self.__documento = _documento

    def set_base(self, _base):
        self.__base = _base

    def set_apellido(self, _apellido):
        self.__apellido = _apellido

    def set_nombre(self, _nombre):
        self.__nombre = _nombre

    def set_nacimiento(self, _fechan):
        self.__fecha_nacimiento = _fechan

    def set_ciudad(self, _ciudad):
        self.__ciudad = _ciudad

    def set_direccion(self, _direccion):
        self.__direccion = _direccion
