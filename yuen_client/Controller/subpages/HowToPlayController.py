'''from client.controller import ClientApplicationController
from client.model.subpages import HowToPlayModel
from client.view.subpages import HowToPlayView
from shared import SwingResources

Class HowToPlayController:
    def __init__(self, view, model, parent):
        self.view = view
        self.model = model
        self.parent = parent

        # action listeners
        self.view.get_btn_join_game.bind("<Button-1>", lambda event: HomeController.JoinGameListener(parent))
        self.view.get_btn_back.bind("<Button-1>", lambda event: parent.view.show_home())

        # mouse listeners
        self.view.get_btn_join_game.bind("<Enter>", lambda event: SwingResources.CursorChanger(self.view.btn_join_game))
        self.view.get_btn_back.bind("<Enter>", lambda event: SwingResources.CursorChanger(self.view.btn_back))
'''