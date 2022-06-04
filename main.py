
from header import *

# Const variables for window size 
SCR_WIDTH = 600
SCR_HEIGHT = 800
# Const variables for coordinate space in between words.
WORD_XSPACE = 130
WORD_YSPACE = 60

# Colours for use
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0 ,0)
lightgrey = (220, 220, 220)
lavender = (230, 230, 250)
black = (0, 0, 0)

_scr = pygame.display.set_mode([SCR_HEIGHT, SCR_WIDTH])
pygame.display.set_caption('Typing Test')

def showText():
    global wordStatuses, wordList
    spacerVariable = 0
    for i in range(len(wordList)):
        if (i == currentWord):
            wordStatuses[i] = WORD_STATUS.WORD_ACTIVE
        if (i % 5 == 0):
            spacerVariable += 1
        colorInUse = (0, 0, 0)
        if (wordStatuses[i] == WORD_STATUS.WORD_ACTIVE):
            colorInUse = lavender
        elif (wordStatuses[i] == WORD_STATUS.WORD_CORRECT):
            colorInUse = green
        elif wordStatuses[i] == WORD_STATUS.WORD_WRONG:
            colorInUse = red
        elif wordStatuses[i] == WORD_STATUS.WORD_UNKNOWN:
            colorInUse = black
        drawText(_scr, wordList[i] + "  ", SCR_WIDTH // 4 + WORD_XSPACE*(i % 5),  SCR_HEIGHT // 2 + (WORD_YSPACE * spacerVariable) - 350, colorInUse)

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

def init():
    global wordCount
    pygame.init()
    wordCount = 25
    setLanguage("english")
    setText()

def OnFirstKeyPress():
    global startDate
    if (typingMode == 'wordcount'):
        startDate = datetime.datetime.now()

def OnKeyPress(keys): 
    global inputFieldStatus, displayScore, inputWordSlice, currentWord, inputFieldValue, correctKeys
    if (typingMode == 'wordcount'):
        if (currentWord < len(wordList)):
            if keys in "abcdefghijklmnopqrstuvwxyzI":
                if (inputFieldValue == '' and currentWord == 0):
                    OnFirstKeyPress()
                inputFieldValue += keys
                currentWordSlice = (wordList[currentWord])[0:len(inputFieldValue)]
                if (inputFieldValue == currentWordSlice):
                    inputFieldStatus = WORD_STATUS.WORD_CORRECT
                    if (inputFieldValue == wordList[currentWord] and currentWord == wordCount - 1):
                        displayScore = True
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
                inputFieldValue = ""
                inputWordSlice = ""
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

def run():
    global displayScore
    running = True
    msg = ""  
    pygame.key.set_repeat(0, 1000)
    while running:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    OnKeyPress("Backspace")
                elif event.key == pygame.K_SPACE:
                    OnKeyPress("Space")
                else:
                    OnKeyPress(event.unicode)
            elif event.type == pygame.KEYUP:
                pass
            
        if (displayScore):
            msg = CalculateScore()
            displayScore = False

        pygame.display.flip()
        _scr.fill((255, 255, 255))
        rectOverText = pygame.Rect((SCR_WIDTH // 2) - 250, (SCR_HEIGHT // 2) - 400, 700, 500)
        pygame.draw.rect(_scr, lightgrey, rectOverText)
        rect = drawInputField()
        pygame.draw.rect(_scr, (255, 255, 255), rect)
        drawText(_scr, msg, 450, 540, black, 48)
        showText()
        updateInputField(rect.centerx, rect.centery)
        pygame.display.update()

init()
run()