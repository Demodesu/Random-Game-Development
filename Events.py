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

event_1_image = pygame.image.load('Images/Background/Events1.png').convert_alpha()
event_2_image = pygame.image.load('Images/Background/Events2.png').convert_alpha()

def draw_text_middle_and_box(text, font, text_col, rect_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	rect = pygame.rect.Rect(x, y, font_size[0] + 20, font_size[1] + 20)
	choice_rect = pygame.draw.rect(screen, rect_col, rect)
	choice_text = screen.blit(img, (x + 10, y + 10))

	return choice_rect, choice_text

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
		title_1_text = draw_text_middle('You stumble upon a long path which will test your endurance.', font, blue, screen_width, 75)
		title_2_text = draw_text_middle('You can gain constitution and strength, as training for you body.', font, blue, screen_width, 75 + 30)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Continue', font, blue, dimgray, screen_width, 300)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Short cut', font, blue, dimgray, screen_width, 375)
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
			draw_text_middle('Hero now tracks the path with ease, benefiting less from the hike.', font, blue, screen_width, 75 + 60)
			draw_text_middle('Hero gains Max HP (1-2) and only 1 STR.', font, blue, screen_width, 75 + 90)
			if click == True:
				event_1 = False			
		if sub_event_2 == True:
			draw_text_middle('Hero is too frail, losing health but gaining strength and constitution.', font, blue, screen_width, 75 + 60)	
			draw_text_middle('Hero loses health but gains (2-3) Max HP and (2-3) STR.', font, blue, screen_width, 75 + 90)		
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
		draw_text_middle('Monsters grow restless by the day.', font, blue, screen_width, 75)
		draw_text_middle('Monsters gain (2-5) Max HP and drop 5 more EXP', font, blue, screen_width, 75 + 30)

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

game_event_list = []
game_event_list.append(game_event_1)
game_event_list.append(game_event_2)



