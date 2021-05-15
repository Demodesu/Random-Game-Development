import math, pygame, random, sys

pygame.init()

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
damage_font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 25)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
			
class Character():
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown):
		#defaults
		self.x = x
		self.y = y
		self.name = name
		#hp
		self.start_max_hp = max_hp
		self.max_hp = max_hp
		self.hp = max_hp
		self.hp_regen = hp_regen
		#mana
		self.start_max_mp = max_mp
		self.max_mp = max_mp
		self.mp = max_mp
		self.mp_regen = mp_regen
		#start stats 
		self.start_strength = strength
		self.start_intelligence = intelligence
		self.start_defense = defense
		self.start_luck = luck
		self.start_agility = agility
		self.start_endurance = endurance
		#current stats
		self.strength = strength
		self.intelligence = intelligence
		self.defense = defense
		self.luck = luck
		self.agility = agility
		self.endurance = endurance
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
		self.speed = speed
		#attack
		self.attack_cooldown = attack_cooldown
		#temp stat reduction
		self.temp_strength = 0
		self.temp_intelligence = 0
		self.temp_agility = 0
		self.temp_luck = 0
		self.temp_endurance = 0
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
			if self.action == 2:
				self.frame_index = len(self.animation_list[self.action]) - 1
			elif self.action == 20 and self.rect.y < 150:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def draw(self):
		screen.blit(self.image, self.rect)
		#check hitbox
		#pygame.draw.rect(screen,(255,0,0),self.rect,2)
		#pygame.draw.rect(screen,(0,255,0),self.hitbox,2)
		# pygame.draw.rect(screen,(255,0,0),self.head_hitbox,2)
		# pygame.draw.rect(screen,(255,0,0),self.body_hitbox,2)
		# pygame.draw.rect(screen,(255,0,0),self.leg_hitbox,2)	
	#---------------------------------------------------------#
	#animations
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def monster_critical_and_damage_calculation(self, target, damage_text_group):

		limb_target_chance = random.randint(0,1)
		limb_list = ['head', 'body']

		target_limb = limb_list[limb_target_chance]

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = math.floor(abs(randdamage) * 1.5)

		if target_limb == 'head':
			roll_head_bonus_damage = random.randint(0,100)
			if roll_head_bonus_damage + (self.luck * 0.25) > 70:
				randdamage += self.strength * 0.25
				head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'HIT', yellow)
				damage_text_group.add(head_critical_text)
			else:
				randdamage -= self.strength * 0.25
				head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'MISS', yellow)
				damage_text_group.add(head_critical_text)

		elif target_limb == 'body':
			randdamage = randdamage

		if (randdamage + self.strength) - (target.defense + (target.endurance / 5)) <= 0:
			damage = 0
		else:
			damage = (randdamage + self.strength) - (target.defense + (target.endurance / 5))

		return damage, roll_crit_chance

	def monster_shield_and_damage_calculation(self, target, damage, damage_text_group):
		if target.shield > 0:
			if target.shield - math.floor(damage) >= 0:
				target.shield -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), '0', red)
			else:
				target.hp -= (target.shield - math.floor(damage)) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{(target.shield - math.floor(damage)) * -1:.2f}', red)
		else:
			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{math.floor(damage):.2f}', red)
		damage_text_group.add(damage_text)

	def attack(self, target, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list):

		damage, roll_crit_chance = self.monster_critical_and_damage_calculation(target, damage_text_group)

		self.monster_shield_and_damage_calculation(target, damage, damage_text_group)

		if 7 in inventory and -1 in inventory:
			if self.shield > 0:
				if float(f'{self.shield - (target.defense * 0.25) + (damage * 0.8):.2f}')  >= 0:
					self.shield -= float(f'{(target.defense * 0.25) + (damage * 0.8):.2f}') 
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, '0', red)
				else:
					self.hp -= float(f'{(self.shield - (target.defense * 0.25) + (damage * 0.8) * -1):.2f}')
					self.shield = 0
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.shield - (target.defense * 0.25) + (damage * 0.8) * -1):.2f}', red)
			else:
				self.hp -= float(f'{((target.defense * 0.25) + (damage * 0.8)):.2f}')
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{((target.defense * 0.25) + (damage * 0.8)):.2f}', red)
			damage_text_group.add(damage_text)

		elif 7 in inventory and -1 not in inventory:
			if self.shield > 0:
				if float(f'{self.shield - (target.defense * 0.25) + (damage * 0.15):.2f}')  >= 0:
					self.shield -= float(f'{(target.defense * 0.25) + (damage * 0.15):.2f}') 
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, '0', red)
				else:
					self.hp -= float(f'{(self.shield - (target.defense * 0.25) + (damage * 0.15) * -1):.2f}')
					self.shield = 0
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.shield - (target.defense * 0.25) + (damage * 0.15) * -1):.2f}', red)
			else:
				self.hp -= float(f'{((target.defense * 0.25) + (damage * 0.15)):.2f}')
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{((target.defense * 0.25) + (damage * 0.15)):.2f}', red)
			damage_text_group.add(damage_text)

		if 19 in inventory:
			target.hp += damage * 0.15
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'{damage * 0.15:.2f}', green)
			damage_text_group.add(damage_text)		

		#check if target is dead
		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def guard(self, skill_sprite_group, damage_text_group):
		self.shield += math.floor((self.max_hp * 0.2) + (self.defense * 0.5))
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, 'Guard ' + str(math.floor((self.max_hp * 0.2) + (self.defense * 0.5))), yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)

	def death(self, ):
		#set variables to attack animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#---------------------------------------------------------#
	#level up
	def level_up_monster(self, hero):
		self.max_hp += random.randint(1,3)
		self.hp = self.max_hp
		self.experience += (self.level * 3.5) + (hero.experience * 0.02)
		if self.gold < 200:
			self.gold += 1 + (self.gold * 0.2)	 
		else:
			self.gold += 2
		self.level += 1

		if self.level >= 40:
			self.strength += random.randint(0,1) * 0.8
		else:
			self.strength += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.luck += random.randint(0,1) * 0.8
		else:
			self.luck += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.endurance += random.randint(0,1) * 0.8
		else:
			self.endurance += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.agility += random.randint(0,1) * 0.8
		else:
			self.agility += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.max_hp += 2

		if self.level % 4 == 0:
			self.speed += 0.5
		if self.endurance % 6 == 0:
			self.hp_regen += 0.25
			self.max_hp += 2
		if self.strength % 6 == 0:
			self.defense += 0.25
	#---------------------------------------------------------#

class Hero(Character):
	def	__init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_amount, stamina_recovery, stamina_threshold, turn_amount, turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, position_bonus, buff_reset_time, buff_duration, attack_cooldown, fireball_charge, lightning_charge):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown)
		#start stat points
		self.start_statpoints = statpoints
		#current stat points
		self.statpoints = statpoints
		#start mana potions
		self.start_mana_potion = mana_potion
		#mana potions
		self.mana_potion = mana_potion
		#stamina
		self.stamina_recovery = stamina_recovery
		self.stamina_threshold = stamina_threshold
		self.stamina_amount = stamina_amount
		#turn
		self.turn_threshold = turn_threshold
		self.turn_amount = turn_amount
		#stat bonuses
		self.added_strength = added_strength
		self.added_intelligence = added_intelligence
		self.added_endurance = added_endurance
		self.added_luck = added_luck
		self.added_agility = added_agility
		#position bonus
		self.position_bonus = position_bonus
		#buff
		self.buff_reset_time = buff_reset_time
		self.buff_duration = buff_duration
		#consumables
		self.fireball_charge = fireball_charge
		self.lightning_charge = lightning_charge
		#attack
		#animation
		self.animation_list = [] #this is the hero's animation list -> hero.animation_list[]
		self.frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills, 5 = counter
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = dead; 3 = skills; 4 = counter; 5 = attack2; 6 = attack3; 7 = critical; 8 = attack4; 9 = guard; 10 = stomp; 11 = attack5; 12 = Stab; 13 = move front; 14 = move back; 15 = move front attack; 16 = move back; 17 = triple head; 18 = whip; 19 = throw;20 = jump;21 = roll;22 = roll back attack run loop to load each set of animation
		number_of_pictures_list = [4,3,5,6,3,3,3,4,4,3,5,5,9,2,2,3,6,9,4,4,2,6,4]
		which_state_list = ['Idle', 'Attack', 'Death', 'Skill', 'Counter', 'Attack2', 'Attack3', 'Critical', 'Attack4', 'Guard', 'Stomp', 'Attack5', 'Stab', 'MoveFront', 'MoveBack', 'MoveFrontAttack', 'MoveBackAttack', 'TripleHead', 'Whip', 'Throw', 'Jump', 'Roll', 'RollBack']
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
		self.hitbox = pygame.rect.Rect(self.rect.x + (self.rect.x * 0.5) + 20, self.rect.y + (self.rect.y * 0.5), 100, 180)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def jump(self):
		#set variables to attack animation
		self.action = 20
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def roll(self):
		#set variables to attack animation
		self.action = 21
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def roll_back(self):
		#set variables to attack animation
		self.action = 22
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def level_up_hero(self, inventory, experiencethreshold = None):
		if experiencethreshold is None:
			self.experiencethreshold = []
		else:
			self.experiencethreshold = experiencethreshold
		if self.experience >= self.experiencethreshold[-1]:

			self.level += 1
			nextexperience = self.experiencethreshold[-1] * 3 # or experiencethreshold[0]
			self.experiencethreshold.append(nextexperience)
			self.statpoints += 3

			if -7 in inventory:
				self.max_hp += 4

			self.max_mp += 2
			self.mp += 2
			self.mp_regen += 0.25
			self.max_hp += 2
			self.hp += 2
			self.hp_regen += 0.25

			self.strength += 1
			self.intelligence += 1
			self.luck += 1
			self.endurance += 1
			self.agility += 1

			self.defense += 0.125

	def str_up_button(self):
		self.strength += 0.75
		self.added_strength += 0.75
		self.statpoints -= 1
		if self.added_strength == 1.5:
			self.stamina_recovery += 0.5
			self.added_strength = 0

	def int_up_button(self):
		self.intelligence += 0.75
		self.added_intelligence += 0.75
		self.statpoints -= 1
		if self.added_intelligence == 1.5:
			self.max_mp += 5
			self.mp += 5
			self.mp_regen += 0.5
			self.added_intelligence = 0

	def end_up_button(self):
		self.endurance += 0.75
		self.added_endurance += 0.75
		self.statpoints -= 1
		if self.added_endurance == 1.5:
			self.max_hp += 5
			self.hp += 5
			self.hp_regen += 0.5
			self.defense += 0.125
			self.added_endurance = 0

	def luc_up_button(self):
		self.luck += 0.75
		self.added_luck += 0.75
		self.statpoints -= 1	

	def agi_up_button(self):
		self.agility += 0.75
		self.added_agility += 0.75
		self.statpoints -= 1

	def drop_items(self, target, inventory, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list):
		if target.alive == False:
			if target.level > 0:
				if 0 not in inventory:			
					rollitemactive = random.randint(0,100)
					if rollitemactive > 80:
						inventory.append(0)
						self.max_hp += 3
						self.hp += 5
				if 2 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 90:
						inventory.append(2)
						self.luck += 1
						self.added_luck += 1
				if 3 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 70:
						inventory.append(3)
						self.speed += 0.25
				if 16 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 80:
						inventory.append(16)
						self.speed += 0.25
						self.stamina_recovery += 0.25
			if target.level > 2:
				if 1 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						inventory.append(1)
						self.strength += 1
						self.added_strength += 1
				if 39 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						inventory.append(39)
						self.defense += 1
			if target.level > 4:
				if 12 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 85:
						inventory.append(12)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.hp_regen -= 1
				if 40 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 85:
						inventory.append(40)
						self.endurance += 3				
			if target.level > 6:
				if 17 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						inventory.append(17)
						self.stamina_threshold -= 50
			if target.level > 15:
				if 22 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 80:
						inventory.append(22)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.defense -= 2
			if target.level > 2 and (monster_index == 0 or monster_index == 3):
				if 11 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 85:
						inventory.append(11)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.speed -= 0.5
			if target.level > 0 and (monster_index == 1 or monster_index == 2 or monster_index == 3):
				if 14 not in inventory:
					if monster_index == 1:
						rollitemactive = random.randint(0,100)
					else:
						rollitemactive = random.randint(90,100)
					if rollitemactive > 95:
						inventory.append(14)
						skills_list.append('zombie_stab')
#----------------------------------------------------------------------------------right click
	#forward movement
	def move_middle_to_front(self, hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group):
		self.rect.x += 125
		self.hitbox.x += 125
		hero_front_position = True
		hero_middle_position = False

		self.strength += self.position_bonus
		self.intelligence += self.position_bonus
		self.luck += self.position_bonus

		self.defense -= (self.position_bonus + 1.5)
		self.endurance -= (self.position_bonus + 1.5)

		if 38 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.01:
				heal_amount = self.max_hp * 0.01
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

		if -9 in inventory:
			self.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

		self.stamina_amount -= self.stamina_threshold * 0.20
		if 32 in inventory:
			self.action = 15
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, inventory)
		else:
			self.action = 13
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		return hero_front_position, hero_middle_position

	def move_back_to_middle(self, hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group):
		self.rect.x += 125
		self.hitbox.x += 125
		hero_back_position = False
		hero_middle_position = True
		
		self.endurance -= self.position_bonus
		self.defense -= self.position_bonus
		self.hp_regen -= self.position_bonus
		self.agility -= self.position_bonus

		self.strength += (self.position_bonus + 1.5)
		self.intelligence += (self.position_bonus + 1.5)
		self.luck += (self.position_bonus + 1.5)

		if 38 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.01:
				heal_amount = self.max_hp * 0.01
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

		if -9 in inventory:
			self.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

		self.stamina_amount -= self.stamina_threshold * 0.20
		if 32 in inventory:
			self.action = 15
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, inventory)
		else:
			self.action = 13
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		return hero_middle_position, hero_back_position

	#backwards movement
	def move_middle_to_back(self, hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group):
		self.rect.x -= 125
		self.hitbox.x -= 125
		hero_back_position = True
		hero_middle_position = False
		
		self.endurance += self.position_bonus
		self.defense += self.position_bonus
		self.hp_regen += self.position_bonus
		self.agility += self.position_bonus

		self.strength -= (self.position_bonus + 1.5)
		self.intelligence -= (self.position_bonus + 1.5)
		self.luck -= (self.position_bonus + 1.5)

		if 38 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.01:
				heal_amount = self.max_hp * 0.01
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

		if -9 in inventory:
			self.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

		self.stamina_amount -= self.stamina_threshold * 0.20
		if 33 in inventory:
			self.action = 16
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, inventory)
		else:
			self.action = 14
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

		return hero_middle_position, hero_back_position

	def move_front_to_middle(self, hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group):
		self.rect.x -= 125
		self.hitbox.x -= 125
		hero_front_position = False
		hero_middle_position = True

		self.strength -= self.position_bonus
		self.intelligence -= self.position_bonus
		self.luck -= self.position_bonus					

		self.defense += (self.position_bonus + 1.5)
		self.endurance += (self.position_bonus + 1.5)

		if 38 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.01:
				heal_amount = self.max_hp * 0.01
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

		if -9 in inventory:
			self.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

		self.stamina_amount -= self.stamina_threshold * 0.20
		if 33 in inventory:
			self.action = 16
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, inventory)
		else:
			self.action = 14
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

		return hero_front_position, hero_middle_position

	def move_attacks(self, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, inventory):
		if len(monster_list[monster_index]) != 1:
			random_monster = random.randint(0,1)
			if random_monster == 0:
				if monster_list[monster_index][0].alive == True:
					target = monster_list[monster_index][0]
				else:
					target = monster_list[monster_index][1]
			elif random_monster == 1:
				if monster_list[monster_index][1].alive == True:
					target = monster_list[monster_index][1]
				else:
					target = monster_list[monster_index][0]
		else:
			target = monster_list[monster_index][0]

		limb_list = ['head', 'body']

		if target.alive == True:
			target_limb = limb_list[random.randint(0,1)]

			damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			if -4 in inventory:
				damage = damage * 1.5
			else:
				damage = damage * 0.5

			self.shield_and_damage_calculation(target, damage, damage_text_group)

			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

	def counter(self, right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skills_list, skill_sprite_group):

		counter_chance = False
		counter_time = pygame.time.get_ticks()

		if counter_time - monster_attack_time < 500:
			counter_text = Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, 'Counter', yellow)

			if len(monster_list[monster_index]) != 1:
				if monster_list[monster_index][0].monster_turn_amount < monster_list[monster_index][1].monster_turn_amount:
					target = monster_list[monster_index][0]
				else:
					target = monster_list[monster_index][1]

				if monster_list[monster_index][0].alive == False:
					target = monster_list[monster_index][1]
				if monster_list[monster_index][1].alive == False:
					target = monster_list[monster_index][0]
			else:
				target = monster_list[monster_index][0]

			randdamage = random.randint(-3,3)

			roll_crit_chance = random.randint(0,100)
			if roll_crit_chance + (self.luck * 0.25) > 70:
				critical_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y - random.randint(30,60), 'CRITICAL', red)
				damage_text_group.add(critical_text)
				randdamage = math.floor(abs(randdamage) * 1.5)

			if 20 not in inventory:
				if (randdamage + self.strength - (target.defense + (target.endurance / 5))) * 0.5 <= 0:
					damage = 0
				else:
					damage = (randdamage + self.strength - (target.defense + (target.endurance / 5))) * 0.5
			else:
				if (randdamage + self.strength - (target.defense + (target.endurance / 5))) <= 0:
					damage = 0
				else:
					damage = (randdamage + self.strength - (target.defense + (target.endurance / 5)))

			self.shield_and_damage_calculation(target, damage, damage_text_group)

			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

			if 34 in inventory:
				bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
				skill_sprite_group.add(bleed_animation)

				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Bleed', red)	
				damage_text_group.add(damage_text)	

			#set variables to attack animation
			self.action = 4
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

		else:
			counter_text = Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, 'Counter Failed', red)

		damage_text_group.add(counter_text)

		return counter_chance, counter_time

#----------------------------------------------------------------------------------left click and spells
	def critical_and_damage_calculation(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb):

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = math.floor(abs(randdamage) * 1.5)

		if target_limb == 'head':
			roll_head_bonus_damage = random.randint(0,100)
			if roll_head_bonus_damage + (self.luck * 0.25) > 70:
				randdamage += self.strength * 0.25
				head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'HIT', yellow)
				damage_text_group.add(head_critical_text)
			else:
				randdamage -= self.strength * 0.25
				head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'MISS', yellow)
				damage_text_group.add(head_critical_text)

		elif target_limb == 'body':
			randdamage = randdamage

		else:
			roll_leg_hit_chance = random.randint(0,100)
			if len(monster_list[monster_index]) == 1 and roll_leg_hit_chance + (self.luck * 0.25) > 25:
				target.monster_turn_amount -= target.monster_turn_threshold * 0.15
				bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'SLIP', yellow)
				damage_text_group.add(bar_reduction_text)
			elif len(monster_list[monster_index]) > 1 and roll_leg_hit_chance + (self.luck * 0.25) > 25:
				target.monster_turn_amount -= target.monster_turn_threshold * 0.5
				bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'SLIP', yellow)
				damage_text_group.add(bar_reduction_text)
			else:
				bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'MISS', yellow)
				damage_text_group.add(bar_reduction_text)
			if target.monster_turn_amount <= 0:
				target.monster_turn_amount = 1
			randdamage -= self.strength * 0.5

		if (randdamage + self.strength) - (target.defense + (target.endurance / 5)) <= 0:
			damage = 0
		else:
			damage = (randdamage + self.strength) - (target.defense + (target.endurance / 5))

		return damage, roll_crit_chance

	def shield_and_damage_calculation(self, target, damage, damage_text_group):
		if target.shield > 0:
			if target.shield - math.floor(damage) >= 0:
				target.shield -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), '0', red)
			else:
				target.hp -= (target.shield - math.floor(damage)) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{(target.shield - math.floor(damage)) * -1:.2f}', red)
		else:
			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{math.floor(damage):.2f}', red)
		damage_text_group.add(damage_text)

	def monster_death_drops(self, target, experiencethreshold, inventory, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list):
		if target.hp <= 0 and target.alive == True:
			target.hp = 0
			target.alive = False
			target.death()
			self.gold += target.gold
			self.experience += target.experience + math.floor(random.randint(-2,2) * 1.5)	
			self.drop_items(target, inventory, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list)

	def attack(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group):

		damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

		damage = damage * 0.35

		self.shield_and_damage_calculation(target, damage, damage_text_group)

		if 4 in inventory:
			if self.max_hp - self.hp > math.ceil(damage * 0.1):
				heal_amount = math.ceil(damage * 0.1)
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

		#set variables to attack animation
		roll_attack_animation = random.randint(0,2)
		if roll_attack_animation == 0:
			self.action = 1
		elif roll_attack_animation == 1:
			self.action = 5
		else:
			self.action = 6
		if roll_crit_chance + (self.luck * 0.25) > 50:
			critical_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y - random.randint(30,60), 'CRITICAL', red)
			damage_text_group.add(critical_text)
			self.action = 7
		if target_limb == 'leg':
			self.action = 8
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		if -5 in inventory:
			amount_of_turns = 2
		else:
			amount_of_turns = 3	

		if 18 in inventory and turn_counter % amount_of_turns == 0:

			damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), str(math.floor(damage)), red)
			damage_text_group.add(damage_text)	

			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

			self.action = 11
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	

	def cleave(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

		self.mp -= 7.5

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:

				damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

				self.shield_and_damage_calculation(target, damage, damage_text_group)

				if target.alive == True:
					if 4 in inventory:
						if self.max_hp - self.hp > math.ceil(damage * 0.1):
							heal_amount = math.ceil(damage * 0.1)
						else:
							heal_amount = self.max_hp - self.hp
						self.hp += heal_amount
						heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(monster) + 1), f'{heal_amount:.2f}', green)
						damage_text_group.add(heal_text)
				
				if 'cleave_bleed' in skills_list:
					bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
					skill_sprite_group.add(bleed_animation)

					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Bleed', red)	
					damage_text_group.add(damage_text)	

				if 'double_cleave' in skills_list:
					damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

					self.shield_and_damage_calculation(target, damage, damage_text_group)

					if target.alive == True:
						if 4 in inventory:
							if self.max_hp - self.hp > math.ceil(damage * 0.1):
								heal_amount = math.ceil(damage * 0.1)
							else:
								heal_amount = self.max_hp - self.hp
							self.hp += heal_amount
							heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(monster) + 1), f'{heal_amount:.2f}', green)
							damage_text_group.add(heal_text)

				cleave_animation = Cleave_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
				skill_sprite_group.add(cleave_animation)

		#set variables to attack animation
		if 'double_cleave' in skills_list:
			self.action = 11
		else:
			self.action = 6
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def zombie_stab(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

		self.mp -= 10

		damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
		damage = damage * 2

		target.hp -= math.floor(damage)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
		damage_text_group.add(damage_text)

		if target.alive == True:
			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(target) + 1), f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

		zombie_stab_animation = Zombie_Stab_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
		skill_sprite_group.add(zombie_stab_animation)

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def triple_combo(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, skills_list):

		self.mp -= 10

		limb_list = ['head', 'body', 'leg']

		for stabs in range(3):

			if 'triple_head' in skills_list:
				target_limb = 'head'
			else:
				target_limb = limb_list[stabs]

			if 'triple_mana_restore' in skills_list:
				if self.max_mp - self.mp > self.max_mp * 0.02:
					restore_amount = self.max_mp * 0.02
				else:
					restore_amount = self.max_mp - self.mp
				self.mp += restore_amount
				restore_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{restore_amount:.2f}', blue)
				damage_text_group.add(restore_text)

			damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			damage = damage * 0.75

			self.shield_and_damage_calculation(target, damage, damage_text_group)

			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

		#set variables to attack animation
		if 'triple_head' in skills_list:
			self.action = 17
		else:
			self.action = 12
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

#----------------------------------------------------------------------------------guard and skills
	def guard(self, skill_sprite_group, damage_text_group, skills_list, experiencethreshold, inventory, monster_list, monster_index, turn_counter):

		shield_amount = math.floor((self.max_hp * 0.2) + (self.defense * 3))
		if shield_amount < 0:
			shield_amount = 0
		else:
			shield_amount = math.floor((self.max_hp * 0.2) + (self.defense * 3))
		self.shield += shield_amount
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, str(math.floor(shield_amount)), yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)
		if 'guard_heal' in skills_list:
			if self.max_hp - self.hp > math.floor((self.max_hp * 0.05) + (self.defense * 0.5)):
				heal_amount = math.floor((self.max_hp * 0.05) + (self.defense * 0.5))
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{heal_amount:.2f}', green)			
			damage_text_group.add(heal_text)

		self.action = 9
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

		if 'guard_slash' in skills_list:
			limb_list = ['head', 'body', 'leg']
			target_limb = limb_list[random.randint(0,2)]
			if len(monster_list[monster_index]) != 1:
				random_monster = random.randint(0,1)
				if random_monster == 0:
					if monster_list[monster_index][0].alive == True:
						target = monster_list[monster_index][0]
					else:
						target = monster_list[monster_index][1]
				elif random_monster == 1:
					if monster_list[monster_index][1].alive == True:
						target = monster_list[monster_index][1]
					else:
						target = monster_list[monster_index][0]
			else:
				target = monster_list[monster_index][0]
			self.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group)

		if 'guard_rush' in skills_list:
			self.turn_amount += self.turn_threshold * 0.25
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +25%', yellow)	
			damage_text_group.add(damage_text)	

	def stomp(self, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

		for monster in monster_list[monster_index]:
			if monster.alive != False:
				if len(monster_list[monster_index]) != 1:
					if -10 in inventory:
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.3
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -30%', yellow)
					else:	
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -20%', yellow)
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.2
					damage_text_group.add(damage_text)	
				else:
					if -10 in inventory:
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.25
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -25%', yellow)	
					else:
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.15
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -15%', yellow)	
					damage_text_group.add(damage_text)					
			if monster.monster_turn_amount <= 0:
				monster.monster_turn_amount = 1

		if -10 in inventory:
			self.temp_endurance += 3
			self.endurance += 3

			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'END +3', yellow)	
			damage_text_group.add(damage_text)				

		if 'stomp_buff' in skills_list:
			self.temp_strength += 2
			self.strength += 2

			self.temp_agility += 2
			self.agility += 2

			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'STR +2', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'AGI +2', yellow)	
			damage_text_group.add(damage_text)	

		if 'stomp_damage' in skills_list:
			for monster in monster_list[monster_index]:
				if monster.alive != False:
					target_limb = 'body'
					damage, roll_crit_chance = self.critical_and_damage_calculation(monster, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
					damage = damage * 0.8

					self.shield_and_damage_calculation(monster, damage, damage_text_group)

		if 'stomp_rush' in skills_list:
			for monster in monster_list[monster_index]:
				if monster.alive != False:
					self.turn_amount += self.turn_threshold * 0.2
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +20%', yellow)	
					damage_text_group.add(damage_text)	

		self.action = 10
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def fireball(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list):

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				randdamage = random.randint(-3,3)
				if 'fireball_agi_damage' in skills_list:
					if randdamage + (self.intelligence * 1.25) + (self.agility * 0.25) <= 0:
						damage = 0
					else:
						damage = randdamage + (self.intelligence * 1.25) + (self.agility * 0.25)
					target.hp -= math.floor(damage)
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
					damage_text_group.add(damage_text)
				else:
					if randdamage + (self.intelligence * 1.25) <= 0:
						damage = 0
					else:
						damage = randdamage + (self.intelligence * 1.25)
					target.hp -= math.floor(damage)
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
					damage_text_group.add(damage_text)
				
				if 5 in inventory:
					target.hp -= math.floor(damage * 0.75)
					damage_text_condensed_lightning = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.floor(damage * 0.75)), red)
					damage_text_group.add(damage_text_condensed_lightning)

				if 31 in inventory:
					monster.monster_turn_amount -= monster.monster_turn_threshold * 0.2
					damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -20%', yellow)	
					damage_text_group.add(damage_text)	
					self.turn_amount += monster.monster_turn_threshold * 0.2
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +20%', yellow)	
					damage_text_group.add(damage_text)	
					fire_ball_animation = Sapphire_Flame_Images(target.x, target.y)
					skill_sprite_group.add(fire_ball_animation)	
				else:
					fire_ball_animation = Fire_Ball_Images(target.x, target.y)
					skill_sprite_group.add(fire_ball_animation)					

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def spark(self, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list):

		if len(monster_list[monster_index]) != 1:
			if monster_list[monster_index][0].monster_turn_amount > monster_list[monster_index][1].monster_turn_amount:
				target = monster_list[monster_index][0]
			else:
				target = monster_list[monster_index][1]

			if monster_list[monster_index][0].alive == False:
				target = monster_list[monster_index][1]
			if monster_list[monster_index][1].alive == False:
				target = monster_list[monster_index][0]
		else:
			target = monster_list[monster_index][0]

		if target.alive != False:
			randdamage = random.randint(-3,3)
			if 'fireball_agi_damage' in skills_list:
				if randdamage + (self.intelligence * 0.5) + (self.agility * 0.25) <= 0:
					damage = 0
				else:
					damage = randdamage + (self.intelligence * 0.5) + (self.agility * 0.25)
				target.hp -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
				damage_text_group.add(damage_text)
			else:
				if randdamage + (self.intelligence * 0.5) <= 0:
					damage = 0
				else:
					damage = randdamage + (self.intelligence * 0.5)
				target.hp -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
				damage_text_group.add(damage_text)
			
			if 5 in inventory:
				target.hp -= math.floor(damage * 0.75)
				damage_text_condensed_lightning = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.floor(damage * 0.75)), red)
				damage_text_group.add(damage_text_condensed_lightning)

			if 31 in inventory:
				target.monster_turn_amount -= target.monster_turn_threshold * 0.05
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -5%', yellow)	
				damage_text_group.add(damage_text)	
				self.turn_amount += target.monster_turn_threshold * 0.05
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +5%', yellow)	
				damage_text_group.add(damage_text)	
				fire_ball_animation = Sapphire_Spark_Images(target.x, target.y)
				skill_sprite_group.add(fire_ball_animation)	
			else:
				spark_animation = Spark_Images(target.x, target.y)
				skill_sprite_group.add(spark_animation)		

	def lightning(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list):

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				randdamage = random.randint(-3,3)
				if 'lightning_agi_damage' in skills_list:
					if randdamage + self.intelligence + (self.agility * 0.25) <= 0:
						damage = 0
					else:
						damage = randdamage + self.intelligence + (self.agility * 0.25)
					target.hp -= math.floor(damage)
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
					damage_text_group.add(damage_text)
				else:
					if randdamage + self.intelligence <= 0:
						damage = 0
					else:
						damage = randdamage + (self.intelligence)
					target.hp -= math.floor(damage)
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
					damage_text_group.add(damage_text)

				if -2 in inventory:
					target.hp -= math.floor(damage)
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.floor(damage)), red)
					damage_text_group.add(damage_text)

				if -2 in inventory:
					eclipse_beam_animation = Eclipse_Beam_Images(target.x, target.hitbox.top)
					skill_sprite_group.add(eclipse_beam_animation)	

				elif 36 in inventory:
					lunar_beam_animation = Lunar_Beam_Images(target.x, target.hitbox.top)
					skill_sprite_group.add(lunar_beam_animation)
	
				elif 37 in inventory:
					solar_beam_animation = Solar_Beam_Images(target.x, target.hitbox.top)
					skill_sprite_group.add(solar_beam_animation)
	
				else:
					lightning_animation = Lightning_Images(target.x, target.hitbox.top)
					skill_sprite_group.add(lightning_animation)

				self.turn_amount += self.turn_threshold * 0.25

		if -2 in inventory:
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Eclipse Beam', yellow)	
			damage_text_group.add(damage_text)	

		if 36 in inventory:
			if self.max_mp - self.mp > self.max_mp * 0.25:
				restore_amount = self.max_mp * 0.25
			else:
				restore_amount = self.max_mp - self.mp
			self.mp += restore_amount
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 30 + random.randint(-60,60), f'+{restore_amount:.2f}% MP', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Lunar Beam', yellow)	
			damage_text_group.add(damage_text)

		if 37 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.25:
				heal_amount = self.max_hp * 0.25
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 30 + random.randint(-60,60), f'+{heal_amount:.2f}% HP', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Solar Beam', yellow)	
			damage_text_group.add(damage_text)	

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def water_blast(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

		if len(monster_list[monster_index]) != 1:
			random_monster = random.randint(0,1)
			if random_monster == 0:
				if monster_list[monster_index][0].alive == True:
					target = monster_list[monster_index][0]
				else:
					target = monster_list[monster_index][1]
			elif random_monster == 1:
				if monster_list[monster_index][1].alive == True:
					target = monster_list[monster_index][1]
				else:
					target = monster_list[monster_index][0]
		else:
			target = monster_list[monster_index][0]

		damage = float(f'{(self.max_hp - self.hp) * 0.5:.2f}')
		if damage > 200:
			damage = 200
		else:
			damage = float(f'{(self.max_hp - self.hp) * 0.5:.2f}')

		target.hp -= damage
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(damage), red)
		damage_text_group.add(damage_text)

		water_blast_animation = Water_Blast_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
		skill_sprite_group.add(water_blast_animation)

	def serpent_wheel(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

		self.mp -= 20

		for monster in monster_list[monster_index]:
			target = monster
			if monster.alive == True:
				randdamage = random.randint(-3,3)

				roll_crit_chance = random.randint(0,100)
				if roll_crit_chance + (self.luck * 0.25) > 70:
					randdamage = math.floor(abs(randdamage) * 1.5)

				if target_limb == 'head':
					roll_head_bonus_damage = random.randint(0,100)
					if roll_head_bonus_damage + (self.luck * 0.25) > 70:
						randdamage += self.strength * 0.25
						head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'HIT', yellow)
						damage_text_group.add(head_critical_text)
					else:
						randdamage -= self.strength * 0.25
						head_critical_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(30,60), 'MISS', yellow)
						damage_text_group.add(head_critical_text)

				elif target_limb == 'body':
					randdamage = randdamage

				else:
					roll_leg_hit_chance = random.randint(0,100)
					if len(monster_list[monster_index]) == 1 and roll_leg_hit_chance + (self.luck * 0.25) > 25:
						target.monster_turn_amount -= target.monster_turn_threshold * 0.15
						bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'SLIP', yellow)
						damage_text_group.add(bar_reduction_text)
					elif len(monster_list[monster_index]) > 1 and roll_leg_hit_chance + (self.luck * 0.25) > 25:
						target.monster_turn_amount -= target.monster_turn_threshold * 0.5
						bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'SLIP', yellow)
						damage_text_group.add(bar_reduction_text)
					else:
						bar_reduction_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y - random.randint(60,60), 'MISS', yellow)
						damage_text_group.add(bar_reduction_text)
					if target.monster_turn_amount <= 0:
						target.monster_turn_amount = 1
					randdamage -= self.strength * 0.5

				if (randdamage + (self.strength * 1.5) + (self.agility * 1.5)) - (target.defense + (target.endurance / 5)) <= 0:
					damage = 0
				else:
					damage = (randdamage + (self.strength * 1.5) + (self.agility * 1.5)) - (target.defense + (target.endurance / 5))

				target.hp -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
				damage_text_group.add(damage_text)

				if target.alive == True:
					if 4 in inventory:
						if self.max_hp - self.hp > math.ceil(damage * 0.1):
							heal_amount = math.ceil(damage * 0.1)
						else:
							heal_amount = self.max_hp - self.hp
						self.hp += heal_amount
						heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(target) + 1), f'{heal_amount:.2f}', green)
						damage_text_group.add(heal_text)

				bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
				skill_sprite_group.add(bleed_animation)

		serpent_wheel_animation = Serpent_Wheel_Images((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
		skill_sprite_group.add(serpent_wheel_animation)

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def venomous_whip(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list):

		self.mp -= 20

		for monster in monster_list[monster_index]:
			target = monster
			if monster.alive == True:
				randdamage = random.randint(-3,3)

				roll_crit_chance = random.randint(0,100)
				if roll_crit_chance + (self.luck * 0.25) > 70:
					randdamage = math.floor(abs(randdamage) * 1.5)

				if (randdamage + (self.intelligence * 2) + (self.strength)) - (target.defense + (target.endurance / 5)) <= 0:
					damage = 0
				else:
					damage = (randdamage + (self.intelligence * 2) + (self.strength)) - (target.defense + (target.endurance / 5))

				target.hp -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
				damage_text_group.add(damage_text)

				if target.alive == True:
					if 4 in inventory:
						if self.max_hp - self.hp > math.ceil(damage * 0.1):
							heal_amount = math.ceil(damage * 0.1)
						else:
							heal_amount = self.max_hp - self.hp
						self.hp += heal_amount
						heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(target) + 1), f'{heal_amount:.2f}', green)
						damage_text_group.add(heal_text)

				poison_animation = Poison_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
				skill_sprite_group.add(poison_animation)

		venomous_whip_animation = Venomous_Whip_Images((self.hitbox.x + self.hitbox.width / 2) + 230, target.hitbox.y + (target.hitbox.height / 2) + 30)
		skill_sprite_group.add(venomous_whip_animation)

		#set variables to attack animation
		self.action = 18
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def thunder_bolt(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list):

		self.mp -= 15

		if target.alive == True:
			randdamage = random.randint(-3,3)

			roll_crit_chance = random.randint(0,100)
			if roll_crit_chance + (self.luck * 0.25) > 70:
				randdamage = math.floor(abs(randdamage) * 1.5)

			if (randdamage + (self.agility * 1.5) - target.defense + (target.endurance / 5)) <= 0:
				damage = 0
			else:
				damage = (randdamage + (self.agility * 1.5) - (target.defense + (target.endurance / 5)))

			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
			damage_text_group.add(damage_text)

			if target.alive == True:
				if 4 in inventory:
					if self.max_hp - self.hp > math.ceil(damage * 0.1):
						heal_amount = math.ceil(damage * 0.1)
					else:
						heal_amount = self.max_hp - self.hp
					self.hp += heal_amount
					heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(target) + 1), f'{heal_amount:.2f}', green)
					damage_text_group.add(heal_text)

			self.turn_amount += self.turn_threshold * 0.25
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +25%', yellow)	
			damage_text_group.add(damage_text)	

		thunder_bolt_animation = Thunder_Bolt_Images((self.hitbox.x + self.hitbox.width / 2) + 500, target.hitbox.y + (target.hitbox.height / 2))
		skill_sprite_group.add(thunder_bolt_animation)

		#set variables to attack animation
		self.action = 19
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Slime(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown)
		self.monster_turn_amount = monster_turn_amount
		self.monster_turn_threshold = monster_turn_threshold
		self.animation_list = [] #this is the slime's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,5,5]
		which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(80,80))
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def armor_corrosion(self, target, damage_text_group, inventory):
		if target.shield > 0:
			shield_destroyed = target.shield
			target.shield = 0
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(shield_destroyed), yellow)
			damage_text_group.add(damage_text)

		target.hp -= math.ceil(self.strength * 0.25)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.ceil(self.strength * 0.25)), red)

		damage_text_group.add(damage_text)
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Armor Corrosion', yellow)	
		damage_text_group.add(damage_text)	
		#check if target is dead
		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Zombie(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown)
		self.monster_turn_amount = monster_turn_amount
		self.monster_turn_threshold = monster_turn_threshold
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,6,7]
		which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(250,250))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + 80, self.rect.y + 100, 100, 150)
		
		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def toxic_bile(self, target, damage_text_group, inventory):
		target.hp -= math.ceil(self.strength / 3)

		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.ceil(self.strength / 3)), red)	
		damage_text_group.add(damage_text)		
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Toxic Bile', yellow)	
		damage_text_group.add(damage_text)	

		#check if target is dead
		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def vomit(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		vomit_animation = Vomit_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.bottom, target, damage_text_group, caster)
		monster_skill_sprite_group.add(vomit_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Vomit', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Zombie_Boss(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown)
		self.monster_turn_amount = monster_turn_amount
		self.monster_turn_threshold = monster_turn_threshold
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [4,5,6]
		which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(250,250))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + 95, self.rect.y + 60, 100, 200)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def scream(self, target, damage_text_group, monster_skill_sprite_group, inventory):
		target.temp_strength += -1 * (target.strength * 0.3)
		target.strength += -1 * (target.strength * 0.3)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'STR {target.temp_strength:.2f}', yellow)	
		damage_text_group.add(damage_text)

		target.temp_intelligence += -1 * (target.intelligence * 0.3)		
		target.intelligence += -1 * (target.intelligence * 0.3)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'INT {target.temp_intelligence:.2f}', yellow)	
		damage_text_group.add(damage_text)	

		target.hp -= self.strength * 0.75
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Scream', yellow)	
		damage_text_group.add(damage_text)	
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'{self.strength * 0.75:.2f}', red)	
		damage_text_group.add(damage_text)	

		scream_animation = Scream_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		monster_skill_sprite_group.add(scream_animation)

		#check if target is dead
		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def special_skill_1(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		vomit_animation = Vomit_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.bottom, target, damage_text_group, caster)
		monster_skill_sprite_group.add(vomit_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Vomit', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Golem_Boss(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, attack_cooldown)
		self.monster_turn_amount = monster_turn_amount
		self.monster_turn_threshold = monster_turn_threshold
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		number_of_pictures_list = [6,9,5]
		which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(which_state_list)):
			each_state_animation_list = []
			for i in range(number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(350,350))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + 75, self.rect.y + 75, self.rect.width - 75, self.rect.height - 75)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def special_skill_1(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		rock_slide_animation = Rock_Slide_Images((target.hitbox.x + target.hitbox.width / 2), -50, target, damage_text_group, caster)
		monster_skill_sprite_group.add(rock_slide_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Rock Slide', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def special_skill_2(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		stalagmite_animation = Stalagmite_Images((target.hitbox.x + target.hitbox.width / 2), 500, target, damage_text_group, caster)
		monster_skill_sprite_group.add(stalagmite_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Stalagmite', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

#----------------------------------------------------------------------------------hero skills
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

class Spark_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(10):
			img = pygame.image.load(f'Images/Icon/Fireball/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
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

class Lightning_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(9):
			img = pygame.image.load(f'Images/Icon/Lightning/{i}.png').convert_alpha()
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

class Cleave_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(4):
			img = pygame.image.load(f'Images/Icon/Cleave/{i}.png').convert_alpha()
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

class Zombie_Stab_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(4):
			img = pygame.image.load(f'Images/Icon/Zombie_Stab/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 14, img.get_height() * 2))
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

class Water_Blast_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Water_Blast/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 8, (img.get_height() * 2) - 30))
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

class Thunder_Bolt_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Thunder_Bolt/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 12, (img.get_height() * 2) - 30))
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

class Venomous_Whip_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Venomous_Whip/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 5, (img.get_height() * 5)))
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

class Sapphire_Flame_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(10):
			img = pygame.image.load(f'Images/Icon/Sapphire_Flame/{i}.png').convert_alpha()
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

class Sapphire_Spark_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(10):
			img = pygame.image.load(f'Images/Icon/Sapphire_Flame/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
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

class Lunar_Beam_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(7):
			img = pygame.image.load(f'Images/Icon/Lunar_Beam/{i}.png').convert_alpha()
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

class Solar_Beam_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(7):
			img = pygame.image.load(f'Images/Icon/Solar_Beam/{i}.png').convert_alpha()
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

class Eclipse_Beam_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(7):
			img = pygame.image.load(f'Images/Icon/Eclipse_Beam/{i}.png').convert_alpha()
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

class Serpent_Wheel_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	

		self.image = pygame.image.load(f'Images/Icon/Serpent_Wheel/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 3), (self.image.get_height() * 3)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.rect.x += 12
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			self.image = pygame.transform.rotate(self.image, 90)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000:
			self.kill()

class Bleed_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.inventory = inventory
		self.experiencethreshold = experiencethreshold
		self.monster_list = monster_list
		self.monster_index = monster_index
		self.skills_list = skills_list
		self.inventory = inventory
		self.hero = hero

		self.image = pygame.image.load(f'Images/Icon/Bleed/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y - (target.hitbox.height * 0.5))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			if -3 in self.inventory:
				self.damage_time = pygame.time.get_ticks()
				damage = float(f'{(self.target.hp * 0.035):.2f}')
				self.target.hp -= damage
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.target.hp * 0.035):.2f}', red)	
				self.damage_text_group.add(damage_text)

				if self.hero.max_hp - self.hero.hp > damage * 0.1:
					heal_amount = damage * 0.1
				else:
					heal_amount = self.hero.max_hp - self.hero.hp
				self.hero.hp += heal_amount
				damage_text = Damage_Text((self.hero.hitbox.x + self.hero.hitbox.width / 2) + random.randint(-60,60), self.hero.hitbox.y + random.randint(-60,60), f'{heal_amount:.2f}', green)	
				self.damage_text_group.add(damage_text)

			else:
				self.damage_time = pygame.time.get_ticks()
				damage = float(f'{(self.target.hp * 0.01):.2f}')
				self.target.hp -= damage
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.target.hp * 0.01):.2f}', red)	
				self.damage_text_group.add(damage_text)	

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			self.image = pygame.transform.rotate(self.image, 90)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 2000 or self.target.alive == False:
			self.kill()

class Poison_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list):
		pygame.sprite.Sprite.__init__(self)
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.inventory = inventory
		self.experiencethreshold = experiencethreshold
		self.monster_list = monster_list
		self.monster_index = monster_index
		self.skills_list = skills_list
		self.inventory = inventory
		self.hero = hero

		self.animation_list = []
		self.frame_index = 0	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Poison/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y - (target.hitbox.height * 0.5))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.image = self.animation_list[self.frame_index]	

		if pygame.time.get_ticks() - self.damage_time > 1000 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			damage = float(f'{(self.target.max_hp * 0.01):.2f}')
			self.target.hp -= damage
			damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.target.max_hp * 0.01):.2f}', red)	
			self.damage_text_group.add(damage_text)	
			self.target.monster_turn_amount -= self.target.monster_turn_threshold * 0.2
			damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'TURN -20%', red)	
			self.damage_text_group.add(damage_text)	
			if self.target.monster_turn_amount < 0:
				self.target.monster_turn_amount = 0

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
			if self.frame_index > len(self.animation_list) - 1:
				self.frame_index = 0

		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 3100 or self.target.alive == False:
			self.kill()

#----------------------------------------------------------------------------------monster skills
class Scream_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Enemy/ZombieBoss/Scream/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
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

class Vomit_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, damage_text_group, caster):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.caster = caster

		for i in range(6):
			img = pygame.image.load(f'Images/Enemy/EnemySkills/Vomit/Vomit{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y - (target.hitbox.height * 0.5))

		self.hitbox = pygame.rect.Rect(self.target.hitbox.x, self.target.hitbox.y, 20, 20)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.Rect.colliderect(self.target.hitbox, self.hitbox) and pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			self.target.hp -= 3
			damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{3}', red)	
			self.damage_text_group.add(damage_text)		
			#check if target is dead
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		#handle animation
		#update image
		self.image = self.animation_list[self.frame_index]
		#check if enough time has passes since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			if self.frame_index == len(self.animation_list) - 1:
				pass
			else:
				self.frame_index += 1
		#if animation runs out then delete it
		if self.frame_index == len(self.animation_list) - 1:
			if pygame.time.get_ticks() - self.cast_time > 5000 or self.caster.alive == False:
				self.kill()

class Rock_Slide_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, damage_text_group, caster):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.caster = caster

		self.image = pygame.image.load(f'Images/Enemy/EnemySkills/RockSlide/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 3) - 75, (self.image.get_height() * 3) - 75))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.rect.y += 2
		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.rect, self.target.hitbox):
				self.target.hp -= float(f'{10 + (self.target.max_hp * 0.05):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{10 + (self.target.max_hp * 0.05):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			#check if target is dead
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			self.image = pygame.transform.rotate(self.image, 90)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 2000 or self.caster.alive == False:
			self.kill()

class Stalagmite_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, damage_text_group, caster):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.caster = caster

		self.image = pygame.image.load(f'Images/Enemy/EnemySkills/Stalagmite/2.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 3) - 75, (self.image.get_height() * 4)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y + 75)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.time.get_ticks() - self.cast_time > 600:
			if self.rect.y != self.target.hitbox.y:
				self.rect.y -= 3
		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.rect, self.target.hitbox):
				self.target.hp -= float(f'{15 + (self.target.max_hp * 0.05):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{15 + (self.target.max_hp * 0.05):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 3000 or self.caster.alive == False:
			self.kill()

#----------------------------------------------------------------------------------misc
class Damage_Text(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = damage_font.render(damage, True, color)
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0

	def update(self):
		#float damage text up
		self.rect.y -= 0.25
		#delete text after few counters
		self.counter += 1
		if self.counter > 120:
			self.kill()

def Random_Stats_Hero(random_stats_list):
	while True:
		start_random_integer = 26
		start_random_strength = random.randint(8, 10)
		start_random_intelligence = random.randint(8, 10)
		start_random_endurance = random.randint(2, 5)
		start_random_agility = random.randint(2, 5)
		start_random_luck = random.randint(0, 3)
		if start_random_integer - 5 < start_random_luck + start_random_agility + start_random_endurance + start_random_strength + start_random_intelligence < start_random_integer:
			random_stats_list.append(start_random_strength)
			random_stats_list.append(start_random_intelligence)
			random_stats_list.append(start_random_agility)
			random_stats_list.append(start_random_luck)
			random_stats_list.append(start_random_endurance)
			break	

def Random_Stats_Monsters(random_stats_list_monsters):
	while True:
		start_random_integer = 13
		start_random_strength = random.randint(4, 5)
		start_random_intelligence = random.randint(0, 1)
		start_random_endurance = random.randint(2, 4)
		start_random_agility = random.randint(1, 4)
		start_random_luck = random.randint(1, 4)
		if start_random_integer - 5 < start_random_luck + start_random_agility + start_random_endurance + start_random_strength + start_random_intelligence < start_random_integer:
			random_stats_list_monsters.append(start_random_strength)
			random_stats_list_monsters.append(start_random_intelligence)
			random_stats_list_monsters.append(start_random_agility)
			random_stats_list_monsters.append(start_random_luck)
			random_stats_list_monsters.append(start_random_endurance)
			break	
