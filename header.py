from math import *
from random import *
from enum import Enum
import pygame
import json
import datetime

class WORD_STATUS(Enum):
    WORD_ACTIVE = 1
    WORD_CORRECT = 2
    WORD_WRONG = 3
    WORD_UNKNOWN = 4

# Initialise variables
inputFieldValue = ""
typingMode = 'wordcount'
wordCount = 0
randomWords = []
wordList = []
wordStatuses = {}
currentWord = 0
correctKeys = 0
startDate = 0
timer = 0
timerActive = False
punctuation = False
displayScore = False
acceptInput = True

# Word slice variables
currentWordSlice = ""
inputFieldStatus = WORD_STATUS.WORD_CORRECT