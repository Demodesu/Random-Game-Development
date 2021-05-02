import math, pygame, random, sys

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

shop_inventory_img = pygame.image.load('Images/Background/Shop_Inventory.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

def draw_text_middle_and_box_consumables(text, font, text_col, rect_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	img = font.render(text, True, text_col)
	rect = pygame.rect.Rect(x, y, font_size[0] + 5, font_size[1] + 5)
	choice_rect = pygame.draw.rect(screen, rect_col, rect)
	choice_text = screen.blit(img, (x + 2.5, y + 2.5))

	return choice_rect, choice_text

#-------------------------------------------------------------------#
#item name:{image:loadimage, description:decription, hitbox:hitbox, index:index, name:name}
items = {
'ring_of_health' : {'image' : pygame.image.load('Images/Icon/Relics/Relics0.png').convert_alpha(), 'description' : 'Max HP + 3', 'hitbox' : pygame.rect.Rect(0, 75, 64, 64), 'index' : 0, 'name' : 'Ring Of Health', 'row_index': 1, 'column_index': 0},
'raptor_claw' : {'image' : pygame.image.load('Images/Icon/Relics/Relics1.png').convert_alpha(), 'description' : 'STR + 1', 'hitbox' : pygame.rect.Rect(80, 75, 64, 64), 'index' : 1, 'name' : 'Raptor Claw', 'row_index': 1, 'column_index': 1},
'four_leaf_clover' : {'image' : pygame.image.load('Images/Icon/Relics/Relics2.png').convert_alpha(), 'description' : 'LUC + 1', 'hitbox' : pygame.rect.Rect(160, 75, 64, 64), 'index' : 2, 'name' : 'Four Leaf Clover', 'row_index': 1, 'column_index': 2},
'feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics3.png').convert_alpha(), 'description' : 'SPD + 0.25', 'hitbox' : pygame.rect.Rect(240, 75, 64, 64), 'index' : 3, 'name' : 'Feather', 'row_index': 1, 'column_index': 3},
'eye_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Relics/Relics4.png').convert_alpha(), 'description' : 'Lifesteal 10% Damage', 'hitbox' : pygame.rect.Rect(320, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(0, 75, 64, 64), 'index' : 4, 'name' : 'Eye Of Vladimir', 'cost' : 1000 + random.randint(-250,250), 'row_index': 1, 'column_index': 4},
'condensed_lightning' : {'image' : pygame.image.load('Images/Icon/Relics/Relics5.png').convert_alpha(), 'description' : 'Fireball Damage * 2, INT + 3', 'hitbox' : pygame.rect.Rect(400, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(80, 75, 64, 64), 'index' : 5, 'name' : 'Condensed Lightning', 'cost' : 1500 + random.randint(-250,250), 'row_index': 1, 'column_index': 5},
'shield' : {'image' : pygame.image.load('Images/Icon/Relics/Relics6.png').convert_alpha(), 'description' : 'Auto Guard After Some Turns, DEF + 1', 'hitbox' : pygame.rect.Rect(480, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(160, 75, 64, 64), 'index' : 6, 'name' : 'Shield', 'cost' : 2000 + random.randint(-250,250), 'row_index': 1, 'column_index': 6},
'razor_mail' : {'image' : pygame.image.load('Images/Icon/Relics/Relics7.png').convert_alpha(), 'description' : 'Return 25% DEF + 15% Damage, DEF + 1', 'hitbox' : pygame.rect.Rect(560, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(240, 75, 64, 64), 'index' : 7, 'name' : 'Razor Mail', 'cost' : 1500 + random.randint(-250,250), 'row_index': 1, 'column_index': 7},
'ruby' : {'image' : pygame.image.load('Images/Icon/Relics/Relics8.png').convert_alpha(), 'description' : 'MP Regen Added To HP Regen', 'hitbox' : pygame.rect.Rect(640, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(320, 75, 64, 64), 'index' : 8, 'name' : 'Ruby', 'cost' : 1000 + random.randint(-250,250), 'row_index': 1, 'column_index': 8},
'infernal_obsidian' : {'image' : pygame.image.load('Images/Icon/Relics/Relics9.png').convert_alpha(), 'description' : 'Mini Fireball Start Of Combat', 'hitbox' : pygame.rect.Rect(720, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(400, 75, 64, 64), 'index' : 9, 'name' : 'Infernal Obsidian', 'cost' : 2000 + random.randint(-250,250), 'row_index': 1, 'column_index': 9},
'mist_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics10.png').convert_alpha(), 'description' : 'Hero MP Regen + 2, Max MP + 5', 'hitbox' : pygame.rect.Rect(0, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(480, 75, 64, 64), 'index' : 10, 'name' : 'Mist Stone', 'cost' : 2000 + random.randint(-250,250), 'row_index': 2, 'column_index': 0},
'slime_ball' : {'image' : pygame.image.load('Images/Icon/Relics/Relics11.png').convert_alpha(), 'description' : 'All Monster SPD - 0.5', 'hitbox' : pygame.rect.Rect(80, 150, 64, 64), 'index' : 11, 'name' : 'Slime Ball', 'row_index': 2, 'column_index': 1},
'crimson_head_snake' : {'image' : pygame.image.load('Images/Icon/Relics/Relics12.png').convert_alpha(), 'description' : 'All Monster HP Regen - 1', 'hitbox' : pygame.rect.Rect(160, 150, 64, 64), 'index' : 12, 'name' : 'Crimson Head Snake', 'row_index': 2, 'column_index': 2},
'stunted_tornado' : {'image' : pygame.image.load('Images/Icon/Relics/Relics13.png').convert_alpha(), 'description' : 'Hero SPD + 1.5, AGI + 1.5', 'hitbox' : pygame.rect.Rect(240, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(560, 75, 64, 64), 'index' : 13, 'name' : 'Stunted Tornado', 'cost' : 2500 + random.randint(-250,250), 'row_index': 2, 'column_index': 3},
'zombie_spine' : {'image' : pygame.image.load('Images/Icon/Relics/Relics14.png').convert_alpha(), 'description' : 'Unlocks Zombie Stab', 'hitbox' : pygame.rect.Rect(320, 150, 64, 64),'index' : 14, 'name' : 'Zombie Spine', 'row_index': 2, 'column_index': 4},
'thunder_charge' : {'image' : pygame.image.load('Images/Icon/Relics/Relics15.png').convert_alpha(), 'description' : 'Hero Stamina Recovery + 0.5', 'hitbox' : pygame.rect.Rect(400, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(640, 75, 64, 64), 'index' : 15, 'name' : 'Thunder Charge', 'cost' : 1000 + random.randint(-250,250), 'row_index': 2, 'column_index': 5},
'fluffy_cloud' : {'image' : pygame.image.load('Images/Icon/Relics/Relics16.png').convert_alpha(), 'description' : 'Hero Stamina Recovery + 0.25, SPD + 0.25', 'hitbox' : pygame.rect.Rect(480, 150, 64, 64),'index' : 16, 'name' : 'Fluffy Cloud', 'row_index': 2, 'column_index': 6},
'grey_opal' : {'image' : pygame.image.load('Images/Icon/Relics/Relics17.png').convert_alpha(), 'description' : 'Stamina Threshold - 50', 'hitbox' : pygame.rect.Rect(640, 150, 64, 64),'index' : 17, 'name' : 'Grey Opal', 'row_index': 2, 'column_index': 7}

}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather', 'eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 'slime_ball', 'crimson_head_snake', 'stunted_tornado', 'zombie_spine', 'thunder_charge', 'fluffy_cloud', 'grey_opal']
shop_names_list = ['eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 'stunted_tornado', 'thunder_charge']

def draw_items(inventory, monster_list, monster_index):
	#draw the image
	for image in names_list:
		if items[image]['index'] in inventory:
			screen.blit(items[image]['image'], (items[image]['column_index'] * 80, items[image]['row_index'] * 75))
	#if collide with hitbox, show the description
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for names in names_list:
		if items[names]['index'] in inventory:
			if items[names]['hitbox'].collidepoint((mousex,mousey)):
				font_size = pygame.font.Font.size(font, items[names]['description'])
				screen.blit(font.render('NAME:' + items[names]['name'], True, blue), ((screen_width / 2) - (font_size[0] / 2), mousey - 40))
				screen.blit(font.render('DESC:' + items[names]['description'], True, blue), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))
					
#option loop#
def options_menu(inventory, monster_list, monster_index, hero):
	inside_menu = True
	while inside_menu:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'INVENTORY', font_heading, red, screen_width, 10)
		draw_text(f'GOLD: {hero.gold}', font, red, 20, screen_height - bottom_panel + 20)
		draw_items(inventory, monster_list, monster_index)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_menu = False
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					inside_menu = False

		pygame.display.update()

#-------------------------------------------------------------------#

def shop(inventory, hero, shop_click, monster_list, monster_index):
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()

	if hero.level >= 5:
		rest = draw_text(f'REST: ' + str(math.floor((hero.gold * 0.2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))), font, yellow, 20, screen_height - bottom_panel + 40)
		rest_rect = pygame.rect.Rect(20, screen_height - bottom_panel + 40, 64, 64)
		if shop_click == True and hero.gold >= math.floor((hero.gold / 2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))  and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
			hero.gold -= math.floor((hero.gold / 2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))
			hp_heal_amount = hero.max_hp - hero.hp
			mp_heal_amount = hero.max_mp - hero.mp
			hero.hp += hp_heal_amount
			hero.mp += mp_heal_amount
	else:
		rest = draw_text(f'REST(LVL <= 5): ' + str('100'), font, yellow, 20, screen_height - bottom_panel + 40)
		rest_rect = pygame.rect.Rect(20, screen_height - bottom_panel + 40, 64, 64)
		if shop_click == True and hero.gold >= 100 and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
			hero.gold -= 100
			hp_heal_amount = hero.max_hp - hero.hp
			mp_heal_amount = hero.max_mp - hero.mp
			hero.hp += hp_heal_amount
			hero.mp += mp_heal_amount

	buy_fireball_rect, buy_fireball_text = draw_text_middle_and_box_consumables(f'FIREBALL: {500 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 60)
	if shop_click == True and hero.gold >= 500 + (hero.level * 20) and buy_fireball_rect.collidepoint((mousex,mousey)):
		hero.gold -= 500 + (hero.level * 20)
		hero.fireball_charge += 1

	buy_lightning_rect, buy_lightning_text = draw_text_middle_and_box_consumables(f'LIGHTNING: {500 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 80)
	if shop_click == True and hero.gold >= 500 + (hero.level * 20) and buy_lightning_rect.collidepoint((mousex,mousey)):
		hero.gold -= 500 + (hero.level * 20)
		hero.lightning_charge += 1

	if 4 not in inventory:
		screen.blit(items['eye_of_vladimir']['image'], (0, 75))
	if 5 not in inventory:
		screen.blit(items['condensed_lightning']['image'], (80, 75))
	if 6 not in inventory:
		screen.blit(items['shield']['image'], (160, 75))	
	if 7 not in inventory:
		screen.blit(items['razor_mail']['image'], (240, 75))	
	if 8 not in inventory:
		screen.blit(items['ruby']['image'], (320, 75))	
	if 9 not in inventory:
		screen.blit(items['infernal_obsidian']['image'], (400, 75))
	if 10 not in inventory:
		screen.blit(items['mist_stone']['image'], (480, 75))
	if 13 not in inventory:
		screen.blit(items['stunted_tornado']['image'], (560, 75))
	if 15 not in inventory:
		screen.blit(items['thunder_charge']['image'], (640, 75))

	for names in shop_names_list:
		if items[names]['shop_hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] not in inventory:
			font_size = pygame.font.Font.size(font, items[names]['description'])
			screen.blit(font.render('NAME:' + items[names]['name'], True, blue), ((screen_width / 2) - (font_size[0] / 2), mousey - 40))
			screen.blit(font.render('DESC:' + items[names]['description'], True, blue), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))	
			screen.blit(font.render('COST:' + str(items[names]['cost']), True, blue), ((screen_width / 2) - (font_size[0] / 2), mousey))	
			if shop_click == True and hero.gold >= items['eye_of_vladimir']['cost'] and items['eye_of_vladimir']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['eye_of_vladimir']['cost']
				inventory.append(4)
				shop_names_list.remove('eye_of_vladimir')
				shop_click = False
			if shop_click == True and hero.gold >= items['condensed_lightning']['cost'] and items['condensed_lightning']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['condensed_lightning']['cost']
				inventory.append(5)
				hero.intelligence += 3
				shop_names_list.remove('condensed_lightning')
				shop_click = False
			if shop_click == True and hero.gold >= items['shield']['cost'] and items['shield']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['shield']['cost']
				hero.defense += 1
				inventory.append(6)
				shop_names_list.remove('shield')
				shop_click = False
			if shop_click == True and hero.gold >= items['razor_mail']['cost'] and items['razor_mail']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['razor_mail']['cost']
				hero.defense += 1
				inventory.append(7)
				shop_names_list.remove('razor_mail')
				shop_click = False
			if shop_click == True and hero.gold >= items['ruby']['cost'] and items['ruby']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['ruby']['cost']
				inventory.append(8)
				shop_names_list.remove('ruby')
				shop_click = False
			if shop_click == True and hero.gold >= items['infernal_obsidian']['cost'] and items['infernal_obsidian']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['infernal_obsidian']['cost']
				inventory.append(9)
				shop_names_list.remove('infernal_obsidian')
				shop_click = False
			if shop_click == True and hero.gold >= items['mist_stone']['cost'] and items['mist_stone']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['mist_stone']['cost']
				hero.max_mp += 5
				hero.mp_regen += 2
				inventory.append(10)
				shop_names_list.remove('mist_stone')
				shop_click = False
			if shop_click == True and hero.gold >= items['stunted_tornado']['cost'] and items['stunted_tornado']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['stunted_tornado']['cost']
				hero.speed += 1.5
				hero.agility += 1.5
				inventory.append(13)
				shop_names_list.remove('stunted_tornado')
				shop_click = False
			if shop_click == True and hero.gold >= items['thunder_charge']['cost'] and items['thunder_charge']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['thunder_charge']['cost']
				hero.stamina_recovery += 0.5
				inventory.append(15)
				shop_names_list.remove('thunder_charge')
				shop_click = False

			shop_click = False
			return shop_click

def shop_menu(inventory, hero, monster_list, monster_index):
	inside_shop = True
	shop_click = False
	while inside_shop:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'SHOP', font_heading, red, screen_width, 10)
		draw_text(f'GOLD: {hero.gold}', font, red, 20, screen_height - bottom_panel + 20)
		shop(inventory, hero, shop_click, monster_list, monster_index)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_shop = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				shop_click = True
				shop_click = shop(inventory, hero, shop_click, monster_list, monster_index)	

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					inside_shop = False

		
		pygame.display.update()	
