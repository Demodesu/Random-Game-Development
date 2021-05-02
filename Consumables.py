import math, pygame, random, sys, Character

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
font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 10)
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 20)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

consumable_inventory_img = pygame.image.load('Images/Background/Shop_Inventory.png').convert_alpha()
fireball_icon_img = pygame.image.load('Images/Icon/FireBallIcon.png').convert_alpha()
lightning_icon_img = pygame.image.load('Images/Icon/LightningIcon.png').convert_alpha()

def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

def draw_text_middle_and_box_consumables(text, font, text_col, rect_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	rect = pygame.rect.Rect(x, y, font_size[0] + 10, font_size[1] + 10)
	choice_rect = pygame.draw.rect(screen, rect_col, rect)
	choice_text = screen.blit(img, (x + 5, y + 5))

	return choice_rect, choice_text

def consumable_1(hero, action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory, fireball_consumable_active, lightning_consumable_active):
	if fireball_consumable_active == True:
		hero.fireball(action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
	if lightning_consumable_active == True:
		hero.lightning(action_cooldown, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)

def consumable_panel(hero, fireball_consumable_active, lightning_consumable_active):
	if fireball_consumable_active == True:
		screen.blit(fireball_icon_img, (0,64))
		draw_text_middle_and_box_consumables(f'{hero.fireball_charge}', font, red, blue, 0, 64)
	if lightning_consumable_active == True:
		screen.blit(lightning_icon_img, (0,64))
		draw_text_middle_and_box_consumables(f'{hero.lightning_charge}', font, red, blue, 0, 64)

def consumable_menu(inventory, monster_list, monster_index):	
	left_click = False
	pygame.mouse.set_visible(True)
	fireball_consumable_active = False
	lightning_consumable_active = False

	inside_consumable_menu = True
	while inside_consumable_menu:
		clock.tick(fps)
		mousex, mousey = pygame.mouse.get_pos()

		screen.blit(consumable_inventory_img, (0,0))
		draw_text_middle(f'CONSUMABLES', font_heading, red, screen_width, 10)

		fireball_rect, fireball_text = draw_text_middle_and_box_consumables('FIREBALL', font, red, blue, screen_width, 50)
		lightning_rect, lightning_text = draw_text_middle_and_box_consumables('LIGHTNING', font, red, blue, screen_width, 80)
		no_consumables_rect, no_consumables_text = draw_text_middle_and_box_consumables('NONE', font, red, blue, screen_width, 110)
		rect_list = [fireball_rect, lightning_rect, no_consumables_rect]
		for choice in rect_list:
			if choice.collidepoint((mousex,mousey)) and left_click == True:
				if choice == fireball_rect:
					fireball_consumable_active = True
					lightning_consumable_active = False
					inside_consumable_menu = False

					return fireball_consumable_active, lightning_consumable_active	

				if choice == lightning_rect:
					fireball_consumable_active = False
					lightning_consumable_active = True
					inside_consumable_menu = False

					return fireball_consumable_active, lightning_consumable_active	

				if choice == no_consumables_rect:
					fireball_consumable_active = False
					lightning_consumable_active = False
					inside_consumable_menu = False

					return fireball_consumable_active, lightning_consumable_active	

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_consumable_menu = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_x:
					fireball_consumable_active = False
					lightning_consumable_active = False
					inside_consumable_menu = False

					return fireball_consumable_active, lightning_consumable_active	
			if event.type == pygame.MOUSEBUTTONDOWN:
				left_click = True				
			if event.type == pygame.MOUSEBUTTONUP:
				left_click = False

		pygame.display.update()