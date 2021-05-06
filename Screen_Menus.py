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
darker_orange = (254,110,0)

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
'condensed_lightning' : {'image' : pygame.image.load('Images/Icon/Relics/Relics5.png').convert_alpha(), 'description' : 'Fireball Damage * 1.75, INT + 3', 'hitbox' : pygame.rect.Rect(400, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(80, 75, 64, 64), 'index' : 5, 'name' : 'Condensed Lightning', 'cost' : 1500 + random.randint(-250,250), 'row_index': 1, 'column_index': 5},
'shield' : {'image' : pygame.image.load('Images/Icon/Relics/Relics6.png').convert_alpha(), 'description' : 'Auto Guard After Some Turns, DEF + 1', 'hitbox' : pygame.rect.Rect(480, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(160, 75, 64, 64), 'index' : 6, 'name' : 'Shield', 'cost' : 1500 + random.randint(-250,250), 'row_index': 1, 'column_index': 6},
'razor_mail' : {'image' : pygame.image.load('Images/Icon/Relics/Relics7.png').convert_alpha(), 'description' : 'Return 25% DEF + 15% Damage, DEF + 1', 'hitbox' : pygame.rect.Rect(560, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(240, 75, 64, 64), 'index' : 7, 'name' : 'Razor Mail', 'cost' : 1500 + random.randint(-250,250), 'row_index': 1, 'column_index': 7},
'ruby' : {'image' : pygame.image.load('Images/Icon/Relics/Relics8.png').convert_alpha(), 'description' : 'MP Regen Added To HP Regen', 'hitbox' : pygame.rect.Rect(640, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(320, 75, 64, 64), 'index' : 8, 'name' : 'Ruby', 'cost' : 1000 + random.randint(-250,250), 'row_index': 1, 'column_index': 8},
'infernal_obsidian' : {'image' : pygame.image.load('Images/Icon/Relics/Relics9.png').convert_alpha(), 'description' : 'Mini Fireball Start Of Combat', 'hitbox' : pygame.rect.Rect(720, 75, 64, 64),'shop_hitbox' : pygame.rect.Rect(400, 75, 64, 64), 'index' : 9, 'name' : 'Infernal Obsidian', 'cost' : 2000 + random.randint(-250,250), 'row_index': 1, 'column_index': 9},
'mist_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics10.png').convert_alpha(), 'description' : 'Hero MP Regen + 2, Max MP + 5', 'hitbox' : pygame.rect.Rect(0, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(480, 75, 64, 64), 'index' : 10, 'name' : 'Mist Stone', 'cost' : 1500 + random.randint(-250,250), 'row_index': 2, 'column_index': 0},
'slime_ball' : {'image' : pygame.image.load('Images/Icon/Relics/Relics11.png').convert_alpha(), 'description' : 'All Monster SPD - 0.5', 'hitbox' : pygame.rect.Rect(80, 150, 64, 64), 'index' : 11, 'name' : 'Slime Ball', 'row_index': 2, 'column_index': 1},
'crimson_head_snake' : {'image' : pygame.image.load('Images/Icon/Relics/Relics12.png').convert_alpha(), 'description' : 'All Monster HP Regen - 1', 'hitbox' : pygame.rect.Rect(160, 150, 64, 64), 'index' : 12, 'name' : 'Crimson Head Snake', 'row_index': 2, 'column_index': 2},
'stunted_tornado' : {'image' : pygame.image.load('Images/Icon/Relics/Relics13.png').convert_alpha(), 'description' : 'Hero SPD + 1.5, AGI + 1.5', 'hitbox' : pygame.rect.Rect(240, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(560, 75, 64, 64), 'index' : 13, 'name' : 'Stunted Tornado', 'cost' : 1500 + random.randint(-250,250), 'row_index': 2, 'column_index': 3},
'zombie_spine' : {'image' : pygame.image.load('Images/Icon/Relics/Relics14.png').convert_alpha(), 'description' : 'Unlocks Zombie Stab', 'hitbox' : pygame.rect.Rect(320, 150, 64, 64),'index' : 14, 'name' : 'Zombie Spine', 'row_index': 2, 'column_index': 4},
'thunder_charge' : {'image' : pygame.image.load('Images/Icon/Relics/Relics15.png').convert_alpha(), 'description' : 'Hero Stamina Recovery + 0.5', 'hitbox' : pygame.rect.Rect(400, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(640, 75, 64, 64), 'index' : 15, 'name' : 'Thunder Charge', 'cost' : 1000 + random.randint(-250,250), 'row_index': 2, 'column_index': 5},
'fluffy_cloud' : {'image' : pygame.image.load('Images/Icon/Relics/Relics16.png').convert_alpha(), 'description' : 'Hero Stamina Recovery + 0.25, SPD + 0.25', 'hitbox' : pygame.rect.Rect(480, 150, 64, 64),'index' : 16, 'name' : 'Fluffy Cloud', 'row_index': 2, 'column_index': 6},
'grey_opal' : {'image' : pygame.image.load('Images/Icon/Relics/Relics17.png').convert_alpha(), 'description' : 'Stamina Threshold - 50', 'hitbox' : pygame.rect.Rect(560, 150, 64, 64),'index' : 17, 'name' : 'Grey Opal', 'row_index': 2, 'column_index': 7},
'dragon_eye' : {'image' : pygame.image.load('Images/Icon/Relics/Relics18.png').convert_alpha(), 'description' : '50% Chance To Attack Twice', 'hitbox' : pygame.rect.Rect(640, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(720, 75, 64, 64), 'index' : 18, 'name' : 'Dragon Eye', 'cost' : 1750 + random.randint(-250,250), 'row_index': 2, 'column_index': 8},
'hydro_vortex' : {'image' : pygame.image.load('Images/Icon/Relics/Relics19.png').convert_alpha(), 'description' : 'Absorbs 15% Normal Attack Damage As HP', 'hitbox' : pygame.rect.Rect(720, 150, 64, 64),'shop_hitbox' : pygame.rect.Rect(0, 150, 64, 64), 'index' : 19, 'name' : 'Hydro Vortex', 'cost' : 1250 + random.randint(-250,250), 'row_index': 2, 'column_index': 9},
'kunai' : {'image' : pygame.image.load('Images/Icon/Relics/Relics20.png').convert_alpha(), 'description' : 'Counter With Full Damage', 'hitbox' : pygame.rect.Rect(0, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(80, 150, 64, 64), 'index' : 20, 'name' : 'Kunai', 'cost' : 1500 + random.randint(-250,250), 'row_index': 3, 'column_index': 0},
'stone_bracelet' : {'image' : pygame.image.load('Images/Icon/Relics/Relics21.png').convert_alpha(), 'description' : 'All Monster SPD - 2', 'hitbox' : pygame.rect.Rect(80, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(160, 150, 64, 64), 'index' : 21, 'name' : 'Stone Bracelet', 'cost' : 1500 + random.randint(-250,250), 'row_index': 3, 'column_index': 1},
'dark_matter' : {'image' : pygame.image.load('Images/Icon/Relics/Relics22.png').convert_alpha(), 'description' : 'All Monster DEF - 2', 'hitbox' : pygame.rect.Rect(160, 225, 64, 64),'index' : 22, 'name' : 'Dark Matter', 'row_index': 3, 'column_index': 2},
'lightning_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics23.png').convert_alpha(), 'description' : 'Hero Stamina Recover + 2', 'hitbox' : pygame.rect.Rect(240, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(240, 150, 64, 64), 'index' : 23, 'name' : 'Lightning Stone', 'cost' : 2000 + random.randint(-250,250), 'row_index': 3, 'column_index': 3},
'war_drum' : {'image' : pygame.image.load('Images/Icon/Relics/Relics24.png').convert_alpha(), 'description' : '25% Chance Stomp After Attack', 'hitbox' : pygame.rect.Rect(320, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(320, 150, 64, 64), 'index' : 24, 'name' : 'War Drum', 'cost' : 1750 + random.randint(-250,250), 'row_index': 3, 'column_index': 4},
'glow_fern' : {'image' : pygame.image.load('Images/Icon/Relics/Relics25.png').convert_alpha(), 'description' : 'Hero HP Regen + 10', 'hitbox' : pygame.rect.Rect(400, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(400, 150, 64, 64), 'index' : 25, 'name' : 'Glow Fern', 'cost' : 2000 + random.randint(-250,250), 'row_index': 3, 'column_index': 5},
'grimoire' : {'image' : pygame.image.load('Images/Icon/Relics/Relics26.png').convert_alpha(), 'description' : 'All Monster HP - 20% Hero INT Every End Turn', 'hitbox' : pygame.rect.Rect(480, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(480, 150, 64, 64), 'index' : 26, 'name' : 'Grimoire', 'cost' : 2000 + random.randint(-250,250), 'row_index': 3, 'column_index': 6},
'bahamut_heart' : {'image' : pygame.image.load('Images/Icon/Relics/Relics27.png').convert_alpha(), 'description' : 'Hero END + 5, DEF + 3 HP Regen + 3', 'hitbox' : pygame.rect.Rect(560, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(560, 150, 64, 64), 'index' : 27, 'name' : 'Bahamut Heart', 'cost' : 2000 + random.randint(-250,250), 'row_index': 3, 'column_index': 7},
'phoenix_feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics28.png').convert_alpha(), 'description' : 'Hero Revives With 50% HP', 'hitbox' : pygame.rect.Rect(640, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(640, 150, 64, 64), 'index' : 28, 'name' : 'Phoenix Feather', 'cost' : 2250 + random.randint(-250,250), 'row_index': 3, 'column_index': 8},
'pocket_ghost' : {'image' : pygame.image.load('Images/Icon/Relics/Relics29.png').convert_alpha(), 'description' : 'All Monster STR - 4', 'hitbox' : pygame.rect.Rect(720, 225, 64, 64),'shop_hitbox' : pygame.rect.Rect(720, 150, 64, 64), 'index' : 29, 'name' : 'Pocket Ghost', 'cost' : 1750 + random.randint(-250,250), 'row_index': 3, 'column_index': 9},
'poison_ivy' : {'image' : pygame.image.load('Images/Icon/Relics/Relics30.png').convert_alpha(), 'description' : 'All Monster HP Regen - 4', 'hitbox' : pygame.rect.Rect(0, 300, 64, 64),'shop_hitbox' : pygame.rect.Rect(0, 225, 64, 64), 'index' : 30, 'name' : 'Poison Ivy', 'cost' : 2000 + random.randint(-250,250), 'row_index': 4, 'column_index': 0},
'hasai_and_hyo' : {'image' : pygame.image.load('Images/Icon/Relics/Relics31.png').convert_alpha(), 'description' : 'Fireball Turns To Sapphire Flame (Steals 20% Turn), Hero INT + 3', 'hitbox' : pygame.rect.Rect(80, 300, 64, 64),'shop_hitbox' : pygame.rect.Rect(80, 225, 64, 64), 'index' : 31, 'name' : 'Hasai And Hyo', 'cost' : 2000 + random.randint(-250,250), 'row_index': 4, 'column_index': 1}

}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather', 'eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 'slime_ball', 'crimson_head_snake', 'stunted_tornado', 'zombie_spine', 'thunder_charge', 'fluffy_cloud', 'grey_opal', 'dragon_eye', 'hydro_vortex', 'kunai', 'stone_bracelet', 'dark_matter', 'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 'phoenix_feather', 'pocket_ghost', 'poison_ivy', 'hasai_and_hyo']
shop_names_list = ['eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 'stunted_tornado', 'thunder_charge', 'dragon_eye', 'hydro_vortex', 'kunai', 'stone_bracelet', 'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 'phoenix_feather', 'pocket_ghost', 'poison_ivy', 'hasai_and_hyo']

#random shop items start of game
for deletion in range(math.floor(len(shop_names_list) * 0.6)):
	random_deletion = random.randint(0,len(shop_names_list) - 1)
	del shop_names_list[random_deletion]

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
				screen.blit(font.render('NAME:' + items[names]['name'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey - 40))
				screen.blit(font.render('DESC:' + items[names]['description'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))
					
#option loop#
def options_menu(inventory, monster_list, monster_index, hero):
	inside_menu = True
	while inside_menu:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'INVENTORY', font_heading, red, screen_width, 10)
		draw_text(f'GOLD: {hero.gold:.2f}', font, red, 20, screen_height - bottom_panel + 20)
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
		rest = draw_text(f'REST: ' + str(math.floor((hero.gold * 0.2) + ((hero.max_hp - hero.hp) * 4) + ((hero.max_mp - hero.mp) * 4))), font, yellow, 20, screen_height - bottom_panel + 40)
		rest_rect = pygame.rect.Rect(20, screen_height - bottom_panel + 40, 64, 64)
		if shop_click == True and hero.gold >= math.floor((hero.gold * 0.2) + ((hero.max_hp - hero.hp) * 4) + ((hero.max_mp - hero.mp) * 4)) and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
			hero.gold -= math.floor((hero.gold * 0.2) + ((hero.max_hp - hero.hp) * 4) + ((hero.max_mp - hero.mp) * 4))
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

	buy_fireball_rect, buy_fireball_text = draw_text_middle_and_box_consumables(f'FIREBALL: {400 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 60)
	if shop_click == True and hero.gold >= 400 + (hero.level * 20) and buy_fireball_rect.collidepoint((mousex,mousey)) and hero.fireball_charge < 3:
		hero.gold -= 400 + (hero.level * 20)
		hero.fireball_charge += 1

	buy_lightning_rect, buy_lightning_text = draw_text_middle_and_box_consumables(f'LIGHTNING: {400 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 80)
	if shop_click == True and hero.gold >= 400 + (hero.level * 20) and buy_lightning_rect.collidepoint((mousex,mousey)) and hero.lightning_charge < 3:
		hero.gold -= 400 + (hero.level * 20)
		hero.lightning_charge += 1

	for item_image in shop_names_list:
		if item_image in shop_names_list:
			screen.blit(items[item_image]['image'], (items[item_image]['shop_hitbox'].x, items[item_image]['shop_hitbox'].y))

	for names in shop_names_list:
		if items[names]['shop_hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] not in inventory:
			font_size = pygame.font.Font.size(font, items[names]['description'])
			screen.blit(font.render('NAME:' + items[names]['name'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey - 40))
			screen.blit(font.render('DESC:' + items[names]['description'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))	
			screen.blit(font.render('COST:' + str(items[names]['cost']), True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey))	
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
			if shop_click == True and hero.gold >= items['dragon_eye']['cost'] and items['dragon_eye']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['dragon_eye']['cost']
				inventory.append(18)
				shop_names_list.remove('dragon_eye')
				shop_click = False
			if shop_click == True and hero.gold >= items['hydro_vortex']['cost'] and items['hydro_vortex']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['hydro_vortex']['cost']
				inventory.append(19)
				shop_names_list.remove('hydro_vortex')
				shop_click = False
			if shop_click == True and hero.gold >= items['kunai']['cost'] and items['kunai']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['kunai']['cost']
				inventory.append(20)
				shop_names_list.remove('kunai')
				shop_click = False
			if shop_click == True and hero.gold >= items['stone_bracelet']['cost'] and items['stone_bracelet']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['stone_bracelet']['cost']
				for monster_group in monster_list:
					for monster in monster_group:
						monster.speed -= 2				
				inventory.append(21)
				shop_names_list.remove('stone_bracelet')
				shop_click = False
			if shop_click == True and hero.gold >= items['lightning_stone']['cost'] and items['lightning_stone']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['lightning_stone']['cost']
				hero.stamina_recovery += 2
				inventory.append(23)
				shop_names_list.remove('lightning_stone')
				shop_click = False
			if shop_click == True and hero.gold >= items['war_drum']['cost'] and items['war_drum']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['war_drum']['cost']
				inventory.append(24)
				shop_names_list.remove('war_drum')
				shop_click = False
			if shop_click == True and hero.gold >= items['glow_fern']['cost'] and items['glow_fern']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['glow_fern']['cost']
				hero.hp_regen += 10
				inventory.append(25)
				shop_names_list.remove('glow_fern')
				shop_click = False
			if shop_click == True and hero.gold >= items['grimoire']['cost'] and items['grimoire']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['grimoire']['cost']
				inventory.append(26)
				shop_names_list.remove('grimoire')
				shop_click = False
			if shop_click == True and hero.gold >= items['bahamut_heart']['cost'] and items['bahamut_heart']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['bahamut_heart']['cost']
				hero.endurance += 5
				hero.defense += 3
				hero.hp_regen += 3
				inventory.append(27)
				shop_names_list.remove('bahamut_heart')
				shop_click = False
			if shop_click == True and hero.gold >= items['phoenix_feather']['cost'] and items['phoenix_feather']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['phoenix_feather']['cost']
				inventory.append(28)
				shop_names_list.remove('phoenix_feather')
				shop_click = False
			if shop_click == True and hero.gold >= items['pocket_ghost']['cost'] and items['pocket_ghost']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['pocket_ghost']['cost']
				for monster_group in monster_list:
					for monster in monster_group:
						monster.strength -= 4				
				inventory.append(29)
				shop_names_list.remove('pocket_ghost')
				shop_click = False
			if shop_click == True and hero.gold >= items['poison_ivy']['cost'] and items['poison_ivy']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['poison_ivy']['cost']
				for monster_group in monster_list:
					for monster in monster_group:
						monster.hp_regen -= 4				
				inventory.append(30)
				shop_names_list.remove('poison_ivy')
				shop_click = False
			if shop_click == True and hero.gold >= items['hasai_and_hyo']['cost'] and items['hasai_and_hyo']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= items['hasai_and_hyo']['cost']	
				hero.intelligence += 3		
				inventory.append(31)
				shop_names_list.remove('hasai_and_hyo')
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
		draw_text(f'GOLD: {hero.gold:.2f}', font, red, 20, screen_height - bottom_panel + 20)
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
