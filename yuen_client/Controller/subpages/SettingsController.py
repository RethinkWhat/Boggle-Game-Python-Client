'''
from client.controller import ClientApplicationController
from client.model.subpages import SettingsModel
from client.view.subpages import AvatarSelectionView, SettingsView
from client.view import ClientApplicationView
from client.view.promtps import ChangePassErrorView, ChangeProfInfoErrorView, PassChangeSuccessView, ProfChangeSuccessView

form server.model import DataPB
form shared import SwingResources

class SettingsController:
    def __init__(self, view, model, parentView, parentModel):
        self.view = view
        self.model = model

    def change_avatar(self):
        self.avatar_selection_view = AvatarSelectionView(self.model.get_username(),dataPB)

    def edit_full_name(self):
        self.view.full_name_entry.config(state='normal')
        self.view.full_name_entry.delete(0, tk.END)
        self.parent_view.after(10000, lambda: self.reset_full_name_entry())

    def save_changes_later(self):
        new_full_name = self.view.full_name_entry.get()
        success = self.model.edit_info(self.model.get_username(), "fullName", new_full_name)

        if success:
            print("FullName Change Success!")
            self.view.full_name_text.set(new_full_name)
            self.view.full_name_entry.config(state='disabled')
            self.prof_change_success_view = ProfChangeSuccessView()
        else:
            print("FullName Change Failed!")
            self.change_prof_info_error_view = ChangeProfInfoErrorView()

    def change_pass(self):
        new_password = self.view.new_password_entry.get()
        confirm_password = self.view.confirm_password_entry.get()

        if new_password == confirm_password:
            success = self.model.edit_password(self.model.get_username(), self.view.current_password_entry.get(), new_password)
            if success:
                print("Change Password Success!")
                self.view.clear_password_fields()
                self.pass_change_success_view = PassChangeSuccessView()
            else:
                print("Change Password Failed!")
                self.view.clear_password_fields()
                self.change_pass_error_view = ChangePassErrorView()
        else:
            self.view.error_label.config(text="Passwords do not match!")
            self.view.clear_password_fields()
            print("Passwords Do Not Match!")
            self.change_pass_error_view = ChangePassErrorView()
            self.parent_view.after(4000, self.view.hide_error_label)

    def toggle_music(self):
        current_state = self.view.music_state.get()
        if current_state == "ON":
            self.view.music_state.set("OFF")
            self.parent_controller.stop_music()
        else:
            self.view.music_state.set("ON")
            self.parent_controller.play_default_music()
'''