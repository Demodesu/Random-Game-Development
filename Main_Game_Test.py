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
#load assets#
background_img = pygame.image.load('Images/Background/BackgroundNew.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_img = pygame.image.load('Images/Icon/SwordButton.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (50,50))
victory_img = pygame.image.load('Images/Icon/Banners0.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Banners1.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Banners2.png').convert_alpha()
allocate_img = pygame.image.load('Images/Icon/Banners3.png').convert_alpha()
stat_point_img = pygame.image.load('Images/Icon/Banners4.png').convert_alpha()

#characters
##hero
Character.Random_Stats_Hero(random_stat_list)
#(x, y, name, max_hp, max_mp, level, experience, statpoints, strength, intelligence, defense, luck, agility, endurance, shield, mana_potion, health_potion, gold, speed, hp_regen, mp_regen, stamina_recovery, stamina_threshold, added_strength, added_intelligence, added_agility, added_luck, added_endurance, fireball_charge, lightning_charge)
hero = Character.Hero(200, 265, 'Hero', 40, 20, 1, 0, 0, random_stat_list[0], random_stat_list[1], 0, random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 2, 2, 1000, 5, 1, 1, 1.5, 1500, 0, 0, 0, 0, 0, 2, 2)
##slime
#(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, agility, endurance, shield, health_potion, gold, speed, hp_regen, mp_regen)
Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(530, 350, 'Slime', 10, 10, 1, 3, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 50, 3 + random.randint(0,1), 1, 1)
slime1 = Character.Slime(650, 350, 'Slime', 10, 10, 1, 3, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 50, 3 + random.randint(0,1), 1, 1)
slime_list = []
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)
##zombie
zombie0 = Character.Zombie(530, 265, 'Zombie', 15, 10, 1, 6, random_stat_list_monsters[0] + random.randint(2,3), random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 80, 2 + random.randint(0,1), 1, 1)
zombie1 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 6, random_stat_list_monsters[0] + random.randint(2,3), random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 80, 2 + random.randint(0,1), 1, 1)
zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)
##zombie boss
zombie_boss0 = Character.Zombie_Boss(530, 265, 'Zombie Boss', 80, 10, 1, 25, random_stat_list_monsters[0] + random.randint(15,20), random_stat_list_monsters[1] + 10, 2, random_stat_list_monsters[2] + 10, random_stat_list_monsters[3] + 10, random_stat_list_monsters[4] + 10, 0, 1, 200, 2 + random.randint(0,1), 1, 1)
zombie_boss_list = []
zombie_boss_list.append(zombie_boss0)
###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)
monster_list.append(zombie_boss_list)

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
###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)
monster_shield_list = []
monster_shield_list.append(slime_shield_list)
monster_shield_list.append(zombie_shield_list)
monster_shield_list.append(zombie_boss_shield_list)

#button
restart_button = Bars.Button(screen, (screen_width / 2) - 125 , 120, reset_img, 250, 50)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = monster.start_frame_index
		monster.action = monster.start_action		

def collide():
	global target
	global attack
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for count, monster in enumerate(monster_list[monster_index]):
		if monster.hitbox.collidepoint((mousex,mousey)):
			screen.blit(font.render('NAME:' + str(monster.name), True, blue), (mousex - 100, mousey - 40))
			screen.blit(font.render('STR:' + str(monster.strength), True, blue), (mousex - 100, mousey - 20))
			screen.blit(font.render('INT:' + str(monster.intelligence), True, blue), (mousex - 100, mousey))
			screen.blit(font.render('LUC:' + str(monster.luck), True, blue), (mousex - 100, mousey + 20))
			screen.blit(font.render('AGI:' + str(monster.agility), True, blue), (mousex - 100, mousey + 40))
			screen.blit(font.render('END:' + str(monster.endurance), True, blue), (mousex - 100, mousey + 60))
			screen.blit(font.render('DEF:' + str(monster.defense), True, blue), (mousex - 100, mousey + 80))
			screen.blit(font.render('SPD:' + str(monster.speed), True, blue), (mousex - 100, mousey + 100))
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, (mousex - 10, mousey - 10))
			if left_click == True:
				attack = True
				target = monster_list[monster_index][count]

#drop item test
inventory = []

#skill active
guard_heal_active = False
cleave_active = False
zombie_stab_active = False

#events
event_1 = True

#skill turn counters
fireball_turn_counter = 0
shield_turn_counter = 0
speed_counter = 0

hero_turn_amount = 0
hero_turn_amount_threshold = 1500
hero_stamina_amount = 0
turn_counter = 0
boost = False

monster0_turn_amount = 0
monster1_turn_amount = 0
monster_turn_amount_threshold = 1500

battle_over = False

monster0_death = False
monster1_death = False

monster_attack_time = 0
counter_time = 0
shield_up = False
counter_chance = True

fireball_consumable_active = False
lightning_consumable_active = False

#sprites
skill_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click)
run = True
while run:
	#how fast the game runs
	clock.tick(fps)

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
		damage_text_group.update()
		damage_text_group.draw(screen)
		#---------------------------#
		#current attack picture
		Load_Interface.draw_current_attack(action_index, cleave_active, zombie_stab_active, inventory)
		#stats
		Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, left_click, battle_over)
		#consumables
		Consumables.consumable_panel(hero, fireball_consumable_active, lightning_consumable_active)
		#---------------------------#
		#default game variables
		attack = False
		target = None
		#---------------------------#
		#clicking on the target returns true value
		#make sure mouse is visible
		collide()
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
			hero_turn_amount, hero_stamina_amount, monster0_turn_amount, monster1_turn_amount = Speed_Stamina.turn_calculations(hero_turn_amount, hero_turn_amount_threshold, hero_stamina_amount, boost, monster0_turn_amount, monster1_turn_amount, monster_turn_amount_threshold, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group)
		#---------------------------#
		#hero guard
		if shield_up == True and hero_stamina_amount > (hero.stamina_threshold * 0.5) and (monster0_turn_amount < monster_turn_amount_threshold or monster1_turn_amount < monster_turn_amount_threshold) and hero.shield == 0 and battle_over != True:
			hero.guard(skill_sprite_group, damage_text_group, guard_heal_active)
			hero_stamina_amount -= (hero.stamina_threshold * 0.5)

		#counter
		if counter_chance == True and battle_over != True:
			pygame.draw.rect(screen, green, ((screen_width / 2) - 170, screen_height - bottom_panel - 10, 20, 20))
		if right_click == True and counter_chance == True and battle_over != True and hero_turn_amount != hero_turn_amount_threshold:
			counter_chance, counter_time = hero.counter(right_click, counter_chance, battle_over, hero_turn_amount, hero_turn_amount_threshold, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, monster0_turn_amount, monster1_turn_amount)

		#player action
		if game_over == 0 and hero.alive == True and hero_turn_amount >= hero_turn_amount_threshold:

			#start item effects
			if 6 in inventory and shield_turn_counter % 5 == 0 and hero.shield == 0:
				hero.guard(skill_sprite_group, damage_text_group, guard_heal_active)
				shield_turn_counter += 1

			if 9 in inventory and fireball_turn_counter == 0:
				target = monster_list[monster_index][0]
				hero.fireball(action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
				fireball_turn_counter += 1

			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#look for player action

				#attacks	
				if attack == True and target != None and target.alive == True:

					#normal attack
					if action_index == 0:
						hero.attack(action_cooldown, target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)
						hero_turn_amount = 0
						action_cooldown = 0

					#cleave
					if action_index == 1 and hero.mp >= 7.5:
						hero.cleave(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, cleave_active, skill_sprite_group)
						hero.mp -= 7.5
						hero_turn_amount = 0
						action_cooldown = 0

					#zombie stab
					if action_index == 2 and hero.mp >= 10:
						hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, zombie_stab_active, skill_sprite_group)
						hero.mp -= 10
						hero_turn_amount = 0
						action_cooldown = 0

					turn_counter += 1
					shield_turn_counter += 1
					counter_chance = True

		#enemy action
		#single enemy
		if len(monster_list[monster_index]) == 1:
			if hero.alive != False and hero.hp > 0 and monster0_turn_amount >= monster_turn_amount_threshold:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					roll_guard_chance = random.randint(0,100)
					if monster_list[monster_index][0].alive != False:
						if monster_list[monster_index][0].hp < monster_list[monster_index][0].max_hp * 0.2 or roll_guard_chance > 70:
							monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group, guard_heal_active)
						monster_list[monster_index][0].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						hero.shield = 0 
						action_cooldown = 0
						monster0_turn_amount = 0		

				if monster_list[monster_index][0].alive == False:
					 monster_list[monster_index][0].death()

		#two enemies
		if len(monster_list[monster_index]) == 2 and hero.alive != False and hero.hp > 0: 
				
				if monster_list[monster_index][0].alive == True and monster0_turn_amount >= monster_turn_amount_threshold:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:

						#monster skills
						if monster_index == 0 and hero.shield > 0 and random.randint(0,100) > 30:
							monster_list[monster_index][0].armor_corrosion(hero, damage_text_group, inventory)
						if monster_index == 1 and random.randint(0,100) > 70:
							monster_list[monster_index][0].toxic_bile(hero, damage_text_group, inventory)
						else:
							#monster guard
							roll_guard_chance = random.randint(0,100)
							if monster_list[monster_index][0].hp < monster_list[monster_index][0].max_hp * 0.2 or roll_guard_chance > 50:
								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group, guard_heal_active)
							monster_list[monster_index][0].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						hero.shield = 0 						
						action_cooldown = 0
						monster0_turn_amount = 0	

					if monster_list[monster_index][0].alive == False:
						 monster_list[monster_index][0].death()
				
				if monster_list[monster_index][1].alive == True and monster1_turn_amount >= monster_turn_amount_threshold:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:

						#monster skills	
						if monster_index == 0 and hero.shield > 0 and random.randint(0,100) > 10:
							monster_list[monster_index][1].armor_corrosion(hero, damage_text_group, inventory)
						if monster_index == 1 and random.randint(0,100) > 70:
							monster_list[monster_index][1].toxic_bile(hero, damage_text_group, inventory)
						else:
							#monster guard
							roll_guard_chance = random.randint(0,100)
							if monster_list[monster_index][1].hp < monster_list[monster_index][1].max_hp * 0.2 or roll_guard_chance > 70:
								monster_list[monster_index][1].guard(skill_sprite_group, damage_text_group, guard_heal_active)
							monster_list[monster_index][1].attack(hero, damage_text_group, inventory)

						monster_attack_time = pygame.time.get_ticks()

						hero.shield = 0 
						action_cooldown = 0
						monster1_turn_amount = 0	

					if monster_list[monster_index][1].alive == False:
						 monster_list[monster_index][1].death()

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
			screen.blit(victory_img, ((screen_width / 2) - 120, 50))
			battle_over = True
			#reset
			hero.shield = 0
			turn_counter = 0
			fireball_turn_counter = 0
			shield_turn_counter = 0
			hero_turn_amount = 0
			hero_stamina_amount = 0
			monster0_turn_amount = 0
			monster1_turn_amount = 0
			counter_time = 0
			monster_attack_time = 0
			counter_chance = True

			if hero.statpoints > 0:
				screen.blit(allocate_img, ((screen_width / 2) - 125, 120))
				screen.blit(stat_point_img, ((screen_width / 2) - 125, 180))
			else:
				if restart_button.draw():
					if hero.mp < hero.max_mp:
						hero.mp += hero.mp_regen
					#trigger level up event	
					if hero.level % 1 == 0 and event_1 == True:
						guard_heal_active, cleave_active = Level_Events.lvl_up_event_1(hero, monster, monster_list, monster_index)
						event_1 = False
					#platformer map menu
					monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click)
					#trigger events if move to next map
					if monster_encounter == False:
						random_event_index = random.randint(0,1)
						roll_event_chance = random.randint(0,100)
						if roll_event_chance > 0:
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
				screen.blit(defeat_img, ((screen_width / 2) - 120, 50))
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
			if event.key == pygame.K_LALT:
				shield_up = False	
		if event.type == pygame.KEYDOWN:
				#stamina
			if event.key == pygame.K_e and hero_turn_amount <= hero_turn_amount_threshold:
				boost = True
				#shield
			if event.key == pygame.K_LALT:
				shield_up = True
				#skills
			if event.key == pygame.K_1:
				action_index = 0
			if cleave_active == True and event.key == pygame.K_2:
				action_index = 1
			if zombie_stab_active == True and event.key == pygame.K_3:
				action_index = 2
				#inventory
			if event.key == pygame.K_z:
				Screen_Menus.options_menu(inventory, monster_list, monster_index, hero)
			if event.key == pygame.K_x:
				fireball_consumable_active, lightning_consumable_active = Consumables.consumable_menu(inventory, monster_list, monster_index)
			if event.key == pygame.K_r: 
				if hero.fireball_charge != 0 and fireball_consumable_active == True:
					hero.fireball_charge -= 1
					Consumables.consumable_1(hero, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active)
				if hero.lightning_charge != 0 and lightning_consumable_active == True:
					hero.lightning_charge -= 1
					hero_turn_amount += hero_turn_amount_threshold * 0.2
					Consumables.consumable_1(hero, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active)

	pygame.display.update()

pygame.quit()

#drop item in character