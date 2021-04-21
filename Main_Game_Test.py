import math, pygame, random, sys, csv, LoadInterface, Character, Bars, Screen_Menus,  Map

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
current_fighter = 1
action_cooldown = 0
action_wait_time = 100
experiencethreshold = [5]
click = False
attack = False
target = None
monster_index = 0
game_over = 0
random_stat_list = []
random_stat_list_monsters = []
gold = 0
#controls player action
action_index = 0 #0 = attack; 1 = fireball
#turns counter
stage_counter = 0
#fonts
font = pygame.font.SysFont('Minecraft', 26)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
#load assets#
background_img = pygame.image.load('Images/Background/Background0.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_img = pygame.image.load('Images/Icon/SwordButton.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (50,50))
victory_img = pygame.image.load('Images/Icon/Victory.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Defeat.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Reset.png').convert_alpha()

#characters
##hero
Character.Random_Stats_Hero(random_stat_list)
hero = Character.Hero(200, 265, 'Hero', 50, 20, 1, 0, 0, random_stat_list[0], random_stat_list[1], 5, random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 2, 2, 1000)
##slime
Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(530, 350, 'Slime', 10, 10, 1, 5, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 20)
slime1 = Character.Slime(650, 350, 'Slime', 10, 10, 1, 5, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 20)
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)
##zombie
zombie0 = Character.Zombie(530, 265, 'Zombie', 15, 10, 1, 5, random_stat_list_monsters[0] + 2, random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 30)
zombie1 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 5, random_stat_list_monsters[0] + 2, random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 30)
zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)
##zombie boss
zombie_boss0 = Character.Zombie_Boss(530, 265, 'Zombie Boss', 50, 10, 1, 5, random_stat_list_monsters[0] + 15, random_stat_list_monsters[1] + 10, 2, random_stat_list_monsters[2] + 10, random_stat_list_monsters[3] + 10, random_stat_list_monsters[4] + 10, 0, 1, 50)
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
hero_mana_bar = Bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
hero_experience_bar = Bars.Experience_Bar(0, screen_height - bottom_panel)
hero_shield_bar = Bars.Shield_Bar(20, screen_height - bottom_panel + 40)
##slime
slime0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
slime1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
##zombie
zombie0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
zombie1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
##zombie boss
zombie_boss_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie_boss0.hp, zombie_boss0.max_hp)
zombie_boss_health_list = []
zombie_boss_health_list.append(zombie_boss_health_bar)
###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)

#button
restart_button = Bars.Button(screen, 345, 120, reset_img, 120, 30)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = monster.start_frame_index
		monster.action = monster.start_action		
	current_fighter = 1
	action_cooldown = 0

def collide():
	global click
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
			screen.blit(font.render('EVA:' + str(monster.evasion), True, blue), (mousex - 100, mousey + 40))
			screen.blit(font.render('ACC:' + str(monster.accuracy), True, blue), (mousex - 100, mousey + 60))
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, (mousex - 10, mousey - 10))
			if click == True:
				attack = True
				target = monster_list[monster_index][count]

#events
event_index = 0

def game_event_1():
	event_1 = True
	while event_1:
		screen.fill((105,105,105))
		screen.blit(font.render('You stumble upon a long path which will test your endurance.', True, (0,0,128)), (0, 0))
		screen.blit(font.render('You can gain constitution and strength, as training for you body.', True, (0,0,128)), (0, 30))
		if hero.strength > 25:
			screen.blit(font.render('Hero now tracks the path with ease, benefiting less from the hike.', True, (0,0,128)), (0, 60))
			screen.blit(font.render('Hero gains max health (2-3) but only 1 strength.', True, (0,0,128)), (0, 90))
		else:
			screen.blit(font.render('Hero has not adjusted to the harsh track, losing health but gaining strength and constitution.', True, (0,0,128)), (0, 60))			
			screen.blit(font.render('Hero loses (3-6) health but gains (2-3) max health and (2-3) strength.', True, (0,0,128)), (0, 90))					
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if hero.strength > 25:
					hero.max_hp += random.randint(2,3)
					hero.strength += 1
					event_1 = False
				else:
					hero.hp -= random.randint(3,6)
					if hero.hp < 0:
						hero.hp = 0
						hero.alive = False
						hero.death()
					hero.max_hp += random.randint(2,3)
					hero.strength += random.randint(2,3)
					event_1 = False					

		pygame.display.update()

def game_event_2():
	event_2 = True					 
	while event_2:
		screen.fill((105,105,105))
		screen.blit(font.render('Monsters on this path are stronger.', True, (0,0,128)), (0, 0))
		screen.blit(font.render('But they also have the potential to make you stronger too.', True, (0,0,128)), (0, 30))
		screen.blit(font.render('Recently fought monsters gain (5-10) max health and drop 5 more experience', True, (0,0,128)), (0, 60))
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				for monster in monster_list[monster_index]:
					monster.max_hp += random.randint(5,10)
					monster.experience += 5
				event_2 = False	

		pygame.display.update()

game_event_list = []
game_event_list.append(game_event_1)
game_event_list.append(game_event_2)

#drop item test
inventory = []

fire_ball_sprite_group = pygame.sprite.Group()
guard_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
run = True
while run:

	#how fast the game runs
	clock.tick(fps)
	#draw background
	LoadInterface.draw_background(background_img)
	#---------------------------#
	#draw panel
	LoadInterface.draw_panel(hero, monster_list, monster_index, red, font, screen_height, bottom_panel, screen)
	#---------------------------#
	#draw hero health bar
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
	for monster in monster_list[monster_index]:
		monster.update()
		monster.draw()
	#---------------------------#
	fire_ball_sprite_group.update()
	fire_ball_sprite_group.draw(screen)
	guard_sprite_group.update()
	guard_sprite_group.draw(screen)
	damage_text_group.update()
	damage_text_group.draw(screen)
	#---------------------------#
	LoadInterface.draw_current_attack(action_index)
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
	#player action
	if game_over == 0:
		if hero.alive == True:
			if current_fighter == 1 or current_fighter == 2:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action

					#attack
					if attack == True and target != None and target.alive and action_index == 0:
						hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group, inventory)
						Screen_Menus.drop_items(monster, hero, inventory)
						if target.alive == False:
							hero.gold += target.gold
						current_fighter += 1
						action_cooldown = 0

					#fireball
					if attack == True and target != None and target.alive and action_index == 1:
						if hero.mp < 5:
							hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group, inventory)
							Screen_Menus.drop_items(monster, hero, inventory)
							if target.alive == False:
								hero.gold += target.gold
						else:
							hero.fire_ball_attack(current_fighter, action_cooldown, target, monster, monster_list, monster_index, experiencethreshold, fire_ball_sprite_group, damage_text_group, inventory)
							Screen_Menus.drop_items(monster, hero, inventory)
							if target.alive == False:
								hero.gold += target.gold
						current_fighter += 1
						action_cooldown = 0

					#guard
					if click == True and action_index == 2:
						hero.guard(guard_sprite_group, damage_text_group)
						current_fighter += 1
						action_cooldown = 0

		#enemy action
		for count, monster in enumerate(monster_list[monster_index]):
			if current_fighter == 3 + count:
				if monster.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
							monster.attack(hero, damage_text_group)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter +=1

		else:
			if hero.alive == False:
				game_over = -1

	#check alive monsters to change game over condition
	alive_monster = 0
	for monster in monster_list[monster_index]:
		if monster.alive == True:
			alive_monster += 1
	if alive_monster == 0:
		game_over = 1

	#if it's a game over -> defeat or victory
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, ((screen_width / 2) - 120, 50))
			if restart_button.draw():
				hero.shield = 0
				if 6 in inventory:
					hero.guard(guard_sprite_group, damage_text_group)
				random_event_index = random.randint(0,2)
				stage_counter += 1
				monster_index = Map.platformer_menu(monster_index, hero)
				print(monster_index)

				if random_event_index == 0:
					pass
				else:
					game_event_list[random_event_index]()			
				start_spawn()
				for i in range(len(monster_list)):
					for monster in monster_list[i]:
						monster.level_up_monster()
				if hero.mp < hero.max_mp:
					hero.mp += 2.5
				current_fighter = 1
				action_cooldown = 0
				game_over = 0

		if game_over == -1:
			screen.blit(defeat_img, ((screen_width / 2) - 120, 50))
			if restart_button.draw():
				run = False
				sys.exit()

	#resets current fighter
	if current_fighter > total_turns:
		current_fighter = 1			

	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			click = True
		else:
			click = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				if hero.statpoints > 0:
					hero.str_up_button()
			if event.key == pygame.K_2:
				if hero.statpoints > 0:
					hero.int_up_button()
			if event.key == pygame.K_3:
				if hero.statpoints > 0:				
					hero.luc_up_button()
			if event.key == pygame.K_4:
				if hero.statpoints > 0:
					hero.acc_up_button()
			if event.key == pygame.K_5:
				if hero.statpoints > 0:				
					hero.eva_up_button()
			if event.key == pygame.K_LALT:
				action_index += 1
				if action_index > 2:
					action_index = 0
			if event.key == pygame.K_r:
				Screen_Menus.options_menu(inventory)
			if event.key == pygame.K_f:
				Screen_Menus.shop_menu(inventory, hero)
				
	pygame.display.update()

pygame.quit()

#do stat