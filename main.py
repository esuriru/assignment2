
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

class Game:
    def showText(self):
        spacerVariable = 0
        for i in range(len(self.wordList)):
            if (i == self.currentWord):
                self.wordStatuses[i] = WORD_STATUS.WORD_ACTIVE
            if (i % 5 == 0):
                spacerVariable += 1
            colorInUse = (0, 0, 0)
            if (self.wordStatuses[i] == WORD_STATUS.WORD_ACTIVE):
                colorInUse = lavender
            elif (self.wordStatuses[i] == WORD_STATUS.WORD_CORRECT):
                colorInUse = green
            elif self.wordStatuses[i] == WORD_STATUS.WORD_WRONG:
                colorInUse = red
            elif self.wordStatuses[i] == WORD_STATUS.WORD_UNKNOWN:
                colorInUse = black


            self.drawText(self._scr, self.wordList[i] + "  ", SCR_WIDTH // 4 + WORD_XSPACE*(i % 5),  SCR_HEIGHT // 2 + (WORD_YSPACE * spacerVariable) - 350, colorInUse)
    
    def setLanguage(self, language):
        with open('lang.json', 'r') as f:
            data = json.loads(f.read())
            self.randomWords = data[language]
    def setText(self):
        if (self.typingMode == 'wordcount'):
            self.wordList = []
            while (len(self.wordList) < self.wordCount):
                randomWord = self.randomWords[floor(random() * len(self.randomWords))]
                if len(self.wordList) == 0:
                    self.wordList.append(randomWord)
                    continue
                if self.wordList[len(self.wordList) - 1] != randomWord:
                    self.wordList.append(randomWord)
            for i in range(self.wordCount):
                self.wordStatuses[i] = WORD_STATUS.WORD_UNKNOWN
            self.wordStatuses[0] = WORD_STATUS.WORD_ACTIVE

    def drawInputField(self):
        inputFieldRect = pygame.Rect((SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2), 600, 60)
        return inputFieldRect

    def updateInputField(self, rectcentre_x, rectcentre_y):
        if (self.inputFieldStatus == WORD_STATUS.WORD_CORRECT):
            self.drawText(self._scr, self.inputFieldValue, rectcentre_x, rectcentre_y, green)
        else:
            self.drawText(self._scr, self.inputFieldValue, rectcentre_x, rectcentre_y, red)

    def drawText(self, screen, message, x, y, color, fsize=32, rectcolor=None):
        font = pygame.font.Font('freesansbold.ttf', fsize)
        text = font.render(message, True, color, rectcolor)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)
    def __init__(self):
        pygame.init()

        # Initialise variables
        self.inputFieldValue = ""
        self.typingMode = 'wordcount'
        self.wordCount = 0
        self.randomWords = []
        self.wordList = []
        self.wordStatuses = {}
        self.currentWord = 0
        self.correctKeys = 0
        self.startDate = 0
        self.timer = 0
        self.timerActive = False
        self.punctuation = False
        self.displayScore = False

        # Buffer variables
        self.keypressed = False
        self.backspace_pressed = False
        self.previouskeypressed = 0
        # Word slice variables
        self.inputWordSlice = ""
        self.currentWordSlice = ""
        self.inputFieldStatus = WORD_STATUS.WORD_CORRECT
        

        
        self.wordCount = 25
        self.setLanguage("english")
        self.setText()
        self._scr = pygame.display.set_mode([SCR_HEIGHT, SCR_WIDTH])
        pygame.display.set_caption('Typing Test')
        self.charactersTyped = []
        self.run()
    def OnFirstKeyPress(self):
        if (self.typingMode == 'wordcount'):
            self.startDate = datetime.datetime.now()
    def OnKeyPress(self, keys): 
        if (self.typingMode == 'wordcount'):
            if (self.currentWord < len(self.wordList)):
                if keys in "abcdefghijklmnopqrstuvwxyzI":
                    if (self.inputFieldValue == '' and self.currentWord == 0):
                        self.OnFirstKeyPress()
                    self.inputFieldValue += keys
                    self.currentWordSlice = (self.wordList[self.currentWord])[0:len(self.inputFieldValue)]
                    if (self.inputFieldValue == self.currentWordSlice):
                        self.inputFieldStatus = WORD_STATUS.WORD_CORRECT
                        if (self.inputFieldValue == self.wordList[self.currentWord] and self.currentWord == self.wordCount - 1):
                            self.displayScore = True
                    else:
                        self.inputFieldStatus = WORD_STATUS.WORD_WRONG
                elif keys == "Backspace":
                    self.inputFieldValue = self.inputFieldValue[:-1]
                    self.currentWordSlice = (self.wordList[self.currentWord])[0:len(self.inputFieldValue)]
                    if (self.inputFieldValue == self.currentWordSlice):
                        self.inputFieldStatus = WORD_STATUS.WORD_CORRECT
                    else:
                        self.inputFieldStatus = WORD_STATUS.WORD_WRONG
                elif keys == "Space":
                    if (self.inputFieldValue == self.wordList[self.currentWord]):
                        self.correctKeys += len(self.wordList[self.currentWord]) + 1
                        self.wordStatuses[self.currentWord] = WORD_STATUS.WORD_CORRECT
                    else:
                        self.wordStatuses[self.currentWord] = WORD_STATUS.WORD_WRONG
                        if (self.currentWord == self.wordCount - 1):
                            self.displayScore = True
                    self.inputFieldValue = ""
                    self.inputWordSlice = ""
                    self.currentWord += 1
                    
                    
    def CalculateScore(self):
        words = 0
        minutes = 0
        accuracy = 0
        if (self.typingMode == 'wordcount'):
            words = self.correctKeys / 5
            minutes = (datetime.datetime.now() - self.startDate)
            minutes = minutes.seconds / 60
            totalKeys = -1
            for word in self.wordList:
                totalKeys += len(word) + 1
            accuracy = floor((self.correctKeys / totalKeys) * 100)
        wpm = floor(words / minutes)
        return f"WPM: {wpm}, ACC: {accuracy}%"

    def run(self):
        self.running = True
        msg = ""  
        pygame.key.set_repeat(0, 1000)
        while self.running:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.OnKeyPress("Backspace")
                    elif event.key == pygame.K_SPACE:
                        self.OnKeyPress("Space")
                    else:
                        self.OnKeyPress(event.unicode)
                elif event.type == pygame.KEYUP:
                    pass
               
            if (self.displayScore):
                msg = self.CalculateScore()
                self.displayScore = False

            pygame.display.flip()
            self._scr.fill((255, 255, 255))
            rectOverText = pygame.Rect((SCR_WIDTH // 2) - 250, (SCR_HEIGHT // 2) - 400, 700, 500)
            pygame.draw.rect(self._scr, lightgrey, rectOverText)
            rect = self.drawInputField()
            pygame.draw.rect(self._scr, (255, 255, 255), rect)
            self.drawText(self._scr, msg, 450, 540, black, 48)
            self.showText()
            self.updateInputField(rect.centerx, rect.centery)
            pygame.display.update()

Game().run()