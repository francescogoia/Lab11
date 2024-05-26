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
        self._memo = {}


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
        #self.check_ianna()

    def cerca_percorso(self, partenza):

        """self._miglior_percorso = []
        self._best_peso_per_len = [1e16 for i in range(len(self._grafo.edges))]
        self.ricorsione(partenza, [], 0)
        lunghezza_best = len(self._miglior_percorso)
        print(f"Percorso più lungo: {self._miglior_percorso},\nLunghezza: {lunghezza_best}")
        for i in self._miglior_percorso:
            print(i)
        #self.check_ianna()"""
        lunghezza_best = self.cerca_percorso2(partenza)
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
        stato = (nodo, peso_max, tuple(parziale))
        if stato in self._memo:
            return self._memo[stato]

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

        self._memo[stato] = self._miglior_percorso
        return self._miglior_percorso




    def filtro(self, nodo, n, parziale):
        for arco in parziale:
            if arco[ :2] == (nodo, n) or arco[ :2] == (n, nodo):              ## se i nodi dell'arco sono quelli passati return True (se parziale contiene già i nodi passati --> False)
                return False
        return True

    def check_ianna(self):
        ianna = [(12110, 115110, 1), (115110, 65110, 1), (65110, 24110, 1), (24110, 144170, 1), (144170, 12110, 1), (12110, 129130, 1), (129130, 74110, 1), (74110, 126140, 1), (126140, 75110, 1), (75110, 144170, 1), (144170, 115110, 1), (115110, 134120, 1), (134120, 12110, 1), (12110, 74110, 2), (74110, 75110, 2), (75110, 14110, 2), (14110, 126140, 2), (126140, 12110, 2), (12110, 136140, 3), (136140, 24110, 3), (24110, 126140, 5), (126140, 115110, 6), (115110, 24110, 6), (24110, 12110, 7), (12110, 113110, 9), (113110, 129130, 10), (129130, 131110, 13), (131110, 129180, 15), (129180, 144170, 15), (144170, 126140, 16), (126140, 129180, 18), (129180, 136140, 23), (136140, 129130, 32), (129130, 126140, 44), (126140, 136140, 61)]
        lista_frago = [(12110, 115110, 1), (115110, 65110, 1), (65110, 24110, 1), (24110, 144170, 1), (144170, 12110, 1), (12110, 129130, 1), (129130, 74110, 1), (74110, 126140, 1), (126140, 75110, 1), (75110, 144170, 1), (144170, 115110, 1), (115110, 134120, 1), (134120, 113110, 2), (113110, 14110, 2), (14110, 75110, 2), (75110, 74110, 2), (74110, 12110, 2), (12110, 126140, 2), (126140, 65110, 2), (65110, 129130, 2), (129130, 24110, 3), (24110, 126140, 5), (126140, 115110, 6), (115110, 24110, 6), (24110, 12110, 7), (12110, 113110, 9), (113110, 129130, 10), (129130, 131110, 13), (131110, 129180, 15), (129180, 144170, 15), (144170, 126140, 16), (126140, 129180, 18), (129180, 136140, 23), (136140, 129130, 32), (129130, 126140, 44), (126140, 136140, 61)],
        if lista_frago == ianna:
            print("uguali")
        for i in ianna:
            for j in lista_frago:
                if i != j:
                    print("diversi")
                    print(i, "-", j)

    def cerca_percorso2(self, partenza):
        # Ordina gli archi per peso crescente
        edges = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'])

        # Inizializza la tabella di programmazione dinamica
        dp = {nodo: ([], 0) for nodo in self._grafo.nodes}
        visited_edges = set()

        for u, v, data in edges:
            peso = data['weight']
            arco = (min(u, v), max(u, v))  # Rappresentazione consistente dell'arco
            if arco in visited_edges:
                continue
            visited_edges.add(arco)
            # Aggiorna il percorso per v solo se il peso dell'arco è maggiore o uguale al peso massimo del percorso corrente di u
            if dp[u][1] == 0 or peso >= (dp[u][0][-1][2] if dp[u][0] else 0):
                if dp[v][1] < dp[u][1] + 1:
                    dp[v] = (dp[u][0] + [(u, v, peso)], dp[u][1] + 1)
            # Aggiorna il percorso per u solo se il peso dell'arco è maggiore o uguale al peso massimo del percorso corrente di v
            if dp[v][1] == 0 or peso >= (dp[v][0][-1][2] if dp[v][0] else 0):
                if dp[u][1] < dp[v][1] + 1:
                    dp[u] = (dp[v][0] + [(v, u, peso)], dp[v][1] + 1)

        self._miglior_percorso = max(dp.values(), key=lambda x: x[1])[0]
        lunghezza_best = len(self._miglior_percorso)
        print(f"Percorso più lungo: {self._miglior_percorso},\nLunghezza: {lunghezza_best}")
        for i in self._miglior_percorso:
            print(i)
        return lunghezza_best