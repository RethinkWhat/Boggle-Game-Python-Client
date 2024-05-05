'''
from client.controller import ClientApplicationController
from client.model.BoggleApp import userInfo
from client.model.subpages import HomeModel,LobbyModel
from client.view.subpages import HomeView
import shared.SwingResources as swing_resources

import javax.swing as swing
import java.awt.event as event

class HomeController:
    def __init__(self, home_view, home_model, parent):
        self.view = view
        self.model = home_model
        self.parent = parent

        self.parent.play_default_music()

        # action listeners
        self.view.set_join_listener(self.JoinGameListener(self.parent))
        self.view.set_edit_listener(self.EditPfpListener())
        self.view.set_tutorial_listener(lambda: self.parent.get_view().show_tutorial())

        self.view.get_lbl_username().set_text(self.model.get_username())

        # mouse listeners
        self.view.get_btn_join_game().add_mouse_listener(SwingResources.CursorChanger(self. view.get_btn_join_game()))
        self.view.get_btn_edit_pfp().add_mouse_listener(SwingResources.CursorChanger(self.view.get_btn_edit_pfp()))
        self.view.get_btn_tutorial().add_mouse_listener(SwingResources.CursorChanger(self.view.get_btn_tutorial()))

        #populateLeaderboard is to be debugged in the future

    def populate_leaderboard(self):
        leaderboards = self.model.get_leaderboard()
        self.view.clear_pnl_leader_board()
        for leaderboard in leaderboards:
            self.view.add_player_in_leaderboard(leaderboard.username, leaderboard.pfp_address, leaderboard.points)
        self.view.revalidate()
        self.view.repaint()

    class JoinGameListener:
        def __init__(self, parent):
            self.parent = parent

        def __call__(self):
            def action():
                self.parent.get_view().show_lobby()
                self.parent.get_view().set_nav_location_text("Lobby")
                print("creating new lobby")

                self.parent.play_lobby_music()
                LobbyController(LobbyModel(self.parent.get_model().get_username(), self.parent.get_model().get_wf_impl()),self.parent.get_view().get_lobby_view(), self.parent)
                print("new lobby created\n")

                self.parent.get_view().get_lobby_view().set_exit_lobby_listener(lambda e: self.exit_lobby())

            import threading
            threading.Thread(target=action).start()

        def exit_lobby(self):
            # self.parent.get_model().get_wf_impl().exit_game_room(self.model.get_username())
            self.parent.get_view().show_home()
            self.parent.get_view().set_nav_location_text("Home")
            self.parent.stop_music()
            self.parent.play_default_music()

    class EditPfpListener:
        def __call__(self, event):
            pass
'''


