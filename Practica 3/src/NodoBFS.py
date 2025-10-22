import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        # El constructor inicializa los atributos del nodo (como id, vecinos y canales de comunicación).
        # Además, establece los valores específicos para el algoritmo BFS: el nodo es su propio padre inicialmente,
        # la distancia es infinita, y se prepara un conjunto de nodos explorados.

        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        
        self.padre = id_nodo  
        self.distancia = float('inf')  
        self.explorados = set()  

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        yield env.timeout(TICK)

        # Este método implementa el algoritmo de Búsqueda en Anchura (BFS).
        # Comienza el proceso de exploración si el nodo es el inicial (id 0).
        # Luego, se encarga de recibir mensajes de los vecinos para explorar los nodos,
        # actualizar la distancia y el padre, y enviar mensajes de exploración a los vecinos aún no explorados.
        if self.id_nodo == 0:
            self.padre = 0
            self.distancia = 0
            yield self.canal_salida.envia(('explorar', 0, 1), self.vecinos)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo, padre_msg, distancia_msg = mensaje
            
            if tipo == 'explorar':
                if distancia_msg < self.distancia:
                    self.distancia = distancia_msg
                    self.padre = padre_msg
                    vecinos_a_explorar = [v for v in self.vecinos if v != self.padre]
                    if vecinos_a_explorar:
                        yield self.canal_salida.envia(('explorar', self.id_nodo, self.distancia + 1), vecinos_a_explorar)

