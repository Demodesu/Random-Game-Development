import math, pygame, random, loadinterface, character, bars, sys

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 120

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
action_wait_time = 100
experiencethreshold = [5]
click = False
attack = False
target = None
monster_index = 1
game_over = 0
random_stat_list = []
random_stat_list_monsters = []
#controls player action
action_index = 0 #0 = attack; 1 = fireball
#fonts
font = pygame.font.SysFont('Minecraft', 26)
potion_font = pygame.font.SysFont('Minecraft', 20)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

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
character.Random_Stats(random_stat_list)
print(random_stat_list)
hero = character.Hero(200, 265, 'Hero', 50, 20, 1, 0, 0, random_stat_list[0], random_stat_list[1], 5, random_stat_list[2], random_stat_list[3], random_stat_list[4], 2, 2)
##slime
character.Random_Stats_Monsters(random_stat_list_monsters)
print(random_stat_list_monsters)
slime0 = character.Slime(530, 350, 'Slime', 10, 10, 1, 5, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 1)
slime1 = character.Slime(650, 350, 'Slime', 10, 10, 1, 5, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 1)
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)
##zombie
zombie0 = character.Zombie(530, 265, 'Zombie', 15, 10, 1, 5, random_stat_list_monsters[0] + 2, random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 1)
zombie1 = character.Zombie(650, 265, 'Zombie', 15, 10, 1, 5, random_stat_list_monsters[0] + 2, random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 1)
zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)
###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)

#bars
##hero
hero_health_bar = bars.Health_Bar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
hero_mana_bar = bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
hero_experience_bar = bars.Experience_Bar(0, screen_height - bottom_panel)
##slime
slime0_health_bar = bars.Health_Bar(550, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
slime1_health_bar = bars.Health_Bar(550, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
##zombie
zombie0_health_bar = bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
zombie1_health_bar = bars.Health_Bar(550, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)

#button
restart_button = bars.Button(screen, 345, 120, reset_img, 120, 30)

def random_spawn():
	global monster_index
	monster_appearance_chance = random.randint(0,100)
	if monster_appearance_chance > 50:
		#zombie
		monster_index = 1
	else:
		#slime
		monster_index = 0

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

fire_ball_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
run = True
while run:

	#how fast the game runs
	clock.tick(fps)
	#draw background
	loadinterface.draw_background(background_img)
	#---------------------------#
	#draw panel
	loadinterface.draw_panel(hero, monster_list, monster_index, red, font, screen_height, bottom_panel, screen)
	#---------------------------#
	#draw hero health bar
	hero_health_bar.draw(hero.hp, hero.max_hp)
	hero_mana_bar.draw(hero.mp, hero.max_mp)
	hero_experience_bar.draw(hero.experience, experiencethreshold)
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
	damage_text_group.update()
	damage_text_group.draw(screen)
	#---------------------------#
	loadinterface.draw_current_attack(action_index)
	#---------------------------#
	#default game variables
	attack = False
	target = None
	#---------------------------#
	#clicking on the target returns true value
	#make sure mouse is visible
	collide()
	#---------------------------#
	# if hero.statpoints > 0:
	# 	hero.Stat_Up_Button(70, 510, click)
	#---------------------------#
	if hero.statpoints > 0:	
		loadinterface.draw_stat_background(screen, screen_height, bottom_panel, blue)

	#player action
	if game_over == 0:
		if hero.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action

					#attack
					if attack == True and target != None and target.alive and action_index == 0:
						hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group)
						current_fighter += 1
						action_cooldown = 0

					#fireball
					if attack == True and target != None and target.alive and action_index == 1:
						if hero.mp < 5:
							hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group)
						else:
							hero.fire_ball_attack(current_fighter, action_cooldown, target, monster, monster_list, monster_index, experiencethreshold, fire_ball_sprite_group, damage_text_group)
						current_fighter += 1
						action_cooldown = 0

		#enemy action
		for count, monster in enumerate(monster_list[monster_index]):
			if current_fighter == 2 + count:
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
				random_spawn()
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
	if current_fighter > total_fighters:
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
			if event.key == pygame.K_KP1:
				if hero.statpoints > 0:
					hero.str_up_button()
			if event.key == pygame.K_KP2:
				if hero.statpoints > 0:
					hero.int_up_button()
			if event.key == pygame.K_KP3:
				if hero.statpoints > 0:				
					hero.luc_up_button()
			if event.key == pygame.K_KP4:
				if hero.statpoints > 0:
					hero.acc_up_button()
			if event.key == pygame.K_KP5:
				if hero.statpoints > 0:				
					hero.eva_up_button()
			if event.key == pygame.K_LALT:
				action_index += 1
				if action_index > 1:
					action_index = 0

	pygame.display.update()

pygame.quit()

#do stat