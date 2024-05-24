import copy

import networkx as nx

from database.DAO import DAO
import networkx as NX

class Model:
    def __init__(self):
        self._sol_best = None
        self._soluzioni = []
        self._colori = DAO.get_colors()
        self._grafo = NX.Graph()
        self._idMap = {}


    def build_graph(self, colore, anno):
        self._grafo.clear()
        self._idMap.clear()
        prodotti = DAO.get_prodotti_colore(colore)
        for p in prodotti:
            self._idMap[p.Product_number] = p
        self._grafo.add_nodes_from(prodotti)
        for v1 in prodotti:
            num_v1 = v1.Product_number
            for v2 in prodotti:
                num_v2 = v2.Product_number
                if num_v1 != num_v2:
                    peso = DAO.conta_date(num_v1, num_v2, anno)
                    if peso[0] > 0:
                        self._grafo.add_edge(v1, v2, weight=peso[0])

    def cerca_percorso(self, partenza):
        self.ricorsione(partenza, [], 0, [])
        for i in self._soluzioni:
            print(i)
        self.cerca_best_sol()
        print(self._sol_best)



    def get_num_nodi(self):
        return len(self._grafo.nodes)
    def get_num_archi(self):
        return len(self._grafo.edges)

    def get_prodotti(self):
        return self._grafo.nodes

    def ricorsione(self, nodo, parziale, peso_max, termina):
        if termina:
            self._soluzioni.append((copy.deepcopy(parziale), len(parziale)))
        else:
            vicini = nx.neighbors(self._grafo, nodo)
            for n in vicini:
                peso_arco = self._grafo[nodo][n]["weight"]
                if peso_arco >= peso_max:
                    if self.filtro(nodo, n, parziale):
                        peso_max = peso_arco
                        parziale.append((nodo, n, peso_arco))
                        self.ricorsione(n, parziale, peso_max, False)
                        parziale.pop()
                    else:           ## parziale contiene già i nodi passati
                        self.ricorsione(n, parziale, peso_max, True)

    def filtro(self, nodo, n, parziale):
        for arco in parziale:
            if arco[ :-1] == (nodo, n) or arco[ :-1] == (n, nodo):              ## se i nodi dell'arco sono quelli passati return True (se parziale contiene già i nodi passati --> False)
                return False
        return True

    def cerca_best_sol(self):
        self._sol_best =  max(self._soluzioni, key=lambda x : x[1])




