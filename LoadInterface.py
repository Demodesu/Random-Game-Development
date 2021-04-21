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

#drawing panel
def draw_panel(hero, monster_list, monster_index, stat_color, font, screen_height, bottom_panel, screen):
	#draw panel rectangle
	screen.blit(panel_img,(0,screen_height - bottom_panel))
	#show knight stats
	draw_text(f'HP: {hero.hp}', font, stat_color, 20, screen_height - bottom_panel + 20)
	draw_text(f'MP: {hero.mp}', font, stat_color, 160, screen_height - bottom_panel + 20)	
	draw_text(f'EXP: {hero.experience}', font, stat_color, 90-60, screen_height - bottom_panel + 70)
	draw_text(f'STAT: {hero.statpoints}', font, stat_color, 180-60, screen_height - bottom_panel + 70)
	draw_text(f'GOLD: {hero.gold}', font, stat_color, 270-60, screen_height - bottom_panel + 70)
	draw_text(f'LVL: {hero.level}', font, stat_color, 240, screen_height - bottom_panel + 20)	
	draw_text(f'STR: {hero.strength}', font, stat_color, 320, screen_height - bottom_panel + 20 - 3)
	draw_text(f'INT: {hero.intelligence}', font, stat_color, 320, screen_height - bottom_panel + 40 - 3)		
	draw_text(f'LUC: {hero.luck}', font, stat_color, 320, screen_height - bottom_panel + 60 - 3)	
	draw_text(f'ACC: {hero.accuracy}', font, stat_color, 320, screen_height - bottom_panel + 80 - 3)	
	draw_text(f'EVA: {hero.evasion}', font, stat_color, 320, screen_height - bottom_panel + 100 - 3)
	draw_text(f'DEF: {hero.defense}', font, stat_color, 320, screen_height - bottom_panel + 120 - 3)

	#show slime stats	
	for count, i in enumerate(monster_list[monster_index]):
		draw_text(f'{i.name} HP: {i.hp}', font, stat_color, 550, (screen_height - bottom_panel + 20) + count * 60)	
		draw_text(f'LVL: {i.level}', font, stat_color, 440, (screen_height - bottom_panel + 20) + count * 60)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_background(background_img):
	screen.blit(background_img, (0,0))

# def draw_stat_background(screen, screen_height, bottom_panel, blue):
# 	s = pygame.Surface((43,20))  # the size of your rect
# 	s.set_alpha(128)                # alpha level
# 	s.fill(blue)           # this fills the entire surface
# 	screen.blit(s, (180-35, screen_height - bottom_panel + 70 - 2))    # (0,0) are the top-left coordinates	

def draw_current_attack(action_index):
	if action_index == 0:
		screen.blit(sword_icon_img, (0,0))
	elif action_index == 1:
		screen.blit(fire_ball_icon_img, (0,0))
	elif action_index == 2:
		screen.blit(guard_icon_img, (0,0))
