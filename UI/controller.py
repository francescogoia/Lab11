import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        for i in [2015, 2016, 2017, 2018]:
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))
        colori = self._model._colori
        for i in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(i))



    def handle_graph(self, e):
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value
        self._model.build_graph(colore, anno)
        Nnodi = self._model.get_num_nodi()
        Narchi = self._model.get_num_archi()
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {Nnodi} nodi"))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {Narchi} archi"))

        self._view.update_page()

    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
