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
        for color in self._model.colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))


    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        self._view.txtOut2.controls.clear()
        self._view._ddnode.options.clear()

        year = self._view._ddyear.value
        try:
            input_year = int(year)
        except Exception:
            self._view.create_alert("seleziona un anno")
            return
        color = self._view._ddcolor.value
        self._model.Create_Graph(color, input_year)
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.Nnodes()} Numero di archi: {self._model.Nedges()}"))

        top3 = self._model.getTop3()
        vertici = []
        nodiRipetuti = []
        for top in top3:
            if top[0] in vertici:
                nodiRipetuti.append(top[0].Product_number)
            if top[1] in vertici:
                nodiRipetuti.append(top[1].Product_number)
            vertici.append(top[0])
            vertici.append(top[1])
            self._view.txtOut.controls.append(ft.Text(f"Ardo da {top[0].Product_number} a {top[1].Product_number},"
                                                      f" peso={self._model.grafo[top[0]][top[1]]['weight']}"))

        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetoti sono: {nodiRipetuti}"))
        self.fillDDProduct()

        self._view.update_page()




    def fillDDProduct(self):
        for product in self._model.grafo:
            self._view._ddnode.options.append(ft.dropdown.Option(product.Product_number))


    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        product_num = int(self._view._ddnode.value)
        self._model.find_path(product_num)
        self._view.txtOut2.controls.append(ft.Text(f"Numero spigoli percorso più lungo: {len(self._model.solBest)}"))
        self._view.update_page()
