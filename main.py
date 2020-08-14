from lib import *
import random
import sys

#setting recursion limit
sys.setrecursionlimit(1500)


#------GRID CONSTANTS
WIDTH = 35
HEIGHT = 35
AMOUNT = 25
MARGIN = 1

MINE_NUMBER = 40



gameLoop(AMOUNT, WIDTH, HEIGHT, MARGIN, MINE_NUMBER)
