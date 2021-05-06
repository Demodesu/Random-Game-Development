import math, pygame, random, sys

pygame.init()

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
statbutton_img = pygame.image.load('Images/Icon/StatButton.png').convert_alpha()
damage_font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 25)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
			
class Character():
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance):
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
				if self.action == 3:
					self.frame_index = len(self.animation_list[self.action]) - 1
				else:
					self.idle()

	def draw(self):
		screen.blit(self.image, self.rect)
		#check hitbox
		# pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
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

	def attack(self, target, damage_text_group, inventory):

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = math.floor(abs(randdamage) * 1.5)

		if (randdamage + self.strength) - (target.defense + (target.endurance / 5)) <= 0:
			damage = 0
		else:
			damage = (randdamage + self.strength) - (target.defense + (target.endurance / 5))

		if 7 in inventory:
			if self.shield > 0:
				if self.shield - math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15)  >= 0:
					self.shield -= math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15) 
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, '0', red)
				else:
					self.hp -= (self.shield - math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15)) * -1
					self.shield = 0
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, str((self.shield - math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15)) * -1), red)
			else:
				self.hp -= math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15) 
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, str(math.ceil(target.defense * 0.25) + math.ceil(damage * 0.15)), red)
			damage_text_group.add(damage_text)

			if self.hp < 1:
				self.hp = 0
				self.alive = False
				self.death()

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

		if 19 in inventory:
			target.hp += damage * 0.15
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'{damage * 0.15:.2f}', green)
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

	def guard(self, skill_sprite_group, damage_text_group):
		self.shield += math.floor((self.max_hp * 0.2) + (self.defense * 0.5))
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, 'Guard ' + str(math.floor((self.max_hp * 0.2) + (self.defense * 0.5))), yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)

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
	def level_up_monster(self, hero):
		self.max_hp += random.randint(1,3)
		self.hp = self.max_hp
		self.experience += (self.level * 3.5) + (hero.experience * 0.02)
		if self.gold < 400:
			self.gold += (self.gold * 0.15)	 
		else:
			self.gold += 2
		self.level += 1

		if self.level >= 30:
			self.strength += random.randint(0,1) * 0.8
		else:
			self.strength += random.randint(0,1) * 0.5

		if self.level >= 30:
			self.luck += random.randint(0,1) * 0.8
		else:
			self.luck += random.randint(0,1) * 0.5

		if self.level >= 30:
			self.endurance += random.randint(0,1) * 0.8
		else:
			self.endurance += random.randint(0,1) * 0.5

		if self.level >= 30:
			self.agility += random.randint(0,1) * 0.8
		else:
			self.agility += random.randint(0,1) * 0.5

		if self.level >= 30:
			self.max_hp += 2

		if self.level % 4:
			self.speed += 0.125
		if self.endurance % 6 == 0:
			self.hp_regen += 0.25
			self.max_hp += 2
		if self.strength % 6 == 0:
			self.defense += 0.25

		if hero.strength > (hero.luck + hero.agility + hero.intelligence + hero.endurance):
			self.speed += 1.5
		if hero.luck > (hero.strength + hero.agility + hero.intelligence + hero.endurance):
			self.speed += 1.5
		if hero.agility > (hero.luck + hero.strength + hero.intelligence + hero.endurance):
			self.speed += 1.5
		if hero.intelligence > (hero.luck + hero.agility + hero.strength + hero.endurance):
			self.speed += 1.5
		if hero.endurance > (hero.luck + hero.agility + hero.intelligence + hero.strength):
			self.speed += 1.5
	#---------------------------------------------------------#


class Hero(Character):
	def	__init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_amount, stamina_recovery, stamina_threshold, turn_amount, turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, fireball_charge, lightning_charge):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance)
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
		#added stats
		self.added_strength = added_strength
		self.added_intelligence = added_intelligence
		self.added_agility = added_agility
		self.added_luck = added_luck
		self.added_endurance = added_endurance
		#consumables
		self.fireball_charge = fireball_charge
		self.lightning_charge = lightning_charge
		#animation
		self.animation_list = [] #this is the hero's animation list -> hero.animation_list[]
		self.frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills, 5 = counter
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills; 5 = counter; 6 = attack2; 7 = attack3; 8 = critical; 9 = attack4; 10 = guard; 11 = stomp; 12 = attack5; 13 = Stab run loop to load each set of animation
		number_of_pictures_list = [4,3,4,5,6,3,3,3,4,4,3,5,5,9]
		which_state_list = ['Idle', 'Attack', 'Hurt', 'Death', 'Skill', 'Counter', 'Attack2', 'Attack3', 'Critical', 'Attack4', 'Guard', 'Stomp', 'Attack5', 'Stab']
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

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

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
		self.strength += 0.5
		self.added_strength += 0.5
		self.statpoints -= 1
		if self.added_strength == 2:
			self.defense += 0.25
			self.added_strength = 0

	def int_up_button(self):
		self.intelligence += 0.5
		self.added_intelligence += 0.5
		self.statpoints -= 1
		if self.added_intelligence == 2:
			self.max_mp += 5
			self.mp += 5
			self.mp_regen += 0.5
			self.added_intelligence = 0

	def end_up_button(self):
		self.endurance += 0.5
		self.added_endurance += 0.5
		self.statpoints -= 1
		if self.added_endurance == 2:
			self.max_hp += 5
			self.hp += 5
			self.hp_regen += 0.5
			self.added_endurance = 0

	def luc_up_button(self):
		self.luck += 0.5
		self.added_luck += 0.5
		self.statpoints -= 1	

	def agi_up_button(self):
		self.agility += 0.5
		self.added_agility += 0.5
		self.statpoints -= 1

	def drop_items(self, target, inventory, monster_list, monster_index, skills_list):
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
				if 17 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 75:
						inventory.append(17)
						self.stamina_threshold -= 50
			if target.level > 2 and (monster_index == 0 or monster_index == 3):
				if 11 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 85:
						inventory.append(11)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.speed -= 0.5
			if target.level > 3:
				if 12 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 85:
						inventory.append(12)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.hp_regen -= 1
			if target.level > 0 and (monster_index == 1 or monster_index == 2 or monster_index == 3):
				if 14 not in inventory:
					if monster_index == 1:
						rollitemactive = random.randint(0,100)
					else:
						rollitemactive = random.randint(90,100)
					if rollitemactive > 95:
						inventory.append(14)
						skills_list.append('zombie_stab')
			if target.level > 10:
				if 22 not in inventory:
					rollitemactive = random.randint(0,100)
					if rollitemactive > 80:
						inventory.append(22)
						for monster_group in monster_list:
							for monster in monster_group:
								monster.defense -= 2

#----------------------------------------------------------------------------------right click
	def counter(self, right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skills_list):

		counter_chance = False
		counter_time = pygame.time.get_ticks()

		if counter_time - monster_attack_time < 400:
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
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, str(heal_amount), green)
				damage_text_group.add(heal_text)

			#run target hurt animation
			target.hurt()

			#check if target is dead
			self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

			#set variables to attack animation
			self.action = 5
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

		else:
			counter_text = Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, 'Counter Failed', red)

		damage_text_group.add(counter_text)

		return counter_chance, counter_time

	def triple_combo(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, skills_list):

		limb_list = ['head', 'body', 'leg']

		for stabs in range(3):

			target_limb = limb_list[stabs]

			damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			damage = damage * 0.75

			self.shield_and_damage_calculation(target, damage, damage_text_group)

			if 4 in inventory:
				if self.max_hp - self.hp > math.ceil(damage * 0.1):
					heal_amount = math.ceil(damage * 0.1)
				else:
					heal_amount = self.max_hp - self.hp
				self.hp += heal_amount
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), str(heal_amount), green)
				damage_text_group.add(heal_text)

		#set variables to attack animation
		self.action = 13
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		#run target hurt animation
		target.hurt()

		#check if target is dead
		self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

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
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), str((target.shield - math.floor(damage)) * -1), red)
		else:
			target.hp -= math.floor(damage)
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), str(math.floor(damage)), red)
		damage_text_group.add(damage_text)

	def monster_death_drops(self, target, experiencethreshold, inventory, monster_list, monster_index, skills_list):
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
			self.gold += target.gold
			self.experience += target.experience + math.floor(random.randint(-2,2) * 1.5)
			self.level_up_hero(experiencethreshold)		
			self.drop_items(target, inventory, monster_list, monster_index, skills_list)

	def attack(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list):

		damage, roll_crit_chance = self.critical_and_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

		self.shield_and_damage_calculation(target, damage, damage_text_group)

		if 4 in inventory:
			if self.max_hp - self.hp > math.ceil(damage * 0.1):
				heal_amount = math.ceil(damage * 0.1)
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), str(heal_amount), green)
			damage_text_group.add(heal_text)

		#set variables to attack animation
		roll_attack_animation = random.randint(0,2)
		if roll_attack_animation == 0:
			self.action = 1
		elif roll_attack_animation == 1:
			self.action = 6
		else:
			self.action = 7
		if roll_crit_chance + (self.luck * 0.25) > 50:
			critical_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y - random.randint(30,60), 'CRITICAL', red)
			damage_text_group.add(critical_text)
			self.action = 8
		if target_limb == 'leg':
			self.action = 9
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		if 18 in inventory and random.randint(0,100) > 50:

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
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), str(heal_amount), green)
				damage_text_group.add(heal_text)

			self.action = 12
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	

		if 24 in inventory and random.randint(0,100) > 75:
			self.stomp(target, damage_text_group, monster_list, monster_index, skills_list)

		#run target hurt animation
		target.hurt()

		#check if target is dead
		self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

	def cleave(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

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
						heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(monster) + 1), str(heal_amount), green)
						damage_text_group.add(heal_text)

				cleave_animation = Cleave_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
				skill_sprite_group.add(cleave_animation)

				#run target hurt animation
				target.hurt()

				#check if target is dead
				self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

		#set variables to attack animation
		self.action = 7
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def zombie_stab(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list):

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
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 * (monster_list[monster_index].index(target) + 1), str(heal_amount), green)
				damage_text_group.add(heal_text)

		#run target hurt animation
		target.hurt()

		#check if target is dead
		self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

		zombie_stab_animation = Zombie_Stab_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
		skill_sprite_group.add(zombie_stab_animation)

		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

#----------------------------------------------------------------------------------guard and skills
	def guard(self, skill_sprite_group, damage_text_group, skills_list):

		self.shield += math.floor((self.max_hp * 0.3) + self.defense)
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, str(math.floor((self.max_hp * 0.5) + self.defense)), yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)
		if 'guard_heal' in skills_list:
			if self.max_hp - self.hp > math.floor((self.max_hp * 0.05) + (self.defense * 0.5)):
				heal_amount = math.floor((self.max_hp * 0.05) + (self.defense * 0.5))
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, str(heal_amount), green)			
			damage_text_group.add(heal_text)

		self.action = 10
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def stomp(self, target, damage_text_group, monster_list, monster_index, skills_list):

		for monster in monster_list[monster_index]:
			if monster.alive != False:
				if len(monster_list[monster_index]) != 1:
					monster.monster_turn_amount -= monster.monster_turn_threshold * 0.2
					damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -20%', yellow)	
					damage_text_group.add(damage_text)	
				else:
					monster.monster_turn_amount -= monster.monster_turn_threshold * 0.15
					damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -15%', yellow)	
					damage_text_group.add(damage_text)					
			if monster.monster_turn_amount <= 0:
				monster.monster_turn_amount = 1

		if 'stomp_buff' in skills_list:
			self.temp_strength += 3
			self.temp_agility += 3
			self.strength += self.temp_strength
			self.agility += self.temp_agility

			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'STR +3', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'AGI +3', yellow)	
			damage_text_group.add(damage_text)	

		self.action = 11
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def fireball(self, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list):

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				randdamage = random.randint(-3,3)
				if randdamage + (self.intelligence * 1.8) <= 0:
					damage = 0
				else:
					damage = randdamage + (self.intelligence * 1.8)
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

				#run target hurt animation
				target.hurt()

				#check if target is dead
				self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def lightning(self, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list):

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				randdamage = random.randint(-3,3)
				if randdamage + (self.intelligence * 1.5) <= 0:
					damage = 0
				else:
					damage = randdamage + (self.intelligence * 1.5)
				target.hp -= math.floor(damage)
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.floor(damage)), red)
				damage_text_group.add(damage_text)

				lightning_animation = Lightning_Images(target.x, target.y)
				skill_sprite_group.add(lightning_animation)

				#run target hurt animation
				target.hurt()

				#check if target is dead
				self.monster_death_drops(target, experiencethreshold, inventory, monster_list, monster_index, skills_list)

		#set variables to attack animation
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Slime(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance)
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
		self.hitbox = pygame.rect.Rect(self.x - 35, self.y - 25, 70, 70)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def armor_corrosion(self, target, damage_text_group, inventory):
		if target.shield > 0:
			shield_destroyed = target.shield
			target.shield = 0
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(shield_destroyed), yellow)
			damage_text_group.add(damage_text)

		target.hp -= math.ceil(self.strength / 4)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, str(math.ceil(self.strength / 4)), red)

		damage_text_group.add(damage_text)
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Armor Corrosion', yellow)	
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

class Zombie(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance)
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
		self.hitbox = pygame.rect.Rect(self.x - 50, self.y - 25, 100, 150)
		
		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def toxic_bile(self, target, damage_text_group, inventory):
		target.hp -= math.ceil(self.strength / 3)

		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(math.ceil(self.strength / 3)), red)	
		damage_text_group.add(damage_text)		
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Toxic Bile', yellow)	
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

class Zombie_Boss(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount, monster_turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance)
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
		self.hitbox = pygame.rect.Rect(self.x - 25, self.y - 60, 100, 200)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

	def scream(self, target, damage_text_group, monster_skill_sprite_group, inventory):
		self.temp_strength = -1 * (target.strength * 0.3)
		self.temp_intelligence = -1 * (target.intelligence * 0.3)
		target.strength += self.temp_strength
		target.intelligence += self.temp_intelligence
		target.hp -= self.strength * 0.75

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Scream', yellow)	
		damage_text_group.add(damage_text)	
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'STR {self.temp_strength:.2f}', yellow)	
		damage_text_group.add(damage_text)
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'INT {self.temp_intelligence:.2f}', yellow)	
		damage_text_group.add(damage_text)		
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'{self.temp_strength * 0.75:.2f}', red)	
		damage_text_group.add(damage_text)	

		scream_animation = Scream_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		monster_skill_sprite_group.add(scream_animation)

		#run target hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 0
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

#----------------------------------------------------------------------------------monster skills
class Scream_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Zombie Boss/Scream/{i}.png').convert_alpha()
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
