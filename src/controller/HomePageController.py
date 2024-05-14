from src.views.py import HomePage
from src.model import HomePageModel


class HomePageController:

    def __init__(self, view: HomePage, model: HomePageModel):
        self.view = view
        self.model = model