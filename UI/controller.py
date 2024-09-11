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
        self._view.ddyear.options = list(map(lambda x: ft.dropdown.Option(x), anni))
    def handle_change(self,e):
        anno = self._view.ddyear.value

        forme = DAO.getForme(int(anno))
        for forma in forme :
            if forma == "" or forma == None :
                forme.remove(forma)
        self._view.ddshape.options = list(map(lambda x: ft.dropdown.Option(x), forme))
        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        try :
            anno = int(anno)
        except ValueError :
            self._view.create_alert("Hain inserito un valore di anno non valido")
        self._model.creaGrafo(anno,forma)
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi : {self._model.grafoDetails()[0]}, Numero di archi : {self._model.grafoDetails()[1]}"))
        lista = self._model.getLista()
        for coppia in lista :
            self._view.txt_result.controls.append(ft.Text(f"Nodo {coppia[0]} somma pesi su archi : {coppia[1]}"))
        self._view.update_page()
    def handle_path(self, e):
        pass