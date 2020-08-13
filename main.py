import pygame
from grid import Box
import random
import sys

#setting recursion limit
sys.setrecursionlimit(1500)

pygame.init()
clock = pygame.time.Clock()

#--------Images
mine = pygame.image.load("images//mine.png")
flag = pygame.image.load("images//flag.png")


#-------Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)


#------GRID CONSTANTS
WIDTH = 35
HEIGHT = 35
AMOUNT = 25
MARGIN = 1

MINE_NUMBER = 20

screen = pygame.display.set_mode((WIDTH * AMOUNT + (AMOUNT + 1) * MARGIN, HEIGHT * AMOUNT + (AMOUNT + 1) * MARGIN))


#initialize grid
grid = []

for row in range(AMOUNT):
	grid.append([])
	for column in range(AMOUNT):
		grid[row].append(Box(row, column, WIDTH, HEIGHT, MARGIN))

#placing mines
mineLocation = []
for i in range(MINE_NUMBER):
	rndX = random.randint(0,AMOUNT-1)
	rndY = random.randint(0,AMOUNT-1)
	while grid[rndX][rndY].value == -1:
		rndX = random.randint(0,AMOUNT-1)
		rndY = random.randint(0,AMOUNT-1)
	mineLocation.append([rndX, rndY])
	grid[rndX][rndY].place_mine()


#calculate the neighbour mines for each box in the grid
for row in range(AMOUNT):
  for column in range(AMOUNT):
    if grid[row][column].value == -1:
    	#if there is a mine
      for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
          if ((i >= 0) and (j >= 0)) and ((i < AMOUNT) and (j < AMOUNT)) and ((i != row) or (j != column)) and (grid[i][j].value != -1):
            grid[i][j].incerease_value()
            grid[i][j].copy()

#Flood Fill algorithm
#more information at https://en.wikipedia.org/wiki/Flood_fill
def floodFill(posx, posy):
  global grid
  grid[posx][posy].onclick()
  if isFillable(posx - 1, posy):
      floodFill(posx - 1, posy)
  if isFillable(posx, posy - 1):
      floodFill(posx, posy - 1)
  if isFillable(posx + 1, posy):
      floodFill(posx + 1, posy)
  if isFillable(posx, posy + 1):
      floodFill(posx, posy + 1)

  if isFillable(posx - 1, posy - 1):
      floodFill(posx - 1, posy - 1)
  if isFillable(posx - 1, posy + 1):
      floodFill(posx - 1, posy + 1)
  if isFillable(posx + 1, posy - 1):
      floodFill(posx + 1, posy - 1)
  if isFillable(posx + 1, posy + 1):
      floodFill(posx + 1, posy + 1)

def isFillable(x, y):
  global grid
  if x >= 0 and x < AMOUNT and y >= 0 and y < AMOUNT:
    if grid[x][y].display == False:
      if grid[x][y].value == 0:
        return True
      elif grid[x][y].value != -1:
        grid[x][y].onclick()


#main game loop
gameOver = False
click = False
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0] == 1:
				pos = pygame.mouse.get_pos()
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				currentBox = grid[row][column]
				currentBox.onclick()
				if currentBox.value == 0:
					click = True
					position = [row, column]
				elif currentBox.value == -1:
					gameOver = True
			elif pygame.mouse.get_pressed()[2] == 1:
				pos = pygame.mouse.get_pos()
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				currentBox = grid[row][column]
				currentBox.placeFlag()


	if click == True:
		floodFill(position[0], position[1])
	click = False



	screen.fill(black)


	#------Draw Boxes
	for row in range(AMOUNT):
		for column in range(AMOUNT):
			currentBox = grid[row][column]
			currentBox.update(screen, row, column)

	if gameOver == True:
		for location in mineLocation:
			row = location[0]
			column = location[1]
			currentBox = grid[row][column]
			currentBox.onclick()
			currentBox.update(screen, row, column)


	pygame.display.update()
	clock.tick(60)

	if gameOver == True:
		run = False
		pygame.time.wait(1000)

pygame.quit()