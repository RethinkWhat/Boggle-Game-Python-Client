import sys
import CORBA
import CosNaming
from BoggleApp import BoggleClient_idl


def main():
    # Initialize the ORB
    orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

    # Get the root naming context
    obj = orb.resolve_initial_references("NameService")
    ncRef = obj._narrow(CosNaming.NamingContext)

    if ncRef is None:
        print("Failed to narrow the root naming context")
        sys.exit(1)

    # Resolve the object reference in the Naming context
    name = [CosNaming.NameComponent("WordFactory", "")]
    try:
        obj = ncRef.resolve(name)
    except CosNaming.NamingContext.NotFound:
        print("Name not found")
        sys.exit(1)

    # Narrow the object reference to BoggleClient
    boggle_client = obj._narrow(BoggleClient_idl)

    if boggle_client is None:
        print("Object reference is not a BoggleClient")
        sys.exit(1)

    # Now you can call methods on the boggle_client object
    # Example:
    # result = boggle_client.someMethod()
    # print(result)


if __name__ == "__main__":
    main()
