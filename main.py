
from header import *

# Const variables for window size 
SCR_WIDTH = 600
SCR_HEIGHT = 800
# Const variables for coordinate space in between words.
WORD_XSPACE = 130
WORD_YSPACE = 60

# Colours for use (RGBA)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0 ,0)
lightgrey = (220, 220, 220)
lightergrey = (244, 244, 244)
lavender = (221,160,221)
black = (0, 0, 0)

_scr = pygame.display.set_mode([SCR_HEIGHT, SCR_WIDTH]) # pygame function to set the display width and height
pygame.display.set_caption('Typing Test') # pygame function to set the name of the window

def getTextColour(status):
    if status == WORD_STATUS.WORD_ACTIVE:
        return lavender
    elif status == WORD_STATUS.WORD_CORRECT:
        return green
    elif status == WORD_STATUS.WORD_WRONG:
        return red
    elif status == WORD_STATUS.WORD_UNKNOWN:
        return black

def iterateText():
    # word count will always be a multiple of 25
    global wordStatuses, wordList, currentWord, acceptInput
    _sctr = currentWord // 25 
    partialWordList = [wordList[i] for i in range(_sctr*25, 25+(_sctr*25))]
    showText(partialWordList, _sctr)
    

def showText(list, sector):
    global wordStatuses, currentWord
    spacerVariable = 0
    for i in range(25):       
        if (i+(sector*25) == currentWord):
            wordStatuses[i + (sector*25)] = WORD_STATUS.WORD_ACTIVE
        if (i % 5 == 0):
            spacerVariable += 1
        colorInUse = getTextColour(wordStatuses[i + (sector * 25)])
        drawText(_scr, list[i] + "  ", SCR_WIDTH // 4 + WORD_XSPACE*(i % 5),  SCR_HEIGHT // 2 + (WORD_YSPACE * spacerVariable) - 350, colorInUse)


def setLanguage(language):
    global randomWords
    with open('lang.json', 'r') as f:
        data = json.loads(f.read())
        randomWords = data[language]
def setText():
    global randomWords, wordStatuses, wordList
    if (typingMode == 'wordcount'):
        wordList = []
        while (len(wordList) < wordCount):
            randomWord = randomWords[floor(random() * len(randomWords))]
            if len(wordList) == 0:
                wordList.append(randomWord)
                continue
            if wordList[len(wordList) - 1] != randomWord:
                wordList.append(randomWord)
        for i in range(wordCount):
            wordStatuses[i] = WORD_STATUS.WORD_UNKNOWN
        wordStatuses[0] = WORD_STATUS.WORD_ACTIVE

def drawInputField():
    inputFieldRect = pygame.Rect((SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2), 600, 60)
    return inputFieldRect

def updateInputField(rectcentre_x, rectcentre_y):
    global inputFieldStatus
    if (inputFieldStatus == WORD_STATUS.WORD_CORRECT):
        drawText(_scr, inputFieldValue, rectcentre_x, rectcentre_y, green)
    else:
        drawText(_scr, inputFieldValue, rectcentre_x, rectcentre_y, red)

def drawText(screen, message, x, y, color, fsize=32, rectcolor=None):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(message, True, color, rectcolor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    return textRect

def init(wc):
    global wordCount, acceptInput
    wordCount = wc
    acceptInput = True
    setLanguage("english")
    setText()

def OnFirstKeyPress():
    global startDate
    if (typingMode == 'wordcount'):
        startDate = datetime.datetime.now()

def OnKeyPress(keys): 
    global inputFieldStatus, displayScore, currentWord, inputFieldValue, correctKeys
    if (typingMode == 'wordcount'):
        if (currentWord < len(wordList)):
            if keys in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if (inputFieldValue == '' and currentWord == 0):
                    OnFirstKeyPress()
                inputFieldValue += keys
                currentWordSlice = (wordList[currentWord])[0:len(inputFieldValue)]
                if (inputFieldValue == currentWordSlice):
                    inputFieldStatus = WORD_STATUS.WORD_CORRECT
                    if (inputFieldValue == wordList[currentWord] and currentWord == wordCount - 1):
                        displayScore = True
                        return 
                else:
                    inputFieldStatus = WORD_STATUS.WORD_WRONG
            elif keys == "Backspace":
                inputFieldValue = inputFieldValue[:-1]
                currentWordSlice = (wordList[currentWord])[0:len(inputFieldValue)]
                if (inputFieldValue == currentWordSlice):
                    inputFieldStatus = WORD_STATUS.WORD_CORRECT
                else:
                    inputFieldStatus = WORD_STATUS.WORD_WRONG
            elif keys == "Space":
                if (inputFieldValue == wordList[currentWord]):
                    correctKeys += len(wordList[currentWord]) + 1
                    wordStatuses[currentWord] = WORD_STATUS.WORD_CORRECT
                else:
                    wordStatuses[currentWord] = WORD_STATUS.WORD_WRONG
                    if (currentWord == wordCount - 1):
                        displayScore = True
                        return
                inputFieldValue = ""
                currentWord += 1
                
                
def CalculateScore():
    global correctKeys, startDate, totalKeys, typingMode
    words = 0
    minutes = 0
    accuracy = 0
    if (typingMode == 'wordcount'):
        words = correctKeys / 5
        minutes = (datetime.datetime.now() - startDate)
        minutes = minutes.seconds / 60
        totalKeys = -1
        for word in wordList:
            totalKeys += len(word) + 1
        accuracy = floor((correctKeys / totalKeys) * 100)
    wpm = floor(words / minutes)
    return f"WPM: {wpm}, ACC: {accuracy}%"

def mouseOverPosition(rect, pos):
    return rect.collidepoint(pos[0], pos[1])

def getTextRect(msg, x, y, color, fsize=32, rectcolor=None):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(msg, True, color, rectcolor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    return textRect

def restartGame(wc=25):
    global inputFieldValue, typingMode, currentWord, wordCount, randomWords, wordList, wordStatuses, correctKeys, startDate, timer, timerActive, punctuation, displayScore, acceptInput
    inputFieldValue = ""
    typingMode = 'wordcount'
    currentWord = 0
    wordCount = 0
    randomWords = []
    wordList = []
    wordStatuses = {}
    correctKeys = 0
    startDate = 0
    timer = 0
    timerActive = False
    punctuation = False
    displayScore = False
    acceptInput = True
    init(wc)
    run()


def run():
    global displayScore, acceptInput, wordCount
    running = True
    msg = ""  
    pygame.key.set_repeat(0, 1000)
    while running:  
        twentyfiveRect = getTextRect("25", (SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2) - 350, black, 30)
        fiftyRect = getTextRect("50", (SCR_WIDTH // 2) - 100, (SCR_HEIGHT // 2) -350, black, 30)
        hundredRect = getTextRect("100", (SCR_WIDTH // 2), (SCR_HEIGHT // 2) - 350, black, 30)

        redoButtonRect = getTextRect("Redo", (SCR_WIDTH // 2) + 350, (SCR_HEIGHT // 2) + 28, black, 30)
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and acceptInput == True:               
                if event.key == pygame.K_BACKSPACE:
                    OnKeyPress("Backspace")
                elif event.key == pygame.K_SPACE:
                    OnKeyPress("Space")
                else:
                    OnKeyPress(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouseOverPosition(redoButtonRect, mousePos):
                    restartGame(wordCount)
                elif mouseOverPosition(twentyfiveRect, mousePos):
                    restartGame(25)
                elif mouseOverPosition(fiftyRect, mousePos):
                    restartGame(50)
                elif mouseOverPosition(hundredRect, mousePos):
                    restartGame(100)

            
        if (displayScore):
            msg = CalculateScore()
            acceptInput = False
            displayScore = False

        pygame.display.flip()
        _scr.fill((255, 255, 255)) # Fill the screen white
        
        # Underline the text
        if wordCount == 25:
            pygame.draw.rect(_scr, black, twentyfiveRect.copy().inflate(1, -25).move(0, 13))
        elif wordCount == 50:
            pygame.draw.rect(_scr, black, fiftyRect.copy().inflate(1, -25).move(0, 13))
        else:
            pygame.draw.rect(_scr, black, hundredRect.copy().inflate(1, -25).move(0, 13))
        # Options to choose different word counts
        drawText(_scr, "25", (SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2) - 350, black, 30)
        drawText(_scr, "50", (SCR_WIDTH // 2) - 100, (SCR_HEIGHT // 2) -350, black, 30)
        drawText(_scr, "100", (SCR_WIDTH // 2), (SCR_HEIGHT // 2) - 350, black, 30)

        rectOverText = pygame.Rect((SCR_WIDTH // 2) - 250, (SCR_HEIGHT // 2) - 330, 700, 410) # Create a grey rectangle background behind the black text for contrast
        pygame.draw.rect(_scr, lightgrey, rectOverText, border_radius=10) # Draw the rectangle

        rect = drawInputField() # Use the function to return us a rectangle.
        pygame.draw.rect(_scr, (255, 255, 255), rect, border_radius=10) # Draw the rectangle returned by the function.

        redoButtonColor = lightergrey if (mouseOverPosition(redoButtonRect, mousePos)) else lightgrey
        drawText(_scr, "Redo", (SCR_WIDTH // 2) + 350, (SCR_HEIGHT // 2) + 28, black, 30, redoButtonColor)

        drawText(_scr, msg, 420, 540, black, 48) # Draw the score, if there is one.
        iterateText() # Draw our text in the game
        updateInputField(rect.centerx, rect.centery) # Update the text in the box when typing
        pygame.display.update() # Pygame function to update the screen

pygame.init()
init(25)
run()