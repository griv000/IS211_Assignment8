import random
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--numHumanPlayers", help="Number of human players in game", type=int, required=True)
    parser.add_argument("--numComputerPlayers",help="Number of CPU players in game", type=int, required=True)
    parser.add_argument("--timed", help="Set whether it's a timed game. Enter 1.", type=int,required=False)
    args = parser.parse_args()
    
    numHumanPlayers = args.numHumanPlayers #Number of human players in game
    numComputerPlayers = args.numComputerPlayers #Number of computer players in game
    myTimed = args.timed #timed flag

    die = Die()
    PlayersList = []
    PF = PlayerFactory()

    if numComputerPlayers + numHumanPlayers >= 2:

        if numHumanPlayers > 0:
            for i in range(1, numHumanPlayers + 1):
                PlayersList.append(PF.instantiate('human',i))
        
        if numComputerPlayers > 0:
            for i in range(1, numComputerPlayers + 1):
                PlayersList.append(PF.instantiate('cpu',i))

        print("Starting a new game of Pig...")

        if myTimed == 1:
            start_time = time.time()
            game = TimedGameProxy(PlayersList,die,start_time)
        else:
            game = Game(PlayersList,die)
        
        game.play()
        
    else:
        print("Insufficient number of players, exiting...")
        quit()


class PlayerFactory:
    def __init__(self):
        pass

    def instantiate(self,myType,slot):
        if myType == 'cpu':
            return ComputerPlayer("Computer Player " + str(slot))
        elif myType == 'human':
            return Player('Human Player ' + str(slot))

class Player:

    def __init__(self,name):
        self.name = name
        self.total = 0
        self.turn_total = 0

    def get_total(self):
        return self.total

    def WhatAmI(self):
        return "Human"

    def __str__(self):
        return f"{self.name} total = {self.total}"

    def display(self):
        print(self.__str__())


class ComputerPlayer(Player):
    def __init__(self,name):
        self.name = name
        self.total = 0
        self.turn_total = 0

    def WhatAmI(self):
        return "Computer"

    def roll_hold_choice(self):
        if self.turn_total > min(25,100 - self.turn_total):
            return "Pass"
        else:
            return "Roll"


class Game:
    def __init__(self,players,die):
        self.players = players
        self.die = die


    def play(self):
        while True:
            
            for i in self.players:
                CurrentTurn = True
                while CurrentTurn:
                    if i.WhatAmI() == "Human":
                        Entered = input(str(i) + "\nEnter 'r' to roll, 'h' to hold, 'q' to quit: ")
                        if Entered == "r":
                            rollValue = self.die.roll()
                            if rollValue == 1:
                                print("\n" + i.name + " rolled a 1, Lost Turn\n")
                                i.turn_total = 0
                                CurrentTurn = False

                            else:
                                i.turn_total += rollValue
                                print("\n" + i.name + " rolled a " + str(rollValue))
                                self.check_winner()
                                print("Current turn total is " + str(i.turn_total))

                        elif Entered == "h":
                            i.total += i.turn_total
                            print("\n" + i.name + " holding at " + str(i.turn_total) + ", " + str(i))
                            i.turn_total = 0
                            self.check_winner()
                            CurrentTurn = False

                        elif Entered == "q":
                            print("\nQuitting Game...")
                            quit()
                        else:
                            print("\nIncorrect Entry...")


                    if i.WhatAmI() == "Computer":
                        if i.roll_hold_choice() == "Pass":
                            i.total += i.turn_total
                            i.turn_total = 0
                            print(i.name + " passes turn with total of " + str(i.total))
                            self.check_winner()
                            CurrentTurn = False

                        elif i.roll_hold_choice() == "Roll":
                            rollValue = self.die.roll()
                            if rollValue == 1:
                                print("\n" + i.name + " rolled a 1, Lost Turn")
                                print(str(i))
                                i.turn_total = 0
                                self.check_winner()
                                CurrentTurn = False

                            else:
                                i.turn_total += rollValue
                                print("\n" + i.name + " rolled a " + str(rollValue))
                                print("Current turn total is " + str(i.turn_total))
                                print(str(i))
                                self.check_winner()
                                CurrentTurn = True

            
    def check_winner(self):
        for i in self.players:
            if i.total + i.turn_total >= 100:
                print(i.name + " current turn total is " + str(i.turn_total))
                print(i)
                print("Game Complete! " + i.name + " wins with total score of " + str(i.total + i.turn_total) + " (" + str(i.total) + " + " + str(i.turn_total) +")!")
                quit()

class TimedGameProxy(Game):

    def __init__(self,players,die,starttime):
        self.players = players
        self.die = die
        self.start_time = starttime

    def check_winner(self):
        print (time.time() - self.start_time)
        if time.time() - self.start_time < 10:
            for i in self.players:
                if i.total + i.turn_total >= 100:
                    print(i.name + " current turn total is " + str(i.turn_total))
                    print(i)
                    print("Game Complete! " + i.name + " wins with total score of " + str(i.total + i.turn_total) + " (" + str(i.total) + " + " + str(i.turn_total) +")!")
                    quit()
        else:
            myDict = {}
            for i in self.players:
                myDict[i.name]=i.total
            print("Time's up!")
            print(max(myDict,key=myDict.get) + " is the winner with " + str(max(myDict.values())) +"!")
            quit()
        

class Die():

    def __init__(self):
        pass        

    def roll(self):
        self.amount = random.randint(1, 6)
        return self.amount


if __name__ == "__main__":
    main()