import javax.swing as swing
import java.awt.event as event
import java.sql as sql
import shared.SwingResources as swing_resources

class LoginController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # action listeners
        self.view.set_password_listener(LoginListener(self))
        self.view.set_login_listener(LoginListener(self))
        self.view.set_show_password_listener(swing_resources.ShowPasswordListener(self.view.get_chk_show_password(),
                                                                                  self.view.get_txt_password()))

        # mouse listeners
        self.view.get_btn_login().add_mouse_listener(swing_resources.CursorChanger(self.view.get_btn_login()))

        # focus listeners
        self.view.get_txt_username().add_focus_listener(swing_resources.TextFieldFocus(self.view.get_txt_username(),
                                                                                        "Username",
                                                                                        self.view.get_lbl_error_message()))
        self.view.get_txt_password().add_focus_listener(swing_resources.PasswordFocusWithCheckbox(self.view.get_txt_password(),
                                                                                                   self.view.get_chk_show_password(),
                                                                                                   "Password",
                                                                                                   self.view.get_lbl_error_message()))

        self.view.revalidate()
        self.view.repaint()

class LoginListener(event.ActionListener):
    def __init__(self, controller):
        self.controller = controller

    def actionPerformed(self, e):
        username = self.controller.view.get_txt_username().getText()
        try:
            if self.controller.model.validate_account(self.controller.view.get_txt_username().getText(),
                                                     self.controller.view.get_txt_password().getText()):
                swing.SwingUtilities.invokeLater(lambda: ClientApplicationController(ClientApplicationView(),
                                                                                     ClientApplicationModel(username,
                                                                                                            self.controller.model.get_wf_impl())))
                self.controller.view.dispose()
            else:
                swing.SwingUtilities.invokeLater(lambda: self.controller.view.set_error_message("Wrong credentials. Try again.")
                                                 and self.controller.view.get_txt_password().setText("Password")
                                                 and self.controller.view.get_txt_password().setEchoChar(chr(0))
                                                 and self.controller.view.get_chk_show_password().setSelected(False))
        except sql.SQLException as sqle:
            sqle.printStackTrace()
        except Exception as ex:
            raise RuntimeException(ex)
