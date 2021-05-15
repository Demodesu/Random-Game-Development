import math, pygame, random, sys

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 120

#game window#
bottom_panel = 150
screen_width, screen_height = 800, 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

#fonts
font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 13)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
dimgray = (112,128,144)

event_1_image = pygame.image.load('Images/Background/Event0.png').convert_alpha()
event_2_image = pygame.image.load('Images/Background/Event1.png').convert_alpha()
event_3_image = pygame.image.load('Images/Background/Event2.png').convert_alpha()
event_4_image = pygame.image.load('Images/Background/Event3.png').convert_alpha()
event_5_image = pygame.image.load('Images/Background/Event4.png').convert_alpha()
event_6_image = pygame.image.load('Images/Background/Event5.png').convert_alpha()

banner_image = pygame.image.load('Images/Icon/Banners.png').convert_alpha()

def draw_text_middle_and_box(text, font, text_col, x, y, image):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	text_image = font.render(text, True, text_col)
	image = pygame.transform.scale(image, (font_size[0] + 20, font_size[1] + 20))
	
	choice_image = screen.blit(image, (x, y))
	choice_text = screen.blit(text_image, (x + 10, y + 10))

	return choice_image

def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x + 10, y + 10))

	return choice_text

def game_event_1(hero, monster, monster_list, monster_index):
	sub_event_1 = False
	sub_event_2 = False
	click = False
	event_1 = True
	while event_1:
		mousex, mousey = pygame.mouse.get_pos()
		screen.blit(event_1_image,(0,0))
		title_1_rect = draw_text_middle_and_box('You stumble upon a long path which will test your endurance.', font, blue, screen_width, 60, banner_image)
		title_2_rect = draw_text_middle_and_box('You can gain constitution and strength, as training for you body.', font, blue, screen_width, 120, banner_image)
		choice_1_rect = draw_text_middle_and_box('Continue', font, blue, screen_width, 320, banner_image)
		choice_2_rect = draw_text_middle_and_box('Short cut', font, blue, screen_width, 400, banner_image)
		choice_list = [choice_1_rect, choice_2_rect]
		if sub_event_1 == False and sub_event_2 == False:
			for choice in choice_list:
				if choice.collidepoint((mousex,mousey)) and click == True:
					if choice == choice_1_rect:
						if hero.strength > 35:
							hero.max_hp += random.randint(1,2)
							hero.strength += 1
							click = False
							sub_event_1 = True

						else:
							reduce_amount = math.floor(hero.hp / 3)
							hero.hp -= reduce_amount
							if hero.hp < 0:
								hero.hp = 0
								hero.alive = False
								hero.death()
							hero.max_hp += random.randint(2,3)
							hero.strength += random.randint(2,3)
							click = False
							sub_event_2 = True
					if choice == choice_2_rect:
						event_1 = False

		if sub_event_1 == True:
			draw_text_middle_and_box('Hero now tracks the path with ease, benefiting less from the hike.', font, blue, screen_width, 180, banner_image)
			draw_text_middle_and_box('Hero gains Max HP (1-2) and only 1 STR.', font, blue, screen_width, 240, banner_image)
			if click == True:
				event_1 = False			
		if sub_event_2 == True:
			draw_text_middle_and_box('Hero is too frail, losing health but gaining strength and constitution.', font, blue, screen_width, 180, banner_image)	
			draw_text_middle_and_box('Hero loses health, but gains (2-3) Max HP and (2-3) STR.', font, blue, screen_width, 240, banner_image)		
			if click == True:
				event_1 = False			

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_event_2(hero, monster, monster_list, monster_index):
	click = False
	event_2 = True	
	while event_2:
		screen.blit(event_2_image,(0,0))
		draw_text_middle_and_box('Monsters grow restless by the day.', font, blue, screen_width, 60, banner_image)
		draw_text_middle_and_box('Monsters gain (2-5) Max HP and drop 5 more EXP', font, blue, screen_width, 120, banner_image)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
				for monster_group in monster_list:
					for monster in monster_group:
						monster.max_hp += random.randint(2,5)
						monster.experience += 5
				event_2 = False	
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_event_3(hero, monster, monster_list, monster_index):
	click = False
	event_3 = True	
	while event_3:
		screen.blit(event_3_image,(0,0))
		draw_text_middle_and_box('A healing wind sweeps by.', font, blue, screen_width, 60, banner_image)
		draw_text_middle_and_box('Hero recovers 15% Max HP and Max MP', font, blue, screen_width, 120, banner_image)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True

				if hero.max_hp - hero.hp > hero.max_hp * 0.15:
					hero.hp += hero.max_hp * 0.15
				else:
					hero.hp += hero.max_hp - hero.hp

				if hero.max_mp - hero.mp > hero.max_mp * 0.15:
					hero.mp += hero.max_mp * 0.15
				else:
					hero.mp += hero.max_mp - hero.mp

				event_3 = False
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_event_4(hero, monster, monster_list, monster_index):
	click = False
	event_4 = True	
	while event_4:
		screen.blit(event_4_image,(0,0))
		draw_text_middle_and_box('Hero finds a leather-bound book dropped in the middle of the road.', font, blue, screen_width, 60, banner_image)
		draw_text_middle_and_box('The book is an old journal of a sorcerer.', font, blue, screen_width, 120, banner_image)
		draw_text_middle_and_box('Hero reads the book and gains (2-3) INT.', font, blue, screen_width, 180, banner_image)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
				hero.intelligence += random.randint(2,3)
				event_4 = False
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_event_5(hero, monster, monster_list, monster_index):
	click = False
	event_5 = True	
	while event_5:
		screen.blit(event_5_image,(0,0))
		draw_text_middle_and_box('Hero stumbled upon a small four leaf clover.', font, blue, screen_width, 60, banner_image)
		draw_text_middle_and_box('Excited and feeling lucky, Hero pockets the clover and continues on the path.', font, blue, screen_width, 120, banner_image)
		draw_text_middle_and_box('Hero gains 1 LUC.', font, blue, screen_width, 180, banner_image)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
				hero.luck += 1
				event_5 = False
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_event_6(hero, monster, monster_list, monster_index):
	click = False
	event_6 = True	
	while event_6:
		screen.blit(event_6_image,(0,0))
		draw_text_middle_and_box('Monsters feast on bodies of the fallen.', font, blue, screen_width, 60, banner_image)
		draw_text_middle_and_box('They grow more powerful with each bite.', font, blue, screen_width, 120, banner_image)
		draw_text_middle_and_box('Monsters gain (1-2) END and (1-2) STR.', font, blue, screen_width, 180, banner_image)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
				for monster_group in monster_list:
					for monster in monster_group:
						monster.strength += random.randint(1,2)
						monster.endurance += random.randint(1,2)
				event_6 = False
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

game_event_list = []
game_event_list.append(game_event_1)
game_event_list.append(game_event_2)
game_event_list.append(game_event_3)
game_event_list.append(game_event_4)
game_event_list.append(game_event_5)
game_event_list.append(game_event_6)