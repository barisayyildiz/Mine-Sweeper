import pygame
from random import randint

pygame.init()

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



class Box():
	def __init__(self, xpos, ypos, width, height, margin):
		self.xpos = xpos
		self.ypos = ypos
		self.width = width
		self.height = height
		self.margin = margin

		self.font = pygame.font.Font('freesansbold.ttf', 20)

		self.value = 0
		self.copyValue = 0
		self.color = black
		self.display = False
	def update(self, screen, row, column):
		if self.display == False:
			color = white
		else:
			color = self.color

		pygame.draw.rect(screen, color, ((self.margin + self.width) * column + self.margin, (self.margin + self.height) * row + self.margin, self.width, self.height))

		try:
			if self.value > 0:
				#text operations
				text = self.font.render(str(self.value), True, white)
				textRect = text.get_rect()
				textRect.center = ((self.margin + self.width)*column + self.margin + self.width//2, (self.margin + self.height)*row + self.margin + self.height//2)
				screen.blit(text, textRect)
			elif self.value < 0 and self.display == True:
				#putting mine images
				imageRect = mine.get_rect()
				imageRect.center = ((self.margin + self.width)*column + self.margin + self.width//2, (self.margin + self.height)*row + self.margin + self.height//2)
				screen.blit(mine, imageRect)
		except TypeError:
			if self.value == "flag":
				#putting flag images
				imageRect = flag.get_rect()
				imageRect.center = ((self.margin + self.width)*column + self.margin + self.width//2, (self.margin + self.height)*row + self.margin + self.height//2)
				screen.blit(flag, imageRect)

		

	def copy(self):
		self.copyValue = self.value

	def onclick(self):
		if self.display == False:
			self.display = True

	def toggleFlag(self):
		if self.value != "flag":
			self.value = "flag"
		elif self.value == "flag":
			self.value = self.copyValue


	def incerease_value(self):
		#increases the value
		if self.value != -1:
			self.value += 1
			if self.value == 1:
				self.color = red
			elif self.value == 2:
				self.color = green
			elif self.value == 3:
				self.color = blue
			elif self.value == 4:
				self.color = yellow

		self.copyValue = self.value

	def place_mine(self):
		self.color = white
		self.value = -1
		self.copyValue = -1



"""
self value:
	1,2,3,4,5,6,7,8	=> number of mines at sides and corners
	0								=> empty
	-1							=> mine
	"flag"					=> flag

"""


#==================FUNCTIONS=======================#


def initializeGrid(AMOUNT, WIDTH, HEIGHT, MARGIN):
	grid = []

	for row in range(AMOUNT):
		grid.append([])
		for column in range(AMOUNT):
			grid[row].append(Box(row, column, WIDTH, HEIGHT, MARGIN))

	return grid

def placeMines(MINE_NUMBER, AMOUNT, grid):
	mineLocation = []

	#placing mines randomly
	for i in range(MINE_NUMBER):
		rndX = randint(0,AMOUNT-1)
		rndY = randint(0,AMOUNT-1)

		while grid[rndX][rndY].value == -1:
			rndX = randint(0,AMOUNT-1)
			rndY = randint(0,AMOUNT-1)

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


	return mineLocation, grid



#Flood Fill algorithm
#more information at https://en.wikipedia.org/wiki/Flood_fill
def floodFill(posx, posy, grid, AMOUNT):
  grid[posx][posy].onclick()
  if isFillable(posx - 1, posy, grid, AMOUNT):
      floodFill(posx - 1, posy, grid, AMOUNT)
  if isFillable(posx, posy - 1, grid, AMOUNT):
      floodFill(posx, posy - 1, grid, AMOUNT)
  if isFillable(posx + 1, posy, grid, AMOUNT):
      floodFill(posx + 1, posy, grid, AMOUNT)
  if isFillable(posx, posy + 1, grid, AMOUNT):
      floodFill(posx, posy + 1, grid, AMOUNT)

  if isFillable(posx - 1, posy - 1, grid, AMOUNT):
      floodFill(posx - 1, posy - 1, grid, AMOUNT)
  if isFillable(posx - 1, posy + 1, grid, AMOUNT):
      floodFill(posx - 1, posy + 1, grid, AMOUNT)
  if isFillable(posx + 1, posy - 1, grid, AMOUNT):
      floodFill(posx + 1, posy - 1, grid, AMOUNT)
  if isFillable(posx + 1, posy + 1, grid, AMOUNT):
      floodFill(posx + 1, posy + 1, grid, AMOUNT)

def isFillable(x, y, grid, AMOUNT):
	if x >= 0 and x < AMOUNT and y >= 0 and y < AMOUNT:
		if grid[x][y].display == False:
			if grid[x][y].value == 0:
				return True
			elif grid[x][y].value != -1:
				grid[x][y].onclick()


def message(beaten, screen, MARGIN, WIDTH, HEIGHT, AMOUNT):
	font = pygame.font.Font('freesansbold.ttf', 64)

	if beaten:
		string = "Well Done..."
	else:
		string = "Game Over..."

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		#fill the screen to black
		screen.fill(black)

		#set the text
		text = font.render(string, True, white)
		textRect = text.get_rect()
		textRect.center = ( ((MARGIN + WIDTH) * AMOUNT ) * 0.5, ((MARGIN + HEIGHT) * AMOUNT ) * 0.5 )
		
		#put the text on the screen
		screen.blit(text, textRect)

		#update the sreen
		pygame.display.update()



def gameLoop(AMOUNT, WIDTH, HEIGHT, MARGIN, MINE_NUMBER):
	
	pygame.init()
	clock = pygame.time.Clock()

	screen = pygame.display.set_mode((WIDTH * AMOUNT + (AMOUNT + 1) * MARGIN, HEIGHT * AMOUNT + (AMOUNT + 1) * MARGIN))



	#main game loop
	gameOver = False
	click = False
	run = True
	beaten = False			#game win or lose
	score = 0


	#initialize grid
	grid = initializeGrid(AMOUNT, WIDTH, HEIGHT, MARGIN)

	mineLocation, grid = placeMines(MINE_NUMBER, AMOUNT, grid)

	while run:
		#event loop
		for event in pygame.event.get():
			#exit condition
			if event.type == pygame.QUIT:
				run = False

			#left click
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


				#right click
				elif pygame.mouse.get_pressed()[2] == 1:
					pos = pygame.mouse.get_pos()
					column = pos[0] // (WIDTH + MARGIN)
					row = pos[1] // (HEIGHT + MARGIN)
					currentBox = grid[row][column]
					currentBox.toggleFlag()


					if currentBox.value == "flag" and currentBox.copyValue == -1:
						score += 1
					elif currentBox.value != "flag" and currentBox.copyValue == -1:
						score -= 1

					if score == MINE_NUMBER:
						gameOver = True
						beaten = True


		if click == True:
			floodFill(position[0], position[1], grid, AMOUNT)
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
			message(beaten, screen, MARGIN, WIDTH, HEIGHT, AMOUNT)

	pygame.quit()


