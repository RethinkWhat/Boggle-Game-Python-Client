from model import LoginModel.LoginModel as LoginModel
from views import Login.Login as Login

class LoginController(QObject):

    def __init__(self, view: Login, model: LoginModel):
        self.view = view
        self.model = model

        self.view.pushButton.clicked.connect(self.loginClicked);


    def loginClicked(self):
        
        username = self.view.user.text()
        password = self.view.passwor.text()

        #set login logic here
        