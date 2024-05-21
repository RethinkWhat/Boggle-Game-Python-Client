import os
import re
import sys
import time
import threading

import select
from omniORB import CORBA
import BoggleApp


class TimerThread(threading.Thread):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.remaining = timeout
        self.stop_event = threading.Event()

    def run(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout and not self.stop_event.is_set():
            time.sleep(1)
            self.remaining = self.timeout - (time.time() - start_time)

    def stop(self):
        self.stop_event.set()

    def get_remaining_time(self):
        return self.remaining


def read_input():
    global user_input
    user_input = input()


def get_input(prompt, timer, lock):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    lock.acquire()
    try:
        input_thread = threading.Thread(target=read_input)
        input_thread.start()
        input_thread.join(timeout=timer.remaining)
    finally:
        lock.release()

    return user_input



if __name__ == "__main__":
    orb = CORBA.ORB_init()
    obj = orb.string_to_object("IOR:000000000000001f49444c3a426f67676c654170702f426f67676c65436c69656e743a312e30000000000001000000000000008a000102000000000f3130302e38342e3136382e3132340000cc17000000000031afabcb00000000209ad69d1800000001000000000000000100000008526f6f74504f410000000008000000010000000014000000000000020000000100000020000000000001000100000002050100010001002000010109000000010001010000000026000000020002")
    server = obj._narrow(BoggleApp.BoggleClient)

    # server.logout("ka")
    input_lock = threading.Lock()
    flag = 0
    while flag == 0:
        try:
            username = input("Enter username: ")
            password = input("Enter passcode: ")
            if username == "bye" and password == "bye":
                flag = 2
                print("bye")
                break
            server.validateAccount(username, password)
            flag = 1
        except Exception as e:
            print("login went wrong")
            flag = 2
            break

    while flag == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("<><><><><><><><><><>")
        output = str(server.getLeaderboard())
        print("             ====HOME====            ")

        pattern = r"username='(\w+)'"
        ptpattern = r"points=(\d+)"
        matches = re.findall(pattern, output)
        ptmatches = re.findall(ptpattern, output)

        print("leaderboard:")
        print("Usernames: ")
        print(matches)
        print("Total Scores: ")
        print(ptmatches)

        print("<><><><><><><><><><>")
        choice = input("enter 1 to join game, enter 2 to logout")
        if choice == "2":
            print("logging out")
            server.logout(username)
            flag = 0
        elif choice == "1":
            server.attemptJoin(username)
            dura = str(server.getCurrLobbyTimerValue())
            pattern = r"\d+"
            match = re.search(pattern, dura)
            value = int(match.group())

            while value != 0:
                output = str(server.getLobbyMembers())
                pattern = r"username='(\w+)'"
                matches = re.findall(pattern, output)

                print("<><><><><><><><><><>")
                print("You are in lobby. Waiting for players :")
                print("Other players in the lobby: ", matches)
                out = "Time remaining: %d seconds" % (value / 1000)
                print(out)
                time.sleep(1)
                dura = str(server.getCurrLobbyTimerValue())
                pattern = r"\d+"
                match = re.search(pattern, dura)
                value = int(match.group())

            if len(server.getLobbyMembers()) == 1:
                print("Leaving lobby because there is no one else.")
                server.exitLobby(username)
            else:
                round = 1
                usernameWinnerGame = server.getOverallWinner(server.getGameID(username))
                defa = (server.getGameDurationVal(server.getGameID(username)))
                while usernameWinnerGame == "undecided":
                    remTime = defa
                    words = []
                    print("++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++GAME ROOM++++++++++++++++")
                    print("round ", round, "!")
                    print("You have ", remTime / 1000, " seconds")
                    while remTime > 0:
                        print("Wordset:")
                        print(server.getLetters(server.getGameID(username)))
                        string = get_input("Please enter your words: ", TimerThread(remTime // 1000), input_lock)

                        string = string.upper()

                        server.getLetters(server.getGameID(username))
                        correctANS = server.getLetters(server.getGameID(username))

                        if len(string) >= 4 and " " not in string and string.isalpha():
                            if server.isValidWord(string):
                                letterset_list = list(server.getLetters(server.getGameID(username)))
                                input_list = list(string)
                                text = len(string)

                                for char in input_list:
                                    if char in letterset_list:
                                        ind = letterset_list.index(char)
                                        letterset_list.pop(ind)
                                        text = text - 1

                                if text == 0:
                                    print(string," is the right word!")
                                    words.append(string)
                                else:
                                    print(string," IS NOT the right word.")

                        else:
                            print("Incorrect input.")
                        remTime = (server.getGameDurationVal(server.getGameID(username)))
                        print("<<Remaining time: ",remTime/1000, " >>")
                    print("TIME'S UP")
                    print("your entered words: " , words)
                    server.sendUserWordList(server.getGameID(username), username, words)
                    time.sleep(5)
                    usernameWinnerRound = server.getRoundWinner(server.getGameID(username))
                    usernameWinnerGame = server.getOverallWinner(server.getGameID(username))
                    print(usernameWinnerRound, " wins this round")
                    #print("and the winner: ", usernameWinnerGame)
                    time.sleep(5)
                    round = round + 1
                print(usernameWinnerGame, " is the winner of this game!")
                time.sleep(2)