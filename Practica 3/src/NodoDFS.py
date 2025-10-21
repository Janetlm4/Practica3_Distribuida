import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de DFS.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = id_nodo
        self.hijos = []
        self.visitados = set()
        self.vecinos_ordenados = sorted(vecinos)
        self.iniciado = False
        self.padre_actual = None  # Para rastrear quién nos envió el mensaje

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        if self.id_nodo == 0 and not self.iniciado:
            self.iniciado = True
            self.padre = 0
            self.visitados.add(0)
            yield env.timeout(TICK)
            
            # Enviar GO al primer vecino (menor identificador)
            if self.vecinos_ordenados:
                k = self.vecinos_ordenados[0]
                self.hijos = [k]
                yield self.canal_salida.envia(('GO', self.id_nodo, {0}), [k])
        
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo, sender, visited_set = mensaje
            
            if tipo == 'GO':
                # El 'sender' es nuestro padre en el árbol DFS
                if self.padre == self.id_nodo:  # Si aún no tenemos padre establecido
                    self.padre = sender
                
                self.visitados.update(visited_set)
                self.visitados.add(self.id_nodo)
                
                # Vecinos no visitados (excluyendo al padre)
                vecinos_no_visitados = [v for v in self.vecinos_ordenados 
                                      if v not in self.visitados and v != self.padre]
                
                if not vecinos_no_visitados:
                    # No hay más vecinos por explorar, retroceder
                    if self.padre != self.id_nodo:
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(('BACK', self.id_nodo, self.visitados), [self.padre])
                    self.hijos = []  # No tenemos hijos en este camino
                else:
                    # Explorar al siguiente vecino no visitado
                    k = vecinos_no_visitados[0]
                    if k not in self.hijos:
                        self.hijos.append(k)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(('GO', self.id_nodo, self.visitados), [k])
            
            elif tipo == 'BACK':
                # Actualizar visitados
                self.visitados.update(visited_set)
                
                # Buscar siguiente vecino no visitado (excluyendo al padre)
                vecinos_no_visitados = [v for v in self.vecinos_ordenados 
                                      if v not in self.visitados and v != self.padre]
                
                if not vecinos_no_visitados:
                    # No hay más vecinos, seguir retrocediendo
                    if self.padre != self.id_nodo:
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(('BACK', self.id_nodo, self.visitados), [self.padre])
                else:
                    # Explorar siguiente vecino no visitado
                    k = vecinos_no_visitados[0]
                    if k not in self.hijos:
                        self.hijos.append(k)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(('GO', self.id_nodo, self.visitados), [k])
