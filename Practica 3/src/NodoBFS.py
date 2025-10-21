import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        # Atributos para BFS
        self.padre = id_nodo  # Por convención, el padre inicial es el mismo nodo
        self.distancia = float('inf')  # Distancia infinita inicialmente
        self.explorados = set()  # Conjunto de nodos ya explorados

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        yield env.timeout(TICK)

        # Si soy el nodo distinguido (índice 0)
        if self.id_nodo == 0:
            self.padre = 0
            self.distancia = 0
            # Enviamos mensaje a todos los vecinos
            yield self.canal_salida.envia(('explorar', 0, 1), self.vecinos)
        
        while True:
            # Esperamos a recibir un mensaje
            mensaje = yield self.canal_entrada.get()
            tipo, padre_msg, distancia_msg = mensaje
            
            if tipo == 'explorar':
                # Si encontramos una distancia menor
                if distancia_msg < self.distancia:
                    self.distancia = distancia_msg
                    self.padre = padre_msg
                    # Exploramos a nuestros vecinos (excepto al padre)
                    vecinos_a_explorar = [v for v in self.vecinos if v != self.padre]
                    if vecinos_a_explorar:
                        yield self.canal_salida.envia(('explorar', self.id_nodo, self.distancia + 1), vecinos_a_explorar)

