import math
import pygame
import random

pygame.init()
#set framerate
clock = pygame.time.Clock()
fps = 60
#game window#
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')
#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potions = False
mana_potion = False
mana_potion_effect = 5
potion_effect = 15
clicked = False
game_over = 0
experiencethreshold = [5]
equipment_state = 0
ring_of_health_active = False
raptor_claw_active = False
four_leaf_clover_active = False
feather_active = False
leather_active = False
#fonts
font = pygame.font.SysFont('Minecraft', 26)
potion_font = pygame.font.SysFont('Minecraft', 20)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
#load assets#
background_img = pygame.image.load('Images/Background/Background.png')
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png')
sword_img = pygame.image.load('Images/Icon/SwordButton.png')
potion_img = pygame.image.load('Images/Icon/PotionButton.png')
mana_potion_img = pygame.image.load('Images/Icon/PotionButtonMana.png')
victory_img = pygame.image.load('Images/Icon/Victory.png')
defeat_img = pygame.image.load('Images/Icon/Defeat.png')
reset_img = pygame.image.load('Images/Icon/Reset.png')
statbutton_img = pygame.image.load('Images/Icon/StatButton.png')
fireballskill_img = pygame.image.load('Images/Icon/Fireball/Fireballskill.png')
healskill_img = pygame.image.load('Images/Icon/Heal/HealButton.png')
ring_of_health_img = pygame.image.load('Images/Icon/Relics/Relic0.png')
ring_of_health_img = pygame.transform.scale(ring_of_health_img,(100,100))
raptor_claw_img = pygame.image.load('Images/Icon/Relics/Relic1.png')
raptor_claw_img = pygame.transform.scale(raptor_claw_img ,(100,100))
four_leaf_clover_img = pygame.image.load('Images/Icon/Relics/Relic2.png')
four_leaf_clover_img = pygame.transform.scale(four_leaf_clover_img ,(70,70))
feather_img = pygame.image.load('Images/Icon/Relics/Relic3.png')
feather_img = pygame.transform.scale(feather_img ,(70,70))
#functions#
# class draw_fireball():
# 	def __init__(self, x, y, name):
# 		self.name = name
# 		self.animation_list = []
# 		self.frame_index = 0
# 		self.update_time = pygame.time.get_ticks()
# 		for i in range(10):
# 			img = pygame.image.load(f'Images/Icon/Fireball/{i}.png')
# 			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
# 			self.animation_list.append(img)
# 		self.image = self.animation_list[self.frame_index]
# 		self.rect = self.image.get_rect()
# 		self.rect.center = (x,y)

# 	def update(self):
# 		animation_cooldown = 100
# 		#handle animation
# 		#update image
# 		self.image = self.animation_list[self.frame_index]
# 		#check if enough time has passes
# 		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
# 			self.update_time = pygame.time.get_ticks()
# 			self.frame_index += 1
# 		#if animation runs our then reset
# 		if self.frame_index >= len(self.animation_list):
# 			self.frame_index = 0

# 	def draw(self):
# 		screen.blit(self.image, self.rect)

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#drawing background
def draw_bg():
	screen.blit(background_img, (0,0))

#drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img,(0,screen_height - bottom_panel))
	#show knight stats
	draw_text(f'HP: {hero.hp}', font, red, 20, screen_height - bottom_panel + 20)
	draw_text(f'MP: {hero.mana}', font, red, 160, screen_height - bottom_panel + 20)	
	draw_text(f'EXP: {hero.experience}', font, red, 90-35, screen_height - bottom_panel + 70)
	draw_text(f'STAT: {hero.statpoints}', font, red, 180-35, screen_height - bottom_panel + 70)
	draw_text(f'LVL: {hero.level}', font, red, 320, screen_height - bottom_panel + 20)	
	draw_text(f'STR: {hero.strength}', font, red, 320, screen_height - bottom_panel + 40)	
	draw_text(f'LUC: {hero.luck}', font, red, 320, screen_height - bottom_panel + 60)	
	draw_text(f'ACC: {hero.accuracy}', font, red, 320, screen_height - bottom_panel + 80)	
	draw_text(f'EVA: {hero.evasion}', font, red, 320, screen_height - bottom_panel + 100)
	draw_text(f'DEF: {hero.defense}', font, red, 320, screen_height - bottom_panel + 120)

	#draw relics
	if ring_of_health_active == True:
		screen.blit(ring_of_health_img,(700,0))
	if raptor_claw_active == True:
		screen.blit(raptor_claw_img,(620,0))
	if four_leaf_clover_active == True:
		screen.blit(four_leaf_clover_img,(540+20,10))
	if feather_active == True:
		screen.blit(feather_img,(460+30,10))
	#show slime stats	
	for count, i in enumerate(slime_list):
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 20) + count * 60)	
		draw_text(f'LVL: {i.level}', font, red, 440, (screen_height - bottom_panel + 20) + count * 60)

#fighter class
class fighter():
	def __init__(self, x, y, name, max_hp, strength, potions, level, experience, luck, evasion, accuracy, statpoints, max_mana, defense, mana_potion):
		#global variables
		global equipment_state
		self.name = name
		#hp
		self.start_max_hp = max_hp
		self.max_hp = max_hp
		self.hp = max_hp
		#mana
		self.start_max_mana = max_mana
		self.max_mana = max_mana
		self.mana = max_mana
		#stats and potions
		self.start_luck = luck
		self.start_potions = potions
		self.start_accuracy = accuracy
		self.start_evasion = evasion
		self.start_strength = strength
		self.start_defense = defense
		self.start_mana_potion = mana_potion
		self.strength = strength
		self.luck = luck
		self.evasion = evasion
		self.accuracy = accuracy
		self.potions = potions
		self.defense = defense
		self.mana_potion = mana_potion
		#experience level and stats
		self.start_experience = experience
		self.start_level = level
		self.experience = experience
		self.level = level
		self.start_statpoints = statpoints
		self.statpoints = statpoints
		#alive
		self.alive = True
		#animation
		self.animation_list = []
		self.animation_list_leather = []
		self.equipment_state = 0
		self.frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills
		self.update_time = pygame.time.get_ticks()
		#-------------------------------------------naked-------------------------------------------#
		#index 0 = idle
		temp_list = []
		for i in range(4):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/{self.name}/Idle/{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/{self.name}/Idle/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)				
		self.animation_list.append(temp_list)
		#index 1 = attack
		temp_list = []
		for i in range(5):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/{self.name}/Attack/{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/{self.name}/Attack/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list.append(temp_list)
		#index 2 = hurt
		temp_list = []
		for i in range(3):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/{self.name}/Hurt/{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/{self.name}/Hurt/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list.append(temp_list)
		#index 3 = death
		temp_list = []
		for i in range(5):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/{self.name}/Death/{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/{self.name}/Death/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list.append(temp_list)
		#index 4 = skills
		temp_list = []
		for i in range(5):
			img = pygame.image.load(f'Images/Hero/Skill/Fireball/{i}.png')
			img = pygame.transform.scale(img,(250 ,250))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#-------------------------------------------leather-------------------------------------------#
		#index 0 = idle
		temp_list = []
		for i in range(4):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/Hero/Idle/L{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/Slime/Idle/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list_leather.append(temp_list)		
		#index 1 = attack
		temp_list = []
		for i in range(5):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/Hero/Attack/L{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/Slime/Attack/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)
		self.animation_list_leather.append(temp_list)
		#index 2 = hurt
		temp_list = []
		for i in range(3):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/Hero/Hurt/L{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/Slime/Hurt/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list_leather.append(temp_list)
		#index 3 = death
		temp_list = []
		for i in range(5):
			if self.name == 'Hero':
				img = pygame.image.load(f'Images/Hero/Death/L{i}.png')
				img = pygame.transform.scale(img,(250,250))
				temp_list.append(img)
			elif self.name == 'Slime':
				img = pygame.image.load(f'Images/Slime/Death/{i}.png')
				img = pygame.transform.scale(img,(80,80))
				temp_list.append(img)	
		self.animation_list_leather.append(temp_list)
		#index 4 = skills
		temp_list = []
		for i in range(5):
			img = pygame.image.load(f'Images/Hero/Skill/Fireball/L{i}.png')
			img = pygame.transform.scale(img,(250 ,250))
			temp_list.append(img)
		self.animation_list_leather.append(temp_list)		
		#-------------------------------------------change equipment-------------------------------------------#
		if self.equipment_state == 0:
			self.image = self.animation_list[self.action][self.frame_index]
		elif self.equipment_state == 1:
			self.image = self.animation_list_leather[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		#handle animation
		#update image
		if equipment_state == 0:
			self.image = self.animation_list[self.action][self.frame_index]	
		elif equipment_state == 1:
			self.image = self.animation_list_leather[self.action][self.frame_index]				
		#check if enough time has passes since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if animation runs out reset to the start
		if equipment_state == 0:
			if self.frame_index >= len(self.animation_list[self.action]):
				if self.action == 3:
					self.frame_index = len(self.animation_list[self.action]) - 1
				else:
					self.idle()
		elif equipment_state ==1:
			if self.frame_index >= len(self.animation_list_leather[self.action]):
				if self.action == 3:
					self.frame_index = len(self.animation_list_leather[self.action]) - 1
				else:
					self.idle()

	#actions

	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()		

	def attack(self, target):
		#luck damage factor
		if self.luck <= 10:
			luckfactor = self.luck
			randdamage = (random.randint(-10 + math.floor(luckfactor), math.floor(luckfactor))) / 2
		elif self.luck > 10:
			luckfactor = self.luck / 2
			randdamage = (random.randint(0, 5 + math.floor(luckfactor))) / 2 
		#miss attack or not, miss percentage is the attacker's chance to miss
		#miss factor is the attacker's accuracy - the target's evasion
		#if the target has a lot of evasion, the more chance the attacker will miss the attack
		#roll for evasion -> if the roll is less than the attacker's miss percentage, the damage will the attacker deals will be reduced
		#luck from both the target and the attacker determines the roll for evasion too
		#if the attacker has more luck than the target, the value will be positive, which increases the attackers chance to not miss

		#for example, if the attacker's strength is 12 and he rolls a randdamage  of -3.5. He calculates the miss percentage to be 6 and rolls the miss to be a -4, this he deals (12 - 3.5) * 0.75 damage
		missfactor = self.accuracy - (target.evasion * 2)
		if missfactor < 0:
			misschance = (missfactor * 2) * - 1
		else:
			misschance = 0
		rollmisschance = random.randint(0,100) + (self.luck - target.luck)
		if rollmisschance < misschance:
			damage = (self.strength + randdamage) * 0.75
		else:
			#critical damage
			criticalchance = (self.accuracy * 2) + self.luck - target.evasion
			rollcriticalchance = random.randint(0,100)
			if self.accuracy + self.luck > target.evasion:
				if criticalchance > rollcriticalchance:
					damage = (self.strength + randdamage) * 1.5
				else:
					damage = self.strength + randdamage	
			else:
				damage = self.strength + randdamage

		#deal damage to enemy			
		target.hp -= (damage - self.defense)
		#run target hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		if target.name == 'Hero':
			#damage text
			damage_text = damagetext(target.rect.centerx - 25, target.rect.y + 80, str(damage), red)
			damage_text_group.add(damage_text)
			#evasion text
			if rollmisschance < misschance:
				damage_text = damagetext(target.rect.centerx - 25, target.rect.y + 100, 'Evaded(' + str(misschance) + ')% chance', red)
				damage_text_group.add(damage_text)
			elif rollmisschance > misschance and criticalchance < rollcriticalchance:
				damage_text = damagetext(target.rect.centerx - 25, target.rect.y + 100, 'Full damage', red)
				damage_text_group.add(damage_text)
			else:
				damage_text = damagetext(target.rect.centerx - 25, target.rect.y + 100, 'Critical(' + str(criticalchance) + ')% chance', red)
				damage_text_group.add(damage_text)							
		if target.name == 'Slime':
			damage_text = damagetext(target.rect.centerx, target.rect.y, str(damage), red)
			damage_text_group.add(damage_text)
			if rollmisschance < misschance:
				damage_text = damagetext(target.rect.centerx, target.rect.y + 20, 'Evaded(' + str(misschance) + ')% chance', red)
				damage_text_group.add(damage_text)
			elif rollmisschance > misschance and criticalchance < rollcriticalchance:
				damage_text = damagetext(target.rect.centerx, target.rect.y + 20, 'Full damage', red)
				damage_text_group.add(damage_text)	
			else:
				damage_text = damagetext(target.rect.centerx, target.rect.y + 20, 'Critical(' + str(criticalchance) + ')% chance', red)
				damage_text_group.add(damage_text)		
	
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def death(self):
		#set variables to hurt animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#drop items
	def drop_items(self):
		global ring_of_health_active
		global raptor_claw_active
		global four_leaf_clover_active
		global feather_active
		global leather_active

		if self.alive == False:
			if self.level > 0:
				if ring_of_health_active == False:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 50:
						ring_of_health_active = True
						hero.max_hp += 5
						hero.hp += 5
			if self.level > 1:
				if raptor_claw_active == False:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						raptor_claw_active = True
						hero.strength += 5
			if self.level > 1:
				if four_leaf_clover_active == False:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						four_leaf_clover_active = True
						hero.luck += 2
			if self.level > 0:
				if feather_active == False:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 50:
						feather_active = True
						hero.evasion += 2
			if self.level > 0:
				if leather_active == False:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 80:
						leather_active = True

	#resets
	def resetdefeat(self):
		global experiencethreshold
		self.alive = True
		experiencethreshold = [5]
		while True:
			start_random_integer = 35
			start_random_strength = random.randint(10, 15)
			start_random_accuracy = random.randint(0, 10)
			start_random_evasion = random.randint(0, 10)
			start_random_luck = random.randint(0, 10)
			if start_random_integer -5 < start_random_luck + start_random_evasion + start_random_accuracy + start_random_strength < start_random_integer:
				break
		self.potions = self.start_potions
		self.mana_potion = self.start_mana_potion
		self.max_hp = self.start_max_hp
		self.max_mana = self.start_max_mana
		self.hp = self.max_hp
		self.mana = self.max_mana
		self.strength = start_random_strength
		self.accuracy = start_random_accuracy
		self.luck = start_random_luck
		self.evasion = start_random_evasion
		self.experience = self.start_experience
		self.level = self.start_level
		self.statpoints = self.start_statpoints
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def resetvictory(self):
		self.alive = True
		self.potions = self.potions
		self.mana_potion = self.mana_potion
		self.hp = self.hp
		if self.mana <= self.max_mana - 5:
			self.mana += 5
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def resetmonsterdefeat(self):
		self.alive = True
		self.max_hp = self.start_max_hp
		self.max_mana = self.start_max_mana
		self.hp = self.max_hp
		self.potions = self.start_potions
		self.strength = self.start_strength
		self.accuracy = self.start_accuracy
		self.luck = self.start_luck
		self.evasion = self.start_evasion
		self.level = self.start_level
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def resetmonstervictory(self):
		self.alive = True
		self.potions = self.start_potions
		self.max_hp += 2
		self.hp = self.max_hp
		self.strength += 1
		self.accuracy += 1
		self.evasion += 1
		self.level += 1
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	#draw
	def draw(self):
		screen.blit(self.image, self.rect)

	#skills
	def fireball(self, target):
		fireballdamage = self.strength * 2
		target.hp -= fireballdamage
		hero.mana -= 5
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = damagetext(target.rect.centerx, target.rect.y, str(fireballdamage), red)
		damage_text_group.add(damage_text)
		#draw fireball img	
		fireball_draw = draw_fireball(target.rect.centerx, target.rect.y)
		fireball_img_group.add(fireball_draw)		
		#set variables to skill animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def heal(self):
		heal_spell_effect = 5 + (hero.max_hp / 2)
		if hero.max_hp - hero.hp > heal_spell_effect:
			heal_spell_amount = heal_spell_effect
		else:
			heal_spell_amount = hero.max_hp - hero.hp
		hero.hp += heal_spell_amount
		hero.mana -= 5
		damage_text = damagetext(self.rect.centerx -25, self.rect.y + 100, str(heal_spell_amount), green)
		damage_text_group.add(damage_text)
		#draw fireball img	
		heal_draw = draw_heal(self.rect.centerx -25, self.rect.y + 150)
		heal_img_group.add(heal_draw)		
		#set variables to skill animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

#draw heal
class draw_heal(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(4):
			img = pygame.image.load(f'Images/Icon/Heal/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.frame_index]	
		#check if enough time has passes since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if animation runs out reset to the start
		if self.frame_index >= len(self.animation_list):
			self.kill()

#draw fireball
class draw_fireball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 5
		self.update_time = pygame.time.get_ticks()	
		for i in range(10):
			img = pygame.image.load(f'Images/Icon/Fireball/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.frame_index]	
		#check if enough time has passes since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if animation runs out reset to the start
		if self.frame_index >= len(self.animation_list):
			self.kill()

#healthbar class
class healthbar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp
	def draw(self, hp):
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 130, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 130 * ratio, 20))	

#manabar class
class manabar():
	def __init__(self, x, y, mana, max_mana):
		self.x = x
		self.y = y
		self.mana = mana
		self.max_mana = max_mana
	def draw(self, mana):
		self.mana = mana
		#calculate mana ratio
		ratio = self.mana / self.max_mana
		pygame.draw.rect(screen, red, (self.x, self.y, 130, 20))
		pygame.draw.rect(screen, blue, (self.x, self.y, 130 * ratio, 20))	

#exp class
class expbar():
	def __init__(self, x, y, experience):
		self.x = x
		self.y = y
		self.experience = experience
	def draw(self, experience):
		self.experience = experience
		#calculate exp ratio
		ratio = self.experience / experiencethreshold[-1]
		pygame.draw.rect(screen, red, (self.x, self.y, 800, 14))
		pygame.draw.rect(screen, yellow, (self.x, self.y, 800 * ratio, 14))	

#button class
class button():
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

#damage text
class damagetext(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, color)
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0

	def update(self):
		#float damage text up
		self.rect.y -= 1
		#delete text after few counters
		self.counter += 1
		if self.counter > 50:
			self.kill()

#instances
damage_text_group = pygame.sprite.Group()
fireball_img_group = pygame.sprite.Group()
heal_img_group = pygame.sprite.Group()

#random starting stats
while True:
	start_random_integer = 35
	start_random_strength = random.randint(10, 15)
	start_random_accuracy = random.randint(0, 10)
	start_random_evasion = random.randint(0, 10)
	start_random_luck = random.randint(0, 10)
	if start_random_integer -5 < start_random_luck + start_random_evasion + start_random_accuracy + start_random_strength < start_random_integer:
		break

#hero
#(self, x, y, name, max_hp, strength, potions, level, experience, luck, evasion, accuracy, statpoints, max_mana)
hero = fighter(200, 265, 'Hero', 50, start_random_strength, 3, 1, 0, start_random_luck, start_random_evasion, start_random_accuracy, 0, 15, 0, 2)

#slime
slime1 = fighter(530, 350, 'Slime', 5, 8, 1, 1, 5, 5, 8, 8, 0, 0, 0, 0)
slime2 = fighter(650, 350, 'Slime', 15, 8, 1, 1, 5, 5, 8, 8, 0, 0, 0, 0)
slime_list = []
slime_list.append(slime1)
slime_list.append(slime2)

#button
potion_button = button(screen, 18, screen_height - bottom_panel + 65, potion_img, 32, 32)
mana_potion_button = button(screen, 18, screen_height - bottom_panel + 100, mana_potion_img, 32, 32)
restart_button = button(screen, 330, 120, reset_img, 120, 30)
statbutton_button_str = button(screen, 120-60, screen_height - bottom_panel + 110, statbutton_img, 24, 24)
statbutton_button_evasion = button(screen, 160-60, screen_height - bottom_panel + 110, statbutton_img, 24, 24)
statbutton_button_accuracy = button(screen, 200-60, screen_height - bottom_panel + 110, statbutton_img, 24, 24)
statbutton_button_luck = button(screen, 240-60, screen_height - bottom_panel + 110, statbutton_img, 24, 24)
fireballskill_button = button(screen, 18, 10, fireballskill_img, 64, 64)
healskill_button = button(screen, 100, 10, healskill_img, 64, 64)
change_to_leather = button(screen, 182, 10, statbutton_img, 64, 64)

#cast costs
fireballcastcost = 5
healcastcost = 5
#pause states
UNPAUSE, PAUSE = 0, 1
state = UNPAUSE

#game#
run = True
while run:

	#how fast the game runs
	clock.tick(fps)

	#put slime healthbar inside the run as to update it everytime reset victory increases max hp of slime
	slime1_health_bar = healthbar(550, screen_height - bottom_panel + 40, slime1.hp, slime1.max_hp)
	slime2_health_bar = healthbar(550, screen_height - bottom_panel + 100, slime2.hp, slime2.max_hp)

	#healthbar
	hero_health_bar = healthbar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
	hero_mana_bar = manabar(160, screen_height - bottom_panel + 40, hero.mana, hero.max_mana)
	hero_exp_bar = expbar(0, screen_height - bottom_panel, hero.experience)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	hero_health_bar.draw(hero.hp)
	hero_mana_bar.draw(hero.mana)
	hero_exp_bar.draw(hero.experience)
	slime1_health_bar.draw(slime1.hp)
	slime2_health_bar.draw(slime2.hp)

	#draw fighters
	hero.update()
	hero.draw()

	#control player actions
	#reset action variables
	attack = False
	potions = False
	target = None

	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, slime in enumerate(slime_list):
		if slime.rect.collidepoint(pos):
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, pos)
			if clicked == True and slime.alive == True:
				attack = True
				target = slime_list[count]

	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)
	#draw fireball
	fireball_img_group.update()
	fireball_img_group.draw(screen)
	#draw heal
	heal_img_group.update()
	heal_img_group.draw(screen)
	#use potion button
	potion_button.draw()
	mana_potion_button.draw()

	#increase stats
	if hero.statpoints > 0:
		draw_text(f'STR', font, red, 115-60, screen_height - bottom_panel + 90)
		draw_text(f'EVA', font, red, 155-60, screen_height - bottom_panel + 90)
		draw_text(f'ACC', font, red, 195-60, screen_height - bottom_panel + 90)
		draw_text(f'LUC', font, red, 235-60, screen_height - bottom_panel + 90)
		if statbutton_button_str.draw():
			hero.statpoints -= 1
			hero.strength += 1
		if statbutton_button_luck.draw():
			hero.statpoints -= 1
			hero.luck += 1
		if statbutton_button_accuracy.draw():
			hero.statpoints -= 1
			hero.accuracy += 1
		if statbutton_button_evasion.draw():
			hero.statpoints -= 1
			hero.evasion += 1

	#show number of potions remaining
	draw_text(str(hero.potions), potion_font, red, 40, screen_height - bottom_panel + 68)
	draw_text(str(hero.mana_potion), potion_font, red, 40, screen_height - bottom_panel + 103)

	#draw slime
	for slime in slime_list:
		slime.update()
		slime.draw()

	if state == UNPAUSE:
		if game_over == 0:
			#player action
			if hero.alive == True:
				if current_fighter == 1:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:

						#auto potion when it's your turn
						if hero.potions > 0 and hero.hp < hero.max_hp / 2:
							#check if potion would heal beyond max health
							if hero.max_hp - hero.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = hero.max_hp - hero.hp
							hero.hp += heal_amount
							hero.potions -= 1
							damage_text = damagetext(hero.rect.centerx - 25, hero.rect.y + 80, str(heal_amount), green)
							damage_text_group.add(damage_text)

						#auto mana potion when it's your turn
						if hero.mana_potion > 0 and hero.mana < 10:
							restore_amount = mana_potion_effect
							hero.mana += restore_amount
							hero.mana_potion -= 1
							damage_text = damagetext(hero.rect.centerx - 25, hero.rect.y + 120, str(restore_amount), blue)
							damage_text_group.add(damage_text)

						#look for player action
						#attack
						if attack == True and target != None:
							hero.attack(target)
							if target.alive == False:
								hero.experience += target.experience
							target.drop_items()
							current_fighter += 1
							action_cooldown = 0

						#fireball
						if hero.mana >= fireballcastcost:
							if fireballskill_button.draw():
								if hero.mana >= 10:
									for count, slime in enumerate(slime_list):
										target = slime
										if target.alive == True:
											hero.fireball(target)
											if target.alive == False:
												hero.experience += target.experience
											target.drop_items()
										current_fighter += 1
										action_cooldown = 0
								elif hero.mana == 5:
									target = slime1
									if target.alive == False:
										target = slime2
									hero.fireball(target)
									if target.alive == False:
										hero.experience += target.experience
									target.drop_items()
									current_fighter += 1
									action_cooldown = 0

						#heal
						if hero.mana >= healcastcost:
							if healskill_button.draw():
								hero.heal()
								current_fighter += 1
								action_cooldown = 0

						#change equipment
						if leather_active == True:
							if change_to_leather.draw():
								if equipment_state == 1:
									equipment_state = 0
								else:
									equipment_state += 1
								if equipment_state == 1:
									hero.defense = 5
								elif equipment_state == 0:
									hero.defense = 0

						#level up
						for length in range(len(experiencethreshold)):
							if hero.experience >= experiencethreshold[-1]:
								hero.level += 1
								nextexperience = experiencethreshold[-1] * 3 # or experiencethreshold[0]
								experiencethreshold.append(nextexperience)
								hero.statpoints += 5
								hero.max_mana += 5

			else:
				game_over = -1

			#enemy action
			for count, slime in enumerate(slime_list):
				if current_fighter == 2 + count:
					if slime.alive == True:
						action_cooldown += 1
						if action_cooldown >= action_wait_time:
							#check if bandit needs heal
							if (slime.hp / slime.max_hp) < 0.5 and slime.potions > 0:
								#check if the potion would heal more than max hp
								if slime.max_hp - slime.hp > potion_effect:
									heal_amount = potion_effect
								else:
									heal_amount = slime.max_hp - slime.hp
								slime.hp += heal_amount
								slime.potions -= 1
								damage_text = damagetext(slime.rect.centerx, slime.rect.y, str(heal_amount), green)
								damage_text_group.add(damage_text)
								current_fighter += 1
								action_cooldown = 0
							else:					
								#attack
								slime.attack(hero)
								current_fighter += 1
								action_cooldown = 0
					else:
						current_fighter += 1

			#if all fighters have had a turn
			if current_fighter > total_fighters:
				current_fighter = 1

		#check if all slimes are dead
		alive_slime = 0
		for slime in slime_list:
			if slime.alive == True:
				alive_slime += 1
		if alive_slime == 0:
			game_over = 1

		#check if game is over
		if game_over != 0:
			if game_over == 1:
				screen.blit(victory_img, (250, 50))
				if restart_button.draw():
					hero.resetvictory()
					for slime in slime_list:
						slime.resetmonstervictory()
					current_fighter = 1
					action_cooldown = 0
					game_over = 0
			if game_over == -1:
				screen.blit(defeat_img, (250, 50))
				if restart_button.draw():
					hero.resetdefeat()
					ring_of_health_active = False
					raptor_claw_active = False
					four_leaf_clover_active = False
					feather_active = False

					for slime in slime_list:
						slime.resetmonsterdefeat()
					current_fighter = 1
					action_cooldown = 0
					game_over = 0

	#if p is pressed, pause
	if state == PAUSE:
		pause_button = pygame.Rect(260,270,100,25)
		pygame.draw.rect(screen, (255,0,0), pause_button)
		draw_text('PAUSED', font, (255,255,255), 275, 275)
		pygame.display.flip()

	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				state = PAUSE
			if event.key == pygame.K_o:
				state = UNPAUSE

	pygame.display.update()

pygame.quit()
