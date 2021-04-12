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

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

#item name:{image:loadimage, description:decription, hitbox:hitbox, index:index, name:name}
items = {
'ring_of_health' : {'image' : pygame.image.load('Images/Icon/Relics/Relics0.png').convert_alpha(), 'description' : 'Max HP + 5', 'hitbox' : pygame.rect.Rect(0, 0, 64, 64), 'index' : 0, 'name' : 'Ring Of Health'},
'raptor_claw' : {'image' : pygame.image.load('Images/Icon/Relics/Relics1.png').convert_alpha(), 'description' : 'Strength + 5', 'hitbox' : pygame.rect.Rect(80, 0, 64, 64), 'index' : 1, 'name' : 'Raptor Claw'},
'four_leaf_clover' : {'image' : pygame.image.load('Images/Icon/Relics/Relics2.png').convert_alpha(), 'description' : 'Luck + 5', 'hitbox' : pygame.rect.Rect(160, 0, 64, 64), 'index' : 2, 'name' : 'Four Leaf Clover'},
'feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics3.png').convert_alpha(), 'description' : 'Evasion + 5', 'hitbox' : pygame.rect.Rect(240, 0, 64, 64), 'index' : 3, 'name' : 'Feather'},
}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather']

def draw_items(inventory):
	#draw the image
	for image in names_list:
		if items[image]['index'] in inventory:
			pygame.draw.rect(screen,(139,69,19),items[image]['hitbox'], 2)
			screen.blit(items[image]['image'], (items[image]['index'] * 80, 0))
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
		draw_items(inventory)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_menu = False
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					inside_menu = False

		pygame.display.update()

