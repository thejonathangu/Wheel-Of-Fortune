from cmu_graphics import *
from collections import Counter
from functools import reduce
import random

class Player():

    def __init__(self, name):
        self.name = name
        self.money = 0
        self.prizes = set()
        self.respin = False
        self.guessedLetters = set()

    def addMoney(self, amount):
        print(amount)
        amount = [char for char in amount if char.isdigit()]
        amount = int(''.join(amount))
        self.money += amount
        return self.money
    
    def __repr__(self):
        return "(f'{self.name} has ${self.money} prize money!)"
    
    def addPrize(self, prize):
        if prize not in self.prizes:
            self.prizes.add(prize)
        else: 
            self.respin = True
            print("Respin the wheel. You already won that prize")
    
    def goBankrupt(self):
        self.money = 0

    def goRespin(self):
        self.respin = True


class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        #self.guessedLetters = set()
    
    def getGuess(self):
        return input("Enter your guess (letter or phrase)")
    

class ComputerPlayer(Player):

    def __init__(self, name, difficulty ):
        super().__init__(name)
        self.difficulty = difficulty
        #self.guessedLetters = set()
        with open("test.txt","r") as readfile:
            self.wordPool = readfile.read()
            self.wordPool = self.wordPool.split()
        print(self.wordPool)
        
    def getPossibleLetters(self, guessed):
        willGuess = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for i in letters:
            if (i not in guessed) and (i in letters):
                willGuess.append(i)
        return willGuess

    def getMove(self, guessed):
        sortedFrequencies = "ZQXJKVBPYGFWMUCLDRHSNIOATE"
        willGuess = self.getPossibleLetters(guessed)
        
        if willGuess == []:
            return 'pass'
        else:
            for i in sortedFrequencies[::-1]:
                if i in willGuess:
                    return i
                
    def isAllEmpty(self, revealedLetters):
        for char in revealedLetters:
            if char != ' ':
                return False
        return True

    def makeGuess(self, guessedLetters, revealedLetters):
        # Get the most popular letter after the last guessed letter
        checkedLetters = set()
        if self.isAllEmpty(revealedLetters):
            return self.getMove(guessedLetters)
        else:
            guess = self.commonNextLetter(guessedLetters, checkedLetters, revealedLetters)
            while guess in guessedLetters:
                checkedLetters.add(guess)
                guess = self.commonNextLetter(guessedLetters, checkedLetters, revealedLetters)
        # Check if the guessed letter is not already guessed

        return guess
    
    def commonNextLetter(self, guessedLetters, checkedLetters, revealedLetters):
        with open("test.txt","r") as readfile:
            list = readfile.read()
            list = list.split()
        characters = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for word in list:
                word = word.upper()
                for i in range(len(word)-2):
                    if letter == word[i]:
                        key = letter+word[i+1]
                        if key in characters:
                            characters[key] +=1
                        else:
                            characters[key] = 1
        print(characters)
        given = ' '
        guess = None
        for i in range(len(revealedLetters)-1):
            if revealedLetters[i] != ' ' and revealedLetters[i+1] == ' ':
                given = revealedLetters[i]
        max = 0
        print(given)
        for key in characters:
            if key[0] == given and key[1] not in checkedLetters:
                if characters[key]>max:
                    max = characters[key]
                    guess = key[1]
                    print(f'max = {max} and key = {guess} and checked Letters {checkedLetters}')
        if guess == None:
            guess = self.getMove(guessedLetters)
        return guess

        
#Constants
HUMAN_PLAYER = "H"
COMPUTER_PLAYER = "C"
