import pygame, math, random, sys

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

#bar
class Bar():
	def __init__(self, screen):
		self.screen = screen

class Health_Bar(Bar):
	def __init__(self, x, y, hp, max_hp):
		super().__init__(screen)
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp, max_hp):
		self.hp = hp
		self.max_hp = max_hp
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 130, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 130 * ratio, 20))	


class Mana_Bar(Bar):
	def __init__(self, x, y, mp, max_mp):
		super().__init__(screen)
		self.x = x
		self.y = y
		self.mp = mp
		self.max_mp = max_mp

	def draw(self, mp, max_mp):
		self.mp = mp
		self.max_mp = max_mp
		ratio = self.mp / self.max_mp
		pygame.draw.rect(screen, red, (self.x, self.y, 130, 20))
		pygame.draw.rect(screen, blue, (self.x, self.y, 130 * ratio, 20))	
		
class Experience_Bar(Bar):
	def __init__(self, x, y):
		super().__init__(screen)
		self.x = x
		self.y = y

	def draw(self, experience, experiencethreshold = None):
		self.experience = experience
		if experiencethreshold is None:
			self.experiencethreshold = []
		else:
			self.experiencethreshold = experiencethreshold
		ratio = self.experience / self.experiencethreshold[-1]
		pygame.draw.rect(screen, red, (self.x, self.y, 800, 14))
		pygame.draw.rect(screen, yellow, (self.x, self.y, 800 * ratio, 14))

class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action