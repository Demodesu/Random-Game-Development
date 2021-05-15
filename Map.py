import pygame, sys, csv, random, math, Screen_Menus, Consumables

clock = pygame.time.Clock()

pygame.init()

game_map = 5
spawn_point_index = 1
monster_encounter = False
current_map_list = []
current_pos_list = []

inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(44,44))

#playformer loop
def platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, skills_list, active_skills_list, all_active_skills_list):

	global game_map
	global spawn_point_index
	global current_map_list
	global current_pos_list

	monster_index = 0
	monster_encounter = False

	current_map_list.append(game_map)

	#all screen elements
	screen_width = 800
	screen_height = 550
	screen_dimension = (screen_width, screen_height)
	screen = pygame.display.set_mode(screen_dimension,0,32)

	display = pygame.Surface((800,550))

	#movement
	moving_right = False
	moving_left = False

	player_y_momentum = 0
	air_timer = 0

	#load tiles and map
	tile_list = []
	for i in range(5):
		img = pygame.image.load(f'Maps/Tiles{i}.png')
		tile_list.append(img)

	game_map_list = []
	if game_map == 0:
		screen_color_tuple = (0,50,0)
		with open('Maps/map_1.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 1:
		screen_color_tuple = (0,50,0)
		with open('Maps/map_2.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 2:
		screen_color_tuple = (43,45,47)
		with open('Maps/map_3.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 3:
		screen_color_tuple = (0,50,0)
		with open('Maps/map_4.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 4:
		screen_color_tuple = (0,50,0) 
		with open('Maps/map_5.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 5:
		screen_color_tuple = (50,70,20)
		with open('Maps/map_6.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))


	screen_color_list = list(screen_color_tuple)

	tile_size = 50

	#function for drawing tiles on map
	def draw_tiles():
		y = 0
		for row in game_map_list:
		    x = 0
		    for tile in row:
		        if tile == '0':
		            display.blit(tile_list[1], (x * tile_size, y * tile_size))
		        if tile == '1':
		            display.blit(tile_list[2], (x * tile_size, y * tile_size))
		        if tile == '2':
		            display.blit(tile_list[3], (x * tile_size, y * tile_size))
		        if tile != '-1':
		            tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
		        x += 1
		    y += 1

	#collision testing 
	def collision_test(rect, tiles):
	    hit_list = []
	    for tile in tiles:
	        if rect.colliderect(tile):
	            hit_list.append(tile)
	    return hit_list

	#movement for character
	def move(rect, movement, tiles):
		collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
		rect.x += movement[0]
		hit_list = collision_test(rect, tiles)
		for tile in hit_list:
			if movement[0] > 0:
		   		rect.right = tile.left
		   		collision_types['right'] = True
			elif movement[0] < 0:
		   		rect.left = tile.right
		   		collision_types['left'] = True
		rect.y += movement[1]
		hit_list = collision_test(rect, tiles)
		for tile in hit_list:
			if movement[1] > 0:
		   		rect.bottom = tile.top
		   		collision_types['bottom'] = True
			elif movement[1] < 0:
		   		rect.top = tile.bottom
		   		collision_types['top'] = True
		return rect, collision_types	

	#movement for monsters
	class Monster_Movement():
		def __init__(self, monster_image, width, height):
			self.monster_image = monster_image
			self.width = width
			self.height = height

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x, monster_rect.y))

	class Slime_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def move(self, monster_x, monster_y, player_rect, tile_rects, monster_rect):
			radians = math.atan2(player_rect.y - monster_y, player_rect.x - monster_x)
			distance = math.hypot(player_rect.y - monster_y, player_rect.x - monster_x)
			dx, dy = math.cos(radians), math.sin(radians)

			hit_list = []
			for tile in tile_rects:
				if monster_rect.colliderect(tile):
					hit_list.append(tile)
			for tile in hit_list:
				monster_rect.bottom = tile.top
			if monster_rect.bottom != tile.top:
				monster_y += 5	
			else:
				if len(hit_list) >= 3:
					monster_y -= tile.height
					monster_x += 0
				else:
					if 390 < distance < 410:
						monster_x += 0
					elif distance > 400:
						monster_x += dx 
					else:
						monster_x -= dx * 3

			return monster_x, monster_y

	class Zombie_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def move(self, monster_x, monster_y, player_rect, tile_rects, monster_rect):
			radians = math.atan2(player_rect.y - monster_y, player_rect.x - monster_x)
			distance = math.hypot(player_rect.y - monster_y, player_rect.x - monster_x)
			dx, dy = math.cos(radians), math.sin(radians)

			hit_list = []
			for tile in tile_rects:
				if monster_rect.colliderect(tile):
					hit_list.append(tile)
			for tile in hit_list:
				monster_rect.bottom = tile.top
			if monster_rect.bottom != tile.top:
				monster_y += 5	
			else:
				if len(hit_list) >= 3:
					monster_y -= tile.height
					monster_x += 0
				else:
					monster_x += dx * 2

			return monster_x, monster_y

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - 20, monster_rect.y - 50))

	class Zombie_Boss_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def move(self, monster_x, monster_y, player_rect, tile_rects, monster_rect):
			radians = math.atan2(player_rect.y - monster_y, player_rect.x - monster_x)
			distance = math.hypot(player_rect.y - monster_y, player_rect.x - monster_x)
			dx, dy = math.cos(radians), math.sin(radians)

			monster_x += dx
			monster_y += dy

			return monster_x, monster_y

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - 20, monster_rect.y - 50))

	class Golem_Boss_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - 40, monster_rect.y - 50))

	class Chest_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def move(self, monster_x, monster_y, player_rect, tile_rects, monster_rect):
			hit_list = []
			for tile in tile_rects:
				if monster_rect.colliderect(tile):
					hit_list.append(tile)
			for tile in hit_list:
				monster_rect.bottom = tile.top
			if monster_rect.bottom != tile.top:
				monster_y += 10	

			return monster_x, monster_y

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x, monster_rect.y))

	def spawn_monster():
		global current_map_list

		spawn_list = []

		#monster spawn
		roll_spawn = random.randint(0,100)
		if roll_spawn > 85:
			spawn_list.append('slime')
		roll_spawn = random.randint(0,100)	
		if game_map == 2:
			spawn_list.append('zombie_boss')
		if game_map == 2:
			spawn_list.append('golem_boss')
		if roll_spawn > 90:
			spawn_list.append('zombie')

		#chest spawn
		roll_spawn = random.randint(0,100) + hero.luck
		if len(current_map_list) > 1 and roll_spawn > 50:
			if current_map_list[-1] != current_map_list[0] and current_map_list[-1] != current_map_list[1]:
				spawn_list.append('chest')
		if len(current_map_list) == 3:
			del current_map_list[0]

		return spawn_list

	#----------------------load images----------------------#
	#hero
	player_image = pygame.image.load('Maps/Tiles0.png').convert_alpha()
	spawn_right = False
	spawn_left = False
	start_pos_dictonary_right = {'0': {'x': 50, 'y': 200}, '1': {'x': 50, 'y': 300}, '2': {'x': 50, 'y': 400}, '3': {'x': 50, 'y': 300}, '4': {'x': 50, 'y': 100}, '5': {'x': 50, 'y': 200}}
	start_pos_dictonary_left = {'0': {'x': 700, 'y': 300}, '1': {'x': 700, 'y': 300}, '2': {'x': 700, 'y': 450}, '3': {'x': 700, 'y': 300}, '4': {'x': 700, 'y': 450}, '5': {'x': 700, 'y': 200}}
	#slime
	slime_image = pygame.image.load('Maps/Tiles4.png').convert_alpha()
	slime_image = pygame.transform.scale(slime_image, (32, 32))
	#zombie
	zombie_image = pygame.image.load('Maps/Tiles5.png').convert_alpha()
	zombie_image = pygame.transform.scale(zombie_image, (80, 80))
	#zombie boss
	zombie_boss_image = pygame.image.load('Maps/Tiles6.png').convert_alpha()
	zombie_boss_image = pygame.transform.scale(zombie_boss_image, (80, 80))
	#golem boss
	golem_boss_image = pygame.image.load('Maps/Tiles7.png').convert_alpha()
	golem_boss_image = pygame.transform.scale(golem_boss_image, (160, 160))
	golem_boss_image = pygame.transform.flip(golem_boss_image, True, False)
	#shop
	shop_image = pygame.image.load('Maps/Shop.png').convert_alpha()
	shop_image = pygame.transform.scale(shop_image, (150,100))
	#chest
	chest_image = pygame.image.load('Maps/Chest.png').convert_alpha()
	#--------------------------rects-------------------------#
	#hero
	if spawn_point_index == 1:
		if len(current_pos_list) != 0:
			player_rect = pygame.Rect(current_pos_list[0], current_pos_list[-1], player_image.get_width() - 15, player_image.get_height())
			current_pos_list.clear()
		else:
			player_rect = pygame.Rect(start_pos_dictonary_right[str(game_map)]['x'], start_pos_dictonary_right[str(game_map)]['y'], player_image.get_width() - 15, player_image.get_height())
	else:
		if len(current_pos_list) != 0:
			player_rect = pygame.Rect(current_pos_list[0], current_pos_list[-1], player_image.get_width() - 15, player_image.get_height())
			current_pos_list.clear()
		else:
			player_rect = pygame.Rect(start_pos_dictonary_left[str(game_map)]['x'], start_pos_dictonary_left[str(game_map)]['y'], player_image.get_width() - 15, player_image.get_height())	
	#slime
	slime_x, slime_y = random.randint(0, 700), -50
	#zombie
	zombie_x, zombie_y = random.randint(0, 700), -50
	#zombie boss
	zombie_boss_x, zombie_boss_y = random.randint(300, 500), random.randint(0, 250)
	#golem boss
	golem_boss_x, golem_boss_y = 600, 150
	#chest
	chest_x, chest_y = random.randint(200, 600), -50
	#--------------------------------------------------------#	
	turn_left = False
	spawn_list = spawn_monster()

	running = True
	while running:

		display.fill(screen_color_tuple)	

		tile_rects = []
		draw_tiles()

		#hero movement
		player_movement = [0, 0]
		if moving_right and player_rect.x < screen_width - player_rect.width:
			player_movement[0] += 4 
		if moving_left and player_rect.x > 0:
			player_movement[0] -= 4
		player_movement[1] += player_y_momentum
		player_y_momentum += 0.2
		if player_rect.y < 0 :
			player_y_momentum += 0.2
		if player_y_momentum > 10:
			player_y_momentum = 10

		#hero collision
		player_rect, player_collisions = move(player_rect, player_movement, tile_rects)
		if player_collisions['bottom']:
			player_y_momentum = 0
			air_timer = 0
		else:
			air_timer += 1
		if player_collisions['top']:
			player_y_momentum += 1

		if player_rect.x > screen_width - player_rect.width - 5:
			game_map += 1
			if game_map > 5:
				game_map = 0
			spawn_point_index = 1
			running = False
			while True:
				monster_index = random.randint(0,3)
				if monster_index != 2:
					break
			monster_encounter = False
			return monster_index, monster_encounter, game_map

		if player_rect.x < 1:
			game_map -= 1
			if game_map < 0:
				game_map = 5	
			spawn_point_index = -1
			running = False
			while True:
				monster_index = random.randint(0,3)
				if monster_index != 2:
					break
			monster_encounter = False
			return monster_index, monster_encounter, game_map

		#monster movement
		if 'slime' in spawn_list and game_map != 5:
			slime = Slime_Movement(slime_image, 32, 32)
			slime_rect = pygame.Rect(slime_x, slime_y, 32, 32)
			slime_x, slime_y = slime.move(slime_x, slime_y, player_rect, tile_rects, slime_rect)
			slime.draw(slime_rect, tile_rects)
		else:
			slime_rect = pygame.Rect(-50, -50, 1, 1)

		if 'zombie' in spawn_list and game_map != 5:
			zombie = Zombie_Movement(zombie_image, 32, 32)
			zombie_rect = pygame.Rect(zombie_x, zombie_y, 32, 32)
			zombie_x, zombie_y = zombie.move(zombie_x, zombie_y, player_rect, tile_rects, zombie_rect)
			zombie.draw(zombie_rect, tile_rects)
		else:
			zombie_rect = pygame.Rect(-50, -50, 0, 0)

		if 'zombie_boss' in spawn_list and game_map != 5 and len(boss_defeated_list) == 0:
			zombie_boss = Zombie_Boss_Movement(zombie_boss_image, 32, 32)
			zombie_boss_rect = pygame.Rect(zombie_boss_x, zombie_boss_y, 32, 32)
			zombie_boss_x, zombie_boss_y = zombie_boss.move(zombie_boss_x, zombie_boss_y, player_rect, tile_rects, zombie_boss_rect)
			zombie_boss.draw(zombie_boss_rect, tile_rects)
		else:
			zombie_boss_rect = pygame.Rect(-50, -50, 0, 0)

		if 'golem_boss' in spawn_list and game_map != 5 and len(boss_defeated_list) == 1: 
			golem_boss = Golem_Boss_Movement(golem_boss_image, 110, 110)
			golem_boss_rect = pygame.Rect(golem_boss_x, golem_boss_y, 110, 110)
			golem_boss.draw(golem_boss_rect, tile_rects)
		else:
			golem_boss_rect = pygame.Rect(-50, -50, 0, 0)

		if 'chest' in spawn_list and game_map != 5:
			chest = Chest_Movement(chest_image, 50, 50)
			chest_rect = pygame.Rect(chest_x, chest_y, 50, 50)
			chest_x, chest_y = chest.move(chest_x, chest_y, player_rect, tile_rects, chest_rect)
			chest.draw(chest_rect, tile_rects)
		else:
			chest_rect = pygame.Rect(-50, -50, 0, 0)

		#hero drawing
		display.blit(player_image, (player_rect.x, player_rect.y))

		#collision encounter fading
		if pygame.Rect.colliderect(player_rect, slime_rect) or pygame.Rect.colliderect(player_rect, zombie_rect) or pygame.Rect.colliderect(player_rect, zombie_boss_rect) or pygame.Rect.colliderect(player_rect, chest_rect) or pygame.Rect.colliderect(player_rect, golem_boss_rect):
			if screen_color_list[0] != 0:
				screen_color_list[0] -= 2
				if screen_color_list[0] < 0:
					screen_color_list[0] = 0
			if screen_color_list[1] != 0:
				screen_color_list[1] -= 2
				if screen_color_list[1] < 0:
					screen_color_list[1] = 0
			if screen_color_list[2] != 0:
				screen_color_list[2] -= 2
				if screen_color_list[2] < 0:
					screen_color_list[2] = 0
			screen_color_tuple = tuple(screen_color_list)
			if screen_color_tuple == (0,0,0):
				monster_collision_dictionary = {'slime': slime_rect, 'zombie': zombie_rect, 'zombie_boss': zombie_boss_rect, 'golem_boss': golem_boss_rect}
				if pygame.Rect.colliderect(player_rect, monster_collision_dictionary['slime']):
					random_slime_and_zombie = random.randint(0,100)
					if random_slime_and_zombie > 50:
						monster_index = 3
					else:
						monster_index = 0

					current_pos_list.append(slime_x)
					current_pos_list.append(slime_y)	

					monster_encounter = True
					running = False
				if pygame.Rect.colliderect(player_rect, monster_collision_dictionary['zombie']):
					random_slime_and_zombie = random.randint(0,100)
					if random_slime_and_zombie > 50:
						monster_index = 3
					else:
						monster_index = 1

					current_pos_list.append(zombie_x)
					current_pos_list.append(zombie_y)	

					monster_encounter = True
					running = False
				if pygame.Rect.colliderect(player_rect, monster_collision_dictionary['zombie_boss']):
					monster_index = 2

					current_pos_list.append(zombie_boss_x)
					current_pos_list.append(zombie_boss_y)					

					monster_encounter = True
					running = False
				if pygame.Rect.colliderect(player_rect, monster_collision_dictionary['golem_boss']):
					monster_index = 4

					current_pos_list.append(golem_boss_x)
					current_pos_list.append(golem_boss_y)					

					monster_encounter = True
					running = False
				if pygame.Rect.colliderect(player_rect, chest_rect):
					monster_index = -1
					hero.gold += 500 + (hero.level * 2)
					roll_obtain_consumable_index = random.randint(0,1)
					if roll_obtain_consumable_index == 0:
						hero.fireball_charge += 1
					else:
						hero.lightning_charge += 1	

					current_pos_list.append(chest_x)
					current_pos_list.append(chest_y - 10)

					monster_encounter = True
					running = False							

		#check for events
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				pygame.quit() 
				sys.exit() 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					moving_right = True
					turn_right = True
				if event.key == pygame.K_a:
					moving_left = True
					player_image = pygame.transform.flip(player_image, True, False)
				if event.key == pygame.K_w:
					if air_timer < 6:
						player_y_momentum = -8
				if event.key == pygame.K_s:
					player_y_momentum = 4
				if event.key == pygame.K_c and game_map == 5:
					shop_rect = pygame.draw.rect(screen, (0,0,0), (screen_width / 2, (550 / 2) - 50 , 0, 0))
					shop_distance = math.hypot(player_rect.y - shop_rect.y, player_rect.x - shop_rect.x)
					if shop_distance < 160:
						Screen_Menus.shop_menu(inventory, hero, monster_list, monster_index)	

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					moving_right = False
				if event.key == pygame.K_a:
					moving_left = False		
					player_image = pygame.transform.flip(player_image, True, False)

			if event.type == pygame.MOUSEBUTTONDOWN:
				inventory_click = True
				mousex, mousey = pygame.mouse.get_pos()
				if inventory_button.collidepoint((mousex,mousey)):
					Screen_Menus.options_menu(inventory, monster_list, monster_index, hero, skills_list, active_skills_list, all_active_skills_list)

		surf = pygame.transform.scale(display, screen_dimension)
		screen.blit(surf, (0, 0))
		
		inventory_button = screen.blit(inventory_icon_img, (0,0))

		if game_map == 5:
			screen.blit(shop_image, ((screen_width / 2) - (150 / 2), 150))
		#pygame.draw.rect(screen,(255,0,0),zombie_rect,2) 
		pygame.display.update() # update display
		clock.tick(60)

	if running == False:
		return monster_index, monster_encounter, game_map

#print