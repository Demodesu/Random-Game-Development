import math, pygame, random, sys, ctypes

pygame.init()

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
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.35)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#

damage_font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 25)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (255,255,255)	

def rot_center(image, angle, x, y):
	rotated_image = pygame.transform.rotate(image, angle)
	new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

	return rotated_image, new_rect

def calculate_randians(source, target):
	radians = math.atan2((target.hitbox.y + (target.original_hitbox.height * 0.5)) - (source.hitbox.y + (source.original_hitbox.height * 0.5)), (target.hitbox.x + (target.original_hitbox.width * 0.5)) - (source.hitbox.x + (source.original_hitbox.width * 0.5)))
	dx, dy = math.cos(radians), math.sin(radians)

	return dx, dy

class Game_Option_And_Variables():
	def __init__(self):
		self.show_hitbox = False
		self.music_on = False

class Character():
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
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
		#monster skill time
		self.monster_skill_time = 400
		#attack length
		self.attack_length = screen_width * 0.15
		#distance
		self.distance = 0
	#---------------------------------------------------------#
	def collide_damage(self, hero, damage_text_group, start_combat_time):
		if pygame.Rect.colliderect(self.hitbox, hero.hitbox) and start_combat_time % 25 == 0 and self.alive == True:
			hero.hp -= float(f'{self.strength * 1.5:.2f}')
			damage_text = Damage_Text((hero.hitbox.x + hero.hitbox.width / 2) + random.randint(-60,60), hero.hitbox.y + random.randint(-60,60), f'{self.strength * 1.5:.2f}', red)	
			damage_text_group.add(damage_text)	

	def y_momentum_calculation(self, hero):
		if self.rect.bottom < bottom_of_bottom_panel and self.alive == True:
			radians = math.atan2((hero.hitbox.y + (hero.original_hitbox.height * 0.5)) - self.hitbox.y, (hero.hitbox.x + (hero.original_hitbox.width * 0.5)) - self.hitbox.x)
			dy = math.sin(radians)
			self.rect.y += self.y_momentum * self.weight
			if pygame.time.get_ticks() - self.movement_time > 200:
				self.y_momentum += self.y_momentum_reduction_rate
				self.movement_time = pygame.time.get_ticks()

		if self.rect.bottom >= bottom_of_bottom_panel:
			self.rect.bottom = bottom_of_bottom_panel
			self.y_momentum = 0

	def reposition_hitboxes(self):
		self.hitbox.x = self.rect.x + self.hitbox_x_offset
		self.hitbox.y = self.rect.y + self.hitbox_y_offset		
		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

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
			else:
				self.idle()				

	def draw(self, game_variables):
		screen.blit(self.image, self.rect)
		#check hitbox
		#pygame.draw.rect(screen,(255,0,0),self.rect,2)
		if game_variables.show_hitbox == True:
			pygame.draw.rect(screen,(0,255,0),self.hitbox,2)
			pygame.draw.circle(screen, (255,0,0), (self.hitbox.x + self.original_hitbox.width * 0.5, self.hitbox.y + self.original_hitbox.height * 0.5), self.attack_length,2)
			pygame.draw.circle(screen, (255,0,0), (self.hitbox.x + (self.original_hitbox.width * 0.5) - 2.5, self.hitbox.y + (self.original_hitbox.height * 0.5) - 2.5), 5)
		#test = pygame.rect.Rect(0, bottom_of_bottom_panel, screen_width, bottom_of_bottom_panel)
		#pygame.draw.rect(screen,(0,255,0),test,2)
		#pygame.draw.rect(screen,(255,0,0),self.head_hitbox,2)
		#pygame.draw.rect(screen,(255,0,0),self.body_hitbox,2)
		#pygame.draw.rect(screen,(255,0,0),self.leg_hitbox,2)	
	#---------------------------------------------------------#
	#animations
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def short_idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 3
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to attack animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def monster_physical_damage_calculation(self, target, damage_text_group):

		limb_target_chance = random.randint(0,1)
		limb_list = ['head', 'body']

		target_limb = limb_list[limb_target_chance]

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = float(f'{(abs(randdamage) * 1.5) + (0.25 * self.strength):.2f}')

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

		if (randdamage + self.strength) - (target.defense + (target.endurance * 0.1)) <= 0:
			damage = 0
		else:
			damage = (randdamage + self.strength) - (target.defense + (target.endurance * 0.1))

		return damage * 4, roll_crit_chance

	def monster_shield_and_damage_calculation(self, target, damage, damage_text_group):
		if target.shield > 0:
			if target.shield - float(f'{damage:.2f}') >= 0:
				target.shield -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), '0', red)
			else:
				target.hp -= (target.shield - float(f'{damage:.2f}')) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{(target.shield - damage) * -1:.2f}', red)
		else:
			target.hp -= float(f'{damage:.2f}')
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{damage:.2f}', red)
		damage_text_group.add(damage_text)

	def attack(self, target, damage_text_group, inventory, experiencethreshold, monster_list, monster_index):

		damage, roll_crit_chance = self.monster_physical_damage_calculation(target, damage_text_group)

		self.monster_shield_and_damage_calculation(target, damage, damage_text_group)

		if 7 in inventory and -1 in inventory:
			if self.shield > 0:
				if float(f'{self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8):.2f}')  >= 0:
					self.shield -= float(f'{((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8):.2f}') 
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, '0', red)
				else:
					self.hp -= float(f'{(self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8) * -1):.2f}')
					self.shield = 0
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8) * -1):.2f}', red)
			else:
				self.hp -= float(f'{(((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8)):.2f}')
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.8)):.2f}', red)
			damage_text_group.add(damage_text)

		elif 7 in inventory and -1 not in inventory:
			if self.shield > 0:
				if float(f'{self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15):.2f}')  >= 0:
					self.shield -= float(f'{((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15):.2f}') 
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, '0', red)
				else:
					self.hp -= float(f'{(self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15) * -1):.2f}')
					self.shield = 0
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.shield - ((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15) * -1):.2f}', red)
			else:
				self.hp -= float(f'{(((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15)):.2f}')
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(((target.defense + (target.endurance * 0.1)) * 0.25) + (damage * 0.15)):.2f}', red)
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
		self.shield += float(f'{(self.max_hp * 0.2) + (self.defense * 0.5):.2f}')
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, 'Guard ' + f'{(self.max_hp * 0.2) + (self.defense * 0.5):.2f}', yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)

	#---------------------------------------------------------#
	#level up
	def level_up_monster(self, hero):
		self.max_hp += random.randint(2,4)

		self.experience += (self.level * 5) + (hero.experience * 0.05)
		if self.gold < 200 + hero.level * 15:
			self.gold += random.randint(10,15) + (self.gold * 0.025)	 
		else:
			self.gold += random.randint(10,15)
		self.level += 1

		if self.level >= 40:
			self.strength += random.randint(0,1)
		else:
			self.strength += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.luck += random.randint(0,1)
		else:
			self.luck += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.endurance += random.randint(0,1)
		else:
			self.endurance += random.randint(0,1) * 0.5

		if self.level >= 40:
			self.agility += random.randint(0,1)
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

		self.hp = self.max_hp
	#---------------------------------------------------------#

class Hero(Character):
	def	__init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		#sound fx
		self.sword_sound_effect = pygame.mixer.Sound(f'Music/Hero/Sword_Sound_Effects1.mp3')
		self.running_sound_effect = pygame.mixer.Sound(f'Music/Hero/Hero_Run.mp3')
		self.attack_sound_effect_list = []
		for sound in range(5):
			sound_effect = pygame.mixer.Sound(f'Music/Hero/Attack_Sound_Effects{sound}.mp3')
			self.attack_sound_effect_list.append(sound_effect)				
		#distance hero to monster
		self.hero_to_monster_distance = 0
		#lock target
		self.lock_target = False
		self.lock_target_index = 0
		#consumables
		self.consumables_list = []
		self.active_consumables_list = []	
		self.consumables_in_inventory_list = []
		self.consumables_combination_list = []
		self.consumables_cost = 400
		self.consumables_combination_cost = 500
		self.consumable_wait_time = 0
		self.orb_limit_cost = 2000
		self.heal_and_restore_consumable_cost = 500
		#combination cost
		self.combination_cost = 500
		#skills list
		self.active_skills_list = ['normal_attack']
		self.skills_list = ['normal_attack']
		self.all_active_skills_list = ['normal_attack', 'cleave', 'zombie_stab', 'triple_combo', 'serpent_wheel', 'venomous_whip', 'thunder_bolt']
		#debuff time
		self.scream_debuff_time = 0	
		#buff time
		self.stomp_buff_time = 0
		self.temp_strength_stomp = 0
		self.temp_agility_stomp = 0
		self.temp_endurance_stomp = 0
		#start stat points
		self.start_statpoints = 0
		#attack time
		self.base_attack_time = 100
		self.attack_time = 0
		self.attack_cooldown_rate = 1
		#attack length
		self.attack_length = screen_width * 0.25
		#current stat points
		self.statpoints = 0
		#start mana potions
		self.start_mana_potion = 1
		#mana potions
		self.mana_potion = 1
		#stamina
		self.stamina_recovery = 10
		self.stamina_threshold = 10000
		self.stamina_amount = 0
		#turn
		self.turn_threshold = 10000
		self.turn_amount = 0
		#stat bonuses
		self.added_strength = 0
		self.added_intelligence = 0
		self.added_endurance = 0
		self.added_luck = 0
		self.added_agility = 0
		#consumables
		self.orb_limit = 2
		#item counters
		self.hibiscus_pixels_moved = 0
		self.phoenix_spark_moved = 0
		self.dragon_item_counter = 0
		self.dragon_item_counter_threshold = 3
		self.heavy_attack_obsidian_counter = 0
		#animation
		self.animation_list = [] #this is the hero's animation list -> hero.animation_list[]
		self.frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead; 4 = skills, 5 = counter
		self.update_time = pygame.time.get_ticks()
		#attack bleed
		self.attack_bleed_counter = 0
		#mist vortex
		self.mist_vortex_time = 0
#----------------------------------------------------------------------------------movement variables
		self.running_right = False
		self.running_left = False
		self.facing_right = True
		self.facing_left = False
		self.pixels_moved_right = 0
		self.pixels_moved_left = 0
		self.player_movement = [0,0]
		self.player_y_momentum = 0
		self.player_x_momentum = 0
		self.jump_counter = 0 
		self.jump_cooldown = 0
		self.on_ground = False
		self.roll_speed_increase_time = 0
		self.player_x_speed = 0 
		self.stand_still_cooldown = 0 	
		self.roll_cooldown = 0	
#----------------------------------------------------------------------------------load images
		#5 animation states; 0 = idle; 1 = attack; 2 = dead; 3 = skills; 4 = counter; 5 = attack2; 6 = attack3; 7 = critical; 8 = attack4; 9 = guard; 10 = stomp; 11 = attack5; 12 = Stab; 13 = move front; 14 = move back; 15 = move front attack; 16 = move back attack; 17 = triple head; 18 = whip; 19 = throw;20 = jump;21 = roll;22 = roll back; 23 = run left; 24 = run right attack run loop to load each set of animation
		self.number_of_pictures_list = [4,3,5,6,3,3,3,4,4,3,5,5,9,2,2,3,2,9,4,4,2,6,6,4,4,4]
		self.which_state_list = ['Idle', 'Attack', 'Death', 'Skill', 'Counter', 'Attack2', 'Attack3', 'Critical', 'Attack4', 'Guard', 'Stomp', 'Attack5', 'Stab', 'MoveFront', 'MoveBack', 'MoveFrontAttack', 'MoveBackAttack', 'TripleHead', 'Whip', 'Throw', 'Jump', 'Roll', 'RollBack', 'RunLeft', 'RunRight', 'RunFacingMonster']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.175),height(0.175)))
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
#----------------------------------------------------------------------------------rect
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.width * 0.3, self.rect.height * 0.55)
		self.original_hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.width * 0.3, self.rect.height * 0.55)

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)
#----------------------------------------------------------------------------------pets attributes
		self.pet_active_time = 0
		self.pet_damage_time = pygame.time.get_ticks()

		self.ghost_pet_original_image = pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics15.png').convert_alpha()
		self.ghost_pet_angle = 0
		self.ghost_pet_image = self.ghost_pet_original_image.copy()
		self.ghost_pet_rect = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, 10, 10)
		self.ghost_pet_update_time = pygame.time.get_ticks()	
#----------------------------------------------------------------------------------consumables
		self.fire_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls0.png').convert_alpha()
		self.fire_orb_image_not_in_use = pygame.transform.scale(self.fire_orb_image,(width(0.01),height(0.01)))
		self.fire_orb_image_in_use = pygame.transform.scale(self.fire_orb_image,(width(0.02),height(0.02)))		
		self.lightning_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls1.png').convert_alpha()	
		self.lightning_orb_image_not_in_use = pygame.transform.scale(self.lightning_orb_image,(width(0.01),height(0.01)))	
		self.lightning_orb_image_in_use = pygame.transform.scale(self.lightning_orb_image,(width(0.02),height(0.02)))	
		self.flame_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls2.png').convert_alpha()	
		self.flame_orb_image_not_in_use = pygame.transform.scale(self.flame_orb_image,(width(0.01),height(0.01)))		
		self.flame_orb_image_in_use = pygame.transform.scale(self.flame_orb_image,(width(0.02),height(0.02)))	
		self.frost_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls3.png').convert_alpha()	
		self.frost_orb_image_not_in_use = pygame.transform.scale(self.frost_orb_image,(width(0.01),height(0.01)))		
		self.frost_orb_image_in_use = pygame.transform.scale(self.frost_orb_image,(width(0.02),height(0.02)))		
		self.heal_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls4.png').convert_alpha()	
		self.heal_orb_image_not_in_use = pygame.transform.scale(self.heal_orb_image,(width(0.01),height(0.01)))		
		self.heal_orb_image_in_use = pygame.transform.scale(self.heal_orb_image,(width(0.02),height(0.02)))	
		self.restore_orb_image = pygame.image.load('Images/Icon/ElementalBalls/ElementalBalls5.png').convert_alpha()	
		self.restore_orb_image_not_in_use = pygame.transform.scale(self.restore_orb_image,(width(0.01),height(0.01)))		
		self.restore_orb_image_in_use = pygame.transform.scale(self.restore_orb_image,(width(0.02),height(0.02)))				
#----------------------------------------------------------------------------------functions
	def draw_consumables(self, start_combat_time):

		mousex, mousey = pygame.mouse.get_pos()

		for count, orbs in enumerate(self.consumables_list):
			if count != 0:
				self.orb = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, 10, 10)													
				self.orb.x = mousex - width(0.005) + (math.cos((3.14 + count) + (start_combat_time * float(f'{count * 0.002 + 0.025}'))) * 25) + (math.sin((3.14 * (count + 1)) + (start_combat_time * float(f'{count * 0.002 + 0.025}'))) * 25)
				self.orb.y = mousey - height(0.005) + (math.cos((3.14 * (count + 1)) + (start_combat_time * float(f'{count * 0.002 + 0.025}'))) * 25) + (math.sin((3.14 + count) + (start_combat_time * float(f'{count * 0.002 + 0.025}'))) * 25)
				# self.orb.x = mousex - width(0.005) - (math.cos(((6.28 / len(self.consumables_list)) * count) + start_combat_time * 0.025) * 50)
				# self.orb.y = mousey - height(0.005) - (math.sin(((6.28 / len(self.consumables_list)) * count) + start_combat_time * 0.025) * 50)
				if self.consumables_list[count] == 'Fireball':
					image = self.fire_orb_image_not_in_use
				elif self.consumables_list[count] == 'Lightning':
					image = self.lightning_orb_image_not_in_use
				elif self.consumables_list[count] == 'Flameball':
					image = self.flame_orb_image_not_in_use
				elif self.consumables_list[count] == 'Frost':
					image = self.frost_orb_image_not_in_use		
				elif self.consumables_list[count] == 'Heal':
					image = self.heal_orb_image_not_in_use	
				elif self.consumables_list[count] == 'Restore':
					image = self.restore_orb_image_not_in_use				
				screen.blit(image, self.orb)
			else:
				self.orb = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, 10, 10)
				self.orb.x = mousex - width(0.01)
				self.orb.y = mousey - height(0.01)
				if self.consumables_list[count] == 'Fireball':
					image = self.fire_orb_image_in_use
				elif self.consumables_list[count] == 'Lightning':
					image = self.lightning_orb_image_in_use
				elif self.consumables_list[count] == 'Flameball':
					image = self.flame_orb_image_in_use
				elif self.consumables_list[count] == 'Frost':
					image = self.frost_orb_image_in_use	
				elif self.consumables_list[count] == 'Heal':
					image = self.heal_orb_image_in_use	
				elif self.consumables_list[count] == 'Restore':
					image = self.restore_orb_image_in_use	
				screen.blit(image, self.orb)

	def ghost_pet_update(self, monster_list, monster_index, damage_text_group, pet_target):
		animation_cooldown = 150
		radians = math.atan2((pet_target.hitbox.y + pet_target.hitbox.height * 0.5) - self.ghost_pet_rect.y, (pet_target.hitbox.x + pet_target.hitbox.width * 0.5) - self.ghost_pet_rect.x)
		distance = math.hypot((pet_target.hitbox.y + pet_target.hitbox.height * 0.5) - self.ghost_pet_rect.y, (pet_target.hitbox.x + pet_target.hitbox.width * 0.5) - self.ghost_pet_rect.x)
		dx, dy = math.cos(radians), math.sin(radians)
		self.ghost_pet_rect.x += dx * 7
		self.ghost_pet_rect.y += dy * 7

		if pygame.Rect.colliderect(self.ghost_pet_rect, pet_target.hitbox) and pygame.time.get_ticks() - self.pet_damage_time > 200 and pet_target.alive == True and pet_target != self:
			self.pet_damage_time = pygame.time.get_ticks()
			pet_target.hp -= float(f'{self.intelligence * 0.1:.2f}')
			damage_text = Damage_Text((pet_target.hitbox.x + pet_target.hitbox.width / 2) + random.randint(-60,60), pet_target.hitbox.y + random.randint(-60,60), f'{self.intelligence * 0.1:.2f}', red)	
			damage_text_group.add(damage_text)				

		screen.blit(self.ghost_pet_image, self.ghost_pet_rect)

	def update(self):
		mousex, mousey = pygame.mouse.get_pos()
		radians = math.atan2((mousey) - (self.hitbox.y + self.hitbox.height * 0.5), (mousex) - (self.hitbox.x + self.hitbox.width * 0.5))
		dx, dy = float(f'{math.cos(radians)}'), float(f'{math.sin(radians)}')
		#animation cooldown in milliseconds
		if self.base_attack_time > 60:
			animation_cooldown = self.base_attack_time
		else:
			animation_cooldown = 60
		#handle animation
		#update image
		if dx > 0:
			self.image = self.animation_list[self.action][self.frame_index]	
		elif dx < 0:
			self.image = self.animation_list[self.action][self.frame_index]	
			self.image = pygame.transform.flip(self.image,True,False)
		#check if enough time has passes since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if animation runs out reset to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 2:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:			
				if self.rect.bottom < bottom_of_bottom_panel:
					self.running_sound_effect.stop()
					self.action = 20
					self.frame_index = len(self.animation_list[self.action]) - 1
				else:
					if self.running_right == True and self.attack_time < self.base_attack_time * 0.5:
						if self.running_sound_effect.get_num_channels() < 1:
							self.running_sound_effect.play()
						if dx < 0:
							self.run_facing_monster()							
						else:
							self.run_right()
					elif self.running_left == True and self.attack_time < self.base_attack_time * 0.5:
						if self.running_sound_effect.get_num_channels() < 1:
							self.running_sound_effect.play()
						if dx > 0:
							self.run_facing_monster()						
						else:
							self.run_left()
					else:
						self.running_sound_effect.stop()
						self.idle()	

	def movement_calculation_and_reposition_hitbox(self, player_y_momentum, player_x_momentum, player_x_speed, roll_speed_increase_time, stand_still_cooldown):
		#fall
		self.player_movement = [0,0]
		self.player_movement[1] += self.player_y_momentum
		self.player_y_momentum += screen_height * 0.00015
		if self.player_y_momentum > screen_height * 0.01:
			self.player_y_momentum = screen_height * 0.01
		if self.rect.bottom >= bottom_of_bottom_panel:
			self.rect.bottom = bottom_of_bottom_panel
			self.player_movement[1] = 0 
			self.jump_counter = 0
			self.on_ground = True
		else:
			self.on_ground = False 
		self.rect.y += self.player_movement[1]
		#move
		if self.roll_speed_increase_time == 0 and (self.hitbox.right < screen_width and self.hitbox.left > 0):
			self.player_x_speed = width_position(0.002)
		if self.running_right and self.hitbox.x < screen_width - self.hitbox.width:
			self.player_movement[0] += self.player_x_speed + self.player_x_momentum
			self.player_x_momentum += self.player_x_speed * 0.01
			if stand_still_cooldown > 0:
				self.player_movement[0] = self.player_x_momentum * 0.5
		if self.running_left and self.hitbox.x > 0:
			self.player_movement[0] -= self.player_x_speed + self.player_x_momentum
			self.player_x_momentum += self.player_x_speed * 0.01
			if self.stand_still_cooldown > 0:
				self.player_movement[0] = - self.player_x_momentum * 0.5
		if self.player_movement[0] > 0:
			self.pixels_moved_right += self.player_movement[0]
		elif self.player_movement[0] < 0:
			self.pixels_moved_left -= self.player_movement[0]
		self.hibiscus_pixels_moved += abs(self.player_movement[0])
		self.phoenix_spark_moved += abs(self.player_movement[0])
		self.rect.x += self.player_movement[0]		

		#hitbox
		self.hitbox.x = self.rect.x + self.rect.width * 0.25
		self.hitbox.y = self.rect.y + self.rect.height * 0.45
		if roll_speed_increase_time > 0:
			self.hitbox.width = 0
			self.hitbox.height = 0
		else:
			self.hitbox.width = self.original_hitbox.width
			self.hitbox.height = self.original_hitbox.height		

	def jump(self):
		#set variables to attack animation
		self.action = 20
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def roll_forward(self, monster_list, monster_index, damage_text_group, experiencethreshold, inventory):
		#set variables to attack animation
		if 32 in inventory and self.on_ground == True:
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, inventory)
			self.action = 15
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()
		else:
			self.action = 21
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def roll_back(self, monster_list, monster_index, damage_text_group, experiencethreshold, inventory):
		#set variables to attack animation
		if 33 in inventory and self.on_ground == True:
			self.move_attacks(monster_list, monster_index, damage_text_group, experiencethreshold, inventory)			
			self.action = 16
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()
		else:
			self.action = 22
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def run_left(self):
		#set variables to attack animation
		self.action = 23
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def run_right(self):
		#set variables to attack animation
		self.action = 24
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def run_facing_monster(self):
		#set variables to attack animation
		self.action = 25
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
			self.statpoints += 4

			if -7 in inventory:
				self.max_hp += 4

			self.max_mp += 1
			self.mp += 1
			self.mp_regen += 0.1
			self.max_hp += 1
			self.hp += 1
			self.hp_regen += 0.1

			self.strength += 1
			self.intelligence += 1
			self.luck += 1
			self.endurance += 1
			self.agility += 1

			self.defense += 0.1

	def str_up_button(self):
		self.strength += 0.5
		self.added_strength += 0.5
		self.statpoints -= 1
		if self.added_strength == 1.5:
			self.stamina_recovery += 0.5
			self.added_strength = 0

	def int_up_button(self):
		self.intelligence += 0.5
		self.added_intelligence += 0.5
		self.statpoints -= 1
		if self.added_intelligence == 1.5:
			self.max_mp += 3
			self.mp += 3
			self.mp_regen += 0.3
			self.added_intelligence = 0

	def end_up_button(self):
		self.endurance += 0.5
		self.added_endurance += 0.5
		self.statpoints -= 1
		if self.added_endurance == 1.5:
			self.max_hp += 3
			self.hp += 3
			self.hp_regen += 0.3
			self.defense += 0.1
			self.added_endurance = 0

	def luc_up_button(self):
		self.luck += 0.5
		self.added_luck += 0.5
		self.statpoints -= 1	

	def agi_up_button(self):
		self.agility += 0.5
		self.added_agility += 0.5
		self.statpoints -= 1

	def drop_items(self, target, inventory, monster_list, monster_index):
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
						self.skills_list.append('zombie_stab')
#----------------------------------------------------------------------------------right click
	def move_attacks(self, monster_list, monster_index, damage_text_group, experiencethreshold, inventory):
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

			damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			if -4 in inventory:
				damage = damage * 0.5
			else:
				damage = damage * 0.15

			self.shield_and_damage_calculation(target, damage, damage_text_group)

			if 4 in inventory:
				self.eye_of_vladimir_calculation(target, damage, damage_text_group)

	def counter(self, right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skill_sprite_group):

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
				randdamage = float(f'{abs(randdamage) * 1.5:.2f}')

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
				self.eye_of_vladimir_calculation(target, damage, damage_text_group)

			if 34 in inventory:
				bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top - target.hitbox.height * 0.5, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
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
	def physical_damage_calculation(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb):

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = float(f'{(abs(randdamage) * 1.5) + (0.25 * self.strength):.2f}')

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

		if -20 in inventory:
			if (randdamage + self.strength + (self.agility * 0.2)) - (target.defense + (target.endurance * 0.1)) <= 0:
					damage = 0
			else:
				damage = (randdamage + self.strength + (self.agility * 0.2)) - (target.defense + (target.endurance * 0.1))
		else:
			if (randdamage + self.strength) - (target.defense + (target.endurance * 0.1)) <= 0:
				damage = 0
			else:
				damage = (randdamage + self.strength) - (target.defense + (target.endurance * 0.1))

		return damage * 2, roll_crit_chance

	def magical_damage_calculation(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index):

		randdamage = random.randint(-3,3)

		roll_crit_chance = random.randint(0,100)
		if roll_crit_chance + (self.luck * 0.25) > 70:
			randdamage = float(f'{(abs(randdamage) * 1.5) + (0.25 * self.intelligence):.2f}')

		if randdamage + self.intelligence <= 0:
			damage = 0
		else:
			damage = randdamage + self.intelligence

		return damage, roll_crit_chance

	def shield_and_damage_calculation(self, target, damage, damage_text_group):
		if target.shield > 0:
			if target.shield - float(f'{damage:.2f}') >= 0:
				target.shield -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), '0', red)
			else:
				target.hp -= (target.shield - float(f'{damage:.2f}')) * -1
				target.shield = 0
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{(target.shield - damage) * -1:.2f}', red)
		else:
			target.hp -= float(f'{damage:.2f}')
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{damage:.2f}', red)
		damage_text_group.add(damage_text)

	def eye_of_vladimir_calculation(self, target, damage, damage_text_group):
		if self.max_hp - self.hp > float(f'{damage * 0.01:.2f}'):
			heal_amount = float(f'{damage * 0.01:.2f}')
		else:
			heal_amount = float(f'{self.max_hp - self.hp:.2f}')
		self.hp += heal_amount
		heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount}', green)
		damage_text_group.add(heal_text)

	def monster_death_drops(self, target, experiencethreshold, inventory, monster_list, monster_index):
		if target.hp <= 0 and target.alive == True:
			target.hp = 0
			target.alive = False
			target.death()
			self.gold += target.gold
			self.experience += target.experience + math.floor(random.randint(-2,4))
			self.drop_items(target, inventory, monster_list, monster_index)

	def light_attack(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group):

		damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

		damage = damage * 0.25

		self.shield_and_damage_calculation(target, damage, damage_text_group)

		if 4 in inventory:
			self.eye_of_vladimir_calculation(target, damage, damage_text_group)

		if 18 in inventory:
			self.dragon_item_counter += 1

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

		if 26 in inventory:
			for monster in monster_list[monster_index]:
				if monster.alive != False:
					monster.hp -= self.intelligence * 0.2
					damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-60,60), monster.hitbox.y + 30 + random.randint(-30,30), f'HP -{self.intelligence * 0.2:.2f}', yellow)	
					damage_text_group.add(damage_text)	
					if -30 in inventory:
						self.hp += self.intelligence * 0.2
						damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 30 + random.randint(-30,30), f'HP +{self.intelligence * 0.2:.2f}', green)	
						damage_text_group.add(damage_text)							

		if -17 in inventory:
			self.attack_bleed_counter += 1

		if -5 in inventory:
			amount_of_turns = 2
		else:
			amount_of_turns = 3	

		if self.attack_bleed_counter == 3:
			bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top - target.hitbox.height * 0.5, target, self, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
			skill_sprite_group.add(bleed_animation)			
			self.attack_bleed_counter = 0

		if -27 in inventory and random.randint(0,100) < 10:
			poison_animation = Poison_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, self, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
			skill_sprite_group.add(poison_animation)			

		if -28 in inventory:
			if len(monster_list[monster_index]) != 1:
				target.monster_turn_amount -= target.monster_turn_threshold * 0.08
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -8%', yellow)	
				damage_text_group.add(damage_text)	
			else:
				target.monster_turn_amount -= target.monster_turn_threshold * 0.04
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -4%', yellow)	
				damage_text_group.add(damage_text)					

		if 18 in inventory and self.dragon_item_counter % self.dragon_item_counter_threshold == 0:

			damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			damage = damage * 0.4

			target.hp -= float(f'{damage:.2f}')
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + random.randint(-30,30), f'{damage:.2f}', red)
			damage_text_group.add(damage_text)	

			self.action = 11
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()				

		self.attack_sound_effect_list[random.randint(0,4)].play()
		if self.action != 8:
			self.sword_sound_effect.play()

	def heavy_attack(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group):

		damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

		self.heavy_attack_obsidian_counter += 1

		if 20 in inventory:
			damage = damage * 1.25
		else:
			damage = damage

		self.shield_and_damage_calculation(target, damage, damage_text_group)

		if 4 in inventory:
			self.eye_of_vladimir_calculation(target, damage, damage_text_group)

		if 34 in inventory:
			bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top - target.hitbox.height * 0.5, target, self, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
			skill_sprite_group.add(bleed_animation)			

		if 9 in inventory and self.heavy_attack_obsidian_counter == 3:
			self.fireball(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
			if -8 in inventory:
				self.lightning(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
			self.heavy_attack_obsidian_counter = 0

		#set variables to attack animation
		self.action = 7
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

		self.attack_sound_effect_list[random.randint(0,4)].play()
		self.sword_sound_effect.play()

	def cleave(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb):

		self.mp -= 7.5

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:

				damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

				self.shield_and_damage_calculation(target, damage, damage_text_group)
				
				if 'cleave_bleed' in self.skills_list:
					bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top - target.hitbox.height * 0.5, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
					skill_sprite_group.add(bleed_animation)

					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Bleed', red)	
					damage_text_group.add(damage_text)	

				if 'double_cleave' in self.skills_list:
					damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

					self.shield_and_damage_calculation(target, damage, damage_text_group)

				cleave_animation = Cleave_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y + (target.hitbox.height / 2))
				skill_sprite_group.add(cleave_animation)

		#set variables to attack animation
		if self.on_ground == True:
			if 'double_cleave' in self.skills_list:
				self.action = 11
			else:
				self.action = 6
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def zombie_stab(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb):

		self.mp -= 10

		damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
	
		damage = damage * 2

		target.hp -= float(f'{damage:.2f}')
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, f'{damage:.2f}', red)
		damage_text_group.add(damage_text)

		zombie_stab_animation = Zombie_Stab_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y + (self.hitbox.height * 0.5), target)
		skill_sprite_group.add(zombie_stab_animation)

		if self.on_ground == True:
			#set variables to attack animation
			self.action = 3
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def triple_combo(self, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index):

		self.mp -= 10

		limb_list = ['head', 'body', 'leg']

		for stabs in range(3):

			if 'triple_head' in self.skills_list:
				target_limb = 'head'
			else:
				target_limb = limb_list[stabs]

			if 'triple_mana_restore' in self.skills_list:
				if self.max_mp - self.mp > self.max_mp * 0.02:
					restore_amount = self.max_mp * 0.02
				else:
					restore_amount = self.max_mp - self.mp
				self.mp += restore_amount
				restore_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{restore_amount:.2f}', blue)
				damage_text_group.add(restore_text)

			damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)

			damage = damage * 0.75

			self.shield_and_damage_calculation(target, damage, damage_text_group)

		if self.on_ground == True:
			#set variables to attack animation
			if 'triple_head' in self.skills_list:
				self.action = 17
			else:
				self.action = 12
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	

#----------------------------------------------------------------------------------guard and skills
	def guard(self, skill_sprite_group, damage_text_group, experiencethreshold, inventory, monster_list, monster_index):

		shield_amount = float(f'{(self.max_hp * 0.2) + ((self.defense + self.endurance * 0.1) * 3):.2f}')
		if shield_amount < 0:
			shield_amount = 0
		else:
			shield_amount = float(f'{(self.max_hp * 0.2) + ((self.defense + self.endurance * 0.1) * 3):.2f}')
		self.shield += shield_amount
		shield_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, f'{(self.max_hp * 0.2) + ((self.defense + self.endurance * 0.1) * 3):.2f}', yellow)
		guard_animation = Guard_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y)
		skill_sprite_group.add(guard_animation)
		damage_text_group.add(shield_text)
		if 'guard_heal' in self.skills_list:
			if self.max_hp - self.hp > float(f'{(self.max_hp * 0.05) + ((self.defense + self.endurance * 0.1) * 0.5):.2f}'):
				heal_amount = float(f'{(self.max_hp * 0.05) + ((self.defense + self.endurance * 0.1) * 0.5):.2f}')
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{heal_amount:.2f}', green)			
			damage_text_group.add(heal_text)

		if 'guard_slash' in self.skills_list:
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
			self.heavy_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)

		if 'guard_rush' in self.skills_list:
			self.turn_amount += self.turn_threshold * 0.25
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +25%', yellow)	
			damage_text_group.add(damage_text)	

		if -21 in inventory:
			self.bat(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group)

	def stomp(self, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb):

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
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.15
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -15%', yellow)	
					else:
						monster.monster_turn_amount -= monster.monster_turn_threshold * 0.1
						damage_text = Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-30,30), monster.hitbox.y + 60 + random.randint(-30,30), f'TURN -10%', yellow)	
					damage_text_group.add(damage_text)					
			if monster.monster_turn_amount <= 0:
				monster.monster_turn_amount = 1

		if -10 in inventory:
			self.temp_endurance_stomp += 3
			self.endurance += 3

			self.stomp_buff_time = 300

			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'END +3', yellow)	
			damage_text_group.add(damage_text)				

		if 'stomp_buff' in self.skills_list:
			self.temp_strength_stomp += 2
			self.strength += 2

			self.temp_agility_stomp += 2
			self.agility += 2

			self.stomp_buff_time = 300

			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'STR +2', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + random.randint(-30,30), f'AGI +2', yellow)	
			damage_text_group.add(damage_text)	

		if 'stomp_damage' in self.skills_list:
			for monster in monster_list[monster_index]:
				if monster.alive != False:
					target_limb = 'body'
					damage, roll_crit_chance = self.physical_damage_calculation(monster, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
					damage = damage * 0.5

					self.shield_and_damage_calculation(monster, damage, damage_text_group)

		if 'stomp_rush' in self.skills_list:
			for monster in monster_list[monster_index]:
				if monster.alive != False:
					self.turn_amount += self.turn_threshold * 0.2
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +20%', yellow)	
					damage_text_group.add(damage_text)	

		if self.on_ground == True:
			self.action = 10
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def fireball(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):

		self.mp -= 5

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = damage * 1.25

				if 'fireball_agi_damage' in self.skills_list:
					damage += self.agility * 0.25

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				if -24 in inventory:
					target.hp -= float(f'{self.hp * 0.5 * 3:.2f}')
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{self.hp * 0.5 * 3:.2f}', red)
					damage_text_group.add(damage_text)	

				if 5 in inventory:
					target.hp -= float(f'{damage * 0.75:.2f}')
					damage_text_condensed_lightning = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage * 0.75:.2f}', red)
					damage_text_group.add(damage_text_condensed_lightning)

				if 31 in inventory:
					if len(monster_list[monster_index]) != 1:
						target.monster_turn_amount -= target.monster_turn_threshold * 0.1
						damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -10%', yellow)	
						damage_text_group.add(damage_text)	
						self.turn_amount += target.monster_turn_threshold * 0.1
						damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +10%', yellow)	
						damage_text_group.add(damage_text)	
						fire_ball_animation = Sapphire_Flame_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
						skill_sprite_group.add(fire_ball_animation)	
					else:
						target.monster_turn_amount -= target.monster_turn_threshold * 0.05
						damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -5%', yellow)	
						damage_text_group.add(damage_text)	
						self.turn_amount += target.monster_turn_threshold * 0.05
						damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +5%', yellow)	
						damage_text_group.add(damage_text)	
						fire_ball_animation = Sapphire_Flame_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
						skill_sprite_group.add(fire_ball_animation)							
				else:
					fire_ball_animation = Fire_Ball_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(fire_ball_animation)							

		if -24 in inventory:
			self.hp -= self.hp * 0.5

	def flameball(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):

		self.mp -= 10

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = damage * 2.25

				if len(monster_list[monster_index]) == 1:
					damage = damage * 4.5

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + random.randint(-60,60), f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				flame_ball_animation = Flame_Ball_Image(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
				skill_sprite_group.add(flame_ball_animation)	

	def spark(self, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):

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
			damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

			damage = damage * 0.3

			if 'fireball_agi_damage' in self.skills_list:
				damage += self.agility * 0.25
				
			target.hp -= float(f'{damage:.2f}')
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
			damage_text_group.add(damage_text)
			
			if 5 in inventory:
				target.hp -= float(f'{damage * 0.75:.2f}')
				damage_text_condensed_lightning = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage * 0.75:.2f}', red)
				damage_text_group.add(damage_text_condensed_lightning)

			if 31 in inventory:
				if len(monster_list[monster_index]) != 1:
					target.monster_turn_amount -= target.monster_turn_threshold * 0.1
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -10%', yellow)	
					damage_text_group.add(damage_text)	
					self.turn_amount += target.monster_turn_threshold * 0.1
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +10%', yellow)	
					damage_text_group.add(damage_text)	
					fire_ball_animation = Sapphire_Flame_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(fire_ball_animation)	
				else:
					target.monster_turn_amount -= target.monster_turn_threshold * 0.05
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-30,30), target.hitbox.y + 60 + random.randint(-30,30), f'TURN -5%', yellow)	
					damage_text_group.add(damage_text)	
					self.turn_amount += target.monster_turn_threshold * 0.05
					damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +5%', yellow)	
					damage_text_group.add(damage_text)	
					fire_ball_animation = Sapphire_Flame_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(fire_ball_animation)							
			else:
				fire_ball_animation = Fire_Ball_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
				skill_sprite_group.add(fire_ball_animation)		

	def auto_spark_phoenix(self, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):
		if -9 in inventory and self.phoenix_spark_moved >= screen_width:
			self.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
			self.phoenix_spark_moved = 0

	def lightning(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):

		self.mp -= 5

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = damage

				if 'lightning_agi_damage' in self.skills_list:
					damage += self.agility * 0.25

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				if -2 in inventory:
					target.hp -= float(f'{damage:.2f}')
					damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
					damage_text_group.add(damage_text)
					eclipse_beam_animation = Eclipse_Beam_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(eclipse_beam_animation)	

				elif 36 in inventory:
					lunar_beam_animation = Lunar_Beam_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(lunar_beam_animation)
	
				elif 37 in inventory:
					solar_beam_animation = Solar_Beam_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(solar_beam_animation)
	
				else:
					lightning_animation = Lightning_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
					skill_sprite_group.add(lightning_animation)

				self.turn_amount += self.turn_threshold * 0.2
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'TURN +20%', yellow)	
				damage_text_group.add(damage_text)	

		if -2 in inventory:
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Eclipse Beam', yellow)	
			damage_text_group.add(damage_text)	

		if 36 in inventory:
			if self.max_mp - self.mp > self.max_mp * 0.1:
				restore_amount = self.max_mp * 0.15
			else:
				restore_amount = self.max_mp - self.mp
			self.mp += restore_amount
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 30 + random.randint(-60,60), f'+{restore_amount:.2f} MP', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Lunar Beam', yellow)	
			damage_text_group.add(damage_text)

		if 37 in inventory:
			if self.max_hp - self.hp > self.max_hp * 0.1:
				heal_amount = self.max_hp * 0.15
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 30 + random.randint(-60,60), f'+{heal_amount:.2f} HP', yellow)	
			damage_text_group.add(damage_text)	
			damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-60,60), self.hitbox.y + 60 + random.randint(-60,60), f'Solar Beam', yellow)	
			damage_text_group.add(damage_text)	

	def frost(self, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):

		self.mp -= 5

		for count, monster in enumerate(monster_list[monster_index]):
			target = monster

			if target.alive != False:
				damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = damage

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				target.monster_turn_amount -= target.monster_turn_threshold * 0.2
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2) + random.randint(-60,60), target.hitbox.y + 60 + random.randint(-60,60), f'TURN -20%', yellow)	
				damage_text_group.add(damage_text)	

				frost_animation = Frost_Images(target.hitbox.x + ((screen_width * 0.01) * random.random()), target.hitbox.y + ((screen_height * 0.01) * random.random()))
				skill_sprite_group.add(frost_animation)

	def water_blast(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time):
		if -11 in inventory and start_combat_time % 400 == 0 and start_combat_time != 0:
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

			water_blast_animation = Water_Blast_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y + (self.hitbox.height * 0.5), target)
			skill_sprite_group.add(water_blast_animation)

	def goblin_bomb(self, target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time):
		if 42 in inventory and start_combat_time % 1000 == 0 and start_combat_time != 0:
			target_limb = 'body'

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

			damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
		
			damage = damage * 1.5

			target.hp -= float(f'{damage:.2f}')
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, f'{damage:.2f}', red)
			damage_text_group.add(damage_text)

			goblin_bomb_image = Goblin_Bomb_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y + (self.hitbox.height * 0.5), target)
			skill_sprite_group.add(goblin_bomb_image)

	def bat(self, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group):

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

		damage = self.max_hp * 0.1

		target.hp -= float(f'{damage:.2f}')
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, f'{damage:.2f}', red)
		damage_text_group.add(damage_text)

		bat_image = Bat_Images(self.hitbox.x, self.hitbox.y, target)
		skill_sprite_group.add(bat_image)

	def serpent_wheel(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb):

		self.mp -= 20

		for monster in monster_list[monster_index]:
			target = monster
			if monster.alive == True:
				damage, roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
			
				damage = (damage * 2) + self.agility

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top - target.hitbox.height * 0.5, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
				skill_sprite_group.add(bleed_animation)

		serpent_wheel_animation = Serpent_Wheel_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y + (self.hitbox.height / 2), target)
		skill_sprite_group.add(serpent_wheel_animation)

		if self.on_ground == True:
			#set variables to attack animation
			self.action = 3
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def bleed(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb):
		bleed_animation = Bleed_Images((target.hitbox.x + target.hitbox.width * 0.5), target.hitbox.top - target.hitbox.height * 0.5, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
		skill_sprite_group.add(bleed_animation)

	def mist_vortex(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time):
		if -29 in inventory and start_combat_time % 1200 == 0 and start_combat_time != 0:		
			mist_vortex_animation = Mist_Vortex_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.top - self.hitbox.height * 0.5, self)
			skill_sprite_group.add(mist_vortex_animation)
			self.mist_vortex_time = 400

	def venomous_whip(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group):

		self.mp -= 20

		for monster in monster_list[monster_index]:
			target = monster
			if monster.alive == True:
				damage, roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = (damage * 2) + self.strength

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				poison_animation = Poison_Images((target.hitbox.x + target.hitbox.width / 2), target.hitbox.top + 50, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
				skill_sprite_group.add(poison_animation)

		venomous_whip_animation = Venomous_Whip_Images((self.hitbox.x + self.hitbox.width), self.hitbox.y + (self.hitbox.height / 2))
		skill_sprite_group.add(venomous_whip_animation)

		if self.on_ground == True:
			#set variables to attack animation
			self.action = 18
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def thunder_bolt(self, target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group):

		self.mp -= 15

		for monster in monster_list[monster_index]:
			target = monster
			if target.alive == True:
				target_limb = 'body'

				phy_damage, phy_roll_crit_chance = self.physical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb)
			
				mag_damage, mag_roll_crit_chance = self.magical_damage_calculation(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)

				damage = (phy_damage * 0.5) + (mag_damage * 0.5)

				target.hp -= float(f'{damage:.2f}')
				damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{damage:.2f}', red)
				damage_text_group.add(damage_text)

				self.turn_amount += self.turn_threshold * 0.1
				damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2) + random.randint(-30,30), self.hitbox.y + 60 + random.randint(-30,30), f'TURN +10%', yellow)	
				damage_text_group.add(damage_text)	

		thunder_bolt_animation = Thunder_Bolt_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y, target)
		skill_sprite_group.add(thunder_bolt_animation)

		#set variables to attack animation
		self.action = 19
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hp_regen_calculation(self, start_combat_time, inventory, damage_text_group, monster_list, monster_index):
		if -12 in inventory:
			calculation_time = 300
		else:
			calculation_time = 500

		if start_combat_time % calculation_time == 0 and start_combat_time != 0:
			if 8 in inventory:
				self.hp += (self.hp_regen + self.endurance * 0.1) + (self.mp_regen + self.intelligence * 0.1)
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.hp_regen + self.endurance * 0.1) + (self.mp_regen + self.intelligence * 0.1):.2f}', green)
			else:			
				self.hp += (self.hp_regen + self.endurance * 0.1)	
				heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30, f'{(self.hp_regen + self.endurance * 0.1):.2f}', green)									
			damage_text_group.add(heal_text)
			if self.hp > self.max_hp:
				self.hp = self.max_hp
			if -23 in inventory:
				for monster in monster_list[monster_index]:
					target = monster
					if target.alive == True:	
						if 8 in inventory:
							decrease_amount = (self.hp_regen + self.endurance * 0.1) + (self.mp_regen + self.intelligence * 0.1)
							negative_regen_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 60, f'{(self.hp_regen + self.endurance * 0.1) + (self.mp_regen + self.intelligence * 0.1):.2f}', red)
						else:
							decrease_amount = (self.hp_regen + self.endurance * 0.1)	
							negative_regen_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 60, f'{(self.hp_regen + self.endurance * 0.1):.2f}', red)
						damage_text_group.add(negative_regen_text)	
						target.hp -= decrease_amount

	def hibiscus_regen_calculation(self, start_combat_time, inventory, damage_text_group, monster_list, monster_index):
		if 38 in inventory and self.hibiscus_pixels_moved >= screen_width * 0.8:
			if self.max_hp - self.hp > self.max_hp * 0.03:
				heal_amount = self.max_hp * 0.03
			else:
				heal_amount = self.max_hp - self.hp
			self.hp += heal_amount
			self.hibiscus_pixels_moved = 0
			heal_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 30 + random.randint(-30,30), f'{heal_amount:.2f}', green)
			damage_text_group.add(heal_text)

	def heal(self, damage_text_group, inventory, skill_sprite_group):
		heal_animation = Heal_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y, self, damage_text_group, inventory)
		skill_sprite_group.add(heal_animation)

	def mp_regen_calculation(self, start_combat_time, inventory, damage_text_group, monster_list, monster_index):
		if start_combat_time % 500 == 0 and start_combat_time != 0:
			self.mp += (self.mp_regen + self.intelligence * 0.1)	
			restore_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y - 60, f'{(self.mp_regen + self.intelligence * 0.1):.2f}', blue)									
			damage_text_group.add(restore_text)
			if self.mp > self.max_mp:
				self.mp = self.max_mp	

	def restore(self, damage_text_group, inventory, skill_sprite_group):
		restore_animation = Restore_Images((self.hitbox.x + self.hitbox.width * 0.5), self.hitbox.y, self, damage_text_group, inventory)
		skill_sprite_group.add(restore_animation)

class Slime(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		self.monster_turn_amount = 0
		self.monster_turn_threshold = 10000
		self.animation_list = [] #this is the slime's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		self.number_of_pictures_list = [4,4,5]
		self.which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.175),height(0.175)))
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		self.hitbox_x_offset = self.rect.width * 0.33
		self.hitbox_y_offset = self.rect.height * 0.65
		self.hitbox = pygame.rect.Rect(self.rect.x + self.hitbox_x_offset, self.rect.bottom + self.hitbox_y_offset, self.rect.width * 0.35, self.rect.height * 0.35)
		self.original_hitbox = self.hitbox.copy()

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

		self.movement_time = pygame.time.get_ticks()
		self.y_momentum = - 3
		self.y_momentum_reduction_rate = screen_height * 0.001
		self.weight = 1
		
		#sound fx
		self.attack_sound_effect_list = []
		for sound in range(3):
			sound_effect = pygame.mixer.Sound(f'Music/Slime/Slime{sound}.mp3')
			sound_effect.set_volume(0.3)
			self.attack_sound_effect_list.append(sound_effect)	

	def movement(self, target, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time):
		dx, dy = calculate_randians(self, target)

		self.rect.x += dx * 4

		if self.rect.bottom >= bottom_of_bottom_panel:
			self.attack_sound_effect_list[2].play()
			self.rect.y -= screen_height * 0.1
			self.y_momentum = random.randint(-3,-2)
			self.action = 1
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	

		self.reposition_hitboxes()

	def armor_corrosion(self, target, damage_text_group, inventory):
		if target.shield > 0:
			shield_destroyed = target.shield
			target.shield = 0
			damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, str(shield_destroyed), yellow)
			damage_text_group.add(damage_text)

		target.hp -= float(f'{self.strength * 0.25:.2f}')
		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y - 30, f'{self.strength * 0.25:.2f}', red)

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

	def slime_ball(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):
		self.attack_sound_effect_list[1].play()

		slime_ball_animation = Slime_Ball_Images((self.hitbox.x + self.hitbox.width / 2), self.hitbox.bottom, target, damage_text_group, caster)
		monster_skill_sprite_group.add(slime_ball_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Slime Ball', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Zombie(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		self.monster_turn_amount = 0
		self.monster_turn_threshold = 10000
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		self.number_of_pictures_list = [4,4,6,4]
		self.which_state_list = ['Idle', 'Attack', 'Death', 'Attack2']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.175),height(0.175)))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		self.hitbox_x_offset = self.rect.width * 0.35
		self.hitbox_y_offset = self.rect.height * 0.45	
		self.hitbox = pygame.rect.Rect(self.rect.x + self.hitbox_x_offset, self.rect.y + self.hitbox_y_offset, self.rect.width * 0.35, self.rect.height * 0.55)
		self.original_hitbox = self.hitbox.copy()

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

		self.movement_time = pygame.time.get_ticks()
		self.moving_duration = 0

		self.y_momentum = 0
		self.y_momentum_reduction_rate = 0
		self.weight = 2
		
		self.x_momentum = 0
		self.x_speed = random.randint(2,5)

		#sound fx
		self.attack_sound_effect_list = []
		for sound in range(2):
			sound_effect = pygame.mixer.Sound(f'Music/Zombie/Zombie_Vomit{sound}.mp3')
			sound_effect.set_volume(0.3)
			self.attack_sound_effect_list.append(sound_effect)	

	def movement(self, target, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time):
		dx, dy = calculate_randians(self, target)

		if start_combat_time % 400 == 0:
			self.moving_duration = 100
			self.x_speed = random.randint(2,4)
			self.attack_sound_effect_list[1].play()

		if self.moving_duration > 0:
			self.moving_duration -= 1
			self.x_momentum += 0.025
			if dx > 0:
				self.rect.x += (abs(dx) * self.x_speed) + self.x_momentum	
			elif dx < 0:
				self.rect.x -= (abs(dx) * self.x_speed) + self.x_momentum
		else:
			if self.x_momentum > 0:
				self.x_momentum -= 0.01
				if self.x_momentum < 0:
					self.x_momentum = 0
			if dx > 0:
				self.rect.x += self.x_momentum	
			elif dx < 0:
				self.rect.x -= self.x_momentum

		self.reposition_hitboxes()

	def toxic_bile(self, target, damage_text_group, inventory):
		target.hp -= float(f'{self.strength * 2:.2f}')

		damage_text = Damage_Text((target.hitbox.x + target.hitbox.width / 2), target.hitbox.y, f'{self.strength * 2:.2f}', red)	
		damage_text_group.add(damage_text)		
		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), target.hitbox.y, 'Toxic Bile', yellow)	
		damage_text_group.add(damage_text)	

		#check if target is dead
		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def vomit(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):
		self.attack_sound_effect_list[0].play()

		vomit_animation = Vomit_Images((target.hitbox.x + target.original_hitbox.width * 0.5), target.hitbox.bottom - target.original_hitbox.height * 0.1, target, damage_text_group, caster)
		monster_skill_sprite_group.add(vomit_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Vomit', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

		#set variables to attack animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

class Swift_Zombie(Character):
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		self.monster_turn_amount = 0
		self.monster_turn_threshold = 10000
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		self.number_of_pictures_list = [4,2,2]
		self.which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.175),height(0.175)))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		self.hitbox_x_offset = self.rect.width * 0.35
		self.hitbox_y_offset = self.rect.height * 0.45	
		self.hitbox = pygame.rect.Rect(self.rect.x + self.hitbox_x_offset, self.rect.y + self.hitbox_y_offset, self.rect.width * 0.35, self.rect.height * 0.55)
		self.original_hitbox = self.hitbox.copy()

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

		self.movement_time = pygame.time.get_ticks()
		self.y_momentum = - 6
		self.y_momentum_reduction_rate = screen_height * 0.003
		self.weight = 2.5

		self.x_speed = random.randint(1,2)
		self.x_jump_speed = random.randint(15,18)

	def movement(self, target, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time):
		dx, dy = calculate_randians(self, target)

		if self.rect.bottom < bottom_of_bottom_panel:
			self.rect.x += dx * self.x_jump_speed
		else:
			self.rect.x += dx * self.x_speed

		if self.rect.bottom >= bottom_of_bottom_panel and start_combat_time % 250 == 0:
			self.x_speed = random.randint(1,2)
			self.x_jump_speed = random.randint(15,18)			
			self.rect.y -= screen_height * 0.1
			self.y_momentum = random.randint(-7,-6)
			self.action = 1
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	

		self.reposition_hitboxes()

	def vomit(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		vomit_animation = Vomit_Images((target.hitbox.x + target.original_hitbox.width * 0.5), target.hitbox.bottom - target.original_hitbox.height * 0.1, target, damage_text_group, caster)
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
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		self.monster_turn_amount = 0
		self.monster_turn_threshold = 10000
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		self.number_of_pictures_list = [4,5,6]
		self.which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.2),height(0.2)))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		self.hitbox_x_offset = self.rect.width * 0.3
		self.hitbox_y_offset = self.rect.height * 0.2
		self.hitbox = pygame.rect.Rect(self.rect.x + self.hitbox_x_offset, self.rect.y + self.hitbox_y_offset, 140, 300)
		self.original_hitbox = self.hitbox.copy()

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

		self.movement_time = pygame.time.get_ticks()
		self.y_momentum = 0
		self.y_momentum_reduction_rate = 0
		self.weight = 5
		
	def movement(self, target, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time):
		dx, dy = calculate_randians(self, target)

		self.rect.y += dy * 2
		self.rect.x += dx * 2

		self.reposition_hitboxes()

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

		target.scream_debuff_time = 300
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

		vomit_animation = Vomit_Images((target.hitbox.x + target.original_hitbox.width * 0.5), target.hitbox.bottom - target.original_hitbox.height * 0.1, target, damage_text_group, caster)
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

	def special_skill_2(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		vomit_animation = Mega_Vomit_Images((target.hitbox.x + target.hitbox.width / 2), height_position(0.75), target, damage_text_group, caster)
		monster_skill_sprite_group.add(vomit_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y, 'Mega Vomit', yellow)	
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
	def __init__(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance):
		super().__init__(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
		self.monster_turn_amount = 0
		self.monster_turn_threshold = 10000
		self.animation_list = [] #this is the zombie's animation list -> slime.animation_list[]
		self.frame_index = 0
		self.start_frame_index = 0
		self.action = 0 #0 = idle; 1 = attack; 2 = hurt; 3 = dead
		self.start_action = 0
		self.update_time = pygame.time.get_ticks()
		self.casting_time = 1000
		self.special_skill_2_counter = 0
		self.special_skill_2_time_counter = 0	
		#load images for each index
		#5 animation states; 0 = idle; 1 = attack; 2 = hurt; 3 = dead; run loop 4 times to load each set of animation
		self.number_of_pictures_list = [6,9,5]
		self.which_state_list = ['Idle', 'Attack', 'Death']
		for state in range(len(self.which_state_list)):
			each_state_animation_list = []
			for i in range(self.number_of_pictures_list[state]):
				img = pygame.image.load(f'Images/Enemy/{self.name}/{self.which_state_list[state]}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img,(width(0.35),height(0.35)))
				img = pygame.transform.flip(img,True,False)
				each_state_animation_list.append(img)			
			self.animation_list.append(each_state_animation_list)
		#which image is currently displayed
		self.image = self.animation_list[self.action][self.frame_index]
		#get the hitbox/rectangle of the character
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		self.hitbox_x_offset = self.rect.width * 0.3
		self.hitbox_y_offset = self.rect.height * 0.25
		self.hitbox = pygame.rect.Rect(self.rect.x + self.hitbox_x_offset, self.rect.y + self.hitbox_y_offset, self.rect.width * 0.5, self.rect.height * 0.75)
		self.original_hitbox = self.hitbox.copy()

		self.head_hitbox = pygame.rect.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height / 3)
		self.body_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + (self.hitbox.height / 3), self.hitbox.width, self.hitbox.height / 3)
		self.leg_hitbox = pygame.rect.Rect(self.hitbox.x, (self.hitbox.y) + ((self.hitbox.height / 3) * 2), self.hitbox.width, self.hitbox.height / 3)

		self.movement_time = pygame.time.get_ticks()
		self.y_momentum = 0
		self.y_momentum_reduction_rate = 0
		self.weight = 10
		
		#attack length
		self.attack_length = screen_width * 0.3

	def movement(self, target, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time):
		self.reposition_hitboxes()

	def special_skill_1(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		for i in range(5):
			rock_slide_animation = Rock_Slide_Images((screen_width * float(f'{random.random()}')), height_position(0.02), target, damage_text_group, caster)
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

		stalagmite_animation = Stalagmite_Images((target.hitbox.x + target.hitbox.width / 2), height_position(0.96), target, damage_text_group, caster)
		monster_skill_sprite_group.add(stalagmite_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y + screen_height * 0.05, 'Stalagmite', yellow)	
		damage_text_group.add(damage_text)	

		if target.hp < 0:
			target.hp = 0
			target.alive = False
			target.death()

	def special_skill_3(self, target, monster_skill_sprite_group, damage_text_group, inventory, caster):

		stalagmite_animation = Rock_Throw_Images((self.hitbox.x + self.hitbox.width / 2), height_position(0.8), target, damage_text_group, caster)
		monster_skill_sprite_group.add(stalagmite_animation)

		damage_text = Damage_Text((self.hitbox.x + self.hitbox.width / 2), self.hitbox.y + screen_height * 0.05, 'Stalagmite', yellow)	
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

class Frost_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Frost/Frost{i}.png').convert_alpha()
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
			if self.frame_index > len(self.animation_list):
				self.frame_index = self.animation_list[-1]
		#if animation runs out reset to the start
		if pygame.time.get_ticks() - self.cast_time > 300:
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
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Zombie_Stab/ZombieStab.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 8, self.original_image.get_height() * 3))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = - (math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x) * (180 / math.pi))

		radians = math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		distance = math.hypot((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		self.dx, self.dy = math.cos(radians), math.sin(radians)

		self.x_speed = 0
		self.y_speed = 0

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 10
		self.x += (abs(self.dx) * 50)
		self.y += (abs(self.dy) * 50) 
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 500:
			self.kill()

class Water_Blast_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Water_Blast/WaterBlast.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 8, self.original_image.get_height() * 3))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = - (math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x) * (180 / math.pi))

		radians = math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		distance = math.hypot((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		self.dx, self.dy = math.cos(radians), math.sin(radians)

		self.x_speed = 0
		self.y_speed = 0

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 10
		self.x += (abs(self.dx) * 50)
		self.y += (abs(self.dy) * 50) 
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 500:
			self.kill()

class Thunder_Bolt_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Thunder_Bolt/ThunderBolt.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 12, self.original_image.get_height() * 3))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = - (math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x) * (180 / math.pi))

		radians = math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		distance = math.hypot((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		self.dx, self.dy = math.cos(radians), math.sin(radians)

		self.x_speed = 0
		self.y_speed = 0

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 10
		self.x += (abs(self.dx) * 50)
		self.y += (abs(self.dy) * 50) 
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 500:
			self.kill()

class Venomous_Whip_Images(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
		for i in range(3):
			img = pygame.image.load(f'Images/Icon/Venomous_Whip/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 7, (img.get_height() * 7)))
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

class Mist_Vortex_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, hero):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.hero = hero

		self.original_image = pygame.image.load(f'Images/Icon/Mist_Vortex/MistVortex.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 5, self.original_image.get_height() * 5))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0

	def update(self):
		self.x = self.hero.hitbox.x + (self.hero.original_hitbox.width * 0.5)
		self.y = self.hero.hitbox.y + (self.hero.original_hitbox.height * 0.5)
		#animation cooldown in milliseconds
		animation_cooldown = 1
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 1
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 3000:
			self.kill()	

class Serpent_Wheel_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Serpent_Wheel/0.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 3, self.original_image.get_height() * 3))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0

		self.x_momentum = 0
		self.y_momentum = 0

	def update(self):
		radians = math.atan2((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		distance = math.hypot((self.target.hitbox.y + (self.target.hitbox.height * 0.5)) - self.y, (self.target.hitbox.x + (self.target.hitbox.width * 0.5)) - self.x)
		dx, dy = math.cos(radians), math.sin(radians)
		#animation cooldown in milliseconds
		animation_cooldown = 10
		self.x_momentum += dx * 0.5
		self.y_momentum += dy * 0.5
		self.x += self.x_momentum
		self.y += self.y_momentum
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 30
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000:
			self.kill()

class Goblin_Bomb_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Goblin_Bomb/GoblinBomb.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 2, self.original_image.get_height() * 2))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0

		self.x_momentum = 0
		self.y_momentum = 0

	def update(self):
		radians = math.atan2((self.target.hitbox.bottom - (self.target.hitbox.height * 0.5)) - self.y, self.target.hitbox.x - self.x)
		distance = math.hypot((self.target.hitbox.bottom - (self.target.hitbox.height * 0.5)) - self.y, self.target.hitbox.x - self.x)
		dx, dy = math.cos(radians), math.sin(radians)
		#animation cooldown in milliseconds
		animation_cooldown = 10
		self.x += dx * 17
		self.y += dy * 17
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 10
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		if pygame.time.get_ticks() - self.cast_time > 700:
			self.image = pygame.image.load(f'Images/Icon/Goblin_Bomb/BombExplosion.png').convert_alpha()
			self.image = pygame.transform.scale(self.image,(self.image.get_width() * 3, self.image.get_height() * 3))
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 800:
			self.kill()

class Bat_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target

		self.animation_list = []
		self.frame_index = 0	
		for i in range(2):
			img = pygame.image.load(f'Images/Icon/Bat/{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		radians = math.atan2(self.target.hitbox.top - self.rect.y, self.target.hitbox.x - self.rect.x)
		distance = math.hypot(self.target.hitbox.top - self.rect.y, self.target.hitbox.x - self.rect.x)
		dx, dy = math.cos(radians), math.sin(radians)
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.rect.x += dx * 15
		self.rect.y += dy * 15
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.frame_index += 1
			if self.frame_index > len(self.animation_list) - 1:
				self.frame_index = 0
			self.image = self.animation_list[self.frame_index]
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000:
			self.kill()

class Bleed_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index):
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
		self.inventory = inventory
		self.hero = hero
		self.x = x
		self.y = y
		self.target = target

		self.original_image = pygame.image.load(f'Images/Icon/Bleed/0.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width(), self.original_image.get_height()))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0
		#self.rect = self.original_image.get_rect(center = (self.x, self.y - (self.target.hitbox.height * 0.5)))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 20
		if pygame.time.get_ticks() - self.damage_time > 100 and self.target.alive == True:
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
			self.angle -= 10
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000 or self.target.alive == False:
			self.kill()

class Heal_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, hero, damage_text_group, inventory):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.heal_time = pygame.time.get_ticks()	
		self.damage_text_group = damage_text_group
		self.inventory = inventory
		self.inventory = inventory
		self.hero = hero
		self.x = x
		self.y = y

		self.original_image = pygame.image.load(f'Images/Icon/Heal_Consumable/Heal.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width(), self.original_image.get_height()))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0
		#self.rect = self.original_image.get_rect(center = (self.x, self.y - (self.target.hitbox.height * 0.5)))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 20	
		if pygame.time.get_ticks() - self.heal_time > 100 and self.hero.alive == True:
			self.heal_time = pygame.time.get_ticks()
			heal = float(f'{(self.hero.max_hp * 0.01):.2f}')
			self.hero.hp += heal
			damage_text = Damage_Text((self.hero.hitbox.x + self.hero.hitbox.width / 2) + random.randint(-60,60), self.hero.hitbox.y + random.randint(-60,60), f'{(self.hero.max_hp * 0.01):.2f}', green)	
			self.damage_text_group.add(damage_text)	

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 10
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)	
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000 or self.hero.alive == False:
			self.kill()

class Restore_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, hero, damage_text_group, inventory):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.restore_time = pygame.time.get_ticks()	
		self.damage_text_group = damage_text_group
		self.inventory = inventory
		self.inventory = inventory
		self.hero = hero
		self.x = x
		self.y = y

		self.original_image = pygame.image.load(f'Images/Icon/Restore_Consumable/Restore.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width(), self.original_image.get_height()))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0
		#self.rect = self.original_image.get_rect(center = (self.x, self.y - (self.target.hitbox.height * 0.5)))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 20
		if pygame.time.get_ticks() - self.restore_time > 100 and self.hero.alive == True:
			self.restore_time = pygame.time.get_ticks()
			restore = float(f'{(self.hero.max_mp * 0.01):.2f}')
			self.hero.mp += restore
			damage_text = Damage_Text((self.hero.hitbox.x + self.hero.hitbox.width / 2) + random.randint(-60,60), self.hero.hitbox.y + random.randint(-60,60), f'{(self.hero.max_mp * 0.01):.2f}', blue)	
			self.damage_text_group.add(damage_text)	

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 10
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000 or self.hero.alive == False:
			self.kill()

class Flame_Ball_Image(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.x = x
		self.y = y

		self.original_image = pygame.image.load(f'Images/Icon/Flame_ball/Flameball.png').convert_alpha()
		self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 3, self.original_image.get_height() * 3))
		self.image = self.original_image.copy()
		self.rect = self.original_image.get_rect()
		self.angle = 0
		#self.rect = self.original_image.get_rect(center = (self.x, self.y - (self.target.hitbox.height * 0.5)))

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 1
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()	
			self.angle -= 2
			self.y -= 3
			self.image, self.rect = rot_center(self.original_image, self.angle, self.x, self.y)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 750:
			self.kill()

class Poison_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index):
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
			if len(self.monster_list[self.monster_index]) != 1:
				self.target.monster_turn_amount -= self.target.monster_turn_threshold * 0.2
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'TURN -20%', red)	
				self.damage_text_group.add(damage_text)	
			else:
				self.target.monster_turn_amount -= self.target.monster_turn_threshold * 0.1
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'TURN -10%', red)	
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
		self.rect.center = (x,y - (target.original_hitbox.height * 0.5))

		self.hitbox = pygame.rect.Rect(x - 30, y - self.rect.height * 0.3, 60, 20)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.Rect.colliderect(self.target.hitbox, self.hitbox) and pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			self.target.hp -= float(f'{(self.caster.strength * 0.2) + self.target.max_hp * 0.01:.2f}')
			damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.caster.strength * 0.2) + self.target.max_hp * 0.01:.2f}', red)	
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
			if pygame.time.get_ticks() - self.cast_time > 4000 or self.caster.alive == False:
				self.kill()

class Mega_Vomit_Images(pygame.sprite.Sprite):
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
			img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
			self.animation_list.append(img)
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y - (target.original_hitbox.height * 0.5))

		self.hitbox = pygame.rect.Rect(x - 60, y, 120, 60)

	def update(self):
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.Rect.colliderect(self.target.hitbox, self.hitbox) and pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			self.target.hp -= float(f'{(self.caster.strength * 0.5) + self.target.max_hp * 0.01:.2f}')
			damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.caster.strength * 0.5) + self.target.max_hp * 0.01:.2f}', red)	
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
			if pygame.time.get_ticks() - self.cast_time > 3000 or self.caster.alive == False:
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
		self.y_momentum = random.randint(0,5)

		self.image = pygame.image.load(f'Images/Enemy/EnemySkills/RockSlide/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 4), (self.image.get_height() * 4)))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + self.rect.width * 0.16, self.rect.y, self.rect.width * 0.6, self.rect.height * 0.6)

	def update(self):
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 2000 or self.caster.alive == False or (pygame.Rect.colliderect(self.hitbox, self.target.hitbox) and self.target.mist_vortex_time > 0):
			self.kill()
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.rect.y += self.y_momentum
		self.hitbox.y = self.rect.y + self.rect.height * 0.15
		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.y_momentum += height_position(0.0002)
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.hitbox, self.target.hitbox):
				self.target.hp -= float(f'{(self.caster.strength * 0.25) + (self.target.max_hp * 0.05):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.caster.strength) + (self.target.max_hp * 0.05):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			#check if target is dead
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			self.image = pygame.transform.rotate(self.image, 90)

class Rock_Throw_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, damage_text_group, caster):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.caster = caster
		self.y_momentum = - random.randint(3,6)
		self.x_momentum = screen_width * 0.003

		self.image = pygame.image.load(f'Images/Enemy/EnemySkills/RockSlide/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 6), (self.image.get_height() * 6)))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + self.rect.width * 0.16, self.rect.y, self.rect.width * 0.6, self.rect.height * 0.6)

	def update(self):
		# pygame.draw.rect(screen,(255,0,0),self.hitbox,2)	
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 5000 or self.caster.alive == False or (pygame.Rect.colliderect(self.hitbox, self.target.hitbox) and self.target.mist_vortex_time > 0):
			self.kill()	
		#animation cooldown in milliseconds
		animation_cooldown = 100
		self.rect.y += self.y_momentum
		self.rect.x -= self.x_momentum
		self.hitbox.y = self.rect.y + self.rect.height * 0.15
		self.hitbox.x = self.rect.x 

		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.y_momentum += height_position(0.0002)
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.hitbox, self.target.hitbox):
				self.target.hp -= float(f'{(self.caster.strength) + (self.target.max_hp * 0.05):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.caster.strength) + (self.target.max_hp * 0.05):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			#check if target is dead
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()		
			self.image = pygame.transform.rotate(self.image, -90)

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
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 5), (self.image.get_height() * 6)))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.hitbox = pygame.rect.Rect(self.rect.x + self.rect.width * 0.37, self.rect.y + self.rect.height * 0.17, self.rect.width * 0.3, self.rect.height)

	def update(self):
		# pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
		#animation cooldown in milliseconds
		animation_cooldown = 100
		if pygame.time.get_ticks() - self.cast_time > 500 and self.rect.y > top_of_bottom_panel:
			self.rect.y -= height_position(0.01)
			self.hitbox.y = self.rect.y + self.rect.height * 0.17
		if pygame.time.get_ticks() - self.damage_time > 200 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.hitbox, self.target.hitbox):
				self.target.hp -= float(f'{(self.caster.strength * 0.5) + (self.target.max_hp * 0.05):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{(self.caster.strength * 0.5) + (self.target.max_hp * 0.05):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 1000 or self.caster.alive == False:
			self.kill()

class Slime_Ball_Images(pygame.sprite.Sprite):
	def __init__(self, x, y, target, damage_text_group, caster):
		pygame.sprite.Sprite.__init__(self)
		self.frame_index = 0
		self.cast_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()	
		self.damage_time = pygame.time.get_ticks()	
		self.target = target
		self.damage_text_group = damage_text_group
		self.caster = caster

		self.image = pygame.image.load(f'Images/Enemy/EnemySkills/SlimeBall/0.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 2) - 75, (self.image.get_height() * 2) - 75))
		self.image = pygame.transform.rotate(self.image, 90)
		self.original_image = self.image
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.original_center = self.rect.center

	def update(self):
		# pygame.draw.rect(screen,(255,0,0),self.rect,2)
		#if animation runs out then delete it
		if pygame.time.get_ticks() - self.cast_time > 3000 or self.caster.alive == False or (pygame.Rect.colliderect(self.rect, self.target.hitbox) and self.target.mist_vortex_time > 0):
			self.kill()
		#animation cooldown in milliseconds
		animation_cooldown = 100
		radians = math.atan2(self.target.hitbox.y - self.rect.y, self.target.hitbox.x - self.rect.x)
		distance = math.hypot(self.target.hitbox.y - self.rect.y, self.target.hitbox.x - self.rect.x)
		dx, dy = math.cos(radians), math.sin(radians)
		self.rect.x += dx * 4
		self.rect.y += dy * 4
		if pygame.time.get_ticks() - self.damage_time > 100 and self.target.alive == True:
			self.damage_time = pygame.time.get_ticks()
			if pygame.Rect.colliderect(self.rect, self.target.hitbox):
				self.target.hp -= float(f'{2 + (self.caster.strength * 0.5):.2f}')
				damage_text = Damage_Text((self.target.hitbox.x + self.target.hitbox.width / 2) + random.randint(-60,60), self.target.hitbox.y + random.randint(-60,60), f'{2 + (self.caster.strength * 0.5):.2f}', red)	
				self.damage_text_group.add(damage_text)		
			#check if target is dead
			if self.target.hp <= 0:
				self.target.hp = 0
				self.target.alive = False
				self.target.death()

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
		start_random_integer = 40
		start_random_strength = random.randint(13, 20)
		start_random_intelligence = random.randint(8, 13)
		start_random_endurance = 5
		start_random_agility = 5
		start_random_luck = 3
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

