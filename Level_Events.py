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
text_x = screen_width / 2
text_y = (screen_height / 2) - 200

level_event_1_image = pygame.image.load('Images/Background/Level_Events.png').convert_alpha()
banner_image = pygame.image.load('Images/Icon/Banners.png').convert_alpha()

def draw_text_middle_and_box(text, font, text_col, rect_col, x, y, image):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	text_image = font.render(text, True, text_col)
	image = pygame.transform.scale(image, (font_size[0] + 20, font_size[1] + 20))
	
	choice_image = screen.blit(image, (x, y))
	choice_text = screen.blit(text_image, (x + 10, y + 10))
	
	return choice_image, choice_text

def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x + 10, y + 10))

	return choice_text

def lvl_up_event_1_guard(hero, monster, monster_list, monster_index, skills_list):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		screen.blit(level_event_1_image, (0, 0))
		title_text = draw_text_middle('You have found inner strength. Choose your new power.', font, blue, screen_width, 75)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Guard Heal, DEF + 2', font, blue, dimgray, screen_width, 300, banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Cleave, STR + 2', font, blue, dimgray, screen_width, 375, banner_image)
		choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain Triple Combo, STR + 2', font, blue, dimgray, screen_width, 450, banner_image)
		choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					skills_list.append('guard_heal')
					hero.defense += 2
				if choice == choice_2_rect:
					skills_list.append('cleave')
					hero.strength += 2	
				if choice == choice_3_rect:
					skills_list.append('triple_combo')
					hero.strength += 2	

				lvl_up_event = False

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				left_click = True
			if event.type == pygame.MOUSEBUTTONUP:
				left_click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def lvl_up_event_1_stomp(hero, monster, monster_list, monster_index, skills_list):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		screen.blit(level_event_1_image, (0, 0))
		title_text = draw_text_middle('You have found inner strength. Choose your new power.', font, blue, screen_width, 75)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Stomp Buff, AGI + 2', font, blue, dimgray, screen_width, 300, banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Cleave, STR + 2', font, blue, dimgray, screen_width, 375, banner_image)
		choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain Triple Combo, STR + 2', font, blue, dimgray, screen_width, 450, banner_image)
		choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					skills_list.append('stomp_buff')
					hero.agility += 2
				if choice == choice_2_rect:
					skills_list.append('cleave')	
					hero.strength += 2	
				if choice == choice_3_rect:
					skills_list.append('triple_combo')
					hero.strength += 2	
					
				lvl_up_event = False

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				left_click = True
			if event.type == pygame.MOUSEBUTTONUP:
				left_click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def lvl_up_event_0(hero, monster_list, monster_index, skills_list):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		screen.blit(level_event_1_image, (0, 0))
		title_text = draw_text_middle('To defend or fight, you decide.', font, blue, screen_width, 75)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Guard, DEF + 2', font, blue, dimgray, screen_width, 375, banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Stomp, AGI + 2', font, blue, dimgray, screen_width, 450, banner_image)
		choice_list = [choice_1_rect, choice_2_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					skills_list.append('guard')
					hero.defense += 2
				if choice == choice_2_rect:
					skills_list.append('stomp')	
					hero.agility += 2	

				lvl_up_event = False

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				left_click = True
			if event.type == pygame.MOUSEBUTTONUP:
				left_click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()



