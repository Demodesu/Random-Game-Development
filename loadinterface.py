import pygame

pygame.init()
#game window#
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))

#load assets#
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()

#drawing panel
def Draw_Panel(hero, slime_list, stat_color, font, screen_height, bottom_panel, screen):
	#draw panel rectangle
	screen.blit(panel_img,(0,screen_height - bottom_panel))
	#show knight stats
	Draw_Text(f'HP: {hero.hp}', font, stat_color, 20, screen_height - bottom_panel + 20)
	Draw_Text(f'MP: {hero.mp}', font, stat_color, 160, screen_height - bottom_panel + 20)	
	Draw_Text(f'EXP: {hero.experience}', font, stat_color, 90-35, screen_height - bottom_panel + 70)
	Draw_Text(f'STAT: {hero.statpoints}', font, stat_color, 180-35, screen_height - bottom_panel + 70)
	Draw_Text(f'LVL: {hero.level}', font, stat_color, 320, screen_height - bottom_panel + 20)	
	Draw_Text(f'STR: {hero.strength}', font, stat_color, 320, screen_height - bottom_panel + 40)	
	Draw_Text(f'LUC: {hero.luck}', font, stat_color, 320, screen_height - bottom_panel + 60)	
	Draw_Text(f'ACC: {hero.accuracy}', font, stat_color, 320, screen_height - bottom_panel + 80)	
	Draw_Text(f'EVA: {hero.evasion}', font, stat_color, 320, screen_height - bottom_panel + 100)
	Draw_Text(f'DEF: {hero.defense}', font, stat_color, 320, screen_height - bottom_panel + 120)
	#show slime stats	
	for count, i in enumerate(slime_list):
		Draw_Text(f'{i.name} HP: {i.hp}', font, stat_color, 550, (screen_height - bottom_panel + 20) + count * 60)	
		Draw_Text(f'LVL: {i.level}', font, stat_color, 440, (screen_height - bottom_panel + 20) + count * 60)

def Draw_Text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def Draw_Background(background_img):
	screen.blit(background_img, (0,0))
