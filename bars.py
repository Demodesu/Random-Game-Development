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

	def Draw(self, hp):
		self.hp = hp
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

	def Draw(self):
		ratio = self.mp / self.max_mp
		pygame.draw.rect(screen, red, (self.x, self.y, 130, 20))
		pygame.draw.rect(screen, blue, (self.x, self.y, 130 * ratio, 20))	
		
class Experience_Bar(Bar):
	def __init__(self, x, y, experience, experiencethreshold = None):
		super().__init__(screen)
		self.x = x
		self.y = y
		self.experience = experience
		if experiencethreshold is None:
			self.experiencethreshold = []
		else:
			self.experiencethreshold = experiencethreshold

	def Draw(self):
		ratio = self.experience / self.experiencethreshold[-1]
		pygame.draw.rect(screen, red, (self.x, self.y, 800, 14))
		pygame.draw.rect(screen, yellow, (self.x, self.y, 800 * ratio, 14))