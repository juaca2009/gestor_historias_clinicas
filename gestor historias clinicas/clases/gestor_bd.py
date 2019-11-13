from cassandra.cluster import Cluster

class gestor_bd(object):
    __instancia = None
    __sesion = None

    def __new__(self, keysp):
        if not self.__instancia:
            self.__instancia = super(gestor_bd, self).__new__(self)
            self.__keyspace = keysp
            self.__cluster = Cluster()
        return self.__instancia

    def conectar_bd(self):
        gestor_bd.__sesion = self.__cluster.connect(self.__keyspace) 


    def get_sesion(self):
        return self.__sesion

    def get_keyspace(self):
        return self.__keyspace
    
    def set_keyspace(self, key):
        self.__keyspace = key



