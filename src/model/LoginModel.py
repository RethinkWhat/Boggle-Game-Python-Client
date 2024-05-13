from BoggleClient_idl import BoggleClient as BoggleClient
from BoggleClient_idl import accountDoesNotExist
from BoggleClient_idl import accountLoggedIn

class LoginModel:

    """
    This is the constructor
    
    wfmpl variable should only be casted to BoggleClient interface from the BoggleClient_idl (line 142)
    """
    def __init__(self, wfmpl: BoggleClient):
        self.wfmpl = wfmpl

    """
    The validateAccount method will use the validateAccount from the wfmpl object
    """
    def validateAccount(self, username, password):
        try:

            self.wfmpl.validateAccount(username, password)
            return "valid"

        except accountDoesNotExist as adne:
            
            return "Account does not exist"

        except accountLoggedIn as ali:

            return "Account already logged in"

    """
    Returns the wfmpl variable
    """
    def getWfmpl(self):
        return self.wfmpl
    
    """
    Sets the wfmpl variable to a BoggleClient object when used
    """
    def setWfmpl(self, wfmpl: BoggleClient):
        self.wfmpl = wfmpl
