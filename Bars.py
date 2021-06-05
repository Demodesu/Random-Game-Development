import math, pygame, random, sys, ctypes

#-------------------------------------------------------------------------------------#
#all screen elements
#ratio is 16:9
def width(width_ratio):
	calculated = screen_width * width_ratio
	calculated = math.ceil(calculated)
	return calculated

def height(height_ratio):
	calculated = screen_width * height_ratio
	calculated = math.ceil(calculated)
	return calculated

def width_position(width_ratio):
	calculated = screen_width * width_ratio
	calculated = math.ceil(calculated)
	return calculated

def height_position(height_ratio):
	calculated = screen_height * height_ratio
	calculated = math.ceil(calculated)
	return calculated

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.25)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

banner_image = pygame.image.load('Images/Icon/Banners.png').convert_alpha()

def draw_text_middle_and_box(text, font, text_col, rect_col, x, y, image):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	text_image = font.render(text, True, text_col)
	image = pygame.transform.scale(image, (font_size[0] + 20, font_size[1] + 20))
	choice_text = screen.blit(text_image, (x + 10, y + 10))
	choice_image = screen.blit(image, (x, y))
	
	return choice_image, choice_text

def draw_box(image, rect):
	image = pygame.transform.scale(image, (rect.width, rect.height))
	choice_image = screen.blit(image, (rect.x, rect.y))

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
		pygame.draw.rect(screen, red, (self.x, self.y, width(0.3), 20))
		pygame.draw.rect(screen, green, (self.x, self.y, width(0.3) * ratio, 20))	


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
		pygame.draw.rect(screen, red, (self.x, self.y, width(0.3), 20))
		pygame.draw.rect(screen, blue, (self.x, self.y, width(0.3) * ratio, 20))	
		
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
		pygame.draw.rect(screen, red, (self.x, self.y, screen_width, 14))
		experience_rect = pygame.rect.Rect(self.x, self.y, screen_width * ratio, 14)
		draw_box(banner_image, experience_rect)

class Shield_Bar(Bar):
	def __init__(self, x, y):
		super().__init__(screen)
		self.x = x
		self.y = y

	def draw(self, shield, max_hp):
		self.shield = shield
		self.max_hp = max_hp
		ratio = self.shield / self.max_hp
		pygame.draw.rect(screen, yellow, (self.x, self.y, width(0.3) * ratio, 20))

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