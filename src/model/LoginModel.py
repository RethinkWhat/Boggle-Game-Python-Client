from BoggleClient_idl import _objref_BoggleClient as BoggleClient
from BoggleClient_idl import accountDoesNotExist
from BoggleClient_idl import accountLoggedIn

class LoginModel:

    def __init__(self, wfmpl):
        self.wfmpl = wfmpl

    def validateAccount(self, username, password):
        try:

            self.wfmpl.validateAccount(username, password)
            return "valid"

        except accountDoesNotExist as adne:
            
            return "Account does not exist"

        except accountLoggedIn as ali:

            return "Account already logged in"

    def getWfmpl(self):
        return self.wfmpl
    
    def setWfmpl(self, wfmpl):
        self.wfmpl = wfmpl
