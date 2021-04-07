import pygame, math, random, sys

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))

class Character():
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion):
		#defaults
		self.x = x
		self.y = y
		self.name = name
		#hp
		self.start_max_hp = max_hp
		self.max_hp = max_hp
		self.hp = max_hp
		#mana
		self.start_max_mp = max_mp
		self.max_mp = max_mp
		self.mp = max_mp
		#start stats 
		self.start_strength = strength
		self.start_intelligence = intelligence
		self.start_defense = defense
		self.start_luck = luck
		self.start_evasion = evasion
		self.start_accuracy = accuracy
		#current stats
		self.strength = strength
		self.intelligence = intelligence
		self.defense = defense
		self.luck = luck
		self.evasion = evasion
		self.accuracy = accuracy
		#start level and experience
		self.start_experience = experience
		self.start_level = level
		#level and experience
		self.experience = experience
		self.level = level
		#start health potion
		self.start_health_potion = health_potion
		self.health_potion = health_potion
		#alive
		self.alive = True
		#hitbox

	def Update(self):
			#animation cooldown in milliseconds
			animation_cooldown = 100
			#handle animation
			#update image
			self.image = self.animation_list[self.action][self.frame_index]	
			#check if enough time has passes since last update
			if pygame.time.get_ticks() - self.update_time > animation_cooldown:
				self.update_time = pygame.time.get_ticks()
				self.frame_index += 1
			#if animation runs out reset to the start
			if self.frame_index >= len(self.animation_list[self.action]):
				if self.action == 3:
					self.frame_index = len(self.animation_list[self.action]) - 1
				else:
					self.Idle()

	def Idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def Attack(self, target):
		randdamage = random.randint(-3,3)
		if randdamage + self.strength - target.defense <= 0:
			damage = 0
		else:
			damage = randdamage + self.strength - target.defense
		target.hp -= math.floor(damage)
		#run target hurt animation
		target.Hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.Death()
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def Hurt(self):
		#set variables to attack animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def Death(self):
		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def Level_Up_Monster(self):
		self.max_hp += random.randint(1,3)
		self.hp = self.max_hp
		self.experience += self.level * 2
		self.level += 1
		self.strength += 1
		self.luck += 1
		self.accuracy += 1
		self.evasion += 1

	def Level_Up_Hero(self, experiencethreshold = None):
		if experiencethreshold is None:
			self.experiencethreshold = []
		else:
			self.experiencethreshold = experiencethreshold
		if self.experience >= self.experiencethreshold[-1]:
			self.level += 1
			nextexperience = self.experiencethreshold[-1] * 3 # or experiencethreshold[0]
			self.experiencethreshold.append(nextexperience)
			self.statpoints += 5
			self.max_mp += 5			

	def Draw(self):
		screen.blit(self.image, self.rect)
		#check hitbox
		#pygame.draw.rect(screen,(255,0,0),self.hitbox,2)

class Hero(Character):
	def	__init__(self, x, y, name, max_hp, max_mp, level, experience, statpoints, strength, intelligence, defense, luck, evasion, accuracy, mana_potion, health_potion):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion)
		#start stat points
		self.start_statpoints = statpoints
		#current stat points
		self.statpoints = statpoints
		#start mana potions
		self.start_mana_potion = mana_potion
		#mana potions
		self.mana_potion = mana_potion
		#animation
		self.animation_list = [] #this is the hero's animation list -> hero.animation_list[]
		self.frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills; run loop 5 times to load each set of animation
		number_of_pictures_list = [4,5,4,5,6]
		which_state_list = ['Idle', 'Attack', 'Hurt', 'Death', 'Skill']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(250,250))
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.x - 70, self.y - 50, 100, 200)

	def Skill(self):
		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Slime(Character):
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion)
		self.animation_list = [] #this is the slime's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,5,4,5]
		which_state_list = ['Idle', 'Attack', 'Hurt', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(80,80))
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.x - 25, self.y - 15, 50, 50)

class Zombie(Character):
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, health_potion)
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,6,4,7]
		which_state_list = ['Idle', 'Attack', 'Hurt', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(250,250))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.x - 50, self.y - 50, 100, 200)


