from PyQt5.QtCore import QObject

from src.views.py import Login
from src.model import LoginModel
from src.views.py import HomePage
from src.model import HomePageModel
from src.controller import HomePageController
import traceback

class LoginController(QObject):

    def __init__(self, view: Login, model: LoginModel):
        self.view = view
        self.model = model

        self.view.pushButton.clicked.connect(self.loginClicked)

        self.view.show()


    def loginClicked(self):
        
        username = self.view.user.text()
        password = self.view.passwor.text()

        try:
            isValid = self.model.validateAccount(username, password)

            if(isValid == "valid"):

                # Open HomeController
                HomePageController(HomePage(), HomePageModel(username ,self.model.getWfmpl()))


                self.view.close()
            else:
                #Error message and mechanisms
                self.view.close()
        except Exception as ex:
            traceback.print_exc()
