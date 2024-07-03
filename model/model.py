import copy

from geopy import distance
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        for stato in DAO.getStati():
            self.idMap[stato.id] = stato
        self.solBest = []
        self.costoBest = 0

    def creaGrafo(self, anno, forma):
        self.grafo.add_nodes_from(self.idMap.keys())
        self.grafo.add_edges_from(DAO.getVicini())
        for (u, v) in self.grafo.edges:
            if u != v:
                self.grafo[u][v]["weight"] = DAO.getPeso(u, anno, forma) + DAO.getPeso(v, anno, forma)

    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def pesiNodi(self):
        ris = []
        for u in self.grafo.nodes:
            pesi = 0
            for nodo in self.grafo.neighbors(u):
                pesi += self.grafo[u][nodo]["weight"]
            ris.append((u, pesi))
        return ris

    def cercaPercorso(self):
        self.solBest = []
        self.costoBest = 0
        for nodo in self.grafo.nodes:
            self.ricorsione([nodo], 0)
        return self.solBest, self.costoBest

    def ricorsione(self, parziale, pesoPrec):
        vicini = self.nodiEsplorabili(parziale, pesoPrec)
        if vicini == []:
            if self.isDistanzaBest(parziale):
                self.solBest = copy.deepcopy(parziale)
        else:
            for nodo in vicini:
                parziale.append(nodo)
                self.ricorsione(parziale, self.grafo[parziale[-2]][nodo]["weight"])
                parziale.pop()

    def nodiEsplorabili(self, lista, pesoPrec):
        ris = []
        for nodo in self.grafo.neighbors(lista[-1]):
            if self.grafo[lista[-1]][nodo]["weight"] > pesoPrec:
                ris.append(nodo)
        return ris

    def isDistanzaBest(self, parziale):
        distanza = 0
        for i in range(len(parziale)-1):
            stato1 = self.idMap[parziale[i]]
            stato2 = self.idMap[parziale[i+1]]
            distanza += distance.geodesic((stato1.Lat, stato1.Lng), (stato2.Lat, stato2.Lng)).km
        if distanza > self.costoBest:
            self.costoBest = distanza
            return True
        return False

    def pesoArco(self, u, v):
        return self.grafo[u][v]["weight"]

    def getDistanza(self, u, v):
        stato1 = self.idMap[u]
        stato2 = self.idMap[v]
        return distance.geodesic((stato1.Lat, stato1.Lng), (stato2.Lat, stato2.Lng)).km