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
font = pygame.font.SysFont('Minecraft', 26)
font_heading = pygame.font.SysFont('Minecraft', 40)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#-------------------------------------------------------------------#
#item name:{image:loadimage, description:decription, hitbox:hitbox, index:index, name:name}
items = {
'ring_of_health' : {'image' : pygame.image.load('Images/Icon/Relics/Relics0.png').convert_alpha(), 'description' : 'Max HP + 5', 'hitbox' : pygame.rect.Rect(0, 50, 64, 64), 'index' : 0, 'name' : 'Ring Of Health'},
'raptor_claw' : {'image' : pygame.image.load('Images/Icon/Relics/Relics1.png').convert_alpha(), 'description' : 'STR + 5', 'hitbox' : pygame.rect.Rect(80, 50, 64, 64), 'index' : 1, 'name' : 'Raptor Claw'},
'four_leaf_clover' : {'image' : pygame.image.load('Images/Icon/Relics/Relics2.png').convert_alpha(), 'description' : 'LUC + 5', 'hitbox' : pygame.rect.Rect(160, 50, 64, 64), 'index' : 2, 'name' : 'Four Leaf Clover'},
'feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics3.png').convert_alpha(), 'description' : 'EVA + 5', 'hitbox' : pygame.rect.Rect(240, 50, 64, 64), 'index' : 3, 'name' : 'Feather'},
'eye_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Relics/Relics4.png').convert_alpha(), 'description' : 'Lifesteal 10% Target Max HP + 10% Hero STR', 'hitbox' : pygame.rect.Rect(320, 50, 64, 64),'shop_hitbox' : pygame.rect.Rect(0, 50, 64, 64), 'index' : 4, 'name' : 'Eye Of Vladimir', 'cost' : 1000},
'condensed_lightning' : {'image' : pygame.image.load('Images/Icon/Relics/Relics5.png').convert_alpha(), 'description' : 'Fireball Damage * 2, INT + 5', 'hitbox' : pygame.rect.Rect(400, 50, 64, 64),'shop_hitbox' : pygame.rect.Rect(80, 50, 64, 64), 'index' : 5, 'name' : 'Condensed Lightning', 'cost' : 1000},
'shield' : {'image' : pygame.image.load('Images/Icon/Relics/Relics6.png').convert_alpha(), 'description' : 'Auto Guard Start Of Turn', 'hitbox' : pygame.rect.Rect(480, 50, 64, 64),'shop_hitbox' : pygame.rect.Rect(160, 50, 64, 64), 'index' : 6, 'name' : 'Shield', 'cost' : 1000}
}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather', 'eye_of_vladimir', 'condensed_lightning', 'shield']
shop_names_list = ['eye_of_vladimir', 'condensed_lightning', 'shield']
def draw_items(inventory):
	#draw the image
	for image in names_list:
		if items[image]['index'] in inventory:
			pygame.draw.rect(screen,(139,69,19),items[image]['hitbox'], 2)
			screen.blit(items[image]['image'], (items[image]['index'] * 80, 50))
	#if collide with hitbox, show the description
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for names in names_list:
		if items[names]['index'] in inventory:
			if items[names]['hitbox'].collidepoint((mousex,mousey)):
				screen.blit(font.render('NAME:' + items[names]['name'], True, blue), (mousex, mousey - 40))
				screen.blit(font.render('DESC:' + items[names]['description'], True, blue), (mousex, mousey - 20))

def drop_items(monster, hero, inventory):
	if monster.alive == False:
		if monster.level > 0:
			if 0 not in inventory:			
				rollitemactive = random.randint(0,100)
				if rollitemactive > 50:
					inventory.append(0)
					hero.max_hp += 5
					hero.hp += 5
			if 1 not in inventory:
				rollitemactive = random.randint(0,100)
				if rollitemactive > 60:
					inventory.append(1)
					hero.strength += 5
			if 2 not in inventory:
				rollitemactive = random.randint(0,100)
				if rollitemactive > 60:
					inventory.append(2)
					hero.luck += 3
			if 3 not in inventory:
				rollitemactive = random.randint(0,100)
				if rollitemactive > 50:
					inventory.append(3)
					hero.evasion += 3

#option loop#
def options_menu(inventory):
	inside_menu = True
	while inside_menu:
		clock.tick(fps)

		screen.fill((160,82,45))
		draw_text(f'INVENTORY', font_heading, yellow, (screen_width / 2) - 80, 10)
		draw_items(inventory)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_menu = False
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					inside_menu = False

		pygame.display.update()

#-------------------------------------------------------------------#

def shop(inventory, hero, shop_click):
	rest = draw_text(f'REST: ' + str(math.floor((hero.gold / 2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))), font, yellow, 20, screen_height - bottom_panel + 40)
	rest_rect = pygame.rect.Rect(20, screen_height - bottom_panel + 40, 64, 64)
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	if shop_click == True and hero.gold >= math.floor((hero.gold / 2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))  and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
		hero.gold -= math.floor((hero.gold / 2) + ((hero.max_hp - hero.hp) * 5) + ((hero.max_mp - hero.mp) * 5))
		hp_heal_amount = hero.max_hp - hero.hp
		mp_heal_amount = hero.max_mp - hero.mp
		hero.hp += hp_heal_amount
		hero.mp += mp_heal_amount
	if 4 not in inventory:
		screen.blit(items['eye_of_vladimir']['image'], (0, 50))
	if 5 not in inventory:
		screen.blit(items['condensed_lightning']['image'], (80, 50))
	if 6 not in inventory:
		screen.blit(items['shield']['image'], (160, 50))	
	for names in shop_names_list:
		if items[names]['shop_hitbox'].collidepoint((mousex,mousey)):
			screen.blit(font.render('NAME:' + items[names]['name'], True, blue), (mousex, mousey - 40))
			screen.blit(font.render('DESC:' + items[names]['description'], True, blue), (mousex, mousey - 20))	
			screen.blit(font.render('COST:' + str(items[names]['cost']), True, blue), (mousex, mousey))	

			if shop_click == True and hero.gold >= 1000 and items['eye_of_vladimir']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= 1000
				inventory.append(4)
				shop_names_list.remove('eye_of_vladimir')
				shop_click = False
			if shop_click == True and hero.gold >= 1000 and items['condensed_lightning']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= 1000
				inventory.append(5)
				hero.intelligence += 5
				shop_names_list.remove('condensed_lightning')
				shop_click = False
			if shop_click == True and hero.gold >= 1000 and items['shield']['shop_hitbox'].collidepoint((mousex,mousey)):
				hero.gold -= 1000
				inventory.append(6)
				shop_names_list.remove('shield')
				shop_click = False

			return shop_click

def shop_menu(inventory, hero):
	inside_shop = True
	shop_click = False
	while inside_shop:
		clock.tick(fps)

		screen.fill((160,82,45))
		draw_text(f'SHOP', font_heading, yellow, (screen_width / 2) - 40, 10)
		draw_text(f'GOLD: {hero.gold}', font, yellow, 20, screen_height - bottom_panel + 20)
		shop(inventory, hero, shop_click)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_shop = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				shop_click = True
				shop_click = shop(inventory, hero, shop_click)	

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					inside_shop = False

		
		pygame.display.update()	
