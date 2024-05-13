from model.LoginModel import LoginModel
from views.Login import Login
from controller.LoginController import LoginController

"""
Create instances of the view and the model
"""
view = Login()
model = LoginModel()

"""
Instantiate the controller
"""
LoginController(view, model)