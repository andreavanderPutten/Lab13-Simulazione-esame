import networkx as nx
import geopy
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.nodi = []
        self.best_valore =  0
        self.best_cammino = []

    def creaGrafo(self,anno,forma):
        self.nodi = DAO.getNodi()
        self.grafo.add_nodes_from(self.nodi)
        vicini = DAO.getVicini()
        for nodo in self.nodi :
            for nodo2 in self.nodi :
                for coppia in vicini :
                    if ((nodo.id == coppia[0] and nodo2.id == coppia[1]) or (nodo.id == coppia[1] and nodo2.id == coppia[0])) :
                        peso = self.getPeso(anno,forma,nodo.id,nodo2.id)
                        print(f"{nodo} -> {nodo2} peso : {peso[0]}")
                        self.grafo.add_edge(nodo,nodo2,weight=peso[0])
    def getLista(self):
        lista = []
        for stato in self.grafo.nodes :
            vicini = self.grafo.neighbors(stato)
            peso_tot = self.calcola_peso_totale(stato,vicini)
            lista.append((stato,peso_tot))
        return lista
    def ricorsione(self,parziale,):
        pass
    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0

        for nodo in self.grafo.nodes:

            self.ricorsione([nodo])
        return self._cammino_ottimo, self._score_ottimo
    def getSuccessiviAmmissibili(self):
        pass
    def getPeso(self,anno,forma,stato1,stato2):
        peso = DAO.getPeso(anno,forma,stato1,stato2)
        return peso






    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)


