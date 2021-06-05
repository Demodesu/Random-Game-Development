import math, pygame, random, sys, ctypes

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 60

#-------------------------------------------------------------------------------------#
#all screen elements
#ratio is 16:9
def width(width_ratio):
	calculated = screen_width * width_ratio
	calculated = math.ceil(calculated)
	return calculated

def height(height_ratio):
	calculated = screen_width * height_ratio
	calculated = math.ceil(calculated)
	return calculated

def width_position(width_ratio):
	calculated = screen_width * width_ratio
	calculated = math.ceil(calculated)
	return calculated

def height_position(height_ratio):
	calculated = screen_height * height_ratio
	calculated = math.ceil(calculated)
	return calculated

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.35)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
dimgray = (112,128,144)

game_event_image_list = []
for events in range(6):
	img = pygame.image.load(f'Images/Background/Event{events}.png').convert_alpha()
	img = pygame.transform.scale(img,(screen_width,screen_height))
	game_event_image_list.append(img)

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
		screen.blit(game_event_image_list[0],(0,0))
		title_1_rect = draw_text_middle_and_box('You stumble upon a long path which will test your endurance.', font, blue, screen_width, height_position(0.1), banner_image)
		title_2_rect = draw_text_middle_and_box('You can gain constitution and strength, as training for you body.', font, blue, screen_width, height_position(0.2), banner_image)
		choice_1_rect = draw_text_middle_and_box('Continue', font, blue, screen_width, height_position(0.5), banner_image)
		choice_2_rect = draw_text_middle_and_box('Short cut', font, blue, screen_width, height_position(0.6), banner_image)
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
			draw_text_middle_and_box('Hero now tracks the path with ease, benefiting less from the hike.', font, blue, screen_width, height_position(0.3), banner_image)
			draw_text_middle_and_box('Hero gains Max HP (1-2) and only 1 STR.', font, blue, screen_width, height_position(0.4), banner_image)
			if click == True:
				event_1 = False			
		if sub_event_2 == True:
			draw_text_middle_and_box('Hero is too frail, losing health but gaining strength and constitution.', font, blue, screen_width, height_position(0.3), banner_image)	
			draw_text_middle_and_box('Hero loses health, but gains (2-3) Max HP and (2-3) STR.', font, blue, screen_width, height_position(0.4), banner_image)		
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
		screen.blit(game_event_image_list[1],(0,0))
		draw_text_middle_and_box('Monsters grow restless by the day.', font, blue, screen_width, height_position(0.1), banner_image)
		draw_text_middle_and_box('Monsters gain (2-5) Max HP and drop 5 more EXP', font, blue, screen_width, height_position(0.2), banner_image)

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
		screen.blit(game_event_image_list[2],(0,0))
		draw_text_middle_and_box('A healing wind sweeps by.', font, blue, screen_width, height_position(0.1), banner_image)
		draw_text_middle_and_box('Hero recovers 15% Max HP and Max MP', font, blue, screen_width, height_position(0.2), banner_image)

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
		screen.blit(game_event_image_list[3],(0,0))
		draw_text_middle_and_box('Hero finds a leather-bound book dropped in the middle of the road.', font, blue, screen_width, height_position(0.1), banner_image)
		draw_text_middle_and_box('The book is an old journal of a sorcerer.', font, blue, screen_width, height_position(0.2), banner_image)
		draw_text_middle_and_box('Hero reads the book and gains (2-3) INT.', font, blue, screen_width, height_position(0.3), banner_image)

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
		screen.blit(game_event_image_list[4],(0,0))
		draw_text_middle_and_box('Hero stumbled upon a small four leaf clover.', font, blue, screen_width, height_position(0.1), banner_image)
		draw_text_middle_and_box('Excited and feeling lucky, Hero pockets the clover and continues on the path.', font, blue, screen_width, height_position(0.2), banner_image)
		draw_text_middle_and_box('Hero gains 1 LUC.', font, blue, screen_width, height_position(0.3), banner_image)

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
		screen.blit(game_event_image_list[5],(0,0))
		draw_text_middle_and_box('Monsters feast on bodies of the fallen.', font, blue, screen_width, height_position(0.1), banner_image)
		draw_text_middle_and_box('They grow more powerful with each bite.', font, blue, screen_width, height_position(0.2), banner_image)
		draw_text_middle_and_box('Monsters gain (1-2) END and (1-2) STR.', font, blue, screen_width, height_position(0.3), banner_image)

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