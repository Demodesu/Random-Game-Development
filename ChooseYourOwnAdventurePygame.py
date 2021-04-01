import math
import pygame
import random
#import button
#choose skill tree ex. enemy deal damage, what ever we predict we reduce the damage they deal

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panal = 150
screen_width = 800
screen_height = 400 + bottom_panal

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False
damagevalue = 0
rollevasion = -1
evasionchance = 0
randatk = 0
experiencethreshold = [5,10,20,40,80,160,320]

#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colors
red = (255,0,0)
green = (0,255,0)

#load image
#background image
background_img = pygame.image.load('Images/Background/Background.png').convert_alpha()
panal_img = pygame.image.load('Images/Icon/icon.png').convert_alpha()
sword_img = pygame.image.load('Images/Icon/Sword.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img,(200,200))
potion_img = pygame.image.load('Images/Icon/icon.png').convert_alpha()
#function for drawing background
def draw_bg():
	screen.blit(background_img, (0,-350))
#function for drawing panal
def draw_pn():
	#draw panel rectangle
	screen.blit(panal_img, (0,screen_height - bottom_panal))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panal + 10)
	draw_text(f'EXP: {knight.experience}', font, green, 20, screen_height - bottom_panal + 100)
	draw_text(f'LVL: {knight.level}', font, green, 20, screen_height - bottom_panal + 70)
	draw_text(f'STR: {knight.strength}', font, green, 120, screen_height - bottom_panal + 70)
	#damage values
	draw_text(f'{knight.name} deals {damagevalue} damage', font, red, (screen_width / 2) - 100, (screen_height - bottom_panal) / 2)
	if 0 < rollevasion < evasionchance:
		draw_text(f'{knight.name} misses and dealt 50% less damage!', font, red, (screen_width / 2) - 100, ((screen_height - bottom_panal) / 2) + 50 )
	elif rollevasion == -1:
		draw_text(f'{knight.name} is waiting to attack.', font, red, (screen_width / 2) - 100, ((screen_height - bottom_panal) / 2) + 50 )		
	else:
		draw_text(f'{knight.name} deals full damage!', font, red, (screen_width / 2) - 100, ((screen_height - bottom_panal) / 2) + 50 )
	for count, i in enumerate(bandit_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panal + 10) + count * 60)

#funtion for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x , y))

#classes
#button class
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
		
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions, luck, evasion, accuracy, experience, level):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.luck = luck
		self.evasion = evasion
		self.accuracy = accuracy
		self.potions = potions
		self.experience = experience
		self.level = level
		self.alive = True
		self.animation_list = []
		self.framge_index = 0
		self.action = 0 #0 = idle, 1 = attack, 2 = hurt, 3 = dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(4):
			img = pygame.image.load(f'Images/{self.name}/Idle/{i}.png').convert_alpha() #still image
			img = pygame.transform.scale(img, (300, 300))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(5):
			img = pygame.image.load(f'Images/{self.name}/Attack/{i}.png').convert_alpha() #still image
			img = pygame.transform.scale(img, (300, 300))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.framge_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.framge_index]
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.framge_index += 1
		#if animation runs out then reset to the start
		if self.framge_index >= len(self.animation_list[self.action]):
			self.idle()

	def idle(self):
		#set variables to attack animation
		self.action = 0
		self.framge_index = 0
		self.update_time = pygame.time.get_ticks()		

	def attack(self, target):
		global damagevalue
		global evasionchance
		global rollevasion
		global randatk
		#deal damage to enemy
		evasionformula = math.log(100 + self.luck, target.accuracy)
		evasionchance = evasionformula * 10
		rollevasion = random.randint(0 , 100)
		if self.luck > 10:
			randatk = random.randint(0, self.luck)			
		else:
			randatk = random.randint(self.luck - 5, self.luck)				
		randeva = evasionchance / 100
		damage = self.strength + randatk
		#attack formula
		if 0 < rollevasion < evasionchance:
			target.hp -= damage * 0.5
			if current_fighter == 1:
				damagevalue = damage * 0.5
		else:
			target.hp -= damage
			if current_fighter == 1:
				damagevalue = damage

		#check if dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
		#set variables to attack animation
		self.action = 1
		self.framge_index = 0
		self.update_time = pygame.time.get_ticks()

	def draw(self):
		screen.blit(self.image, self.rect)

class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

knight = Fighter(200, 350, 'Hero1', 40, 10, 3, 5, 3, 2, 0, 0)
bandit1 = Fighter(550, 380, 'Enemy1', 20, 6, 1, 2, 2, 2, 5, 1)
bandit2 = Fighter(700, 380, 'Enemy1', 20, 6, 1, 2, 2, 2, 5, 1)
bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panal + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panal + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panal + 100, bandit2.hp, bandit2.max_hp)

#create buttons
#potion_button = button.Button(screen, 100, screen_height - bottom_panal + 70, potion_img, 64, 64)

run = True
while run:

	clock.tick(fps)
	#draw background
	draw_bg()
	#draw panal
	draw_pn()
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)
	#draw fighter
	knight.update()
	knight.draw()

	#control player actions
	#reset action variables
	attack = False
	potion = False
	target = None

	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, bandit in enumerate(bandit_list):
		if bandit.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword in place
			screen.blit(sword_img, pos)
			if clicked == True:
				attack = True
				target = bandit_list[count]

	#draw bandit
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()

	#player action
	if knight.alive == True:
		knight.strength = 10 + ((knight.level * 5) / 2)
		for levels in range(len(experiencethreshold)):
			if knight.experience >= experiencethreshold[levels]:
				knight.level = levels + 1
		if current_fighter == 1:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#look for player action
				#attack
				if attack == True and target != None and target.alive == True:
					knight.attack(target)
					if target.alive == False:
						knight.experience += target.experience
					current_fighter += 1
					action_cooldown 
		else:
			current_fighter += 1

	#if all fighters have a turn then reset
	if current_fighter > total_fighters:
		current_fighter = 1

	#enemy action
	for count, bandit in enumerate(bandit_list):
		if current_fighter == 2 + count:
			if bandit.alive == True:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#attack
					bandit.attack(knight)
					current_fighter += 1
					action_cooldown = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False
	pygame.display.update()

pygame.quit()