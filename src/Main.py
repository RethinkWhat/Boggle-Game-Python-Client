import os
import re
import sys
import time
import threading

from omniORB import CORBA
import BoggleApp



if __name__ == "__main__":
    orb = CORBA.ORB_init()
    """
    IOR is to be entered/changed everytime the server on java's end restarts
    """
    obj = orb.string_to_object(
        "IOR:000000000000001f49444c3a426f67676c654170702f426f67676c65436c69656e743a312e30000000000001000000000000008a000102000000000f3136392e3235342e38332e3130370000c776000000000031afabcb000000002082178eaa00000001000000000000000100000008526f6f74504f410000000008000000010000000014000000000000020000000100000020000000000001000100000002050100010001002000010109000000010001010000000026000000020002")
    server = obj._narrow(BoggleApp.BoggleClient)


    #logout is performed incase the last run didn't log out successfully
    # server.logout("ka")
    flag = 0;
    while (flag == 0):

        try:
            # login.
            username = input("Enter username:")
            password = input("Enter passcode:")
            if username == "bye" and password=="bye":
                flag = 2
                print("bye")
                break
            server.validateAccount(username, password)
            flag=1
            # login exceptions
        except Exception as e:
            print("login went wrong")
            flag = 2
            break

        """
        logged in
        """
        while(flag == 1):
            os.system('cls' if os.name == 'nt' else 'clear')
            #lobby
            """
            home page
            """
            print("<><><><><><><><><><>")
            output = str(server.getLeaderboard())
            print("             ====HOME====            ")

            # Regular expression pattern to extract username and points
            pattern = r"username='(\w+)'"
            ptpattern =  r"points=(\d+)"

            # Find all matches
            matches = re.findall(pattern, output)
            ptmatches = re.findall(ptpattern, output)

            #print leaderboard
            print("leaderboard:")
            print("Usernames: ")
            print(matches)
            print("Total Scores: ")
            print(ptmatches)

            print("<><><><><><><><><><>")
            choice=input("enter 1 to join game, enter 2 to logout")
            if choice =="2":
                print("logging out")
                server.logout(username)
                flag = 0
            elif choice =="1":
                sys.stdout.flush()
                server.attemptJoin(username)
                dura = str(server.getCurrLobbyTimerValue())

                pattern = r"\d+"
                match = re.search(pattern,dura)
                value = int(match.group())

                while value != 0:
                    output = str(server.getLobbyMembers())
                    pattern = r"username='(\w+)'"
                    matches = re.findall(pattern, output)

                    print("<><><><><><><><><><>")
                    print("You are in lobby. Waiting for players :")
                    print("Other players in the lobby: ", matches)
                    out ="Time remaining: %d seconds" % (value/1000)
                    print(out)
                    time.sleep(1);
                    dura = str(server.getCurrLobbyTimerValue())

                    pattern = r"\d+"
                    match = re.search(pattern, dura)
                    value = int(match.group())

                if len(server.getLobbyMembers())==1:
                    print("Leaving lobby because there is no one else.")
                    server.exitLobby(username)
                else:
                    #get duration
                    round = 1
                    usernameWinnerGame = server.getOverallWinner(server.getGameID(username))
                    remTime = (server.getGameDurationVal(server.getGameID(username)))
                    while usernameWinnerGame == "undecided":
                        #array of words to be sent to server and get pts.
                        words= []
                        print("++++++++++++++++++++++++++++++++++++++++")
                        print("+++++++++++++++GAME ROOM++++++++++++++++")
                        print("round ", round, "!")
                        print("You have ", remTime/1000, " seconds")
                        while remTime > 0:
                            print(remTime)
                            print("Wordset:")
                            print(server.getLetters(server.getGameID(username)))
                            string = input("Please enter your words:")
                            string =string.upper()


                            #get letter list
                            server.getLetters(server.getGameID(username))
                            correctANS =server.getLetters(server.getGameID(username))

                            if len(string) >=4 and " " not in string and string.isalpha():
                                if server.isValidWord(string):
                                    #checking if the said word could be made with the letter set
                                    letterset_list = list(server.getLetters(server.getGameID(username)))
                                    input_list = list(string)
                                    text = len(string)

                                    for char in input_list:
                                        if char in letterset_list:
                                            ind = letterset_list.index(char)
                                            # Remove just one character from the letter set based on given index
                                            letterset_list.pop(ind)
                                            text = text - 1

                                    # If input list is empty (meaning to say thatall the letters exist in the set), return True
                                    if text == 0:
                                        print(string, " is the right word.")
                                        words.append(string)
                                    else:
                                        print(string, " is NOT the right word.")

                            else:
                                print("Incorrect input.")
                            sys.stdout.flush()
                            remTime = (server.getGameDurationVal(server.getGameID(username)))
                        print("TIME'S UP")
                        server.sendUserWordList(server.getGameID(username), username, words)
                        time.sleep(5)
                        usernameWinnerRound = server.getRoundWinner(server.getGameID(username))
                        usernameWinnerGame = server.getOverallWinner(server.getGameID(username))
                        print(usernameWinnerRound," wins this round")
                        print("and the winner: ", usernameWinnerGame)
                        time.sleep(5)
                        round = round + 1
                        #flush out inputs so as to
                        sys.stdout.flush()
                        os.system('cls' if os.name == 'nt' else 'clear')
                print(usernameWinnerGame," is the winner of this game!")
                time.sleep(3)
