import copy
import random

import networkx as nx

from database.DAO import DAO
from geopy.distance import distance


class Model:
    def __init__(self):
        self._providers = DAO.getAllProviders()
        self._graph = nx.Graph()
        self._bestNodes = []
        self._bestPath = []
        self._bestScore = 0


    def getBestPath(self, target, substring):
        self._bestPath = []
        self._bestScore = 0

        sources = self._bestNodes
        source = sources[random.randint(0, len(sources)-1)]
        if not nx.has_path(self._graph, source, target):
            print(f"{source} e {target} non sono connessi.")
            return

        parziale = [source]
        self.ricorsione(parziale, source, target, substring)

        print(self._bestScore)

    def ricorsione(self, parziale, source, target, substring):
        if parziale[-1] == target:
            if len(parziale) > self._bestScore:
                self._bestScore = len(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale and substring not in n.Location:
                parziale.append(n)
                self.ricorsione(parziale, source, target, substring)
                parziale.pop()


    def buildGraph(self, provider, soglia):
        locations = DAO.getAllLocation(provider)
        self._graph.add_nodes_from(locations)

        for l1 in self._graph.nodes:
            for l2 in self._graph.nodes:
                if l1 != l2:
                    dist = distance((l1.latitude, l1.longitude), (l2.latitude, l2.longitude)).km
                    if dist < soglia:
                        self._graph.add_edge(l1, l2, weight=dist)

        print(len(self._graph.nodes), len(self._graph.edges))


    def getMostVicini(self):
        listMostVicini = []
        for n in self._graph.nodes:
            listMostVicini.append((n, len(list(self._graph.neighbors(n)))))
        listaSorted = sorted(listMostVicini, key= lambda x: x[1], reverse=True)
        nodiMigliori = [x for x in listaSorted if x[1] == listaSorted[0][1]]
        self._bestNodes = [x[0] for x in nodiMigliori]
        return nodiMigliori



    def getNumNodi(self):
        return len(self._graph.nodes)
    def getNumArchi(self):
        return len(self._graph.edges)
    def getLocalita(self):
        return self._graph.nodes
