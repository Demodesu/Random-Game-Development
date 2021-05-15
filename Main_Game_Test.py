# import math, pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events, Speed_Stamina, Consumables

# pygame.init()

# #set framerate
# clock = pygame.time.Clock()
# fps = 120

# #game window#
# bottom_panel = 150
# screen_width, screen_height = 800, 400 + bottom_panel
# screen = pygame.display.set_mode((screen_width,screen_height))
# pygame.display.set_caption('Battle')

# #define game variables
# experiencethreshold = [5]
# left_click = False
# right_click = False
# attack = False
# target = None
# monster_index = 0 #0 = slime, 1 = zombie, 2 = zombie_boss
# game_over = 0
# random_stat_list = []
# random_stat_list_monsters = []
# gold = 0
# game_map = 0
# #controls player action
# action_index = 0 #0 = attack
# #turns counter
# stage_counter = 0
# #fonts
# font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 10)

# #define colors
# red = (255,0,0)
# green = (0,255,0)
# blue = (0,0,255)
# yellow = (255,255,0)
# orange = (255,165,0)
# darker_orange = (254,110,0)

# #load assets#
# background_img = pygame.image.load('Images/Background/BackgroundNew.png').convert_alpha()
# background_img = pygame.transform.scale(background_img,(800,400))
# panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
# victory_img = pygame.image.load('Images/Icon/Banners0.png').convert_alpha()
# defeat_img = pygame.image.load('Images/Icon/Banners1.png').convert_alpha()
# reset_img = pygame.image.load('Images/Icon/Banners2.png').convert_alpha()
# allocate_img = pygame.image.load('Images/Icon/Banners3.png').convert_alpha()
# stat_point_img = pygame.image.load('Images/Icon/Banners4.png').convert_alpha()
# inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
# inventory_icon_img = pygame.transform.scale(inventory_icon_img,(44,44))
# active_skills_hitbox_img = pygame.image.load('Images/Icon/SkillIcons/ActiveButtons.png').convert_alpha()
# active_skills_hitbox_img = pygame.transform.scale(active_skills_hitbox_img,(44,44))

# #characters
# #----------------------------------------------------------------------------------hero
# #(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_amount, stamina_recovery, stamina_threshold, turn_amount, turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, position_bonus, buff_reset_time, buff_duration, attack cooldown, fireball_charge, lightning_charge):

# ##hero

# Character.Random_Stats_Hero(random_stat_list)
# hero = Character.Hero(200, 265, 'Hero', 50, 20, 1, 1, 2, 2, 1, 0, 2000, 0, 0, 25, 0, random_stat_list[0], random_stat_list[1], random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 0, 0, 0, 0, 0, 10, 10000, 0, 10000, 0, 0, 0, 0, 0, 5, 500, 0, 90, 1, 1)
# random_stat_list.clear()

# #----------------------------------------------------------------------------------monster
# #(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

# ##slime

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# slime0 = Character.Slime(530, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# slime1 = Character.Slime(650, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# slime_list = []
# slime_list.append(slime0)
# slime_list.append(slime1)

# ##zombie

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# zombie0 = Character.Zombie(530, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# zombie1 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# zombie_list = []
# zombie_list.append(zombie0)
# zombie_list.append(zombie1)

# ##zombie boss

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# zombie_boss0 = Character.Zombie_Boss(530, 265, 'ZombieBoss', 700, 10, 3, 3, 1, 1, 1000, 1000, 1, 0, 12 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(35,40), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# zombie_boss_list = []
# zombie_boss_list.append(zombie_boss0)

# ##zombie and slime

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# slime2 = Character.Slime(530, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# zombie2 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# zombie_and_slime_list = []
# zombie_and_slime_list.append(slime2)
# zombie_and_slime_list.append(zombie2)

# ##golem boss

# Character.Random_Stats_Monsters(random_stat_list_monsters)
# golem_boss0 = Character.Golem_Boss(530, 225, 'GolemBoss', 1900, 10, 3, 3, 1, 1, 2000, 2000, 7, 0, 8 + random.randint(-1,1), random_stat_list_monsters[0] + random.randint(60,80), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
# random_stat_list_monsters.clear()

# golem_boss_list = []
# golem_boss_list.append(golem_boss0)

# ###append all monsters into list
# monster_list = []
# monster_list.append(slime_list)
# monster_list.append(zombie_list)
# monster_list.append(zombie_boss_list)
# monster_list.append(zombie_and_slime_list)
# monster_list.append(golem_boss_list)

# #bars
# ##hero
# hero_health_bar = Bars.Health_Bar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
# hero_shield_bar = Bars.Shield_Bar(20, screen_height - bottom_panel + 40)
# hero_mana_bar = Bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
# hero_experience_bar = Bars.Experience_Bar(0, screen_height - 13)
# ##slime
# slime0_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
# slime1_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
# slime0_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
# slime1_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
# slime_health_list = []
# slime_health_list.append(slime0_health_bar)
# slime_health_list.append(slime1_health_bar)
# slime_shield_list = []
# slime_shield_list.append(slime0_shield_bar)
# slime_shield_list.append(slime1_shield_bar)
# ##zombie
# zombie0_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
# zombie1_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
# zombie0_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
# zombie1_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
# zombie_health_list = []
# zombie_health_list.append(zombie0_health_bar)
# zombie_health_list.append(zombie1_health_bar)
# zombie_shield_list = []
# zombie_shield_list.append(zombie0_shield_bar)
# zombie_shield_list.append(zombie1_shield_bar)
# ##zombie boss
# zombie_boss_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie_boss0.hp, zombie_boss0.max_hp)
# zombie_boss_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
# zombie_boss_health_list = []
# zombie_boss_health_list.append(zombie_boss_health_bar)
# zombie_boss_shield_list = []
# zombie_boss_shield_list.append(zombie_boss_shield_bar)
# ##zombie and slime
# zombie2_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie2.hp, zombie2.max_hp)
# slime2_health_bar = Bars.Health_Bar(screen_width  - 150, screen_height - bottom_panel + 100, slime2.hp, slime2.max_hp)
# zombie2_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
# slime2_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
# zombie_and_slime_health_list = []
# zombie_and_slime_health_list.append(zombie2_health_bar)
# zombie_and_slime_health_list.append(slime2_health_bar)
# zombie_and_slime_shield_list = []
# zombie_and_slime_shield_list.append(zombie2_shield_bar)
# zombie_and_slime_shield_list.append(slime2_shield_bar)
# ##golem boss
# golem_boss_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, golem_boss0.hp, golem_boss0.max_hp)
# golem_boss_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
# golem_boss_health_list = []
# golem_boss_health_list.append(golem_boss_health_bar)
# golem_boss_shield_list = []
# golem_boss_shield_list.append(golem_boss_shield_bar)

# ###append all monster's health bar into list
# monster_health_list = []
# monster_health_list.append(slime_health_list)
# monster_health_list.append(zombie_health_list)
# monster_health_list.append(zombie_boss_health_list)
# monster_health_list.append(zombie_and_slime_health_list)
# monster_health_list.append(golem_boss_health_list)
# monster_shield_list = []
# monster_shield_list.append(slime_shield_list)
# monster_shield_list.append(zombie_shield_list)
# monster_shield_list.append(zombie_boss_shield_list)
# monster_shield_list.append(zombie_and_slime_shield_list)
# monster_shield_list.append(golem_boss_shield_list)

# #button
# restart_button = Bars.Button(screen, (screen_width / 2) - 125 , 160, reset_img, 250, 50)

# def start_spawn():
# 	for count, monster in enumerate(monster_list[monster_index]):	
# 		monster.alive = True
# 		monster.hp = monster.max_hp
# 		monster.frame_index = 0
# 		monster.action = 0		

# def draw_text(text, font, text_col, x, y):
# 	img = font.render(text, True, text_col)
# 	choice_text = screen.blit(img, (x, y))

# def collide():
# 	mousex, mousey = pygame.mouse.get_pos()
# 	for monster in monster_list[monster_index]:
# 		head = monster.head_hitbox
# 		body = monster.body_hitbox
# 		leg = monster.leg_hitbox
# 		limb_list = [head,body,leg]
# 		if monster.hitbox.collidepoint((mousex,mousey)):
# 			screen.blit(font.render('NAME:' + str(monster.name), True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 40))
# 			screen.blit(font.render(f'STR: {monster.strength:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 20))
# 			screen.blit(font.render(f'INT: {monster.intelligence:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y))
# 			screen.blit(font.render(f'LUC: {monster.luck:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 20))
# 			screen.blit(font.render(f'AGI: {monster.agility:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 40))
# 			screen.blit(font.render(f'END: {monster.endurance:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 60))
# 			screen.blit(font.render(f'DEF: {monster.defense:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 80))
# 			screen.blit(font.render(f'SPD: {monster.speed:.2f} + {monster.agility / 5:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 100))
# 			for limb in limb_list:
# 				if limb.collidepoint((mousex, mousey)):
# 					if limb == head:
# 						draw_text('HEAD', font, red, mousex, mousey - 25)
# 						if left_click == True:
# 							attack = True
# 							target = monster
# 							target_limb = 'head'
# 							return target_limb, target, attack							
# 					if limb == body:
# 						draw_text('BODY', font, red, mousex, mousey - 25)
# 						if left_click == True:
# 							attack = True
# 							target = monster
# 							target_limb = 'body'
# 							return target_limb, target, attack		
# 					if limb == leg:
# 						draw_text('LEG', font, red, mousex, mousey - 25)
# 						if left_click == True:
# 							attack = True
# 							target = monster
# 							target_limb = 'leg'
# 							return target_limb, target, attack

# def return_hero_buff(hero):
# 	#self buff return
# 	hero.strength -= hero.temp_strength
# 	hero.intelligence -= hero.temp_intelligence
# 	hero.agility -= hero.temp_agility
# 	hero.luck -= hero.temp_luck
# 	hero.endurance -= hero.temp_endurance

# 	hero.temp_strength = 0
# 	hero.temp_intelligence = 0
# 	hero.temp_agility = 0
# 	hero.temp_luck = 0
# 	hero.temp_endurance = 0

# def return_boss_debuff(hero, monster_list, monster_index):
# 	#return boss debuff
# 	hero.strength -= monster_list[monster_index][0].temp_strength
# 	hero.intelligence -= monster_list[monster_index][0].temp_intelligence
# 	hero.agility -= monster_list[monster_index][0].temp_agility
# 	hero.luck -= monster_list[monster_index][0].temp_luck
# 	hero.endurance -= monster_list[monster_index][0].temp_endurance

# 	monster_list[monster_index][0].temp_strength = 0
# 	monster_list[monster_index][0].temp_intelligence = 0
# 	monster_list[monster_index][0].temp_agility = 0
# 	monster_list[monster_index][0].temp_luck = 0
# 	monster_list[monster_index][0].temp_endurance = 0

# #inventory and skills
# #inventory = [2,3,4,5,25,6,7,8,9,10,11,12,13,14,29,15,16,17,1,18,19,20,35,21,31,22,23,24,26,27,28,30,32,33,34]
# inventory = []
# skills_list = ['normal_attack', 'fireball', 'lightning']

# all_active_skills_list = ['normal_attack', 'cleave', 'zombie_stab', 'triple_combo', 'serpent_wheel', 'venomous_whip', 'thunder_bolt']
# active_skills_list = ['normal_attack']

# active_skills_indexes = {
# 	'normal_attack' : {'active_index' : 0},
# 	'cleave' : {'active_index' : 1},
# 	'triple_combo' : {'active_index' : 2},
# 	'zombie_stab' : {'active_index' : 3},
# 	'serpent_wheel' : {'active_index' : 4},
# 	'venomous_whip' : {'active_index' : 5},
# 	'thunder_bolt' : {'active_index' : 6}

# }

# skill_hitbox_active = 0

# skill_active_hitbox_indexes = {
# 	'hitbox' : {0 : (44,0), 1 : (88,0), 2 : (132,0), 3 : (176,0), 4 : (220,0)},	

# }

# chosen_skill = 0

# #events
# event_1 = True
# event_2 = True
# event_3 = True

# #bosses
# boss_defeated_list = []

# #skill turn counters
# fireball_turn_counter = 0
# lightning_turn_counter = 0
# shield_turn_counter = 0
# speed_counter = 0

# start_combat_time = 0
# level_up_time = 0

# turn_counter = 0
# boost = False

# battle_over = False

# monster_attack_time = 0
# counter_time = 0
# counter_chance = True

# fireball_consumable_active = True
# lightning_consumable_active = False

# boss_turn_amount = 0
# monster_special_skill = False

# #position
# hero_front_position = False
# hero_middle_position = True
# hero_back_position = False

# #sprites
# skill_sprite_group = pygame.sprite.Group()
# monster_skill_sprite_group = pygame.sprite.Group()
# damage_text_group = pygame.sprite.Group()

# #game#
# Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

# monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)

# #event 0
# Level_Events.lvl_up_event_0(hero, monster_list, monster_index, skills_list)

# run = True
# while run:
# 	#how fast the game runs
# 	clock.tick(fps)

# 	if monster_index != -1:

# 		#draw background
# 		Load_Interface.draw_background(background_img)
# 		#---------------------------#
# 		#draw panel
# 		Load_Interface.draw_panel(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen)
# 		#---------------------------#
# 		#draw hero bars
# 		hero_health_bar.draw(hero.hp, hero.max_hp)
# 		hero_mana_bar.draw(hero.mp, hero.max_mp)
# 		hero_experience_bar.draw(hero.experience, experiencethreshold)
# 		hero_shield_bar.draw(hero.shield, hero.max_hp)
# 		#---------------------------#
# 		#draw hero
# 		hero.update()
# 		hero.draw()
# 		#---------------------------#
# 		#draw each monster's health bar according to each spawned
# 		for count, monster_health_bar in enumerate(monster_health_list[monster_index]):
# 			monster_health_bar.draw(monster_list[monster_index][count].hp, monster_list[monster_index][count].max_hp)
# 		#draw monster shield bars
# 		for count, monster_shield_bar in enumerate(monster_shield_list[monster_index]):		
# 			monster_shield_bar.draw(monster_list[monster_index][count].shield, monster_list[monster_index][count].max_hp)
# 		#draw monsters
# 		for monster in monster_list[monster_index]:
# 			monster.update()
# 			monster.draw()
# 		#---------------------------#
# 		skill_sprite_group.update()
# 		skill_sprite_group.draw(screen)
# 		monster_skill_sprite_group.update()
# 		monster_skill_sprite_group.draw(screen)
# 		damage_text_group.update()
# 		damage_text_group.draw(screen)
# 		#---------------------------#
# 		#if battle is not over shown items
# 		Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, left_click, battle_over)
# 		#---------------------------#	
# 		if hero.rect.y < 150:
# 			hero.rect.y += 4
# 		#---------------------------#		
# 		if battle_over == False and hero.alive == True:
# 			#turn system
# 			Speed_Stamina.turn_calculations(boost, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group)
# 			#current attack picture
# 			Load_Interface.draw_current_attack(action_index, inventory, skills_list, hero, active_skills_list, all_active_skills_list)
# 			#consumables
# 			Consumables.consumable_panel(hero, fireball_consumable_active, lightning_consumable_active)
# 			#show skills icon highlights
# 			screen.blit(active_skills_hitbox_img,skill_active_hitbox_indexes['hitbox'][skill_hitbox_active])
			
# 			#balance and checks	
# 			if hero.fireball_charge > 3:
# 				hero.fireball_charge = 3
# 			if hero.lightning_charge > 3:
# 				hero.lightning_charge = 3
# 			if hero.hp > hero.max_hp:
# 				hero.hp = hero.max_hp
# 			if hero.mp > hero.max_mp:
# 				hero.mp = hero.max_mp

# 			#attack cooldown
# 			if hero.attack_cooldown > 0:
# 				hero.attack_cooldown -= 1

# 			#auto items
# 			#auto stomp from war drum and stone drum
# 			if 24 in inventory and start_combat_time % 800 == 0 and start_combat_time != 0:
# 				hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
# 			#auto water blast from hydra heart
# 			if -11 in inventory and start_combat_time % 400 == 0 and start_combat_time != 0:
# 				hero.water_blast(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
# 			#auto regen blast from blue ruby
# 			if -12 in inventory and start_combat_time % 300 == 0 and start_combat_time != 0:
# 				if hero.max_hp - hero.hp > (hero.hp_regen + hero.mp_regen):
# 					heal_amount = (hero.hp_regen + hero.mp_regen)
# 				else:
# 					heal_amount = hero.max_hp - hero.hp
# 				hero.hp += heal_amount
# 				heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 30, f'{heal_amount:.2f}', green)
# 				damage_text_group.add(heal_text)

# 			#combat start time
# 			start_combat_time += 1
# 		else:
# 			start_combat_time = 0
# 		#---------------------------#
# 		#draw inventory button
# 		inventory_button = screen.blit(inventory_icon_img, (0,0))
# 		#---------------------------#
# 		try:
# 			target_limb, target, attack = collide()
# 		except:
# 			attack = False
# 			target = None
# 			target_limb = None			
# 		#---------------------------#
# 		#hero guard
# 		if'guard' in skills_list and start_combat_time % 500 == 0 and start_combat_time != 0 and hero.shield == 0 and battle_over != True:
# 			hero.guard(skill_sprite_group, damage_text_group, skills_list, experiencethreshold, inventory, monster_list, monster_index, turn_counter)

# 		#hero stomp
# 		if'stomp' in skills_list and start_combat_time % 500 == 0 and start_combat_time != 0 and battle_over != True:
# 			hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)

# 		#counter
# 		if counter_chance == True and battle_over == False and hero.alive == True:
# 			pygame.draw.rect(screen, green, (hero.hitbox.x + 110, hero.hitbox.y - 10, 20, 20))
# 		if right_click == True and counter_chance == True and battle_over == False:
# 			counter_chance, counter_time = hero.counter(right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skills_list, skill_sprite_group)			

# 		#out of turn skills
# 		#thunder bolt
# 		if action_index == 6 and hero.mp >= 15 and attack == True and target != None and target.alive == True and hero.turn_amount != hero.turn_threshold:
# 			hero.thunder_bolt(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list)					
# 			attack = True 
# 			target = None
# 				#normal attack
# 		if action_index == 0 and attack == True and target != None and target.alive == True and hero.attack_cooldown == 0:
# 			hero.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group)	
# 			hero.attack_cooldown = 80
# 		#---------------------------#	
# 		#player action
# 		if game_over == 0 and hero.alive == True and hero.turn_amount >= hero.turn_threshold:

# 			#start item effects
# 			if 6 in inventory and shield_turn_counter % 3 == 0 and hero.shield == 0:
# 				hero.guard(skill_sprite_group, damage_text_group, skills_list, experiencethreshold, inventory, monster_list, monster_index, turn_counter)
# 				shield_turn_counter += 1

# 			if 9 in inventory and fireball_turn_counter == 0:
# 				target = monster_list[monster_index][0]
# 				hero.fireball(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)
# 				fireball_turn_counter += 1

# 			if -8 in inventory and lightning_turn_counter == 0:
# 				target = monster_list[monster_index][0]
# 				hero.lightning(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)
# 				lightning_turn_counter += 1

# 			#look for player action
# 			#attacks	
# 			if attack == True and target != None and target.alive == True:

# 				if 26 in inventory:
# 					for monster in monster_list[monster_index]:
# 						if monster.alive != False:
# 							monster.hp -= hero.intelligence * 0.2
# 							damage_text = Character.Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-60,60), monster.hitbox.y + 30 + random.randint(-30,30), f'HP -{hero.intelligence * 0.2:.2f}', yellow)	
# 							damage_text_group.add(damage_text)						
					
# 				#cleave
# 				elif action_index == 1 and hero.mp >= 7.5:
# 					hero.cleave(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
# 					hero.turn_amount = 0

# 				#triple combo
# 				elif action_index == 2 and hero.mp >= 10:
# 					hero.triple_combo(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, skills_list)
# 					hero.turn_amount = 0

# 				#zombie stab
# 				elif action_index == 3 and hero.mp >= 10:
# 					hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
# 					hero.turn_amount = 0

# 				#serpent wheel
# 				elif action_index == 4 and hero.mp >= 20:
# 					hero.serpent_wheel(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
# 					hero.turn_amount = 0

# 				#venomous whip
# 				elif action_index == 5 and hero.mp >= 20:
# 					hero.venomous_whip(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list)
# 					hero.turn_amount = 0

# 				#normal attack
# 				else:
# 					hero.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group)						
# 					hero.turn_amount = 0				

# 				#self buff return
# 				return_hero_buff(hero)

# 				turn_counter += 1
# 				shield_turn_counter += 1
# 				counter_chance = True
# 				if turn_counter % 3 == 0:
# 					monster_special_skill = True

# 		#enemy action
# 		#single enemy
# 		if len(monster_list[monster_index]) == 1 and hero.alive != False and hero.hp > 0:

# 			if monster_index == 2:
# 				if monster_special_skill == True:
# 					monster_list[monster_index][0].special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
# 					monster_special_skill = False
				
# 				if monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

# 					roll_guard_chance = random.randint(0,100)
# 					if monster_list[monster_index][0].alive != False:
# 						if boss_turn_amount % 3 == 0:
# 							monster_list[monster_index][0].scream(hero, damage_text_group, monster_skill_sprite_group, inventory)
# 						else:
# 							if roll_guard_chance > 80:
# 								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
# 							monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
# 							if 35 in inventory:
# 								hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

# 						monster_attack_time = pygame.time.get_ticks()

# 						boss_turn_amount += 1
# 						hero.shield = 0 
# 						monster_list[monster_index][0].monster_turn_amount = 0		

# 				if monster_list[monster_index][0].alive == False and len(boss_defeated_list) == 0:
# 					boss_defeated_list.append('zombie_boss')
# 					Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

# 			if monster_index == 4:
# 				if monster_special_skill == True:
# 					monster_list[monster_index][0].special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
# 					monster_special_skill = False

# 				if start_combat_time % 1000 == 0 and start_combat_time != 0:
# 					monster_list[monster_index][0].monster_turn_amount += monster_list[monster_index][0].monster_turn_threshold * 0.25
# 					boost_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 30, f'Boost', green)
# 					damage_text_group.add(boost_text)

# 				if monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

# 					roll_guard_chance = random.randint(0,100)
# 					if monster_list[monster_index][0].alive != False:
# 						if boss_turn_amount % 2 == 0:
# 							monster_list[monster_index][0].special_skill_2(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
# 						else:
# 							if roll_guard_chance > 80:
# 								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
# 							monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
# 						if 35 in inventory:
# 							hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

# 						monster_attack_time = pygame.time.get_ticks()

# 						boss_turn_amount += 1
# 						hero.shield = 0 
# 						monster_list[monster_index][0].monster_turn_amount = 0	

# 				if monster_list[monster_index][0].alive == False and len(boss_defeated_list) == 1:
# 					boss_defeated_list.append('golem_boss')
# 					Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

# 		#two enemies
# 		if len(monster_list[monster_index]) == 2 and hero.alive != False and hero.hp > 0: 
				
# 			if monster_list[monster_index][0].alive == True and monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

# 				#monster skills
# 				if monster_list[monster_index][0] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 30:
# 					monster_list[monster_index][0].armor_corrosion(hero, damage_text_group, inventory)
# 				if monster_list[monster_index][0] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 20:
# 					if random.randint(0,100) > 30:
# 						monster_list[monster_index][0].toxic_bile(hero, damage_text_group, inventory)
# 					else:
# 						monster_list[monster_index][0].vomit(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
# 				else:
# 					#monster guard
# 					roll_guard_chance = random.randint(0,100)
# 					if roll_guard_chance > 80:
# 						monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
# 					monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
# 					if 35 in inventory:
# 						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

# 				monster_attack_time = pygame.time.get_ticks()

# 				hero.shield = 0 						
# 				monster_list[monster_index][0].monster_turn_amount = 0	
		
# 			if monster_list[monster_index][1].alive == True and monster_list[monster_index][1].monster_turn_amount >= monster_list[monster_index][1].monster_turn_threshold:

# 				#monster skills	
# 				if monster_list[monster_index][1] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 10:
# 					monster_list[monster_index][1].armor_corrosion(hero, damage_text_group, inventory)
# 				if monster_list[monster_index][1] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 20:
# 					if random.randint(0,100) > 30:
# 						monster_list[monster_index][1].toxic_bile(hero, damage_text_group, inventory)
# 					else:
# 						monster_list[monster_index][1].vomit(hero, monster_skill_sprite_group, damage_text_group, inventory)
# 				else:
# 					#monster guard
# 					roll_guard_chance = random.randint(0,100)
# 					if roll_guard_chance > 80:
# 						monster_list[monster_index][1].guard(skill_sprite_group, damage_text_group)
# 					monster_list[monster_index][1].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
# 					if 35 in inventory:
# 						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

# 				monster_attack_time = pygame.time.get_ticks()

# 				hero.shield = 0 
# 				monster_list[monster_index][1].monster_turn_amount = 0	

# 		#check if dead and drop exp, loot, gold
# 		for monster in monster_list[monster_index]:
# 			hero.monster_death_drops(monster, experiencethreshold, inventory, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list)

# 		#phoenix feather revive
# 		if 28 in inventory and hero.alive == False:
# 			hero.hp += hero.max_hp * 0.5
# 			hero.alive = True
# 			hero.action = 0
# 			inventory.remove(28)

# 	#check alive monsters to change game over condition
# 	if hero.alive != False and hero.hp > 0:
# 		alive_monster = 0
# 		for monster in monster_list[monster_index]:
# 			if monster.alive == True:
# 				alive_monster += 1
# 		if alive_monster == 0:
# 			game_over = 1
# 	else:
# 		game_over = -1

# 	#if it's a game over -> defeat or victory
# 	if game_over != 0 and monster_index != -1:
# 		if game_over == 1:
# 			screen.blit(victory_img, ((screen_width / 2) - 125, 100))
# 			battle_over = True
# 			#reset

# 			if 'start_fireball' in skills_list:
# 				if hero.fireball_charge == 0:
# 					hero.fireball_charge = 1
# 			if 'start_lightning' in skills_list:
# 				if hero.lightning_charge == 0:
# 					hero.lightning_charge = 1

# 			hero.level_up_hero(inventory, experiencethreshold)

# 			return_hero_buff(hero)

# 			hero.shield = 0
# 			turn_counter = 0
# 			fireball_turn_counter = 0
# 			lightning_turn_counter = 0
# 			shield_turn_counter = 0
# 			hero.turn_amount = 0
# 			hero.stamina_amount = 0
# 			boss_turn_amount = 0
# 			monster_special_skill = False

# 			if len(monster_list[monster_index]) != 1:
# 				monster_list[monster_index][0].monster_turn_amount = 0
# 				monster_list[monster_index][1].monster_turn_amount = 0
# 			else:
# 				monster_list[monster_index][0].monster_turn_amount = 0				
# 			counter_time = 0
# 			monster_attack_time = 0
# 			counter_chance = True

# 			if hero.statpoints > 0:
# 				screen.blit(allocate_img, ((screen_width / 2) - 125, 160))
# 				screen.blit(stat_point_img, ((screen_width / 2) - 125, 220))
# 			else:
# 				if restart_button.draw():
# 					if hero.mp < hero.max_mp:
# 						hero.mp += hero.mp_regen

# 					if hero_back_position == True:
# 						hero_middle_position, hero_back_position = hero.move_back_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)
# 					elif hero_front_position == True:
# 						hero_front_position, hero_middle_position = hero.move_front_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)

# 					#trigger level up event	
# 					if hero.level > 1 and event_1 == True:
# 						Level_Events.lvl_up_event_1(hero, monster, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list)
# 						event_1 = False			

# 					if hero.level > 3 and event_2 == True:
# 						if 'guard' in skills_list:
# 							Level_Events.lvl_up_event_2_guard(hero, monster, monster_list, monster_index, skills_list)
# 							event_2 = False
# 						elif 'stomp' in skills_list:
# 							Level_Events.lvl_up_event_2_stomp(hero, monster, monster_list, monster_index, skills_list)
# 							event_2 = False		
# 						else:
# 							Level_Events.lvl_up_event_2(hero, monster, monster_list, monster_index, skills_list)
# 							event_2 = False				

# 					if hero.level > 6 and event_3 == True:
# 						if 'cleave' in skills_list:
# 							Level_Events.lvl_up_event_3_cleave(hero, monster, monster_list, monster_index, skills_list)
# 							event_3 = False
# 						elif 'triple_combo' in skills_list:
# 							Level_Events.lvl_up_event_3_triple_combo(hero, monster, monster_list, monster_index, skills_list)
# 							event_3 = False		
															
# 					#platformer map menu
# 					monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)
# 					#trigger events if move to next map
# 					if monster_encounter == False:
# 						random_event_index = random.randint(0,5)
# 						Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)
# 					#reset spawns and monsters			
# 					start_spawn()
# 					for monster_group in range(len(monster_list)):
# 						for monster in monster_list[monster_group]:
# 							monster.level_up_monster(hero)
# 					if 14 in inventory:
# 						zombie_stab_active = True
# 					battle_over = False
# 					game_over = 0

# 		if game_over == -1:
# 			screen.blit(defeat_img, ((screen_width / 2) - 120, 100))
# 			battle_over = True
# 			if restart_button.draw():
# 				run = False
# 				sys.exit()

# 	elif monster_index == -1:
# 		monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)
# 		if monster_encounter == False:
# 			random_event_index = random.randint(0,1)
# 			roll_event_chance = random.randint(0,100)
# 			if roll_event_chance > 0:
# 				Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)			
# 		start_spawn()
# 		game_over = 0

# 	left_click = False
# 	right_click = False	

# 	#check for events ex. mouse clicks, key down etc.
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			run = False
# 			sys.exit()

# 		if event.type == pygame.MOUSEBUTTONDOWN: #left
# 			if event.button == 1:
# 				left_click = True
# 				mousex, mousey = pygame.mouse.get_pos()
# 				if inventory_button.collidepoint((mousex,mousey)):
# 					Screen_Menus.options_menu(inventory, monster_list, monster_index, hero, skills_list, active_skills_list, all_active_skills_list)

# 			if event.button == 3:
# 				right_click = True	

# 			if event.button == 4 or event.button == 5:
# 				#consumables
# 				Consumables.consumable_1(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active, skills_list)

# 		if event.type == pygame.KEYUP:
# 			if event.key == pygame.K_e:
# 				boost = False	
# 		if event.type == pygame.KEYDOWN:
				
# 				#stamina
# 			if event.key == pygame.K_e and hero.turn_amount <= hero.turn_threshold:
# 				boost = True

# 				#movement
# 			if event.key == pygame.K_d and hero.stamina_amount > hero.stamina_threshold * 0.20:
# 				if hero_middle_position == True:
# 					hero_front_position, hero_middle_position = hero.move_middle_to_front(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)

# 				if hero_back_position == True:
# 					hero_middle_position, hero_back_position = hero.move_back_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)

# 			if event.key == pygame.K_a and hero.stamina_amount > hero.stamina_threshold * 0.20:
# 				if hero_middle_position == True:
# 					hero_middle_position, hero_back_position = hero.move_middle_to_back(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)					

# 				if hero_front_position == True:
# 					hero_front_position, hero_middle_position = hero.move_front_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)

# 				#consumables
# 			if event.key == pygame.K_x:
# 				fireball_consumable_active, lightning_consumable_active = Consumables.consumable_menu(inventory, monster_list, monster_index)

# 				#skills
# 			if event.key == pygame.K_1:
# 				action_index = active_skills_indexes[active_skills_list[0]]['active_index']
# 				skill_hitbox_active = 0

# 			if event.key == pygame.K_2 and len(active_skills_list) > 1:
# 				action_index = active_skills_indexes[active_skills_list[1]]['active_index']
# 				skill_hitbox_active = 1

# 			if event.key == pygame.K_3 and len(active_skills_list) > 2:
# 				action_index = active_skills_indexes[active_skills_list[2]]['active_index']
# 				skill_hitbox_active = 2

# 			if event.key == pygame.K_4 and len(active_skills_list) > 3:
# 				action_index = active_skills_indexes[active_skills_list[3]]['active_index']
# 				skill_hitbox_active = 3

# 			if event.key == pygame.K_5 and len(active_skills_list) > 4:
# 				action_index = active_skills_indexes[active_skills_list[4]]['active_index']
# 				skill_hitbox_active = 4

# 			if event.key == pygame.K_w:
# 				hero.jump()

# 	pygame.display.update()

# pygame.quit()

# #drop item in character

# #(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_recovery, stamina_threshold, fireball_charge, lightning_charge)
# #(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

import math,pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events, Speed_Stamina, Consumables, ctypes

user32 = ctypes.windll.user32
screensize_width, screensize_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

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
inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(44,44))
active_skills_hitbox_img = pygame.image.load('Images/Icon/SkillIcons/ActiveButtons.png').convert_alpha()
active_skills_hitbox_img = pygame.transform.scale(active_skills_hitbox_img,(44,44))

#characters
#----------------------------------------------------------------------------------hero
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_amount, stamina_recovery, stamina_threshold, turn_amount, turn_threshold, temp_strength, temp_intelligence, temp_agility, temp_luck, temp_endurance, position_bonus, buff_reset_time, buff_duration, attack cooldown, fireball_charge, lightning_charge):

##hero

Character.Random_Stats_Hero(random_stat_list)
hero = Character.Hero(200, 265, 'Hero', 50, 50, 1, 1, 2, 2, 1, 0, 2000, 0, 0, 25, 0, random_stat_list[0], random_stat_list[1], random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 0, 0, 0, 0, 0, 10, 10000, 0, 10000, 0, 0, 0, 0, 0, 5, 500, 0, 90, 1, 1)
random_stat_list.clear()

#----------------------------------------------------------------------------------monster
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

##slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(530, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime1 = Character.Slime(650, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)

##zombie

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie0 = Character.Zombie(530, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie1 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)

##zombie boss

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie_boss0 = Character.Zombie_Boss(530, 265, 'ZombieBoss', 700, 10, 3, 3, 1, 1, 1000, 1000, 1, 0, 12 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(35,40), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

zombie_boss_list = []
zombie_boss_list.append(zombie_boss0)

##zombie and slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime2 = Character.Slime(530, 350, 'Slime', 8, 10, 1, 1, 1, 1, 5, 5, 1, 0, 20 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie2 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 1, 1, 1, 15, 15, 1, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

zombie_and_slime_list = []
zombie_and_slime_list.append(slime2)
zombie_and_slime_list.append(zombie2)

##golem boss

Character.Random_Stats_Monsters(random_stat_list_monsters)
golem_boss0 = Character.Golem_Boss(530, 225, 'GolemBoss', 1900, 10, 3, 3, 1, 1, 2000, 2000, 7, 0, 8 + random.randint(-1,1), random_stat_list_monsters[0] + random.randint(60,80), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(1,2), random_stat_list_monsters[3] + random.randint(1,2), random_stat_list_monsters[4] + random.randint(1,2), 0, 10000, 0, 0, 0, 0, 0, 90)
random_stat_list_monsters.clear()

golem_boss_list = []
golem_boss_list.append(golem_boss0)

###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)
monster_list.append(zombie_boss_list)
monster_list.append(zombie_and_slime_list)
monster_list.append(golem_boss_list)

#bars
##hero
hero_health_bar = Bars.Health_Bar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
hero_shield_bar = Bars.Shield_Bar(20, screen_height - bottom_panel + 40)
hero_mana_bar = Bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
hero_experience_bar = Bars.Experience_Bar(0, screen_height - 13)
##slime
slime0_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
slime1_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
slime0_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
slime1_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
slime_shield_list = []
slime_shield_list.append(slime0_shield_bar)
slime_shield_list.append(slime1_shield_bar)
##zombie
zombie0_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
zombie1_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
zombie0_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
zombie1_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
zombie_shield_list = []
zombie_shield_list.append(zombie0_shield_bar)
zombie_shield_list.append(zombie1_shield_bar)
##zombie boss
zombie_boss_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie_boss0.hp, zombie_boss0.max_hp)
zombie_boss_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
zombie_boss_health_list = []
zombie_boss_health_list.append(zombie_boss_health_bar)
zombie_boss_shield_list = []
zombie_boss_shield_list.append(zombie_boss_shield_bar)
##zombie and slime
zombie2_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, zombie2.hp, zombie2.max_hp)
slime2_health_bar = Bars.Health_Bar(screen_width  - 150, screen_height - bottom_panel + 100, slime2.hp, slime2.max_hp)
zombie2_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
slime2_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 100)
zombie_and_slime_health_list = []
zombie_and_slime_health_list.append(zombie2_health_bar)
zombie_and_slime_health_list.append(slime2_health_bar)
zombie_and_slime_shield_list = []
zombie_and_slime_shield_list.append(zombie2_shield_bar)
zombie_and_slime_shield_list.append(slime2_shield_bar)
##golem boss
golem_boss_health_bar = Bars.Health_Bar(screen_width - 150, screen_height - bottom_panel + 40, golem_boss0.hp, golem_boss0.max_hp)
golem_boss_shield_bar = Bars.Shield_Bar(screen_width - 150, screen_height - bottom_panel + 40)
golem_boss_health_list = []
golem_boss_health_list.append(golem_boss_health_bar)
golem_boss_shield_list = []
golem_boss_shield_list.append(golem_boss_shield_bar)

###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)
monster_health_list.append(zombie_and_slime_health_list)
monster_health_list.append(golem_boss_health_list)
monster_shield_list = []
monster_shield_list.append(slime_shield_list)
monster_shield_list.append(zombie_shield_list)
monster_shield_list.append(zombie_boss_shield_list)
monster_shield_list.append(zombie_and_slime_shield_list)
monster_shield_list.append(golem_boss_shield_list)

#button
restart_button = Bars.Button(screen, (screen_width / 2) - 125 , 160, reset_img, 250, 50)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = 0
		monster.action = 0		

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
#inventory = [2,3,4,5,25,6,7,8,9,10,11,12,13,14,29,15,16,17,1,18,19,20,35,21,31,22,23,24,26,27,28,30,32,33,34]
inventory = []
skills_list = ['normal_attack', 'fireball', 'lightning']

all_active_skills_list = ['normal_attack', 'cleave', 'zombie_stab', 'triple_combo', 'serpent_wheel', 'venomous_whip', 'thunder_bolt']
active_skills_list = ['normal_attack']

active_skills_indexes = {
	'normal_attack' : {'active_index' : 0},
	'cleave' : {'active_index' : 1},
	'triple_combo' : {'active_index' : 2},
	'zombie_stab' : {'active_index' : 3},
	'serpent_wheel' : {'active_index' : 4},
	'venomous_whip' : {'active_index' : 5},
	'thunder_bolt' : {'active_index' : 6}

}

skill_hitbox_active = 0

skill_active_hitbox_indexes = {
	'hitbox' : {0 : (44,0), 1 : (88,0), 2 : (132,0), 3 : (176,0), 4 : (220,0)},	

}

chosen_skill = 0

#events
event_1 = True
event_2 = True
event_3 = True

#bosses
boss_defeated_list = []

#skill turn counters
fireball_turn_counter = 0
lightning_turn_counter = 0
shield_turn_counter = 0
speed_counter = 0

start_combat_time = 0
level_up_time = 0

turn_counter = 0
boost = False

battle_over = False

jump_cooldown = 0
stand_still_cooldown = 0
on_ground = True

monster_attack_time = 0
counter_time = 0
counter_chance = True

fireball_consumable_active = True
lightning_consumable_active = False

boss_turn_amount = 0
monster_special_skill = False

player_y_momentum = 0
player_x_momentum = 0
move_right = False
move_left = False

#position
hero_front_position = False
hero_middle_position = True
hero_back_position = False

#sprites
skill_sprite_group = pygame.sprite.Group()
monster_skill_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)

#event 0
Level_Events.lvl_up_event_0(hero, monster_list, monster_index, skills_list)

run = True
while run:
	#how fast the game runs
	clock.tick(fps)
	hero.hitbox.x = hero.rect.x
	hero.hitbox.y = hero.rect.y
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
		#if battle is not over shown items
		Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, left_click, battle_over)
		#---------------------------#

		#---------------------------#		
		if battle_over == False and hero.alive == True:
			#turn system
			Speed_Stamina.turn_calculations(boost, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group)
			#current attack picture
			Load_Interface.draw_current_attack(action_index, inventory, skills_list, hero, active_skills_list, all_active_skills_list)
			#consumables
			Consumables.consumable_panel(hero, fireball_consumable_active, lightning_consumable_active)
			#show skills icon highlights
			screen.blit(active_skills_hitbox_img,skill_active_hitbox_indexes['hitbox'][skill_hitbox_active])

			#movement
			player_movement = [0,0]
			if move_right and hero.rect.x < screen_width - hero.rect.width:
				player_movement[0] += 4
			if move_left and hero.rect.x > 0:
				player_movement[0] -= 4
			player_movement[1] += player_y_momentum
			player_y_momentum += 0.2
			if hero.rect.y < 0 :
				player_y_momentum += 0.2
			if player_y_momentum > 10:
				player_y_momentum = 10
			if hero.rect.y >= 151:
				player_movement[1] = 0 
				jump_counter = 0
				on_ground = True
			else:
				on_ground = False 
			if stand_still_cooldown > 0:
				player_movement[0] = 0
			hero.rect.x += player_movement[0]
			hero.rect.y += player_movement[1]

			#balance and checks	
			if hero.fireball_charge > 3:
				hero.fireball_charge = 3
			if hero.lightning_charge > 3:
				hero.lightning_charge = 3
			if hero.hp > hero.max_hp:
				hero.hp = hero.max_hp
			if hero.mp > hero.max_mp:
				hero.mp = hero.max_mp

			#cooldown
			if hero.attack_cooldown > 0:
				hero.attack_cooldown -= 1
			if jump_cooldown > 0:
				jump_cooldown -= 1
			if stand_still_cooldown > 0:
				stand_still_cooldown -= 1

			#auto items
			#auto stomp from war drum and stone drum
			if 24 in inventory and start_combat_time % 800 == 0 and start_combat_time != 0:
				hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
			#auto water blast from hydra heart
			if -11 in inventory and start_combat_time % 400 == 0 and start_combat_time != 0:
				hero.water_blast(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
			#auto regen blast from blue ruby
			if -12 in inventory and start_combat_time % 300 == 0 and start_combat_time != 0:
				if hero.max_hp - hero.hp > (hero.hp_regen + hero.mp_regen):
					heal_amount = (hero.hp_regen + hero.mp_regen)
				else:
					heal_amount = hero.max_hp - hero.hp
				hero.hp += heal_amount
				heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 30, f'{heal_amount:.2f}', green)
				damage_text_group.add(heal_text)

			#combat start time
			start_combat_time += 1
		else:
			start_combat_time = 0
		#---------------------------#
		#draw inventory button
		inventory_button = screen.blit(inventory_icon_img, (0,0))
		#---------------------------#
		try:
			target_limb, target, attack = collide()
		except:
			attack = False
			target = None
			target_limb = None			
		#---------------------------#
		#hero guard
		if'guard' in skills_list and start_combat_time % 500 == 0 and start_combat_time != 0 and hero.shield == 0 and battle_over != True:
			hero.guard(skill_sprite_group, damage_text_group, skills_list, experiencethreshold, inventory, monster_list, monster_index, turn_counter)

		#hero stomp
		if'stomp' in skills_list and start_combat_time % 500 == 0 and start_combat_time != 0 and battle_over != True and on_ground == True:
			hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)

		#counter
		if counter_chance == True and battle_over == False and hero.alive == True:
			pygame.draw.rect(screen, green, (hero.hitbox.x + 110, hero.hitbox.y - 10, 20, 20))
		if right_click == True and counter_chance == True and battle_over == False:
			counter_chance, counter_time = hero.counter(right_click, counter_chance, battle_over, counter_time, monster_attack_time, hero, monster_list, monster_index, experiencethreshold, damage_text_group, inventory, target, skills_list, skill_sprite_group)			

		#out of turn skills
		#thunder bolt
		if action_index == 6 and hero.mp >= 15 and attack == True and target != None and target.alive == True and hero.turn_amount != hero.turn_threshold:
			hero.thunder_bolt(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list)					
			attack = True 
			target = None
				#normal attack
		if action_index == 0 and attack == True and target != None and target.alive == True and hero.attack_cooldown == 0 and on_ground == True:
			hero.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group)	
			hero.attack_cooldown = 80
			stand_still_cooldown = 50
		#---------------------------#	
		#player action
		if game_over == 0 and hero.alive == True and hero.turn_amount >= hero.turn_threshold and on_ground == True and action_index != 0:

			#start item effects
			if 6 in inventory and shield_turn_counter % 3 == 0 and hero.shield == 0:
				hero.guard(skill_sprite_group, damage_text_group, skills_list, experiencethreshold, inventory, monster_list, monster_index, turn_counter)
				shield_turn_counter += 1

			if 9 in inventory and fireball_turn_counter == 0:
				target = monster_list[monster_index][0]
				hero.fireball(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)
				fireball_turn_counter += 1

			if -8 in inventory and lightning_turn_counter == 0:
				target = monster_list[monster_index][0]
				hero.lightning(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)
				lightning_turn_counter += 1

			#look for player action
			#attacks	
			if attack == True and target != None and target.alive == True:

				if 26 in inventory:
					for monster in monster_list[monster_index]:
						if monster.alive != False:
							monster.hp -= hero.intelligence * 0.2
							damage_text = Character.Damage_Text((monster.hitbox.x + monster.hitbox.width / 2) + random.randint(-60,60), monster.hitbox.y + 30 + random.randint(-30,30), f'HP -{hero.intelligence * 0.2:.2f}', yellow)	
							damage_text_group.add(damage_text)						
					
				#cleave
				elif action_index == 1 and hero.mp >= 7.5:
					hero.cleave(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
					hero.turn_amount = 0

				#triple combo
				elif action_index == 2 and hero.mp >= 10:
					hero.triple_combo(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, skills_list)
					hero.turn_amount = 0

				#zombie stab
				elif action_index == 3 and hero.mp >= 10:
					hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
					hero.turn_amount = 0

				#serpent wheel
				elif action_index == 4 and hero.mp >= 20:
					hero.serpent_wheel(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb, skills_list)
					hero.turn_amount = 0

				#venomous whip
				elif action_index == 5 and hero.mp >= 20:
					hero.venomous_whip(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, skills_list)
					hero.turn_amount = 0

				#normal attack
				else:
					hero.attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skills_list, turn_counter, skill_sprite_group)						
					hero.turn_amount = 0				

				#self buff return
				return_hero_buff(hero)

				turn_counter += 1
				shield_turn_counter += 1
				counter_chance = True
				if turn_counter % 3 == 0:
					monster_special_skill = True

		#enemy action
		#single enemy
		if len(monster_list[monster_index]) == 1 and hero.alive != False and hero.hp > 0:

			if monster_index == 2:
				if monster_special_skill == True:
					monster_list[monster_index][0].special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
					monster_special_skill = False
				
				if monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

					roll_guard_chance = random.randint(0,100)
					if monster_list[monster_index][0].alive != False:
						if boss_turn_amount % 3 == 0:
							monster_list[monster_index][0].scream(hero, damage_text_group, monster_skill_sprite_group, inventory)
						else:
							if roll_guard_chance > 80:
								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
							monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
							if 35 in inventory:
								hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

						monster_attack_time = pygame.time.get_ticks()

						boss_turn_amount += 1
						hero.shield = 0 
						monster_list[monster_index][0].monster_turn_amount = 0		

				if monster_list[monster_index][0].alive == False and len(boss_defeated_list) == 0:
					boss_defeated_list.append('zombie_boss')
					Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

			if monster_index == 4:
				if monster_special_skill == True:
					monster_list[monster_index][0].special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
					monster_special_skill = False

				if start_combat_time % 1000 == 0 and start_combat_time != 0:
					monster_list[monster_index][0].monster_turn_amount += monster_list[monster_index][0].monster_turn_threshold * 0.25
					boost_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 30, f'Boost', green)
					damage_text_group.add(boost_text)

				if monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

					roll_guard_chance = random.randint(0,100)
					if monster_list[monster_index][0].alive != False:
						if boss_turn_amount % 2 == 0:
							monster_list[monster_index][0].special_skill_2(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
						else:
							if roll_guard_chance > 80:
								monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
							monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
						if 35 in inventory:
							hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

						monster_attack_time = pygame.time.get_ticks()

						boss_turn_amount += 1
						hero.shield = 0 
						monster_list[monster_index][0].monster_turn_amount = 0	

				if monster_list[monster_index][0].alive == False and len(boss_defeated_list) == 1:
					boss_defeated_list.append('golem_boss')
					Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

		#two enemies
		if len(monster_list[monster_index]) == 2 and hero.alive != False and hero.hp > 0: 
				
			if monster_list[monster_index][0].alive == True and monster_list[monster_index][0].monster_turn_amount >= monster_list[monster_index][0].monster_turn_threshold:

				#monster skills
				if monster_list[monster_index][0] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 30:
					monster_list[monster_index][0].armor_corrosion(hero, damage_text_group, inventory)
				if monster_list[monster_index][0] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 20:
					if random.randint(0,100) > 30:
						monster_list[monster_index][0].toxic_bile(hero, damage_text_group, inventory)
					else:
						monster_list[monster_index][0].vomit(hero, monster_skill_sprite_group, damage_text_group, inventory, monster_list[monster_index][0])
				else:
					#monster guard
					roll_guard_chance = random.randint(0,100)
					if roll_guard_chance > 80:
						monster_list[monster_index][0].guard(skill_sprite_group, damage_text_group)
					monster_list[monster_index][0].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
					if 35 in inventory:
						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

				monster_attack_time = pygame.time.get_ticks()

				hero.shield = 0 						
				monster_list[monster_index][0].monster_turn_amount = 0	
		
			if monster_list[monster_index][1].alive == True and monster_list[monster_index][1].monster_turn_amount >= monster_list[monster_index][1].monster_turn_threshold:

				#monster skills	
				if monster_list[monster_index][1] == (slime0 or slime1 or slime2) and hero.shield > 0 and random.randint(0,100) > 10:
					monster_list[monster_index][1].armor_corrosion(hero, damage_text_group, inventory)
				if monster_list[monster_index][1] == (zombie0 or zombie1 or zombie2) and random.randint(0,100) > 20:
					if random.randint(0,100) > 30:
						monster_list[monster_index][1].toxic_bile(hero, damage_text_group, inventory)
					else:
						monster_list[monster_index][1].vomit(hero, monster_skill_sprite_group, damage_text_group, inventory)
				else:
					#monster guard
					roll_guard_chance = random.randint(0,100)
					if roll_guard_chance > 80:
						monster_list[monster_index][1].guard(skill_sprite_group, damage_text_group)
					monster_list[monster_index][1].attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index, skills_list)
					if 35 in inventory:
						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, skills_list)

				monster_attack_time = pygame.time.get_ticks()

				hero.shield = 0 
				monster_list[monster_index][1].monster_turn_amount = 0	

		#check if dead and drop exp, loot, gold
		for monster in monster_list[monster_index]:
			hero.monster_death_drops(monster, experiencethreshold, inventory, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list)

		#phoenix feather revive
		if 28 in inventory and hero.alive == False:
			hero.hp += hero.max_hp * 0.5
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

			if 'start_fireball' in skills_list:
				if hero.fireball_charge == 0:
					hero.fireball_charge = 1
			if 'start_lightning' in skills_list:
				if hero.lightning_charge == 0:
					hero.lightning_charge = 1

			hero.level_up_hero(inventory, experiencethreshold)

			return_hero_buff(hero)

			hero.shield = 0
			turn_counter = 0
			fireball_turn_counter = 0
			lightning_turn_counter = 0
			shield_turn_counter = 0
			hero.turn_amount = 0
			hero.stamina_amount = 0
			boss_turn_amount = 0
			monster_special_skill = False

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

					if hero_back_position == True:
						hero_middle_position, hero_back_position = hero.move_back_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)
					elif hero_front_position == True:
						hero_front_position, hero_middle_position = hero.move_front_to_middle(hero_front_position, hero_middle_position, hero_back_position, inventory, monster_list, monster_index, damage_text_group, experiencethreshold, skills_list, skill_sprite_group)

					#trigger level up event	
					if hero.level > 1 and event_1 == True:
						Level_Events.lvl_up_event_1(hero, monster, monster_list, monster_index, skills_list, active_skills_list, all_active_skills_list)
						event_1 = False			

					if hero.level > 3 and event_2 == True:
						if 'guard' in skills_list:
							Level_Events.lvl_up_event_2_guard(hero, monster, monster_list, monster_index, skills_list)
							event_2 = False
						elif 'stomp' in skills_list:
							Level_Events.lvl_up_event_2_stomp(hero, monster, monster_list, monster_index, skills_list)
							event_2 = False		
						else:
							Level_Events.lvl_up_event_2(hero, monster, monster_list, monster_index, skills_list)
							event_2 = False				

					if hero.level > 6 and event_3 == True:
						if 'cleave' in skills_list:
							Level_Events.lvl_up_event_3_cleave(hero, monster, monster_list, monster_index, skills_list)
							event_3 = False
						elif 'triple_combo' in skills_list:
							Level_Events.lvl_up_event_3_triple_combo(hero, monster, monster_list, monster_index, skills_list)
							event_3 = False		
															
					#platformer map menu
					monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)
					#trigger events if move to next map
					if monster_encounter == False:
						random_event_index = random.randint(0,5)
						Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)
					#reset spawns and monsters			
					start_spawn()
					for monster_group in range(len(monster_list)):
						for monster in monster_list[monster_group]:
							monster.level_up_monster(hero)
					if 14 in inventory:
						zombie_stab_active = True
					battle_over = False
					game_over = 0

		if game_over == -1:
			screen.blit(defeat_img, ((screen_width / 2) - 120, 100))
			battle_over = True
			if restart_button.draw():
				run = False
				sys.exit()

	elif monster_index == -1:
		monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list)
		if monster_encounter == False:
			random_event_index = random.randint(0,1)
			roll_event_chance = random.randint(0,100)
			if roll_event_chance > 0:
				Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)			
		start_spawn()
		game_over = 0

	left_click = False
	right_click = False	

	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN: #left
			if event.button == 1:
				left_click = True
				mousex, mousey = pygame.mouse.get_pos()
				if inventory_button.collidepoint((mousex,mousey)):
					Screen_Menus.options_menu(inventory, monster_list, monster_index, hero, skills_list, active_skills_list, all_active_skills_list)

			if event.button == 3:
				right_click = True	

			if event.button == 4 or event.button == 5:
				#consumables
				Consumables.consumable_1(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active, skills_list)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_e:
				boost = False

				#movement
			if event.key == pygame.K_d:
				move_right = False

			if event.key == pygame.K_a:
				move_left = False

		if event.type == pygame.KEYDOWN:
				
				#stamina
			if event.key == pygame.K_e and hero.turn_amount <= hero.turn_threshold:
				boost = True

				#movement
			if event.key == pygame.K_d:
				move_right = True
	
			if event.key == pygame.K_a:
				move_left = True

			if event.key == pygame.K_LSHIFT:
				if move_left == True:
					hero.rect.x -= 100
					hero.roll_back()	
				if move_right == True:
					hero.rect.x += 100
					hero.roll()

			if event.key == pygame.K_w and jump_counter < 2:
				hero.rect.y -= 100
				jump_cooldown = 65
				player_y_momentum -= 15
				jump_counter += 1
				hero.jump()

				#consumables
			if event.key == pygame.K_x:
				fireball_consumable_active, lightning_consumable_active = Consumables.consumable_menu(inventory, monster_list, monster_index)

				#skills
			if event.key == pygame.K_1:
				action_index = active_skills_indexes[active_skills_list[0]]['active_index']
				skill_hitbox_active = 0

			if event.key == pygame.K_2 and len(active_skills_list) > 1:
				action_index = active_skills_indexes[active_skills_list[1]]['active_index']
				skill_hitbox_active = 1

			if event.key == pygame.K_3 and len(active_skills_list) > 2:
				action_index = active_skills_indexes[active_skills_list[2]]['active_index']
				skill_hitbox_active = 2

			if event.key == pygame.K_4 and len(active_skills_list) > 3:
				action_index = active_skills_indexes[active_skills_list[3]]['active_index']
				skill_hitbox_active = 3

			if event.key == pygame.K_5 and len(active_skills_list) > 4:
				action_index = active_skills_indexes[active_skills_list[4]]['active_index']
				skill_hitbox_active = 4

	pygame.display.update()

pygame.quit()

#drop item in character

#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_recovery, stamina_threshold, fireball_charge, lightning_charge)
#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

