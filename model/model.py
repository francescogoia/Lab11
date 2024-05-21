import networkx as nx

from database.DAO import DAO
import networkx as NX

class Model:
    def __init__(self):
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

    def get_num_nodi(self):
        return len(self._grafo.nodes)
    def get_num_archi(self):
        return len(self._grafo.edges)
