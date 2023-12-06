from cmu_graphics import *
import random
import math
import string # string.ascii_.lowercase
import button
import message
import player

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
    app.currentPlayerIndex = player.HUMAN_PLAYER
    app.humanPlayer = player.HumanPlayer('You')
    app.computerPlayer1 = player.ComputerPlayer('Computer 1', difficulty = 'easy')

    app.players = [app.humanPlayer, app.computerPlayer1]
    app.buttons = []
    app.statusMessage = message.Message(400, 20, 800, 36, "Game Started!", 20, active=True)
    app.humanMessage = message.Message(200, 780, 400, 36, "Human :", 20, fill="lightpink", active=True)
    app.computerMessage = message.Message(600, 780, 400, 36, "Computer :", 20, fill="lightblue",  active=False)
    app.count = 0
    app.spinSpeed = 0
    build26LetterBoard(app)
    app.events = []

    app.setSpin = False
    
    restartGame(app)

def build26LetterBoard(app):
    # build the letter board
    for index , letter in enumerate(string.ascii_lowercase):
        (x,y) = getCellLeftTop(app, 30+int(index/9) , 6+index%9 )
        w,h = (40,30)
        y += 10*(index//9)
        btn = button.Button(x, y, w, h, letter.upper(), size = 20, active=True)
        app.buttons.append(btn)


def restartGame(app):
    app.gameOver = False
    app.maxScore = 0
    app.rows = 5
    app.cols = 16
    app.boardLeft = 100
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
    app.colors = []
    for key in app.prizes:
        app.colors.append(app.prizes[key])
    app.money = list(app.prizes.keys())
    app.userInput = []
    app.computerInput = []
    app.currentPlayerIndex = player.HUMAN_PLAYER
    with open("test.txt","r") as readfile:
            app.randomWords = readfile.read()
            app.randomWords = app.randomWords.split()
    app.answer = random.choice(app.randomWords)
    app.answer = app.answer.upper()
    app.guessedLetters = set()
    app.filledInAnswer = False
    app.spinFriction = 10
    app.selectedLabel = ""
    app.revealedLetters = set()

    for playerObj in app.players:
        playerObj.money = 0
        playerObj.prizes.clear()
        playerObj.guessedLetters.clear()
        playerObj.respin = False

    #make all letters active
    for btn in app.buttons:
        btn.active = True

    app.events = []
    app.spinSpeed = 0
    addEvent(app, "New Game")

def addEvent(app, event):
    app.events.append({app.currentPlayerIndex : event})

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
    drawCircle(app.width/2, app.height/2, 40, fill='lightgray', border='red')
    drawLabel('SPIN', app.width/2, app.height/2, size= 30, bold=True)


#draw new game button
def drawNewGameButton(app):
    drawRect(app.width/2-60, app.height - 60, 120, 22 , fill='lightgray', border='green')
    drawLabel('New Game?', app.width/2, app.height - 50, size = 20, bold=True)


#draw solve game button
def drawSolveGameButton(app):
    drawRect(app.width/2-72, app.height - 70, 140, 22, fill='lightgray', border='green')
    drawLabel('Solve Game?', app.width/2, app.height - 60, size = 20, bold=True)


#gets the size of each cell
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)


# draw A-Z 26 letters
def draw26Letters(app):
    for btn in app.buttons:
        btn.draw()


def getSelectedLetter(app, mouseX, mouseY):
    for btn in app.buttons:
        if btn.contains(mouseX, mouseY):
            return btn
    return None    


def getNewGame(app, mouseX, mouseY):
    labels = [s for s in app.group if (isinstance(s, Label) and s.contains(mouseX, mouseY))]
    letters = [ l.value for l in labels if (l.value  == "New Game?")]
    return letters[0] if len(letters) > 0 else None 


def getSolveGame(app, mouseX, mouseY):
    labels = [s for s in app.group if (isinstance(s, Label) and s.contains(mouseX, mouseY))]
    letters = [ l.value for l in labels if (l.value  == "Solve Game?")]
    return letters[0] if len(letters) > 0 else None 


def isSolved(app):
    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        for letter in app.answer:
            if letter.upper() not in app.humanPlayer.guessedLetters:
                return False
        return True
    else:
        for letter in app.answer:
            if letter.upper() not in (app.computerPlayer1.guessedLetters | app.humanPlayer.guessedLetters):
                return False
        return True

def setCurrentPlayer(app, playerIndex):
    print(f'**********Change player {app.currentPlayerIndex} to {playerIndex}')
    #ans = app.getTextInput(f'Changing player:{app.currentPlayerIndex} to {playerIndex}\n Hit Ok to continue')
    app.currentPlayerIndex = playerIndex
    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        app.humanMessage.setActive(True)
        app.computerMessage.setActive(False)
    else:
        app.humanMessage.setActive(False)
        app.computerMessage.setActive(True)


def checkIfInAnswer(app, userInput):
    if app.gameOver:
        print("The game is over.")
        return

    if ''.join(userInput) == app.answer:
        print(f"Congratulations! You guessed the correct phrase: {app.answer}")
        app.gameOver = True
        return
    elif len(userInput) == 1 and userInput[0] in app.answer:
        if userInput[0] not in app.userInput:
            app.userInput.append(userInput[0])
            print(f"Good guess! '{userInput[0]}' is in the phrase.")
            addEvent(app, f'SL {userInput[0]} for {app.selectedLabel.value}')
            if app.currentPlayerIndex == player.COMPUTER_PLAYER:
                if app.selectedLabel.value == 'BANKRUPT':
                    app.computerPlayer1.goBankrupt()
                    addEvent(app, "BK")
                    return False
                elif app.selectedLabel.value == 'Lose a Turn':
                    addEvent(app, "LT")
                    return False
                else:
                    app.computerPlayer1.addMoney(app.selectedLabel.value)
                    addEvent(app, f'SL {userInput[0]} for {app.selectedLabel.value}')
                    app.spinSet = False
                    return True
            elif app.currentPlayerIndex == player.HUMAN_PLAYER:
                if app.selectedLabel.value == 'BANKRUPT':
                    app.humanPlayer.goBankrupt()
                    addEvent(app, "BK")
                    return False
                elif app.selectedLabel.value == 'Lose a Turn':
                    addEvent(app, "LT")
                    return False
                else:
                    app.humanPlayer.addMoney(app.selectedLabel.value)
                    addEvent(app, f'SL {userInput[0]} for {app.selectedLabel.value}')
                    app.spinSet = False
                    return True
            app.spinSet = False
            return True
        else:
            print(f"You already guessed '{userInput[0]}'. Try a different letter.")
            addEvent(app, f'DP {userInput[0]}')
            return

    else:
        print(f"Incorrect! '{''.join(userInput)}' is not in the phrase.")
        if app.currentPlayerIndex == player.HUMAN_PLAYER:
            addEvent(app, f'GW {userInput[0]}')
            return False
        else:
            addEvent(app, f'GW {userInput[0]}')
            return False


def drawAnswerPhrase(app):
    #if app.filledInAnswer:
    #    return
    answerLength = len(app.answer)
    cellWidth, cellHeight = getCellSize(app)
    for i in range(answerLength):
        x, y = getCellLeftTop(app, 2, i+1)
        drawRect(x, y, cellWidth, cellHeight, fill='lightgrey', border='black', borderWidth=app.cellBorderWidth)
        if app.answer[i].upper() in app.computerPlayer1.guessedLetters:
            drawLabel(app.answer[i].upper(), x + cellWidth / 2, y + cellHeight / 2, size=20, bold=True)
        if app.answer[i].upper() in app.humanPlayer.guessedLetters:
            drawLabel(app.answer[i].upper(), x + cellWidth / 2, y + cellHeight / 2, size=20, bold=True)


def takePlayerTurn(app, letter):
    # Check if it's the player's turn
    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        app.humanPlayer.guessedLetters.add(letter)
        print(f"{app.humanPlayer.name} guessed: {letter}")
        if checkIfInAnswer(app, letter):
            if isSolved(app):
                app.gameOver = True
            app.setSpin = False
            return
        else:
            addEvent(app, "switch to C")
            setCurrentPlayer(app, player.COMPUTER_PLAYER)
            app.setSpin = False
    else:
        addEvent(app, "Not your turn")
        print("It's not your turn!")


def setSpinSpeed(app):
    app.spinWheel = True
    app.spinSpeed = random.randint(48,72)


def setSpinFriction(app):
    if app.spinSpeed > 30:
        app.spinFriction = 10 
    elif app.spinSpeed > 20:
        app.spinFriction = 6
    elif app.spinSpeed > 10:
        app.spinFriction = 2
    else:
        app.spinFriction = 1


def takeComputerTurn(app):
    # Check if it's the computer's turn
    if app.gameOver:
        return
    if app.currentPlayerIndex == player.COMPUTER_PLAYER:
        #setSpinSpeed(app)
        print("****************computer's turn and spin")
        if app.spinSpeed <=0 :
            revealedLettersList = []
            guessedLetters = (app.computerPlayer1.guessedLetters | app.humanPlayer.guessedLetters)
            for letter in app.answer:
                if letter in guessedLetters:
                    revealedLettersList.append(letter)
                else:
                    revealedLettersList.append(' ')
            print(revealedLettersList)
            computerGuess = app.computerPlayer1.makeGuess(app.computerPlayer1.guessedLetters | 
                                                          app.humanPlayer.guessedLetters, 
                                                          revealedLettersList)
            print(computerGuess)
            app.computerPlayer1.guessedLetters.add(computerGuess)
            print(f'****************computer guessed {computerGuess}')
            checkAnswer = checkIfInAnswer(app, computerGuess)
            print(f'checkAnswer {checkAnswer}')
            if checkAnswer:
                print('computer guess correct')
                addEvent(app, f'GR {computerGuess}')
                app.spinSet = False # nedd to spin again
                if isSolved(app):
                    app.gameOver = True
                    addEvent(app, "Game Over")
                return
            if checkAnswer == False:
                print('computer guess wrong')
                addEvent(app, f'GW {computerGuess}')
                addEvent(app, "switch to H")
                setCurrentPlayer(app, player.HUMAN_PLAYER) #switch back to player


def onMousePress(app, mouseX, mouseY):
    print(app.events)
    print(app.humanPlayer.guessedLetters)
    print(app.computerPlayer1.guessedLetters)
    print(f'gameOver: {app.gameOver}')
    if isSolved(app):
        app.gameOver = True
    newGame = getNewGame(app, mouseX, mouseY)
    if newGame is not None:
        app.gameOver = False
        restartGame(app)

    if app.currentPlayerIndex == player.COMPUTER_PLAYER: # computer's turn, no human key press action
        return
    if app.spinWheel: # diable mouse press during wheel spin
        return

    if mouseX <= app.width / 2 + 20 and mouseX >= app.width / 2 - 20:
        if mouseY <= app.height / 2 + 20 and mouseY >= app.height / 2 - 20:
            if app.currentPlayerIndex == player.HUMAN_PLAYER:
                setSpinSpeed(app)
                app.setSpin = False
            else:
                print("It's not your turn!")
                print("It's computer turn!")
    if isSolved(app):
        app.gameOver = True

    # Check input only during the player's turn
    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        btn = getSelectedLetter(app, mouseX, mouseY)
        if btn is not None:
            btn.active = False
            takePlayerTurn(app, btn.text)
        if isSolved(app):
            app.gameOver = True

    #check input
    solveGame = getSolveGame(app, mouseX, mouseY)
    if solveGame is not None:
        guessedInput = app.getTextInput('Your guess:')
        for letter in guessedInput:
            app.humanPlayer.guessedLetters.add(letter.upper())
        if isSolved(app):
            app.gameOver = True
        

def isLose_a_Turn(app):
    return app.selectedLabel.value == 'Lose a Turn'


def isBankrupt(app):
    return app.selectedLabel.value == 'BANKRUPT'


def onStep(app):
    if isSolved(app):
        app.gameOver = True
    app.count += 1
    if app.count > 5:
        app.count = 0
        if app.currentPlayerIndex == player.HUMAN_PLAYER:
            if app.humanMessage.borderWidth == 3:
                app.humanMessage.borderWidth = 5
            else:
                app.humanMessage.borderWidth = 3
        else:
            if app.computerMessage.borderWidth == 3:
                app.computerMessage.borderWidth = 5
            else:
                app.computerMessage.borderWidth = 3

    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        if app.spinWheel == True:
            if app.spinSpeed >= 0:
                takeStep(app)
                app.spinSpeed -= app.spinFriction
                setSpinFriction(app)
            else:
                app.spinWheel = False
                app.selectedLabel = getSelectedLabel(app)
                print(f'Spin to: {app.selectedLabel.value}')
                print(f'{app.answer}')
                if isBankrupt(app):
                    app.humanPlayer.goBankrupt()
                    addEvent(app, "BK")
                    print(f'Switch to Computer player')
                    setCurrentPlayer(app, player.COMPUTER_PLAYER)
                    app.setSpin = False
                if isLose_a_Turn(app):
                    addEvent(app, "LT")
                    print(f'Switch to Computer player')
                    setCurrentPlayer(app, player.COMPUTER_PLAYER)
                    app.setSpin = False

                if isSolved(app):
                    addEvent(app, "GAME OVER")
                    app.gameOver = True
    # Check if it's the computer's turn
    else: # spin COMPUTER_PLAYER:
        if not app.setSpin:
            setSpinSpeed(app)
            app.setSpin = True
            return
        if app.spinWheel == True:
            if app.spinSpeed >= 0:
                takeStep(app)
                app.spinSpeed -= app.spinFriction
                setSpinFriction(app)
            else:
                takeComputerTurn(app)
                app.setSpin = False

    
def getSelectedLabel(app):
    labels = [s for s in app.group if isinstance(s, Label)]
    selectedLabel = min (labels , key = lambda x : abs((x.rotateAngle+360) %360 - 90))

    return selectedLabel


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
    app.humanMessage.text = f'Human : {playerMoney}'
    app.humanMessage.draw()


def drawComputerMoney(app):
    playerObj = app.computerPlayer1
    playerName = playerObj.name
    playerMoney = playerObj.money
    app.computerMessage.text = f'AI : {playerMoney}'
    app.computerMessage.draw()


def gameOverScreen(app):
    drawLabel("Game Over!", app.width // 2, app.height // 2, size=50, bold=True)
    drawLabel(f"The correct phrase was: {app.answer}", app.width // 2, app.height // 2 + 50, size=20)
    winner = "You are the winner" if app.currentPlayerIndex == player.HUMAN_PLAYER else "Computer is the winner"
    money = f'Amount: {app.humanPlayer.money}' if app.currentPlayerIndex == player.HUMAN_PLAYER else f'Amount: {app.computerPlayer1.money}'
    drawLabel(winner, app.width // 2, app.height // 2 + 80, size=20)
    drawLabel(money, app.width // 2, app.height // 2 + 110, size=20)


def drawStatusMessage(app):
    if app.currentPlayerIndex == player.HUMAN_PLAYER:
        app.statusMessage.text = "Human Turn: "
    else:
        app.statusMessage.text = "AI Turn: "
    recentEvents = str(app.events[-8:])
    app.statusMessage.text = app.statusMessage.text + recentEvents
    app.statusMessage.draw()
    app.statusMessage.size = 12


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
        drawStatusMessage(app)
    else:
        gameOverScreen(app)
        drawNewGameButton(app)
        drawBoard(app)
        drawAnswerPhrase(app)
        drawBoardBorder(app)
        drawStatusMessage(app)
        drawPlayerMoney(app)
        drawComputerMoney(app)


def main():
    runApp()


main()


#https://www.geeksforgeeks.org/python-rotate-dictionary-by-k/
#https://www.cs.cmu.edu/~112/syllabus.html
#https://academy.cs.cmu.edu/exercise/13131
#https://towardsdatascience.com/hands-on-markov-chains-example-using-python-8138bf2bd971
