import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de DFS.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # El constructor inicializa los atributos del nodo. Establece:
        # - El nodo como su propio padre inicialmente.
        # - Una lista vacía para los hijos.
        # - Un conjunto vacío para los nodos visitados.
        # - Ordena los vecinos para facilitar su exploración.
        # - Marca que el nodo aún no ha sido iniciado y no tiene un padre actual.

        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = id_nodo
        self.hijos = []
        self.visitados = set()
        self.vecinos_ordenados = sorted(vecinos)
        self.iniciado = False
        self.padre_actual = None  

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Este método implementa el algoritmo de búsqueda en profundidad (DFS).
        # Comienza con el nodo raíz (id 0), explora los vecinos y sigue el recorrido DFS,
        # enviando mensajes a los nodos vecinos para continuar o retroceder según corresponda.

        if self.id_nodo == 0 and not self.iniciado:
            self.iniciado = True
            self.padre = 0
            self.visitados.add(0)
            yield env.timeout(TICK)

            # Si hay vecinos para explorar, comienza el recorrido DFS.
            
            if self.vecinos_ordenados:
                k = self.vecinos_ordenados[0]
                self.hijos = [k]
                yield self.canal_salida.envia(('GO', self.id_nodo, {0}), [k])
        
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo, sender, visited_set = mensaje
            
            if tipo == 'GO':
                # Si el nodo aún no tiene un padre, lo establece.
                if self.padre == self.id_nodo:  
                    self.padre = sender
                
                # Actualiza el conjunto de nodos visitados.
                self.visitados.update(visited_set)
                self.visitados.add(self.id_nodo)
                
                # Filtra los vecinos no visitados y no padres.
                vecinos_no_visitados = [v for v in self.vecinos_ordenados 
                                      if v not in self.visitados and v != self.padre]
                
                if not vecinos_no_visitados:
                    # Si no hay vecinos, envía un mensaje de retroceso al nodo padre.
                    if self.padre != self.id_nodo:
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(('BACK', self.id_nodo, self.visitados), [self.padre])
                    self.hijos = []  # No tenemos hijos en este camino
                else:
                    k = vecinos_no_visitados[0]
                    if k not in self.hijos:
                        self.hijos.append(k)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(('GO', self.id_nodo, self.visitados), [k])
            
            elif tipo == 'BACK':
                # En el caso de retroceso, actualiza los nodos visitados y sigue explorando.
                self.visitados.update(visited_set)
                
                vecinos_no_visitados = [v for v in self.vecinos_ordenados 
                                      if v not in self.visitados and v != self.padre]
                
                if not vecinos_no_visitados:
                    if self.padre != self.id_nodo:
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(('BACK', self.id_nodo, self.visitados), [self.padre])
                else:
                    k = vecinos_no_visitados[0]
                    if k not in self.hijos:
                        self.hijos.append(k)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(('GO', self.id_nodo, self.visitados), [k])
