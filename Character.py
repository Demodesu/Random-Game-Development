import math, pygame, random, sys

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
statbutton_img = pygame.image.load('Images/Icon/StatButton.png').convert_alpha()
damage_font = pygame.font.SysFont('Minecraft', 40)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)


class Character():
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold):
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
		self.shield = shield
		self.gold = gold
		#hitbox
	#---------------------------------------------------------#
	#update and draw
	def update(self):
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
					self.idle()

	def draw(self):
		screen.blit(self.image, self.rect)
		#check hitbox
		#pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
	#---------------------------------------------------------#
	#animations
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def attack(self, target, damage_text_group):
		randdamage = random.randint(-3,3)
		if randdamage + self.strength - target.defense <= 0:
			damage = 0
		else:
			damage = randdamage + self.strength - target.defense
		if target.shield > 0:
			if target.shield - math.floor(damage) >= 0:
				target.shield -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, '0', red)
			else:
				target.hp -= (target.shield - math.floor(damage)) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str((target.shield - math.floor(damage)) * -1), red)
		else:
			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
		damage_text_group.add(damage_text)
		#run target hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def guard(self, guard_sprite_group, damage_text_group):
		if self.shield > self.max_hp / 2:
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, '0', yellow)
			pass
		else:
			self.shield += self.max_hp / 4 	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, str(self.max_hp / 4), yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		guard_sprite_group.add(guard_animation)
		damage_text_group.add(damage_text)

	def hurt(self):
		#set variables to attack animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
	#---------------------------------------------------------#
	#level up
	def level_up_monster(self):
		self.max_hp += random.randint(1,3)
		self.hp = self.max_hp
		self.experience += self.level * 2
		self.gold += 2	
		self.level += 1
		self.strength += random.randint(0, 2)
		self.luck += random.randint(0, 2)
		self.accuracy += random.randint(0, 2)
		self.evasion += random.randint(0, 2)
	#---------------------------------------------------------#

class Hero(Character):
	def	__init__(self, x, y, name, max_hp, max_mp, level, experience, statpoints, strength, intelligence, defense, luck, evasion, accuracy, shield, mana_potion, health_potion, gold):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold)
		#start stat points
		self.start_statpoints = statpoints
		#current stat points
		self.statpoints = statpoints
		#start mana potions
		self.start_mana_potion = mana_potion
		#mana potions
		self.mana_potion = mana_potion
		self.fireballcastcost = 5
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

	def skill(self):
		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def fire_ball(self, target, damage_text_group, inventory):
		randdamage = random.randint(-3,3)
		if randdamage + self.intelligence <= 0:
			damage = 0
		else:
			damage = randdamage + self.intelligence
		target.hp -= math.floor(damage)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
		damage_text_group.add(damage_text)
		if 5 in inventory:
			target.hp -= math.floor(damage)
			damage_text_condensed_lightning = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.floor(damage)), red)
			damage_text_group.add(damage_text_condensed_lightning)			
		#run target hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def level_up_hero(self, experiencethreshold = None):
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
			self.mp += 5

	def str_up_button(self):
		self.strength += 1
		self.statpoints -= 1

	def int_up_button(self):
		self.intelligence += 1
		self.statpoints -= 1

	def luc_up_button(self):
		self.luck += 1
		self.statpoints -= 1	

	def acc_up_button(self):
		self.accuracy += 1
		self.statpoints -= 1

	def eva_up_button(self):
		self.evasion += 1
		self.statpoints -= 1

	def attack(self, target, damage_text_group, inventory):
		randdamage = random.randint(-3,3)
		if randdamage + self.strength - target.defense <= 0:
			damage = 0
		else:
			damage = randdamage + self.strength - target.defense
		if target.shield > 0:
			if target.shield - math.floor(damage) >= 0:
				target.shield -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, '0', red)
			else:
				target.hp -= (target.shield - math.floor(damage)) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str((target.shield - math.floor(damage)) * -1), red)
		else:
			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
		damage_text_group.add(damage_text)

		if 4 in inventory:
			if self.max_hp - self.hp > math.floor(target.max_hp * 0.1) + math.floor(self.strength * 0.1):
				heal_amount = math.floor(target.max_hp * 0.1) + math.floor(self.strength * 0.1)
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount

		#run target hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def normal_attack(self, current_fighter, action_cooldown, target, experiencethreshold, damage_text_group, inventory):
		self.attack(target, damage_text_group, inventory)
		if target.alive == False:
			self.experience += target.experience - math.floor(random.randint(0,2) * 1.5)
			self.level_up_hero(experiencethreshold)

	def fire_ball_attack(self, current_fighter, action_cooldown, target, monster, monster_list, monster_index, experiencethreshold, fire_ball_sprite_group, damage_text_group, inventory):
		alive_monster = 0
		for monster in monster_list[monster_index]:
			if monster.alive == True:
				alive_monster += 1

		if alive_monster == 2  and self.mp >= 10:
			for monster in monster_list[monster_index]:
				target = monster
				self.fire_ball(target, damage_text_group, inventory)
				fire_ball_animation = Fire_Ball_Images(target.x, target.y)
				fire_ball_sprite_group.add(fire_ball_animation)
				if target.alive == False:
					self.experience += target.experience - math.floor(random.randint(0,2) * 1.5)
					self.level_up_hero(experiencethreshold)
			self.mp -= 10	

		elif self.mp >= 5:
			self.fire_ball(target, damage_text_group, inventory)
			fire_ball_animation = Fire_Ball_Images(target.x, target.y)
			fire_ball_sprite_group.add(fire_ball_animation)							
			if target.alive == False:
				self.experience += target.experience - math.floor(random.randint(0,2) * 1.5)
				self.level_up_hero(experiencethreshold)	
			self.mp -= 5

class Slime(Character):
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold)
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
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold)
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

class Zombie_Boss(Character):
	def __init__(self, x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold):
		super().__init__(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold)
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,5,4,6]
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

class Fire_Ball_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(10):
			img = pygame.image.load(f'Images/Icon/Fireball/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

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

class Guard_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Shield/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

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

class Damage_Text(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = damage_font.render(damage, True, color)
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

def Random_Stats_Hero(random_stats_list):
	while True:
		start_random_integer = 50
		start_random_strength = random.randint(10, 15)
		start_random_intelligence = random.randint(10, 15)
		start_random_accuracy = random.randint(0, 10)
		start_random_evasion = random.randint(0, 10)
		start_random_luck = random.randint(0, 10)
		if start_random_integer - 5 < start_random_luck + start_random_evasion + start_random_accuracy + start_random_strength + start_random_intelligence < start_random_integer:
			random_stats_list.append(start_random_strength)
			random_stats_list.append(start_random_intelligence)
			random_stats_list.append(start_random_luck)
			random_stats_list.append(start_random_evasion)
			random_stats_list.append(start_random_accuracy)
			break	

def Random_Stats_Monsters(random_stats_list_monsters):
	while True:
		start_random_integer = 15
		start_random_strength = random.randint(3, 5)
		start_random_intelligence = random.randint(0, 3)
		start_random_accuracy = random.randint(0, 3)
		start_random_evasion = random.randint(0, 3)
		start_random_luck = random.randint(0, 3)
		if start_random_integer - 5 < start_random_luck + start_random_evasion + start_random_accuracy + start_random_strength + start_random_intelligence < start_random_integer:
			random_stats_list_monsters.append(start_random_strength)
			random_stats_list_monsters.append(start_random_intelligence)
			random_stats_list_monsters.append(start_random_luck)
			random_stats_list_monsters.append(start_random_evasion)
			random_stats_list_monsters.append(start_random_accuracy)
			break	

	#None
	# def Stat_Up_Button(self, x, y, click, key_1):
	# 	# mousex, mousey = pygame.mouse.get_pos()
	# 	# statbutton_button_str = bars.Button(screen, x, y, statbutton_img, 24, 24)
	# 	# statbutton_button_str.Draw()
	# 	# statbutton_button_luc = bars.Button(screen, x + 35, y, statbutton_img, 24, 24)
	# 	# statbutton_button_luc.Draw()
	# 	# statbutton_button_eva = bars.Button(screen, x + 70, y, statbutton_img, 24, 24)
	# 	# statbutton_button_eva.Draw()
	# 	# statbutton_button_acc = bars.Button(screen, x + 105, y, statbutton_img, 24, 24)
	# 	# statbutton_button_acc.Draw()
	# 	# str_button_hitbox = pygame.rect.Rect(x, y, 24, 24)
	# 	# luc_button_hitbox = pygame.rect.Rect(x + 35, y, 24, 24)
	# 	# eva_button_hitbox = pygame.rect.Rect(x + 70, y, 24, 24)
	# 	# acc_button_hitbox = pygame.rect.Rect(x + 105, y, 24, 24)
	# 	# #pygame.draw.rect(screen,(255,0,0),str_button_hitbox,2)
	# 	# #pygame.draw.rect(screen,(255,0,0),luc_button_hitbox,2)		
	# 	# #pygame.draw.rect(screen,(255,0,0),eva_button_hitbox,2)	
	# 	# if str_button_hitbox.collidepoint((mousex,mousey)):
	# 	# 	if click == True:
	# 	# 		self.strength += 3
	# 	# 		self.luck += 1
	# 	# 		self.accuracy += 1
	# 	# 		self.evasion += 1
	# 	# 		self.statpoints -= 1				
	# 	# if luc_button_hitbox.collidepoint((mousex,mousey)):
	# 	# 	if click == True:
	# 	# 		self.strength += 1
	# 	# 		self.luck += 3
	# 	# 		self.accuracy += 1
	# 	# 		self.evasion += 1
	# 	# 		self.statpoints -= 1
	# 	# if eva_button_hitbox.collidepoint((mousex,mousey)):
	# 	# 	if click == True:
	# 	# 		self.strength += 1
	# 	# 		self.luck += 1
	# 	# 		self.accuracy += 1
	# 	# 		self.evasion += 3
	# 	# 		self.statpoints -= 1
	# 	# if acc_button_hitbox.collidepoint((mousex,mousey)):
	# 	# 	if click == True:
	# 	# 		self.strength += 1
	# 	# 		self.luck += 1
	# 	# 		self.accuracy += 3
	# 	# 		self.evasion += 1
	# 	# 		self.statpoints -= 1

	#creating sprite groups
#1) create class
#2) class Player(pygame.sprite.Sprite):
#    def __init__(self):
#       pygame.sprite.Sprite.__init__(self)
#3) def updatee
#4) define image + define rect (self.image, self.rect = self.image.get_rect())
#5) add to sprite group 
#	all_sprites_group = pygame.sprite.Group()
#	player = Player()
#	all_sprites_group.add(player)
#6) call the update and draw
#	all_sprites.update() *****must be lowercase***** since it takes from the pygame.sprite class
#	all_sprites.draw() *****must be lowercase***** since it takes from the pygame.sprite class
# 	
