import math, pygame, random, sys

pygame.init()
#game window#
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_icon_img = pygame.image.load('Images/Icon/SwordIcon.png').convert_alpha()
fire_ball_icon_img = pygame.image.load('Images/Icon/FireBallIcon.png').convert_alpha()
guard_icon_img = pygame.image.load('Images/Shield/ShieldButton.png').convert_alpha()
cleave_icon_img = pygame.image.load('Images/Icon/CleaveIcon.png').convert_alpha()
zombie_stab_img = pygame.image.load('Images/Icon/ZombieStabIcon.png').convert_alpha()

orange = (255,140,0)
red = (255,0,0)
brown = (48,24,0)
gold = (255,215,0)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_text_and_rect(text, font, text_col, rect_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	img = font.render(text, True, text_col)
	rect = pygame.rect.Rect(x, y, font_size[0], font_size[1])
	choice_rect = pygame.draw.rect(screen, rect_col, rect)
	choice_text = screen.blit(img, (x, y))

	return choice_rect, choice_text

#drawing panel
def draw_panel(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen):
	#draw panel rectangle
	screen.blit(panel_img,(0,screen_height - bottom_panel))
	#show knight stats
	draw_text(f'HP: {hero.hp}', font, red, 20, screen_height - bottom_panel + 20)
	draw_text(f'MP: {hero.mp}', font, red, 160, screen_height - bottom_panel + 20)	
	draw_text(f'EXP: {hero.experience}', font, red, 30, screen_height - bottom_panel + 70)
	draw_text(f'DEF: {hero.defense}', font, red, 30, screen_height - bottom_panel + 90)
	draw_text(f'SPD: {hero.speed}', font, red, 30, screen_height - bottom_panel + 110)
	draw_text(f'STAT: {hero.statpoints}', font, red, 180-60, screen_height - bottom_panel + 70)
	draw_text(f'GOLD: {hero.gold}', font, red, 270-60, screen_height - bottom_panel + 70)
	draw_text(f'LVL: {hero.level}', font, red, 240, screen_height - bottom_panel + 20)

	#show monster stats	
	for count, i in enumerate(monster_list[monster_index]):
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 20) + count * 60)	
		draw_text(f'LVL: {i.level}', font, red, 440, (screen_height - bottom_panel + 20) + count * 60)

def draw_background(background_img):
	screen.blit(background_img, (0,0))

def stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, click, battle_over):
	mousex, mousey = pygame.mouse.get_pos()
	str_stat_rect, str_stat_rect = draw_text_and_rect(f'STR: {hero.strength}', font, red, gold, 320, screen_height - bottom_panel + 20 - 3)
	int_stat_rect, int_stat_rect = draw_text_and_rect(f'INT: {hero.intelligence}', font, red, gold, 320, screen_height - bottom_panel + 40 - 3)	
	agi_stat_rect, agi_stat_rect = draw_text_and_rect(f'AGI: {hero.agility}', font, red, gold, 320, screen_height - bottom_panel + 60 - 3)	
	luc_stat_rect, luc_stat_rect = draw_text_and_rect(f'LUC: {hero.luck}', font, red, gold, 320, screen_height - bottom_panel + 80 - 3)	
	end_stat_rect, end_stat_rect = draw_text_and_rect(f'END: {hero.endurance}', font, red, gold, 320, screen_height - bottom_panel + 100 - 3)	

	if battle_over == True:
		if str_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0:				
			hero.str_up_button()
		if agi_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0:
			hero.agi_up_button()
		if int_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0:
			hero.int_up_button()
		if luc_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0:
			hero.luc_up_button()
		if end_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0:
			hero.end_up_button()


# def draw_stat_background(screen, screen_height, bottom_panel, blue):
# 	s = pygame.Surface((43,20))  # the size of your rect
# 	s.set_alpha(128)                # alpha level
# 	s.fill(blue)           # this fills the entire surface
# 	screen.blit(s, (180-35, screen_height - bottom_panel + 70 - 2))    # (0,0) are the top-left coordinates	

def draw_current_attack(action_index, cleave_active, zombie_stab_active, inventory):
	if action_index == 0:
		screen.blit(sword_icon_img, (0,0))
	elif cleave_active == True and action_index == 1:
		screen.blit(cleave_icon_img, (0,0))
	elif zombie_stab_active == True and action_index == 2:
		screen.blit(zombie_stab_img, (0,0))