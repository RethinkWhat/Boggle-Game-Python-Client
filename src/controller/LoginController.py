from PyQt5.QtCore import QObject

from src.views.py import Login
from src.model import LoginModel
import traceback

class LoginController(QObject):

    def __init__(self, view: Login, model: LoginModel):
        self.view = view
        self.model = model

        self.view.pushButton.clicked.connect(self.loginClicked)


    def loginClicked(self):
        
        username = self.view.user.text()
        password = self.view.passwor.text()

        try:
            isValid = self.model.validateAccount(username, password)

            if(isValid == "valid"):
                # Open HomeController
                self.view.close()
            else:
                #Error message and mechanisms
                self.view.close()
        except Exception as ex:
            traceback.print_exc()
