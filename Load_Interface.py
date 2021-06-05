import math, pygame, random, sys, ctypes

pygame.init()
#game window#
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
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.25)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#

panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img,(width(1),height(0.14)))
sword_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/SwordIcon.png').convert_alpha()
sword_icon_img = pygame.transform.scale(sword_icon_img,(width(0.035),height(0.035)))
cleave_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/CleaveIcon.png').convert_alpha()
cleave_icon_img = pygame.transform.scale(cleave_icon_img,(width(0.035),height(0.035)))
zombie_stab_img = pygame.image.load('Images/Icon/SkillDisplayIcon/ZombieStabIcon.png').convert_alpha()
zombie_stab_img = pygame.transform.scale(zombie_stab_img,(width(0.035),height(0.035)))
triple_combo_img = pygame.image.load('Images/Icon/SkillDisplayIcon/TripleComboIcon.png').convert_alpha()
triple_combo_img = pygame.transform.scale(triple_combo_img,(width(0.035),height(0.035)))
serpent_wheel_img = pygame.image.load('Images/Icon/SkillDisplayIcon/SerpentWheelIcon.png').convert_alpha()
serpent_wheel_img = pygame.transform.scale(serpent_wheel_img,(width(0.035),height(0.035)))
venomous_whip_img = pygame.image.load('Images/Icon/SkillDisplayIcon/VenomousWhipIcon.png').convert_alpha()
venomous_whip_img = pygame.transform.scale(venomous_whip_img,(width(0.035),height(0.035)))
thunder_bolt_img = pygame.image.load('Images/Icon/SkillDisplayIcon/ThunderBoltIcon.png').convert_alpha()
thunder_bolt_img = pygame.transform.scale(thunder_bolt_img,(width(0.035),height(0.035)))

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
	#show knight stats
	draw_text(f'HP: {hero.hp:.2f}', font, crimson, width_position(0.1), height_position(0.86))
	draw_text(f'MP: {hero.mp:.2f}', font, crimson, width_position(0.1), height_position(0.92))	

	#show monster stats	
	for count, i in enumerate(monster_list[monster_index]):
		monster_text_size = pygame.font.Font.size(font, f'{i.name} HP: {i.hp:.2f}')
		draw_text(f'{i.name} HP: {i.hp:.2f}', font, crimson, width_position(0.6), height_position(0.87) + (count * height_position(0.05)))	
		draw_text(f'LVL: {i.level}', font, crimson, width_position(0.6) + (monster_text_size[0] * 1.2), height_position(0.87) + (count * height_position(0.05)))

def draw_background(background_img):
	screen.blit(background_img, (0,0))

def stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, click, battle_over):
	all_stats_added = hero.strength + hero.intelligence + hero.agility + hero.luck + hero.endurance
	mousex, mousey = pygame.mouse.get_pos()
	str_stat_rect, str_stat_text = draw_text_middle_and_box(f'STR: {hero.strength:.2f}', font, brown, gold, screen_width, height_position(0.83), banner_image)
	int_stat_rect, int_stat_text = draw_text_middle_and_box(f'INT: {hero.intelligence:.2f}', font, brown, gold, screen_width, height_position(0.86), banner_image)	
	agi_stat_rect, agi_stat_text = draw_text_middle_and_box(f'AGI: {hero.agility:.2f}', font, brown, gold, screen_width, height_position(0.89), banner_image)	
	luc_stat_rect, luc_stat_text = draw_text_middle_and_box(f'LUC: {hero.luck:.2f}', font, brown, gold, screen_width, height_position(0.92), banner_image)	
	end_stat_rect, end_stat_text = draw_text_middle_and_box(f'END: {hero.endurance:.2f}', font, brown, gold, screen_width, height_position(0.95), banner_image)	

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

def draw_current_attack(action_index, inventory, hero):
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

	for skills in hero.active_skills_list:
		skill_x += width(0.035)
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