
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
        return lavender # The colour used for the active word.
    elif status == WORD_STATUS.WORD_CORRECT:
        return green # The colour used for words that are correct.
    elif status == WORD_STATUS.WORD_WRONG:
        return red # The colour used for words that are wrong.
    elif status == WORD_STATUS.WORD_UNKNOWN:
        return black # The colour used for words that are not typed yet.

def iterateText():
    global wordStatuses, wordList, currentWord # We are using these global variables in the function. python requires use to declare this before we use them.
    _sctr = currentWord // 25 # Use floor division to get the 'sector' of the word list, as only 25 words are shown at the start.
    partialWordList = [wordList[i] for i in range(_sctr*25, 25+(_sctr*25))] # One line function to add the 25 items in the sector that we are on.
    showText(partialWordList, _sctr) # Send the data to our function to draw the text.
    

def showText(list, sector):
    global wordStatuses, currentWord # We are using these global variables in the function. python requires use to declare this before we use them.
    spacerVariable = 0 # The variable we use for spacing out the words vertically.
    for i in range(25): # Iterate through 25 times.       
        if (i+(sector*25) == currentWord): # If the word is the word the user is currently on,
            wordStatuses[i + (sector*25)] = WORD_STATUS.WORD_ACTIVE # Change that word to the active word.
        if (i % 5 == 0): # If we are on the next line(5 words have been written already), add one.
            spacerVariable += 1
        colorInUse = getTextColour(wordStatuses[i + (sector * 25)]) # Use the function to return the colour of the text.
        drawText(_scr, list[i] + "  ", SCR_WIDTH // 4 + WORD_XSPACE*(i % 5),  SCR_HEIGHT // 2 + (WORD_YSPACE * spacerVariable) - 350, colorInUse) # Draw the text on the screen, with the color we have found.


def setLanguage(language):
    global randomWords # Global variable that needs to be changed.
    with open('lang.json', 'r') as f: # Open the file 'lang.json' and read it, returning it as f.
        data = json.loads(f.read()) # Use the json library to import the language as a list of dictionaries.
        randomWords = data[language] # The random words will be imported with the language that we have input into the function.
def setText():
    global randomWords, wordStatuses, wordList # We are using these global variables in the function. python requires use to declare this before we use them.
    if (typingMode == 'wordcount'): # Check for the typing mode, this allows for the implementation of a timer in the future.
        wordList = [] # Empty the word list.
        while (len(wordList) < wordCount): # Make a while loop that iterates through the random words.
            randomWord = randomWords[floor(random() * len(randomWords))] # Get a random word.
            if len(wordList) == 0: # If the list is empty, place the word without any checks.
                wordList.append(randomWord)
                continue
            if wordList[len(wordList) - 1] != randomWord: # If the latest word is not the random word we have gotten, add it in.
                wordList.append(randomWord)
        for i in range(wordCount): # Now, intialise all the words with the unknown status.
            wordStatuses[i] = WORD_STATUS.WORD_UNKNOWN
        wordStatuses[0] = WORD_STATUS.WORD_ACTIVE # Initialise the first word with active, because it is first word they will type.

def drawInputField():
    inputFieldRect = pygame.Rect((SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2), 600, 60) # Pygame function to return a rectangle's size and coordinates.
    return inputFieldRect # Return that rectangle.

def updateInputField(rectcentre_x, rectcentre_y):
    global inputFieldStatus # Global variable that needs to be changed.
    if (inputFieldStatus == WORD_STATUS.WORD_CORRECT):
        drawText(_scr, inputFieldValue, rectcentre_x, rectcentre_y, green) # Draw the text green cause it is correct.
    else:
        drawText(_scr, inputFieldValue, rectcentre_x, rectcentre_y, red) # Draw the text red cause it is incorrect.

def drawText(screen, message, x, y, color, fsize=32, rectcolor=None):
    font = pygame.font.Font('freesansbold.ttf', fsize) # Use the freesansbold.ttf font and font size(fsize) in the pygame function.
    text = font.render(message, True, color, rectcolor) # Create the text using the pygame function
    textRect = text.get_rect() # Get the rectangle that surrounds the text.
    textRect.center = (x, y) # Centre it around the position that has been provided to us.
    screen.blit(text, textRect) # Draw the text.
    return textRect # Return the rectangle.

def init(wc): # Initialise the game.
    global wordCount, acceptInput # Use this global values.
    wordCount = wc # Change the word count to the input.
    acceptInput = True # Accept input.
    setLanguage("english") # Set language to english.
    setText() # Get the text for the game.

def OnFirstKeyPress():
    global startDate # Global variable we need to change.
    if (typingMode == 'wordcount'): # Check for the typing mode, this allows for the implementation of a timer in the future.
        startDate = datetime.datetime.now() # Get the time now, for use later.

def OnKeyPress(keys): 
    global inputFieldStatus, displayScore, currentWord, inputFieldValue, correctKeys # Global variables we need to change.
    if (typingMode == 'wordcount'): # Check for the typing mode, this allows for the implementation of a timer in the future.
        if (currentWord < len(wordList)): # Go through if the current word is still in the word list.
            if keys in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": # Check if the key inputed is an alphabet.
                if (inputFieldValue == '' and currentWord == 0): # There is a key input, check if the input field value is empty first and it is the first word.
                    OnFirstKeyPress() # Start the 'timer'
                inputFieldValue += keys # Add the key input into the input field.
                currentWordSlice = (wordList[currentWord])[0:len(inputFieldValue)] # Get the slice of the word that we use to compare to the input field value, it will be the same length.
                if (inputFieldValue == currentWordSlice): # If the input in the field is correct, show it as correct.
                    inputFieldStatus = WORD_STATUS.WORD_CORRECT
                    if (inputFieldValue == wordList[currentWord] and currentWord == wordCount - 1): # If it is correct, and it is the last word, end the test there.
                        correctKeys += len(wordList[currentWord]) # Add to the number of correct keys.
                        wordStatuses[currentWord] = WORD_STATUS.WORD_CORRECT # Change it to correct.
                        displayScore = True # Event for displaying score.
                        return # Stop the function here.
                else:
                    inputFieldStatus = WORD_STATUS.WORD_WRONG # Else, show it as wrong.
            elif keys == "Backspace": # Check if the person wants to delete his last keystroke.
                inputFieldValue = inputFieldValue[:-1] # Delete the last letter of the string
                currentWordSlice = (wordList[currentWord])[0:len(inputFieldValue)] # Get the slice of the word that we use to compare to the input field value, it will be the same length.
                if (inputFieldValue == currentWordSlice): # If the input in the field is correct, show it as correct.
                    inputFieldStatus = WORD_STATUS.WORD_CORRECT
                    if (inputFieldValue == wordList[currentWord] and currentWord == wordCount - 1): # If it is correct, and it is the last word, end the test there.
                        displayScore = True # Event for displaying score.
                        return # Stop the function here.
                else:
                    inputFieldStatus = WORD_STATUS.WORD_WRONG # Else, show it as wrong.
            elif keys == "Space": # Go to the next word.
                if (inputFieldValue == wordList[currentWord]): # Another check to see if it is correct, the correct slice may be inputed, so we need to check the string.
                    correctKeys += len(wordList[currentWord]) # Add to the number of correct keys inputed.
                    wordStatuses[currentWord] = WORD_STATUS.WORD_CORRECT # Change the status of the word to correct.
                else:
                    wordStatuses[currentWord] = WORD_STATUS.WORD_WRONG # Change the status of the word to incorrect.
                    if (currentWord == wordCount - 1): # If it is the last word, display the score.
                        displayScore = True # Event for displaying score.
                        return # Stop the function here.
                inputFieldValue = "" # Empty the input field value.
                currentWord += 1 # Go to the next word.
                
                
def CalculateScore():
    global correctKeys, startDate, totalKeys, typingMode # Global variables used.
    words = 0 # WPM
    minutes = 0 # Time taken to finish the test.
    accuracy = 0 # Accuracy of the test.
    if (typingMode == 'wordcount'):
        words = correctKeys / 5 # Formula for one word is 5 letters inputted correctly.
        minutes = (datetime.datetime.now() - startDate) # Get the difference of the time we started the test and the current time now.
        minutes = minutes.seconds / 60 # Change it into minutes.
        totalKeys = -1 # Initialise totalkeys.
        for word in wordList:
            totalKeys += len(word) # Add on the amount of keys inputted for the test.
        accuracy = floor((correctKeys / totalKeys) * 100) # Get the percentage of accuracy.
    wpm = floor(words / minutes) # Get the words per minute.
    return f"WPM: {wpm}, ACC: {accuracy}%" # Return the formatted string.

def mouseOverPosition(rect, pos):
    return rect.collidepoint(pos[0], pos[1]) # Pygame function to check if the position is over the rectangle.

def getTextRect(msg, x, y, color, fsize=32, rectcolor=None):
    font = pygame.font.Font('freesansbold.ttf', fsize) # Use the same font to check, some fonts might have different size.
    text = font.render(msg, True, color, rectcolor) # Render the text.
    textRect = text.get_rect() # Get the rectangle surrounding the text.
    textRect.center = (x, y) # Change the center to the coords.
    return textRect # Return that rectangle.

def restartGame(wc=25):
    global inputFieldValue, typingMode, currentWord, wordCount, randomWords, wordList, wordStatuses, correctKeys, startDate, displayScore, acceptInput # Global variables used.
    inputFieldValue = "" # Reset to empty.
    typingMode = 'wordcount' # Default typing mode.
    currentWord = 0 # Change current word to the first one.
    wordCount = 0 # Reset word count.
    randomWords = [] # Clear random words.
    wordList = [] # Clear word list.
    wordStatuses = {} # Clear word statuses.
    correctKeys = 0 # Clear correct keys.
    startDate = 0 # Initialise start date.
    displayScore = False # We are not displaying score at the start.
    acceptInput = True # Accept input is true.
    init(wc) # Initialise the word value.
    run() # Run the game again.


def run():
    global displayScore, acceptInput, wordCount # Global variables used.
    running = True # Our runtime variable
    msg = ""  # Display score variable.
    pygame.key.set_repeat(0, 1000) # Pygame function to stop repeating of key inputs.
    while running:  
        twentyfiveRect = getTextRect("25", (SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2) - 350, black, 30) # The rectangle surrounding the 25.
        fiftyRect = getTextRect("50", (SCR_WIDTH // 2) - 100, (SCR_HEIGHT // 2) -350, black, 30) # The rectangle surrounding the 50.
        hundredRect = getTextRect("100", (SCR_WIDTH // 2), (SCR_HEIGHT // 2) - 350, black, 30) # The rectangle surrounding the 100.

        redoButtonRect = getTextRect("Redo", (SCR_WIDTH // 2) + 350, (SCR_HEIGHT // 2) + 28, black, 30) # The rectangle surrounding the redo button.
        mousePos = pygame.mouse.get_pos() # Get the mouse position.

        for event in pygame.event.get(): # Get all the events happening in the current frame.
            if event.type == pygame.QUIT: # If the user has pressed the exit button.
                running = False # Stop runtime.
                pygame.quit() # Quit the program.
            elif event.type == pygame.KEYDOWN and acceptInput == True: # If we are accepting input and the user and pressed a key.          
                if event.key == pygame.K_BACKSPACE: # Check if the user sends a backspace
                    OnKeyPress("Backspace") # Send it to our function.
                elif event.key == pygame.K_SPACE: # Check if the user sends a space.
                    OnKeyPress("Space") # Send it to our function.
                else:
                    OnKeyPress(event.unicode) # Send whatever else to the function.
            elif event.type == pygame.MOUSEBUTTONDOWN: # Check if the user has pressed his mouse button.
                if mouseOverPosition(redoButtonRect, mousePos): # Check if it is on one of the buttons.
                    restartGame(wordCount) # Reset to the word count we previously had.
                elif mouseOverPosition(twentyfiveRect, mousePos): # 25
                    restartGame(25)
                elif mouseOverPosition(fiftyRect, mousePos): # 50
                    restartGame(50)
                elif mouseOverPosition(hundredRect, mousePos): # 100
                    restartGame(100)            
        if (displayScore): # Check if it is time to display the score.
            msg = CalculateScore() # Calculate the score and produce the message.
            acceptInput = False # Turn off input.
            displayScore = False # We can turn off the event.

        pygame.display.flip() # Pygame necessary function.
        _scr.fill((255, 255, 255)) # Fill the screen white
        
        # Underline the text
        if wordCount == 25:
            pygame.draw.rect(_scr, black, twentyfiveRect.copy().inflate(1, -25).move(0, 13)) # We copy the rectangle surrounding the text and resize it to be an underline, so we keep the coordinates.
        elif wordCount == 50:
            pygame.draw.rect(_scr, black, fiftyRect.copy().inflate(1, -25).move(0, 13)) # We copy the rectangle surrounding the text and resize it to be an underline, so we keep the coordinates.
        else:
            pygame.draw.rect(_scr, black, hundredRect.copy().inflate(1, -25).move(0, 13)) # We copy the rectangle surrounding the text and resize it to be an underline, so we keep the coordinates.

        # Options to choose different word counts, draw them in.
        drawText(_scr, "25", (SCR_WIDTH // 2) - 200, (SCR_HEIGHT // 2) - 350, black, 30)
        drawText(_scr, "50", (SCR_WIDTH // 2) - 100, (SCR_HEIGHT // 2) -350, black, 30)
        drawText(_scr, "100", (SCR_WIDTH // 2), (SCR_HEIGHT // 2) - 350, black, 30)

        rectOverText = pygame.Rect((SCR_WIDTH // 2) - 250, (SCR_HEIGHT // 2) - 330, 700, 410) # Create a grey rectangle background behind the black text for contrast
        pygame.draw.rect(_scr, lightgrey, rectOverText, border_radius=10) # Draw the rectangle

        rect = drawInputField() # Use the function to return us a rectangle.
        pygame.draw.rect(_scr, (255, 255, 255), rect, border_radius=10) # Draw the rectangle returned by the function.

        redoButtonColor = lightergrey if (mouseOverPosition(redoButtonRect, mousePos)) else lightgrey # Check if the mouse is over the redo button, if it is, draw it lighter.
        drawText(_scr, "Redo", (SCR_WIDTH // 2) + 350, (SCR_HEIGHT // 2) + 28, black, 30, redoButtonColor) # Draw the text on the redo button.

        drawText(_scr, msg, 420, 540, black, 48) # Draw the score, if there is one.
        iterateText() # Draw our text in the game
        updateInputField(rect.centerx, rect.centery) # Update the text in the box when typing
        pygame.display.update() # Pygame function to update the screen

pygame.init() # Pygame init function.
init(25) # Initialise the game with a word count of 25.
run() # Run the game.