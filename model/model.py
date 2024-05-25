import copy

import networkx as nx

from database.DAO import DAO
import networkx as NX

class Model:
    def __init__(self):
        self._memo = {}
        self._miglior_percorso = []
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
        self._miglior_percorso = []
        self._best_peso_per_len = [1e16 for i in range(len(self._grafo.edges))]
        self.ricorsione(partenza, [], 0)
        lunghezza_best = len(self._miglior_percorso)
        print(f"Percorso più lungo: {self._miglior_percorso},\nLunghezza: {lunghezza_best}")
        """for i in self._miglior_percorso:
            print(i)"""
        return lunghezza_best



    def get_num_nodi(self):
        return len(self._grafo.nodes)
    def get_num_archi(self):
        return len(self._grafo.edges)

    def get_prodotti(self):
        return self._grafo.nodes

    """def ricorsione(self, nodo, parziale, peso_max, termina):
        if termina:
            self._soluzioni.append((copy.deepcopy(parziale), len(parziale)))
        else:
            vicini = self._grafo.neighbors(nodo)
            for n in vicini:
                peso_arco = self._grafo[nodo][n]["weight"]
                if self.filtro(nodo, n, parziale)and peso_arco >= peso_max:
                        peso_max = peso_arco
                        parziale.append((nodo, n, peso_arco))
                        self.ricorsione(n, parziale, peso_max, False)
                        parziale.pop()
                else:           ## parziale contiene già i nodi passati
                  self.ricorsione(n, parziale, peso_max, True"""

    def ricorsione(self, nodo, parziale, peso_max):
        if self._best_peso_per_len[len(parziale)] < peso_max:
            return

        # Se il percorso attuale è più lungo del miglior percorso trovato, aggiorno il miglior percorso
        if len(parziale) > len(self._miglior_percorso):
            self._miglior_percorso = copy.deepcopy(parziale)

        vicini = self._grafo.neighbors(nodo)
        for n in vicini:
            peso_arco = self._grafo[nodo][n]["weight"]
            if self.filtro(nodo, n, parziale) and peso_arco >= peso_max:            ## quando non supero più il filtro e ho finito i vicini esco
                if peso_arco < self._best_peso_per_len[len(parziale)]:
                    self._best_peso_per_len[len(parziale)] = peso_arco
                parziale.append((nodo, n, peso_arco))
                self.ricorsione(n, parziale, peso_arco)             ## passo alla nuova ricorsione peso_arco (che diventa così peso_max)
                parziale.pop()




    def filtro(self, nodo, n, parziale):
        for arco in parziale:
            if arco[ :2] == (nodo, n) or arco[ :2] == (n, nodo):              ## se i nodi dell'arco sono quelli passati return True (se parziale contiene già i nodi passati --> False)
                return False
        return True





