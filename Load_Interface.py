import math, pygame, random, sys

pygame.init()
#game window#
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/SwordIcon.png').convert_alpha()
sword_icon_img = pygame.transform.scale(sword_icon_img,(44,44))
cleave_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/CleaveIcon.png').convert_alpha()
cleave_icon_img = pygame.transform.scale(cleave_icon_img,(44,44))
zombie_stab_img = pygame.image.load('Images/Icon/SkillDisplayIcon/ZombieStabIcon.png').convert_alpha()
zombie_stab_img = pygame.transform.scale(zombie_stab_img,(44,44))
triple_combo_img = pygame.image.load('Images/Icon/SkillDisplayIcon/TripleComboIcon.png').convert_alpha()
triple_combo_img = pygame.transform.scale(triple_combo_img,(44,44))
serpent_wheel_img = pygame.image.load('Images/Icon/SkillDisplayIcon/SerpentWheelIcon.png').convert_alpha()
serpent_wheel_img = pygame.transform.scale(serpent_wheel_img,(44,44))
venomous_whip_img = pygame.image.load('Images/Icon/SkillDisplayIcon/VenomousWhipIcon.png').convert_alpha()
venomous_whip_img = pygame.transform.scale(venomous_whip_img,(44,44))
thunder_bolt_img = pygame.image.load('Images/Icon/SkillDisplayIcon/ThunderBoltIcon.png').convert_alpha()
thunder_bolt_img = pygame.transform.scale(thunder_bolt_img,(44,44))

orange = (255,140,0)
red = (255,0,0)
brown = (48,24,0)
gold = (255,215,0)
darker_orange = (254,110,0)
fire_brick = (178,34,34)
crimson = (220,20,60)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

banner_image = pygame.image.load('Images/Icon/Banners.png').convert_alpha()

def draw_text_middle_and_box(text, font, text_col, rect_col, x, y, image):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	text_image = font.render(text, True, text_col)
	image = pygame.transform.scale(image, (font_size[0] + 5, font_size[1] + 5))
	choice_image = screen.blit(image, (x, y))
	choice_text = screen.blit(text_image, (x + 2.5, y + 2.5))

	return choice_image, choice_text

#drawing panel
def draw_panel(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen):
	#draw panel rectangle
	screen.blit(panel_img,(0,screen_height - bottom_panel))
	#show knight stats
	draw_text(f'HP: {hero.hp:.2f}', font, crimson, 20, screen_height - bottom_panel + 20)
	draw_text(f'MP: {hero.mp:.2f}', font, crimson, 160, screen_height - bottom_panel + 20)	
	draw_text(f'EXP: {hero.experience:.1f}', font, crimson, 30, screen_height - bottom_panel + 70)
	draw_text(f'DEF: {hero.defense:.2f} + {hero.endurance * 0.2:.2f}', font, crimson, 30, screen_height - bottom_panel + 90)
	draw_text(f'SPD: {hero.speed:.2f} + {hero.agility * 0.2:.2f}', font, crimson, 30, screen_height - bottom_panel + 110)
	draw_text(f'STAT: {hero.statpoints}', font, crimson, 270-90, screen_height - bottom_panel + 90)
	draw_text(f'GOLD: {hero.gold:.2f}', font, crimson, 270-90, screen_height - bottom_panel + 70)
	draw_text(f'LVL: {hero.level}', font, crimson, 270-90, screen_height - bottom_panel + 110)

	#show monster stats	
	for count, i in enumerate(monster_list[monster_index]):
		monster_text_size = pygame.font.Font.size(font, f'{i.name} HP: {i.hp:.2f}')
		draw_text(f'{i.name} HP: {i.hp:.2f}', font, crimson, screen_width - (monster_text_size[0] + 20), (screen_height - bottom_panel + 20) + count * 60)	
		draw_text(f'LVL: {i.level}', font, crimson, screen_width - (monster_text_size[0] + 100), (screen_height - bottom_panel + 20) + count * 60)

def draw_background(background_img):
	screen.blit(background_img, (0,0))

def stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, click, battle_over):
	all_stats_added = hero.strength + hero.intelligence + hero.agility + hero.luck + hero.endurance
	mousex, mousey = pygame.mouse.get_pos()
	if hero.hitbox.collidepoint((mousex,mousey)) or battle_over == True:
		str_stat_rect, str_stat_text = draw_text_middle_and_box(f'STR: {hero.strength:.2f} ({hero.temp_strength:.2f})', font, brown, gold, screen_width, bottom_panel + 260, banner_image)
		int_stat_rect, int_stat_text = draw_text_middle_and_box(f'INT: {hero.intelligence:.2f} ({hero.temp_intelligence:.2f})', font, brown, gold, screen_width, bottom_panel + 282.5, banner_image)	
		agi_stat_rect, agi_stat_text = draw_text_middle_and_box(f'AGI: {hero.agility:.2f} ({hero.temp_agility:.2f})', font, brown, gold, screen_width, bottom_panel + 305, banner_image)	
		luc_stat_rect, luc_stat_text = draw_text_middle_and_box(f'LUC: {hero.luck:.2f} ({hero.temp_luck:.2f})', font, brown, gold, screen_width, bottom_panel + 327.5, banner_image)	
		end_stat_rect, end_stat_text = draw_text_middle_and_box(f'END: {hero.endurance:.2f} ({hero.temp_endurance:.2f})', font, brown, gold, screen_width, bottom_panel + 350, banner_image)	

	if battle_over == True:
		if str_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0 and hero.strength < all_stats_added - hero.strength:				
			hero.str_up_button()
		if agi_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0 and hero.agility < all_stats_added - hero.agility:
			hero.agi_up_button()
		if int_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0 and hero.intelligence < all_stats_added - hero.intelligence:
			hero.int_up_button()
		if luc_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0 and hero.luck < all_stats_added - hero.luck:
			hero.luc_up_button()
		if end_stat_rect.collidepoint((mousex,mousey)) and click == True and hero.statpoints > 0 and hero.endurance < all_stats_added - hero.endurance:
			hero.end_up_button()


# def draw_stat_background(screen, screen_height, bottom_panel, blue):
# 	s = pygame.Surface((43,20))  # the size of your rect
# 	s.set_alpha(128)                # alpha level
# 	s.fill(blue)           # this fills the entire surface
# 	screen.blit(s, (180-35, screen_height - bottom_panel + 70 - 2))    # (0,0) are the top-left coordinates	

def draw_current_attack(action_index, inventory, skills_list, hero, active_skills_list, all_active_skills_list):
	icon_image_dict = {
	'normal_attack' : { 'image' : sword_icon_img, 'index' : 0},
	'cleave' : { 'image' : cleave_icon_img, 'index' : 1},
	'zombie_stab' : { 'image' : zombie_stab_img, 'index' : 2},
	'triple_combo' : { 'image' : triple_combo_img, 'index' : 3},
	'serpent_wheel' : { 'image' : serpent_wheel_img, 'index' : 4},
	'venomous_whip' : { 'image' : venomous_whip_img, 'index' : 5},
	'thunder_bolt' : { 'image' : thunder_bolt_img, 'index' : 6}
	}
	skill_x = 0
	skill_y = 0

	for skills in active_skills_list:
		skill_x += 44
		screen.blit(icon_image_dict[skills]['image'], (skill_x, skill_y))
	# if action_index == 0:
	# 	screen.blit(sword_icon_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'cleave' in skills_list and action_index == 1:
	# 	screen.blit(cleave_icon_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'zombie_stab' in skills_list and action_index == 2:
	# 	screen.blit(zombie_stab_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'triple_combo' in skills_list and action_index == 3:
	# 	screen.blit(triple_combo_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'serpent_wheel' in skills_list and action_index == 4:
	# 	screen.blit(serpent_wheel_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'venomous_whip' in skills_list and action_index == 5:
	# 	screen.blit(venomous_whip_img, (hero.hitbox.right, hero.hitbox.top + 20))
	# elif 'thunder_bolt' in skills_list and action_index == 6:
	# 	screen.blit(thunder_bolt_img, (hero.hitbox.right, hero.hitbox.top + 20))