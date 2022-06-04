from math import *
from random import *
import pygame
import json
from enum import Enum
import datetime

class WORD_STATUS(Enum):
    WORD_ACTIVE = 1
    WORD_CORRECT = 2
    WORD_WRONG = 3
    WORD_UNKNOWN = 4