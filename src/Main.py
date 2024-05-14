from src.views.py import Login
from src.model import LoginModel
from src.controller import LoginController

if __name__ == "__main__":
    """
    Create instances of the view and the model
    """
    view = Login()
    model = LoginModel()

    """
    Instantiate the controller
    """
    LoginController(view, model)
