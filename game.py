from cmu_graphics import *
import random
import time
from collections import Counter
import math
import string # string.ascii_.lowercase

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

        # Check if the guessed letter is not already guessed
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
    app.cols = 16
    app.boardLeft = 40
    app.boardTop = 45
    app.boardWidth = 600
    app.boardHeight = 100
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.spinWheel = False
    app.filledInAnswer = False
    app.currentPrize = 0
#    app.prizes = {'Lose a Turn':'white', 
#                  '$800':'red', 
#                  '$550':'darkViolet',
#                  '$650':'pink',
#                  '$500':'green',
#                  '$900':'orange',
#                  'BANKRUPT':'black',
#                  '$600':'gold',
#                  '$400':'blue',
#                  '$300':'yellow',
#                  '$1000':'indigo',
#                  '$450':'cyan',
#                  'Lose a Turn':'white', 
#                  '$800':'red', 
#                  '$550':'darkViolet',
#                  '$650':'pink',
#                  '$500':'green',
#                  '$900':'orange',
#                  'BANKRUPT':'black',
#                  '$600':'gold',
#                  '$400':'blue',
#                  '$300':'yellow',
#                  '$1000':'indigo',
#                  '$450':'cyan'}
    app.humanPlayer = humanPlayer('You')
    app.computerPlayer1 = computerPlayer1('Computer 1', difficulty = 'easy')

    app.players = [app.humanPlayer, app.computerPlayer1]

    restartGame(app)

def restartGame(app):
    app.gameOver = False
    app.maxScore = 0
    app.rows = 5
    app.cols = 16
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
    app.guessedLetters = set()
    app.filledInAnswer = False
    app.spinSpeed = random.randint(10,30)*200
    app.spinFriction = 100

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
             #fill=color, border='black',
             fill='green', border='black',
             borderWidth=app.cellBorderWidth, opacity = opac)

#gets the location of each cell's locations
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#draw red arrow
def drawRedArrow(app):
    drawStar(app.width/2, app.height/5+20, 20, 3, rotateAngle = 180, fill='red', border='red')

#draw spin button
def drawSpinButton(app):
    drawCircle(app.width/2, app.height/2, 20, fill='lightgray', border='red')
    drawLabel('SPIN', app.width/2, app.height/2)

#draw new game button
def drawNewGameButton(app):
    drawRect(app.width/2-60, app.height - 60, 120, 22 , fill='lightgray', border='green')
    drawLabel('New Game?', app.width/2, app.height - 50, size = 20, bold=True)

#draw solve game button
def drawSolveGameButton(app):
    drawRect(app.width/2-72, app.height - 60, 140, 22, fill='lightgray', border='green')
    drawLabel('Solve Game?', app.width/2, app.height - 50, size = 20, bold=True)


#gets the size of each cell
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def draw26Letters(app):
    for idx , letter in enumerate(string.ascii_lowercase):
        (x,y) = getCellLeftTop(app, 30 + int(idx/9) , 5+idx%9 )
        w,h = getCellSize(app)
        drawRect(x-w/2,y-h/2,w,h,fill='darkgreen', opacity= 90)
        drawLabel(letter.upper(),x,y, size=20, fill='gold', bold =True)


def onKeyPress(app, key):
    if key == 's':
        takeStep(app)
    if key != 'enter':
        app.userInput.append(key)
    if key == 'enter':
        checkIfInAnswer(app,app.userInput)


def getSelectedLetter(app, mouseX, mouseY):
    labels = [s for s in app.group if (isinstance(s, Label) and s.contains(mouseX, mouseY))]
    letters = [ l.value for l in labels if (l.value.lower() in list(string.ascii_lowercase)) ] 
    return letters[0] if len(letters) > 0 else None 

def getNewGame(app, mouseX, mouseY):
    labels = [s for s in app.group if (isinstance(s, Label) and s.contains(mouseX, mouseY))]
    letters = [ l.value for l in labels if (l.value  == "New Game?")]
    return letters[0] if len(letters) > 0 else None 

def getSolveGame(app, mouseX, mouseY):
    labels = [s for s in app.group if (isinstance(s, Label) and s.contains(mouseX, mouseY))]
    letters = [ l.value for l in labels if (l.value  == "Solve Game?")]
    return letters[0] if len(letters) > 0 else None 


def isSolved(app):
    for letter in app.answer:
        if letter.upper() not in app.guessedLetters:
            return False
    return True

def onMousePress(app, mouseX, mouseY):
    if mouseX <= app.width/2 + 20 and mouseX >= app.width/2 - 20:
        if mouseY <= app.height/2 + 20 and mouseY >= app.height/2 - 20:
            app.spinSpeed = random.randint(800, 1600)
            app.spinWheel = True
            #restartGame(app)
            return

    #check input
    letter = getSelectedLetter(app, mouseX, mouseY)
    if letter is not None:
        print(f'the selected letter is : {letter}')
        app.guessedLetters.add(letter)
        print(app.guessedLetters)
        print(app.answer, app.guessedLetters)
        if isSolved(app):
            app.gameOver = True

    #check input
    solveGame = getSolveGame(app, mouseX, mouseY)
    if solveGame is not None:
        guessedInput = app.getTextInput('Your guess:')
        for letter in guessedInput:
            app.guessedLetters.add(letter.upper())
        if isSolved(app):
            app.gameOver = True


    newGame = getNewGame(app, mouseX, mouseY)
    if newGame is not None:
        app.gameOver = False
        restartGame(app)


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
        x, y = getCellLeftTop(app, 2, i+1)
        drawRect(x, y, cellWidth, cellHeight, fill='lightgrey', border='black', borderWidth=app.cellBorderWidth)
        if app.answer[i].upper() in app.guessedLetters:
            drawLabel(app.answer[i].upper(), x + cellWidth / 2, y + cellHeight / 2, size=20, bold=True)

    #app.filledInAnswer = True
        
def onStep(app):
    if app.spinWheel == True:
        if app.spinSpeed>=0:
            takeStep(app)
            app.spinSpeed -=app.spinFriction
            #print (list(app.prizes.keys())[0])
        else:
            app.spinWheel = False
            print (list(app.prizes.keys())[0], list(app.prizes.values())[0])
            selected_label = getSelectedLabel(app)
            print (f'Spin to :{selected_label.value}')
            print (f'{app.answer}')
            #app.gameOver = True
    
def getSelectedLabel(app):
    labels = [s for s in app.group if isinstance(s, Label)]
    selected_label = min (labels , key = lambda x : abs((x.rotateAngle+360) %360 - 90))

    return selected_label

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
    (x,y) = getCellLeftTop(app, 40  , 3 )
    w,h = getCellSize(app)
    drawLabel(f"{playerName}: ${playerMoney}", x,  app.height-20, bold=True )

def drawComputerMoney(app):

    playerObj = app.computerPlayer1
    playerName = playerObj.name
    playerMoney = playerObj.money
    (x,y) = getCellLeftTop(app, 40  , 15 )
    w,h = getCellSize(app)
    drawLabel(f"{playerName}: ${playerMoney}", x,  app.height-20, bold=True )

def gameOverScreen(app):
    drawLabel("Game Over!", app.width // 2, app.height // 2, size=50, bold=True)
    drawLabel(f"The correct phrase was: {app.answer}", app.width // 2, app.height // 2 + 50, size=20)

def redrawAll(app):
    if app.gameOver == False:
        drawBoard(app)
        drawBoardBorder(app)
        drawWheel(app)
        drawRedArrow(app)
        drawSpinButton(app)
        drawPlayerMoney(app)
        drawComputerMoney(app)
        drawAnswerPhrase(app)
        draw26Letters(app)
        drawSolveGameButton(app)
    else:
        gameOverScreen(app)
        drawNewGameButton(app)


def main():
    runApp()

main()


#https://www.geeksforgeeks.org/python-rotate-dictionary-by-k/
#https://www.cs.cmu.edu/~112/syllabus.html
#https://academy.cs.cmu.edu/exercise/13131
#https://towardsdatascience.com/hands-on-markov-chains-example-using-python-8138bf2bd971
