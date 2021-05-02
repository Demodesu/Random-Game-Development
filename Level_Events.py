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

level_event_1_image = pygame.image.load('Images/Background/Level_Events1.png').convert_alpha()

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

def lvl_up_event_1(hero, monster, monster_list, monster_index):
	guard_heal_active = False
	cleave_active = False
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		screen.blit(level_event_1_image, (0, 0))
		title_text = draw_text_middle('You have found inner strength. Choose your new power.', font, blue, screen_width, 75)
		choice_1_rect, choice_2_text = draw_text_middle_and_box('Gain Guardheal, DEF + 3', font, blue, dimgray, screen_width, 375)
		choice_2_rect, choice_3_text = draw_text_middle_and_box('Gain Cleave, STR + 3', font, blue, dimgray, screen_width, 450)
		choice_list = [choice_1_rect, choice_2_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					guard_heal_active = True
					hero.defense += 3
				if choice == choice_2_rect:
					cleave_active = True	
					hero.strength += 3	

				lvl_up_event = False

				return guard_heal_active, cleave_active

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				left_click = True
			if event.type == pygame.MOUSEBUTTONUP:
				left_click = False
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()





