'''import threading

class LobbyController:
    def __init__(self, lobby_model, lobby_view, parent):
        self.model = lobby_model
        self.view = lobby_view
        self.parent = parent

        #Thread nT = new Thread(new Runnable() {
        #    @Override
        #    public void run() {
        #        timer();
        #    }
        #});
        #nT.start();

        nT = threading.Thread(target=self.timer)
        nT.start()

    def timer(self):
        self.view.set_lbl_timer_txt("00:" + str(10000 // 1000))
        timer_val = -1
        users_in_lobby = None
        temp_users_in_lobby = None
        try:
            self.model.get_wf_impl().attempt_join(self.model.get_username())
            users_in_lobby = self.model.get_users_in_lobby()
            self.populate_lobby(users_in_lobby)

            start_lobby = False
            while timer_val != 0:
                timer_val, start_lobby = self.model.get_wf_impl().get_curr_lobby_timer_value()
                print("TIMER VALUE:", timer_val)

                users_in_lobby = self.model.get_users_in_lobby()
                for user in users_in_lobby:
                    print("user sent:", user.username, "|", user.pfp_address)

                temp_users_in_lobby = self.model.get_users_in_lobby()
                if len(temp_users_in_lobby) != len(users_in_lobby):
                    print("reached")
                    users_in_lobby = temp_users_in_lobby
                    self.populate_lobby(users_in_lobby)

                self.view.set_lbl_timer_txt("00:0" + str(timer_val // 1000))

            if start_lobby:
                self.parent.get_view().show_game_room()
                self.parent.stop_music()
                self.parent.play_game_music()
                GameRoomController(GameRoomModel(self.model.get_username(), self.model.get_wf_impl()),
                                   self.parent.get_view().get_game_room_view(), self.parent)
            else:
                self.parent.get_view().show_home()
                self.parent.play_default_music()
        except Exception as e:
            print(e)

    def populate_lobby(self, users):
        self.view.remove_players_in_user_panel()
        for user in users:
            self.view.add_player_in_user_panel(user.pfp_address, user.username)
'''