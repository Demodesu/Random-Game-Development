import math, pygame, random, loadinterface, character, bars

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 60

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

#characters
##hero
hero = character.Hero(200, 265, 'Hero', 50, 20, 1, 0, 0, 10, 5, 5, 5, 5, 5, 2, 2)
##slime
slime0 = character.Slime(530, 350, 'Slime', 20, 10, 1, 5, 5, 2, 2, 2, 2, 2, 2)
slime1 = character.Slime(650, 350, 'Slime', 20, 10, 1, 5, 5, 2, 2, 2, 2, 2, 2)
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)

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

#game#
run = True
while run:

	#how fast the game runs
	clock.tick(fps)

	#draw background
	loadinterface.Draw_Background(background_img)

	#draw panel
	loadinterface.Draw_Panel(hero, slime_list, red, font, screen_height, bottom_panel, screen)

	#draw hero health bar
	hero_health_bar.Draw(hero.hp)
	hero_mana_bar.Draw()

	#draw slime health bar
	for count, slime_health_bar in enumerate(slime_health_list):
		slime_health_bar.Draw(slime_list[count].hp)

	#draw hero
	hero.Update()
	hero.Draw()

	#draw slime
	for slime in slime_list:
		slime.Update()
		slime.Draw()

	#default game variables
	attack = False
	target = None

	#clicking on the target returns true value
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for count, slime in enumerate(slime_list):
		if slime.rect.collidepoint((mousex,mousey)):
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, (mousex - 10, mousey - 10))
			if click == True:
				attack = True
				target = slime_list[count]

	#player action
	if hero.alive == True:
		if current_fighter == 1:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:

				if attack == True and target != None:
					hero.Attack(target)
					current_fighter += 1
					action_cooldown = 0
				#look for player action

	#enemy action
	for count, slime in enumerate(slime_list):
		if current_fighter == 2 + count:
			if slime.alive == True:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
						slime.Attack(hero)
						current_fighter += 1
						action_cooldown = 0
			else:
				current_fighter +=1

	if current_fighter > total_fighters:
		current_fighter = 1			
					
	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
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