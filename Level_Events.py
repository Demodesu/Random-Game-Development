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
text_x = screen_width / 2
text_y = (screen_height / 2) - 200

level_event_1_image = pygame.image.load('Images/Background/Level_Events.png').convert_alpha()
level_event_1_image = pygame.transform.scale(level_event_1_image,(screen_width,screen_height))
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

def lvl_up_event_0(hero, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Auto Guard Every 10 Seconds, DEF + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Auto Stomp Every 10 Seconds, AGI + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain 1 Fireball Every 10 Seconds, INT + 2', font, blue, dimgray, screen_width, height_position(0.7), banner_image)
		choice_4_rect, choice_4_text = draw_text_middle_and_box('Gain 1 Lightning Every 10 Seconds, INT + 2', font, blue, dimgray, screen_width, height_position(0.8), banner_image)
		choice_list = [choice_1_rect, choice_2_rect, choice_3_rect, choice_4_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('guard')
					hero.defense += 2
				if choice == choice_2_rect:
					hero.skills_list.append('stomp')	
					hero.agility += 2	
				if choice == choice_3_rect:
					hero.skills_list.append('start_fireball')	
					hero.intelligence += 2	
				if choice == choice_4_rect:
					hero.skills_list.append('start_lightning')	
					hero.intelligence += 2	

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

def lvl_up_event_1(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Cleave, STR + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Triple Combo, STR + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_list = [choice_1_rect, choice_2_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('cleave')
					hero.strength += 2	
				if choice == choice_2_rect:
					hero.skills_list.append('triple_combo')
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

def lvl_up_event_2_guard(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Guard Heal, DEF + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Guard Slash, STR + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain Guard Rush, Stamina Recovery + 1', font, blue, dimgray, screen_width, height_position(0.7), banner_image)
		choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('guard_heal')
					hero.defense += 2
				if choice == choice_2_rect:
					hero.skills_list.append('guard_slash')
					hero.strength += 2	
				if choice == choice_3_rect:
					hero.skills_list.append('guard_rush')
					hero.stamina_recovery += 1	

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

def lvl_up_event_2_stomp(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Stomp Buff, AGI + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Stomp Damage, STR + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain Stomp Rush, Stamina Recovery + 1', font, blue, dimgray, screen_width, height_position(0.7), banner_image)
		choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('stomp_buff')
					hero.agility += 2
				if choice == choice_2_rect:
					hero.skills_list.append('stomp_damage')	
					hero.strength += 2	
				if choice == choice_3_rect:
					hero.skills_list.append('stomp_rush')
					hero.stamina_recovery += 1	
					
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

def lvl_up_event_2(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		if 'start_fireball' in hero.skills_list:
			title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
			choice_1_rect, choice_1_text = draw_text_middle_and_box('Fireball 10% Not Consumed, LUC + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
			choice_2_rect, choice_2_text = draw_text_middle_and_box('Fireball Deals 25% AGI As Damage, AGI + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
			choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain 1 Lightning Every 10 Seconds, INT + 2', font, blue, dimgray, screen_width, height_position(0.7), banner_image)
			choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
			for choice in choice_list:
				if choice.collidepoint((mousex,mousey)) and left_click == True:				
					if choice == choice_1_rect:
						hero.skills_list.append('fireball_unconsumed')
						hero.luck += 2
					if choice == choice_2_rect:
						hero.skills_list.append('fireball_agi_damage')	
						hero.agility += 2	
					if choice == choice_3_rect:
						hero.skills_list.append('start_lightning')
						hero.intelligence += 2	
						
					lvl_up_event = False
		else:
			title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
			choice_1_rect, choice_1_text = draw_text_middle_and_box('Lightning 10% Not Consumed, LUC + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
			choice_2_rect, choice_2_text = draw_text_middle_and_box('Lightning Deals 25% AGI As Damage, AGI + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
			choice_3_rect, choice_3_text = draw_text_middle_and_box('Gain 1 Fireball Every 10 Seconds, INT + 2', font, blue, dimgray, screen_width, height_position(0.7), banner_image)
			choice_list = [choice_1_rect, choice_2_rect, choice_3_rect]
			for choice in choice_list:
				if choice.collidepoint((mousex,mousey)) and left_click == True:				
					if choice == choice_1_rect:
						hero.skills_list.append('lightning_unconsumed')
						hero.luck += 2
					if choice == choice_2_rect:
						hero.skills_list.append('lightning_agi_damage')	
						hero.agility += 2	
					if choice == choice_3_rect:
						hero.skills_list.append('start_fireball')
						hero.intelligence += 2	
						
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

def lvl_up_event_3_cleave(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Double Cleave, STR + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Cleave Bleed, AGI + 2', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_list = [choice_1_rect, choice_2_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('double_cleave')
					hero.strength += 2
				if choice == choice_2_rect:
					hero.skills_list.append('cleave_bleed')	
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

def lvl_up_event_3_triple_combo(hero, monster, monster_list, monster_index):
	left_click = False
	lvl_up_event = True
	while lvl_up_event:
		mousex, mousey = pygame.mouse.get_pos()
		title_rect, title_text = draw_text_middle_and_box('You have found inner strength. Choose your new power.', font, blue, dimgray, screen_width, height_position(0.1), banner_image)
		choice_1_rect, choice_1_text = draw_text_middle_and_box('Gain Triple Head, STR + 2', font, blue, dimgray, screen_width, height_position(0.5), banner_image)
		choice_2_rect, choice_2_text = draw_text_middle_and_box('Gain Triple Mana Restore, MP Regen + 1', font, blue, dimgray, screen_width, height_position(0.6), banner_image)
		choice_list = [choice_1_rect, choice_2_rect]
		for choice in choice_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:				
				if choice == choice_1_rect:
					hero.skills_list.append('triple_head')
					hero.strength += 2
				if choice == choice_2_rect:
					hero.skills_list.append('triple_mana_restore')	
					hero.mp_regen += 1	
					
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




