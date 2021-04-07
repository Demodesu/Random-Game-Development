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

#fonts
font = pygame.font.SysFont('Minecraft', 26)
potion_font = pygame.font.SysFont('Minecraft', 20)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

#load assets#
background_img = pygame.image.load('Images/Background/Background.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_img = pygame.image.load('Images/Icon/SwordButton.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (50,50))
victory_img = pygame.image.load('Images/Icon/Victory.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Defeat.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Reset.png').convert_alpha()

#characters
##hero
hero = character.Hero(200, 265, 'Hero', 50, 20, 1, 0, 0, 50, 5, 5, 5, 5, 5, 2, 2)
##slime
slime0 = character.Slime(530, 350, 'Slime', 20, 10, 1, 5, 5, 2, 2, 2, 2, 2, 1)
slime1 = character.Slime(650, 350, 'Slime', 20, 10, 1, 5, 5, 2, 2, 2, 2, 2, 1)
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)
##zombie
zombie0 = character.Zombie(530, 265, 'Zombie', 30, 10, 1, 5, 5, 3, 3, 3, 3, 3, 2)
zombie1 = character.Zombie(650, 265, 'Zombie', 30, 10, 1, 5, 5, 3, 3, 3, 3, 3, 2)
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

#restart button
restart_button = bars.Button(screen, 330, 120, reset_img, 120, 30)

def Random_Spawn():
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

def Monster_Collide():
	global click
	global target
	global attack
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for count, monster in enumerate(monster_list[monster_index]):
		if monster.hitbox.collidepoint((mousex,mousey)):
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, (mousex - 10, mousey - 10))
			if click == True:
				attack = True
				target = monster_list[monster_index][count]

#game#
run = True
while run:

	#how fast the game runs
	clock.tick(fps)
	#draw background
	loadinterface.Draw_Background(background_img)

	#draw panel
	loadinterface.Draw_Panel(hero, monster_list, monster_index, red, font, screen_height, bottom_panel, screen)
	#---------------------------#
	#draw hero health bar
	hero_health_bar.Draw(hero.hp, hero.max_hp)
	hero_mana_bar.Draw(hero.mp)
	#---------------------------#
	#draw hero
	hero.Update()
	hero.Draw()
	#---------------------------#
	for count, monster_health_bar in enumerate(monster_health_list[monster_index]):
		monster_health_bar.Draw(monster_list[monster_index][count].hp, monster_list[monster_index][count].max_hp)

	for monster in monster_list[monster_index]:
		monster.Update()
		monster.Draw()
	#---------------------------#
	#default game variables
	attack = False
	target = None
	#---------------------------#
	#clicking on the target returns true value
	#make sure mouse is visible
	Monster_Collide()
	#---------------------------#

	#player action
	if game_over == 0:
		if hero.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:

					if attack == True and target != None and target.alive:
						hero.Attack(target)
						print(hero.experience)
						if target.alive == False:
							hero.experience += target.experience
							hero.Level_Up_Hero(experiencethreshold)
						current_fighter += 1
						action_cooldown = 0
					#look for player action

		#enemy action
		for count, monster in enumerate(monster_list[monster_index]):
			if current_fighter == 2 + count:
				if monster.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
							monster.Attack(hero)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter +=1

	elif hero.alive == False:
		game_over = -1

	alive_monster = 0
	for monster in monster_list[monster_index]:
		if monster.alive == True:
			alive_monster += 1
	if alive_monster == 0:
		game_over = 1

	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
			if restart_button.Draw():
				Random_Spawn()
				for i in range(len(monster_list)):
					for monster in monster_list[i]:
						monster.Level_Up_Monster()
				current_fighter = 1
				action_cooldown = 0
				game_over = 0
		if game_over == -1:
			screen.blit(defeat_img, (250, 50))
			if restart_button.Draw():
				Random_Spawn()
				current_fighter = 1
				action_cooldown = 0
				game_over = 0

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

	pygame.display.update()

pygame.quit()

#menus
#bosses
#equipment
#monsters