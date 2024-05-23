import networkx as nx

from database.DAO import DAO
import networkx as NX

class Model:
    def __init__(self):
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
                        self._grafo.add_edge(v1, v2, weight=peso)

    def cerca_percorso(self, partenza):
        t = list(self._grafo.edges(partenza, True))
        for i in self._grafo.edges(partenza, True):
            print(i)

        archi_successivi_non_controllati = set()
        for i in self._grafo.edges(partenza):
            archi_successivi_non_controllati.add(i[1].Product_number)
        self.ricorsione(partenza, [], 0, archi_successivi_non_controllati)
        print(self._soluzioni)


    def get_num_nodi(self):
        return len(self._grafo.nodes)
    def get_num_archi(self):
        return len(self._grafo.edges)

    def get_prodotti(self):
        return self._grafo.nodes

    def ricorsione(self, partenza, parziale, peso_max, archi_successivi_non_controllati):
        #uscita
        if len(archi_successivi_non_controllati) == 0:
            self._soluzioni.append(parziale)
        else:
            successori_partenza = list(self._grafo.edges(partenza, True))
            for i in successori_partenza:
                if i[1].Product_number in archi_successivi_non_controllati:
                    archi_successivi_non_controllati.remove(i[1].Product_number)
                    peso = i[2]["weight"][0]
                    if peso >= peso_max:
                        peso_max = peso
                        parziale.append(i)
                        self.ricorsione(i[1], parziale, peso_max, archi_successivi_non_controllati)
                        parziale.pop()
                else:
                    print("f")


