from cmu_graphics import *
import random
import time
from collections import Counter
import math

class player():
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.prizes = set()
        self.respin = False

    def addMoney(self, amount):
        self.money += amount

    
    def __repr__(self):
        return "(f'{self.name} has ${self.money} prize money!)"
    
    def addPrize(self, prize):
        if prize not in self.prizes:
            self.prizes.add(prize)
        else: 
            self.respin = True
            print("Respin the wheel. You already won that prize")
    
    def goBankrupt(self):
        self.prizeMoney = 0

    def goRespin(self):
        self.respin = True

class humanPlayer(player):
    def __init__(self, name):
        super().__init__(name)
    
    def getGuess(self):
        return input("Enter your guess (letter or phrase)")
    
class computerPlayer1(player):

    def __init__(self, name, difficulty ):
        player.__init__(self, name)
        self.difficulty = difficulty
        self.guessedLetters = []
        with open("test.txt","r") as readfile:
            self.wordPool = readfile.read()
            self.wordPool = self.wordPool.split("\n")
        
    def getPossibleLetters(self, guessed):
        willGuess = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for i in letters:
            if (i not in guessed) and (i in letters):
                willGuess.append(i)
        return willGuess
    
    def getMove(self, category, obscuredPhrase, guessed):
        sortedFrequencies = "ZQXJKVBPYGFWMUCLDRHSNIOATE"
        willGuess = self.getPossibleLetters(guessed)
        
        if willGuess == []:
            return 'pass'
        else:
            for i in sortedFrequencies[::-1]:
                if i in willGuess:
                    return i
    
    def makeGuess(self, revealedLetters):
        # Get the most popular letter after the last guessed letter
        guess = self.commonNextLetter(revealedLetters)

        # Check if the  guessed letter is not already guessed
        while guess in self.guessedLetters:
            guess = self.commonNextLetter(revealedLetters)

        self.guessedLetters.add(guess)
        self.lastGuess = guess
        return guess

    def commonNextLetter(self, revealedLetters):
        # Filter remaining words based on revealed letters and the last guessed letter
        remainingWords = [
            word for word in self.wordPool
            if all(letter not in self.guessedLetters for letter in word)
            and all((revealed == '-' or (revealed == letter and letter != self.lastGuess))
                    for revealed, letter in zip(revealedLetters, word))
        ]

        # Get the most common letter after the last guessed letter
        lettersAfter = [
            word[revealedLetters.index(self.lastGuess) + 1]
            for word in remainingWords
            if self.lastGuess in word and revealedLetters.index(self.lastGuess) < len(word) - 1
        ]

        # Count letter frequencies
        letterFrequencies = Counter(lettersAfter)

        # Get the most common letter
        mostCommonLetter = letterFrequencies.mostCommon(1)
        if mostCommonLetter:
            return mostCommonLetter[0][0]
        else:
            return ''
        

def onAppStart(app):
    app.stepsPerSecond = 50
    app.width = 800
    app.height = 800
    app.gameOver = False
    app.maxScore = 0
    app.rows = 5
    app.cols = 15
    app.boardLeft = 40
    app.boardTop = 45
    app.boardWidth = 600
    app.boardHeight = 100
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.spinWheel = False
    app.prizes = {'Lose a Turn':'white', 
                  '$800':'red', 
                  '$550':'darkViolet',
                  '$650':'pink',
                  '$500':'green',
                  '$900':'orange',
                  'BANKRUPT':'black',
                  '$600':'gold',
                  '$400':'blue',
                  '$300':'yellow',
                  '$1000':'indigo',
                  '$450':'cyan',
                  'Lose a Turn':'white', 
                  '$800':'red', 
                  '$550':'darkViolet',
                  '$650':'pink',
                  '$500':'green',
                  '$900':'orange',
                  'BANKRUPT':'black',
                  '$600':'gold',
                  '$400':'blue',
                  '$300':'yellow',
                  '$1000':'indigo',
                  '$450':'cyan'}
    app.humanPlayer = humanPlayer('You')
    app.computerPlayer1 = computerPlayer1('Computer 1', difficulty = 'easy')

    app.players = [app.humanPlayer, app.computerPlayer1]

    restartGame(app)

def restartGame(app):
    app.gameOver = False
    app.maxScore = 0
    app.rows = 5
    app.cols = 15
    app.boardLeft = 40
    app.boardTop = 45
    app.boardWidth = 600
    app.boardHeight = 100
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.spinWheel = True
    app.prizes = {'Lose a Turn':'white', 
                  '$800':'red', 
                  '$550':'darkViolet',
                  '$650':'pink',
                  '$500':'green',
                  '$900':'orange',
                  'BANKRUPT':'black',
                  '$600':'gold',
                  '$400':'blue',
                  '$300':'yellow',
                  '$1000':'indigo',
                  '$450':'cyan',
                  'Lose a Turn':'white', 
                  '$800':'red', 
                  '$550':'darkViolet',
                  '$650':'pink',
                  '$500':'green',
                  '$900':'orange',
                  'BANKRUPT':'black',
                  '$600':'gold',
                  '$400':'blue',
                  '$300':'yellow',
                  '$1000':'indigo',
                  '$450':'cyan'}
    app.colors = []
    for key in app.prizes:
        app.colors.append(app.prizes[key])
    app.money = list(app.prizes.keys())
    app.userInput = []
    app.randomWords = ['pit','hover','brand','barrel','hilarious','man','office','background','case',
                       'infection','discrimination','union','weave','interrupt','deputy','hear',
                       'laborer','spring','relate','angle','monstrous','hierarchy','owe','promotion',
                       'grimace','norm','loot','captain','lawyer','bubble']
    app.answer = random.choice(app.randomWords)
    app.filledInAnswer = False
    app.spinSpeed = 800

    for playerObj in app.players:
        playerObj.money = 0
        playerObj.prizes = set()
        playerObj.respin = False

#draws the board
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color, 100)

#draws the board border
def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
  cellWidth, cellHeight = getCellSize(app)
  
  drawRect(app.boardLeft, app.boardTop, cellWidth, app.boardHeight)
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, cellHeight)
  drawRect(app.boardLeft+cellWidth*(app.cols-1), app.boardTop, cellWidth, app.boardHeight)
  drawRect(app.boardLeft, app.boardTop+cellHeight*(app.rows-1), app.boardWidth, cellHeight)

#draws each cell
def drawCell(app, row, col, color, opac):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth, opacity = opac)

#gets the location of each cell's locations
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#gets the size of each cell
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def onKeyPress(app, key):
    if key == 's':
        takeStep(app)
    if key != 'enter':
        app.userInput.append(key)
    if key == 'enter':
        checkIfInAnswer(app,app.userInput)

def checkIfInAnswer(app, userInput):
    if app.gameOver:
        print("The game is over.")
        return

    if ''.join(userInput) == app.answer:
        print(f"Congratulations! You guessed the correct phrase: {app.answer}")
        app.gameOver = True
    elif len(userInput) == 1 and userInput[0] in app.answer:
        if userInput[0] not in app.userInput:
            app.userInput.append(userInput[0])
            print(f"Good guess! '{userInput[0]}' is in the phrase.")
            drawAnswerPhrase(app)
        else:
            print(f"You already guessed '{userInput[0]}'. Try a different letter.")
    else:
        print(f"Try again! '{''.join(userInput)}' is not in the phrase.")

def drawAnswerPhrase(app):
    if app.filledInAnswer:
        return
    answerLength = len(app.answer)
    cellWidth, cellHeight = getCellSize(app)

    for i in range(answerLength):
        x, y = getCellLeftTop(app, 2, i)
        drawRect(x, y, cellWidth, cellHeight, fill='lightgrey', border='black', borderWidth=app.cellBorderWidth)
        if app.answer[i] in app.userInput:
            drawLabel(app.answer[i], x + cellWidth / 2, y + cellHeight / 2, fontSize=20, bold=True)

    app.filledInAnswer = True
        
def onStep(app):
    if app.spinWheel == True:
        if app.spinSpeed>=0:
            takeStep(app)
            app.spinSpeed -=2
        else:
            app.spinWheel = False
    

def takeStep(app):
    rotateList(app)
    app.colors = list(app.prizes.values())
    app.money = list(app.prizes.keys())

def rotateList(app):
    keys = list(app.prizes.keys())
    vals = list(app.prizes.values())

    keys = keys[1:] + keys[:1]
    vals = vals[1:] + vals[:1]

    app.prizes = dict(zip(keys, vals))
    

def drawWheel(app):
    cx, cy = app.width//2, app.height//2
    radius = 200
    numSections = len(app.prizes)*2
    for i in range(numSections):
        drawSection(app, cx, cy, radius, 360/numSections*i, 360/numSections, i)
    for i in range(numSections):
        drawMoneyLabels(app, cx, cy, radius, numSections, i)

def drawSection(app, cx, cy, radius, startAngle, sweepAngle, counter):
    drawArc(cx, cy, radius*2, radius*2, startAngle+app.spinSpeed, sweepAngle, fill = app.colors[counter%12])
    
def drawMoneyLabels(app, cx, cy, radius, numSections, counter):
    labelRadius = 2*radius/3  # Distance of the labels from the center of the wheel
    labelAngle = 360 / numSections * counter + app.spinSpeed
    angleOffset = 360/(numSections*2)
    labelX = cx + labelRadius * math.cos(math.radians(labelAngle+angleOffset))
    labelY = cy - labelRadius * math.sin(math.radians(labelAngle+angleOffset))
    labelAngle = 0-labelAngle-angleOffset
    if app.money[counter%12] != 'BANKRUPT':
        fillColor = 'black'
    else:
        fillColor = 'white'

    drawLabel(app.money[counter%12], labelX, labelY, rotateAngle = labelAngle,
              fill=fillColor, bold = True)

def drawPlayerMoney(app):

    playerObj = app.humanPlayer
    playerName = playerObj.name
    playerMoney = playerObj.money
    drawLabel(f"{playerName}: ${playerMoney}", 0,app.height-20,)

def drawComputerMoney(app):

    playerObj = app.computerPlayer1
    playerName = playerObj.name
    playerMoney = playerObj.money
    drawLabel(f"{playerName}: ${playerMoney}", 100, app.height-20)

def gameOverScreen(app):
    drawLabel("Game Over!", app.width // 2, app.height // 2, size=50, bold=True)
    drawLabel(f"The correct phrase was: {app.answer}", app.width // 2, app.height // 2 + 50, size=20)

def redrawAll(app):
    if app.gameOver == False:
        drawBoard(app)
        drawBoardBorder(app)
        drawWheel(app)
        drawPlayerMoney(app)
    else:
        gameOverScreen(app)


def main():
    runApp()

main()


#https://www.geeksforgeeks.org/python-rotate-dictionary-by-k/
#https://www.cs.cmu.edu/~112/syllabus.html
#https://academy.cs.cmu.edu/exercise/13131
#https://towardsdatascience.com/hands-on-markov-chains-example-using-python-8138bf2bd971
