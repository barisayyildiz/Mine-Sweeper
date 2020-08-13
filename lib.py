import pygame

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

font = pygame.font.Font('freesansbold.ttf', 20)

class Box():
	def __init__(self, xpos, ypos, width, height, margin):
		self.xpos = xpos
		self.ypos = ypos
		self.width = width
		self.height = height
		self.margin = margin

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
				text = font.render(str(self.value), True, white)
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
