import math, pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events, Speed_Stamina, Consumables

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 120

#game window#
bottom_panel = 150
screen_width, screen_height = 800, 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

#define game variables
action_cooldown = 0
action_wait_time = 100
experiencethreshold = [5]
left_click = False
right_click = False
attack = False
target = None
monster_index = 0 #0 = slime, 1 = zombie, 2 = zombie_boss
game_over = 0
random_stat_list = []
random_stat_list_monsters = []
gold = 0
game_map = 0
#controls player action
action_index = 0 #0 = attack
#turns counter
stage_counter = 0
#fonts
font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 10)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
darker_orange = (254,110,0)

#load assets#
background_img = pygame.image.load('Images/Background/BackgroundNew.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
victory_img = pygame.image.load('Images/Icon/Banners0.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Banners1.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Banners2.png').convert_alpha()
allocate_img = pygame.image.load('Images/Icon/Banners3.png').convert_alpha()
stat_point_img = pygame.image.load('Images/Icon/Banners4.png').convert_alpha()

#characters
#----------------------------------------------------------------------------------hero
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_amount, stamina_recovery, stamina_threshold, turn_amount, turn_threshold, fireball_charge, lightning_charge)

##hero

Character.Random_Stats_Hero(random_stat_list)
hero = Character.Hero(200, 265, 'Hero', 50, 20, 1, 1, 2, 2, 1, 0, 1500, 0, 0, 25, 0, random_stat_list[0], random_stat_list[1], random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 0, 0, 0, 0, 0, 10, 10000, 0, 10000, 0, 0, 0, 0, 0, 1, 1)
random_stat_list.clear()

#----------------------------------------------------------------------------------monster
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

##slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(530, 350, 'Slime', 10, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime1 = Character.Slime(650, 350, 'Slime', 10, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)

##zombie

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie0 = Character.Zombie(530, 265, 'Zombie', 18, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie1 = Character.Zombie(650, 265, 'Zombie', 18, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)

##zombie boss

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie_boss0 = Character.Zombie_Boss(530, 265, 'Zombie Boss', 650, 10, 3, 3, 1, 1, 100, 100, 1, 0, 10 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(35,40), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

zombie_boss_list = []
zombie_boss_list.append(zombie_boss0)

##zombie and slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime2 = Character.Slime(530, 350, 'Slime', 10, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie2 = Character.Zombie(650, 265, 'Zombie', 18, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0)
random_stat_list_monsters.clear()

zombie_and_slime_list = []
zombie_and_slime_list.append(slime2)
zombie_and_slime_list.append(zombie2)

###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)
monster_list.append(zombie_boss_list)
monster_list.append(zombie_and_slime_list)

#bars
##hero
hero_health_bar = Bars.Health_Bar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
hero_shield_bar = Bars.Shield_Bar(20, screen_height - bottom_panel + 40)
hero_mana_bar = Bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
hero_experience_bar = Bars.Experience_Bar(0, screen_height - 13)
##slime
slime0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
slime1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
slime0_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
slime1_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 100)
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
slime_shield_list = []
slime_shield_list.append(slime0_shield_bar)
slime_shield_list.append(slime1_shield_bar)
##zombie
zombie0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
zombie1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
zombie0_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
zombie1_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 100)
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
zombie_shield_list = []
zombie_shield_list.append(zombie0_shield_bar)
zombie_shield_list.append(zombie1_shield_bar)
##zombie boss
zombie_boss_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie_boss0.hp, zombie_boss0.max_hp)
zombie_boss_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
zombie_boss_health_list = []
zombie_boss_health_list.append(zombie_boss_health_bar)
zombie_boss_shield_list = []
zombie_boss_shield_list.append(zombie_boss_shield_bar)
##zombie and slime
zombie2_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie2.hp, zombie2.max_hp)
slime2_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, slime2.hp, slime2.max_hp)
zombie2_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
slime2_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 100)
zombie_and_slime_health_list = []
zombie_and_slime_health_list.append(zombie2_health_bar)
zombie_and_slime_health_list.append(slime2_health_bar)
zombie_and_slime_shield_list = []
zombie_and_slime_shield_list.append(zombie2_shield_bar)
zombie_and_slime_shield_list.append(slime2_shield_bar)
###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)
monster_health_list.append(zombie_and_slime_health_list)
monster_shield_list = []
monster_shield_list.append(slime_shield_list)
monster_shield_list.append(zombie_shield_list)
monster_shield_list.append(zombie_boss_shield_list)
monster_shield_list.append(zombie_and_slime_shield_list)

#button
restart_button = Bars.Button(screen, (screen_width / 2) - 125 , 160, reset_img, 250, 50)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = monster.start_frame_index
		monster.action = monster.start_action		

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

def collide():
	mousex, mousey = pygame.mouse.get_pos()
	for monster in monster_list[monster_index]:
		head = monster.head_hitbox
		body = monster.body_hitbox
		leg = monster.leg_hitbox
		limb_list = [head,body,leg]
		if monster.hitbox.collidepoint((mousex,mousey)):
			screen.blit(font.render('NAME:' + str(monster.name), True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 40))
			screen.blit(font.render(f'STR: {monster.strength:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 20))
			screen.blit(font.render(f'INT: {monster.intelligence:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y))
			screen.blit(font.render(f'LUC: {monster.luck:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 20))
			screen.blit(font.render(f'AGI: {monster.agility:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 40))
			screen.blit(font.render(f'END: {monster.endurance:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 60))
			screen.blit(font.render(f'DEF: {monster.defense:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 80))
			screen.blit(font.render(f'SPD: {monster.speed:.2f} + {monster.agility / 5:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 100))
			for limb in limb_list:
				if limb.collidepoint((mousex, mousey)):
					if limb == head:
						draw_text('HEAD', font, red, mousex, mousey - 25)
						if left_click == True:
							attack = True
							target = monster
							target_limb = 'head'
							return target_limb, target, attack							
					if limb == body:
						draw_text('BODY', font, red, mousex, mousey - 25)
						if left_click == True:
							attack = True
							target = monster
							target_limb = 'body'
							return target_limb, target, attack		
					if limb == leg:
						draw_text('LEG', font, red, mousex, mousey - 25)
						if left_click == True:
							attack = True
							target = monster
							target_limb = 'leg'
							return target_limb, target, attack

def return_hero_buff(hero):
	#self buff return
	hero.strength -= hero.temp_strength
	hero.intelligence -= hero.temp_intelligence
	hero.agility -= hero.temp_agility
	hero.luck -= hero.temp_luck
	hero.endurance -= hero.temp_endurance

	hero.temp_strength = 0
	hero.temp_intelligence = 0
	hero.temp_agility = 0
	hero.temp_luck = 0
	hero.temp_endurance = 0

def return_boss_debuff(hero, monster_list, monster_index):
	#return boss debuff
	hero.strength -= monster_list[monster_index][0].temp_strength
	hero.intelligence -= monster_list[monster_index][0].temp_intelligence
	hero.agility -= monster_list[monster_index][0].temp_agility
	hero.luck -= monster_list[monster_index][0].temp_luck
	hero.endurance -= monster_list[monster_index][0].temp_endurance

	monster_list[monster_index][0].temp_strength = 0
	monster_list[monster_index][0].temp_intelligence = 0
	monster_list[monster_index][0].temp_agility = 0
	monster_list[monster_index][0].temp_luck = 0
	monster_list[monster_index][0].temp_endurance = 0

#inventory and skills
inventory = []
skills_list = ['normal_attack']
chosen_skill = 0

#events
event_1 = True

#skill turn counters
fireball_turn_counter = 0
shield_turn_counter = 0
speed_counter = 0

turn_counter = 0
boost = False

battle_over = False

monster_attack_time = 0
counter_time = 0
shield_up = False
stomp = False
counter_chance = True

fireball_consumable_active = True
lightning_consumable_active = False

boss_turn_amount = 0

#sprites
skill_sprite_group = pygame.sprite.Group()
monster_skill_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click)

#event 0
Level_Events.lvl_up_event_0(hero, monster_list, monster_index, skills_list)

run = True
while run:
	#how fast the game runs
	clock.tick(fps)

	if hero.fireball_charge > 3:
		hero.fireball_charge = 3
	if hero.lightning_charge > 3:
		hero.lightning_charge = 3

	if monster_index != -1:
		#draw background
		Load_Interface.draw_background(background_img)
		#---------------------------#
		#draw panel
		Load_Interface.draw_panel(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen)
		#---------------------------#
		#draw hero bars
		hero_health_bar.draw(hero.hp, hero.max_hp)
		hero_mana_bar.draw(hero.mp, hero.max_mp)
		hero_experience_bar.draw(hero.experience, experiencethreshold)
		hero_shield_bar.draw(hero.shield, hero.max_hp)
		#---------------------------#
		#draw hero
		hero.update()
		hero.draw()
		#---------------------------#
		#draw each monster's health bar according to each spawned
		for count, monster_health_bar in enumerate(monster_health_list[monster_index]):
			monster_health_bar.draw(monster_list[monster_index][count].hp, monster_list[monster_index][count].max_hp)
		#draw monster shield bars
		for count, monster_shield_bar in enumerate(monster_shield_list[monster_index]):		
			monster_shield_bar.draw(monster_list[monster_index][count].shield, monster_list[monster_index][count].max_hp)
		#draw monsters
		for monster in monster_list[monster_index]:
			monster.update()
			monster.draw()
		#---------------------------#
		skill_sprite_group.update()
		skill_sprite_group.draw(screen)
		monster_skill_sprite_group.update()
		monster_skill_sprite_group.draw(screen)
		damage_text_group.update()
		damage_text_group.draw(screen)
		#---------------------------#
		#current attack picture
		Load_Interface.draw_current_attack(action_index, inventory, skills_list)
		#stats
		Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, left_click, battle_over)
		#consumables
		Consumables.consumable_panel(hero, fireball_consumable_active, lightning_consumable_active)
		#---------------------------#
		try:
			target_limb, target, attack = collide()
		except:
			attack = False
			target = None
			target_limb = None			
		#---------------------------#
		if monster_index == 2:
			total_turns = 3
		else:
			total_turns = 4
		#---------------------------#
		#death
		if hero.hp <= 0:
			hero.alive = False
			hero.hp = 0
			hero.death()
			game_over = -1
		#---------------------------#
		#turn system
		if battle_over != True:
			Speed_Stamina.turn_calculations(boost, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group)
		#---------------------------#
		#hero guard
		if shield_up == True and 'guard' in skills_list and hero.stamina_amount > (hero.stamina_threshold * 0.5) and hero.shield == 0 and battle_over != True:
			hero.guard(skill_sprite_group, damage_text_group, skills_list)
			hero.stamina_amount -= (hero.stamina_threshold * 0.5)

		#hero stomp
		if stomp == True and 'stomp' in skills_list and hero.stamina_amount > (hero.stamina_threshold * 0.5) and battle_over != True:
			hero.stomp(target, damage_text_group, monster_list, monster_index, skills_list)
			hero.stamina_amount -= (hero.stamina_threshold * 0.5)

		#counter
		if counter_chance == True and battle_over != True:
			pygame.draw.rect(screen, green, ((screen_width / 2) - 170, screen_height - bottom_panel - 10, 20, 20))
		if right_click == True and counter_chance == True and battle_over != True:
			counter_chance, counter_time = hero.counter(right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skills_list)
		#---------------------------#	

		#player action
		if game_over == 0 and hero.alive == True and hero.turn_amount >= hero.turn_threshold:

			#start item effects
			if 6 in inventory and shield_turn_counter % 5 == 0 and hero.shield == 0:
				hero.guard(skill_sprite_group, damage_text_group, skills_list)
				shield_turn_counter += 1

			if 9 in inventory and fireball_turn_counter == 0:
				target = monster_list[monster_index][0]
				hero.fireball(action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)
				fireball_turn_counter += 1

			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#look for player action

				#attacks	
				if attack == True and target != None and target.alive == True:

					if 26 in inventory:
						for monster in monster_list[monster_index]:
							if monster.alive != False:
								monster.hp -= hero.intelligence * 0.2
								damage_text = Character.Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-60,60), monster.hitbox.y + 30 + random.randint(-30,30), f'HP -{hero.intelligence * 0.2:.2f}', yellow)	
								damage_text_group.add(damage_text)	

					#normal attack
					if action_index == 0:
						hero.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list)						
						hero.turn_amount = 0
						action_cooldown = 0
						
					#cleave
					if action_index == 1 and hero.mp >= 7.5:
						hero.cleave(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
						hero.mp -= 7.5
						hero.turn_amount = 0
						action_cooldown = 0

					#zombie stab
					if action_index == 2 and hero.mp >= 10:
						hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
						hero.mp -= 10
						hero.turn_amount = 0
						action_cooldown = 0

					#triple combo
					if action_index == 3 and hero.mp >= 10:
						hero.triple_combo(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, skills_list)
						hero.mp -= 10
						hero.turn_amount = 0
						action_cooldown = 0

					#self buff return
					return_hero_buff(hero)

					turn_counter += 1
					shield_turn_counter += 1
					counter_chance = True

		#enemy action
		#single enemy
		if len(monster_list[monster_index]) == 1:
			if hero.alive != False and hero.hp > 0 and monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

				#return boss debuff
				return_boss_debuff(hero, monster_list, monster_index)

				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					roll_guard_chance = random.randint(0,100)
					if monster_list[monster_index][0].alive != False:
						if monster_list[monster_index][0] == zombie_boss0 and boss_turn_amount % 3 == 0:
							monster_list[monster_index][0].scream(hero, damage_text_group, monster_skill_sprite_group, inventory)
						else:
							if roll_guard_chance > 70:
								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
							monster_list[monster_index][0].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						boss_turn_amount += 1
						hero.shield = 0 
						action_cooldown = 0
						monster_list[monster_index][0].monster_turn_amount = 0		

				if monster_list[monster_index][0].alive == False:
					 monster_list[monster_index][0].death()

		#two enemies
		if len(monster_list[monster_index]) == 2 and hero.alive != False and hero.hp > 0: 
				
				if monster_list[monster_index][0].alive == True and monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:

						#monster skills
						if monster_list[monster_index][0] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 30:
							monster_list[monster_index][0].armor_corrosion(hero, damage_text_group, inventory)
						if monster_list[monster_index][0] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 70:
							monster_list[monster_index][0].toxic_bile(hero, damage_text_group, inventory)
						else:
							#monster guard
							roll_guard_chance = random.randint(0,100)
							if roll_guard_chance > 50:
								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
							monster_list[monster_index][0].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						hero.shield = 0 						
						action_cooldown = 0
						monster_list[monster_index][0].monster_turn_amount = 0	

					if monster_list[monster_index][0].alive == False:
						 monster_list[monster_index][0].death()
				
				if monster_list[monster_index][1].alive == True and monster_list[monster_index][1].monster_turn_amount >= monster_list[monster_index][1].monster_turn_threshold:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:

						#monster skills	
						if monster_list[monster_index][1] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 10:
							monster_list[monster_index][1].armor_corrosion(hero, damage_text_group, inventory)
						if monster_list[monster_index][1] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 70:
							monster_list[monster_index][1].toxic_bile(hero, damage_text_group, inventory)
						else:
							#monster guard
							roll_guard_chance = random.randint(0,100)
							if roll_guard_chance > 70:
								monster_list[monster_index][1].guard(skill_sprite_group, damage_text_group)
							monster_list[monster_index][1].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						hero.shield = 0 
						action_cooldown = 0
						monster_list[monster_index][1].monster_turn_amount = 0	

					if monster_list[monster_index][1].alive == False:
						 monster_list[monster_index][1].death()

		#phoenix feather revive
		if 28 in inventory and hero.alive == False:
			hero.hp += hero.max_hp
			hero.alive = True
			hero.action = 0
			inventory.remove(28)

	#check alive monsters to change game over condition
	if hero.alive != False and hero.hp > 0:
		alive_monster = 0
		for monster in monster_list[monster_index]:
			if monster.alive == True:
				alive_monster += 1
		if alive_monster == 0:
			game_over = 1
	else:
		game_over = -1

	#if it's a game over -> defeat or victory
	if game_over != 0 and monster_index != -1:
		if game_over == 1:
			screen.blit(victory_img, ((screen_width / 2) - 125, 100))
			battle_over = True
			#reset

			return_hero_buff(hero)
			return_boss_debuff(hero, monster_list, monster_index)

			hero.shield = 0
			turn_counter = 0
			fireball_turn_counter = 0
			shield_turn_counter = 0
			hero.turn_amount = 0
			hero.stamina_amount = 0
			boss_turn_amount = 0
			if len(monster_list[monster_index]) != 1:
				monster_list[monster_index][0].monster_turn_amount = 0
				monster_list[monster_index][1].monster_turn_amount = 0
			else:
				monster_list[monster_index][0].monster_turn_amount = 0				
			counter_time = 0
			monster_attack_time = 0
			counter_chance = True

			if hero.statpoints > 0:
				screen.blit(allocate_img, ((screen_width / 2) - 125, 160))
				screen.blit(stat_point_img, ((screen_width / 2) - 125, 220))
			else:
				if restart_button.draw():
					if hero.mp < hero.max_mp:
						hero.mp += hero.mp_regen
					#trigger level up event	
					if hero.level % 1 == 0 and event_1 == True:
						if 'guard' in skills_list:
							Level_Events.lvl_up_event_1_guard(hero, monster, monster_list, monster_index, skills_list)
							event_1 = False
						elif 'stomp' in skills_list:
							Level_Events.lvl_up_event_1_stomp(hero, monster, monster_list, monster_index, skills_list)
							event_1 = False							
					#platformer map menu
					monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click)
					#trigger events if move to next map
					if monster_encounter == False:
						random_event_index = random.randint(0,5)
						Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)
					#reset spawns and monsters			
					start_spawn()
					for i in range(len(monster_list)):
						for monster in monster_list[i]:
							monster.level_up_monster(hero)
					if 14 in inventory:
						zombie_stab_active = True
					battle_over = False
					action_cooldown = 0
					game_over = 0

			if game_over == -1:
				screen.blit(defeat_img, ((screen_width / 2) - 120, 100))
				if restart_button.draw():
					run = False
					sys.exit()

	elif monster_index == -1:
		monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click)
		if monster_encounter == False:
			random_event_index = random.randint(0,1)
			roll_event_chance = random.randint(0,100)
			if roll_event_chance > 0:
				Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)			
		start_spawn()
		action_cooldown = 0
		game_over = 0

	left_click = False
	right_click = False	
	shield_up = False
	stomp = False

	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN: #left
			left_click = True
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #right
			right_click = True			
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_e:
				boost = False	
		if event.type == pygame.KEYDOWN:
				#stamina
			if event.key == pygame.K_e and hero.turn_amount <= hero.turn_threshold:
				boost = True
				#shield
			if event.key == pygame.K_LALT:
				if 'guard' in skills_list:
					shield_up = True
				else:
					stomp = True
				#skills
			if event.key == pygame.K_q:
				all_skills_list = ['normal_attack', 'cleave', 'zombie_stab', 'triple_combo']
				chosen_skill += 1

				while True:
					if chosen_skill > len(skills_list) - 1:
						chosen_skill = 0
						action_index = 0
					if skills_list[chosen_skill] in all_skills_list:

						action_index = all_skills_list.index(skills_list[chosen_skill])
						break
					else:
						chosen_skill +=1

				#inventory
			if event.key == pygame.K_z:
				Screen_Menus.options_menu(inventory, monster_list, monster_index, hero)
			if event.key == pygame.K_x:
				fireball_consumable_active, lightning_consumable_active = Consumables.consumable_menu(inventory, monster_list, monster_index)
			if event.key == pygame.K_r: 
				if hero.fireball_charge != 0 and fireball_consumable_active == True:
					hero.fireball_charge -= 1
					Consumables.consumable_1(hero, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active, skills_list)
				if hero.lightning_charge != 0 and lightning_consumable_active == True:
					hero.lightning_charge -= 1
					hero.turn_amount += hero.turn_threshold * 0.25
					Consumables.consumable_1(hero, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active, skills_list)

	pygame.display.update()

pygame.quit()

#drop item in character

#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_recovery, stamina_threshold, fireball_charge, lightning_charge)
#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)
