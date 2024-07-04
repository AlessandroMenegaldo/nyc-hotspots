import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceLocation = None

    def fillDDProvider(self):
        providers = self._model._providers
        for p in providers:
            self._view._ddProvider.options.append(ft.dropdown.Option(p))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        provider = self._view._ddProvider.value
        lunghezzaStr = self._view._txtInDistanza.value

        if provider == None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"selezione prima un provider"))
        try: lunghezza_max = float(lunghezzaStr)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Inserisci soglia valida"))

        self._model.buildGraph(provider, lunghezza_max)
        self._view._txt_result.controls.append(ft.Text(f"Nodi: {self._model.getNumNodi()} Archi: {self._model.getNumArchi()}"))

        self.fillDDTarget()
        self._view.update_page()






    def handleAnalizzaGrafo(self, e):
        sortedListOfNodes = self._model.getMostVicini()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Vertici con più vicini:"))
        for n in sortedListOfNodes:
            self._view._txt_result.controls.append(ft.Text(f"{n[0].Location} --- {n[1]}"))
        self._view.update_page()


    def handleCalcolaPercorso(self, e):
        if self._choiceLocation == None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Seleziona target"))
            self._view.update_page()
            return

        stringa = self._view._txtInString.value
        self._model.getBestPath(self._choiceLocation, stringa)



    def fillDDTarget(self):
        localita = self._model.getLocalita()
        for l in localita:
            self._view._ddTarget.options.append(ft.dropdown.Option( data=l,
                                                                    text=l.Location,
                                                                    on_click=self.readChoiceLocation))

        self._view.update_page()

    def readChoiceLocation(self, e):
        if e.control.data is None:
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data