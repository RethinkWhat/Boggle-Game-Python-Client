from BoggleClient_idl import BoggleClient


class HomePageModel:

    # Constructor
    def __init__(self, username, wfmpl: BoggleClient):
        self.wfmpl = wfmpl
        self.username = username

    # Methods