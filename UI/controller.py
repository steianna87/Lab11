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

        year = self._view._ddyear.value
        try:
            input_year = int(year)
        except Exception:
            self._view.create_alert("seleziona un anno")
            return
        color = self._view._ddcolor.value
        self._model.Create_Graph(color, input_year)
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.Nnodes()} Numero di archi: {self._model.Nedges()}"))
        self._view.update_page()




    def fillDDProduct(self):
        for product in self._model.productList:
            self._view._ddnode.options.append(ft.dropdown.Option(product.Product_number))


    def handle_search(self, e):
        pass
