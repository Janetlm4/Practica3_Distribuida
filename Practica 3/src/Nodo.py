import simpy

class Nodo:
    """Representa un nodo.

    Cada nodo tiene un id, una lista de vecinos y dos canales de comunicación.
    Los métodos que tiene son únicamente getters.
    """
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        '''Inicializa los atributos del nodo.'''
        # 'self' hace referencia a la instancia actual del objeto 'Nodo'
        # que se está creando. Permite que cada objeto tenga sus propios
        # valores almacenados en los atributos.
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

    def get_id(self) -> int:
        '''Regresa el id del nodo.'''
        # Este método simplemente devuelve el valor del atributo 'id_nodo'
        # que pertenece a esta instancia del objeto.
        # 'self.id_nodo' significa "el id_nodo de este objeto en particular".
        return self.id_nodo