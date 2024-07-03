import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        anni = DAO.getAnni()
        forme = DAO.getForme()

        self._view.ddyear.options = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view.ddshape.options = list(map(lambda x: ft.dropdown.Option(x), forme))

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if not self._view.ddyear.value:
            self._view.create_alert("vaffanculo")
            return
        if not self._view.ddshape.value:
            self._view.create_alert("vaffanculo")
            return
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        self._model.creaGrafo(anno, forma)
        self._view.txt_result.controls.append(ft.Text(f"nodi: {self._model.grafoDetails()[0]}, archi: {self._model.grafoDetails()[1]}"))
        for nodo in self._model.pesiNodi():
            self._view.txt_result.controls.append(ft.Text(f"nodo {nodo[0]}, somma pesi su archi {nodo[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        sol, dist = self._model.cercaPercorso()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {dist}"))
        for i in range(len(sol)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{sol[i]} --> {sol[i+1]}: weight {self._model.pesoArco(sol[i], sol[i+1])}"
                                                       f" distance {self._model.getDistanza(sol[i], sol[i+1])}"))
        self._view.update_page()