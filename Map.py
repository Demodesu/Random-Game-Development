import pygame, sys, csv, random, math

clock = pygame.time.Clock()

pygame.init()

game_map = 0
spawn_point_index = 1

#playformer loop
def platformer_menu(monster_index, hero):

	global game_map
	global spawn_point_index
	monster_index = 0

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
		screen_color_tuple = (173,216,230)
		with open('Maps/map_1.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 1:
		screen_color_tuple = (173,216,230)
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
		screen_color_tuple = (173,216,230)
		with open('Maps/map_4.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))
	if game_map == 4:
		screen_color_tuple = (173,216,230)
		with open('Maps/map_5.csv', 'r') as data:
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

	def spawn_monster():
		roll_spawn = random.randint(0,100)
		spawn_list = []
		spawn_list.append('slime')
		if roll_spawn > 60:
			spawn_list.append('zombie_boss')
		else:
			spawn_list.append('zombie')
		if 'zombie' not in spawn_list:
			roll_spawn = random.randint(0,100)
			if roll_spawn > 50:
				spawn_list.append('zombie')

		return spawn_list

	#----------------------load images----------------------#
	#hero
	player_image = pygame.image.load('Maps/Tiles0.png').convert_alpha()
	#slime
	slime_image = pygame.image.load('Maps/Tiles4.png').convert_alpha()
	slime_image = pygame.transform.scale(slime_image, (32, 32))
	spawn_right = False
	spawn_left = False
	start_pos_dictonary_right = {'0': {'x': 50, 'y': 200}, '1': {'x': 50, 'y': 300}, '2': {'x': 50, 'y': 400}, '3': {'x': 50, 'y': 300}, '4': {'x': 50, 'y': 100}}
	start_pos_dictonary_left = {'0': {'x': 700, 'y': 300}, '1': {'x': 700, 'y': 300}, '2': {'x': 700, 'y': 450}, '3': {'x': 700, 'y': 300}, '4': {'x': 700, 'y': 450}}

	#zombie
	zombie_image = pygame.image.load('Maps/Tiles5.png').convert_alpha()
	zombie_image = pygame.transform.scale(zombie_image, (80, 80))
	#zombie boss
	zombie_boss_image = pygame.image.load('Maps/Tiles6.png').convert_alpha()
	zombie_boss_image = pygame.transform.scale(zombie_boss_image, (80, 80))
	#--------------------------rects-------------------------#
	#hero
	if spawn_point_index == 1:
		player_rect = pygame.Rect(start_pos_dictonary_right[str(game_map)]['x'], start_pos_dictonary_right[str(game_map)]['y'], player_image.get_width() - 15, player_image.get_height())
	else:
		player_rect = pygame.Rect(start_pos_dictonary_left[str(game_map)]['x'], start_pos_dictonary_left[str(game_map)]['y'], player_image.get_width() - 15, player_image.get_height())		
	#slime
	slime_x, slime_y = random.randint(0, 700), -50
	#zombie
	zombie_x, zombie_y = random.randint(0, 700), -50
	#zombie boss
	zombie_boss_x, zombie_boss_y = random.randint(0, 800), random.randint(0, 550)
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
		if player_rect.y > screen_height:
			hero.hp -= hero.max_hp / 2
			if hero.hp < 0:
				hero.hp = 0
				hero.alive = False
				hero.death()
			running = False

		#hero collision
		player_rect, player_collisions = move(player_rect, player_movement, tile_rects)
		if player_collisions['bottom']:
			player_y_momentum = 0
			air_timer = 0
		else:
			air_timer += 1
		if player_collisions['top']:
			player_y_momentum += 1

		if player_rect.x > screen_width - player_rect.width:
			game_map += 1
			if game_map > 4:
				game_map = 0
			spawn_point_index = 1
			running = False
			monster_index = random.randint(0,2)
			return monster_index

		if player_rect.x < 1:
			game_map -= 1
			if game_map < 0:
				game_map = 4	
			spawn_point_index = -1
			running = False
			monster_index = random.randint(0,2)
			return monster_index

		#monster movement
		if 'slime' in spawn_list:
			slime = Slime_Movement(slime_image, 32, 32)
			slime_rect = pygame.Rect(slime_x, slime_y, 32, 32)
			slime_x, slime_y = slime.move(slime_x, slime_y, player_rect, tile_rects, slime_rect)
			slime.draw(slime_rect, tile_rects)
		else:
			slime_rect = pygame.Rect(-50, -50, 1, 1)

		if 'zombie' in spawn_list:
			zombie = Zombie_Movement(zombie_image, 32, 32)
			zombie_rect = pygame.Rect(zombie_x, zombie_y, 32, 32)
			zombie_x, zombie_y = zombie.move(zombie_x, zombie_y, player_rect, tile_rects, zombie_rect)
			zombie.draw(zombie_rect, tile_rects)
		else:
			zombie_rect = pygame.Rect(-50, -50, 1, 1)

		if 'zombie_boss' in spawn_list:
			zombie_boss = Zombie_Boss_Movement(zombie_boss_image, 32, 32)
			zombie_boss_rect = pygame.Rect(zombie_boss_x, zombie_boss_y, 32, 32)
			zombie_boss_x, zombie_boss_y = zombie_boss.move(zombie_boss_x, zombie_boss_y, player_rect, tile_rects, zombie_boss_rect)
			zombie_boss.draw(zombie_boss_rect, tile_rects)
		else:
			zombie_boss_rect = pygame.Rect(-50, -50, 1, 1)

		#hero drawing
		display.blit(player_image, (player_rect.x, player_rect.y))

		#collision encounter fading
		if pygame.Rect.colliderect(player_rect, slime_rect) or pygame.Rect.colliderect(player_rect, zombie_rect) or pygame.Rect.colliderect(player_rect, zombie_boss_rect):
			if screen_color_list[0] != 0:
				screen_color_list[0] -= 5
				if screen_color_list[0] < 0:
					screen_color_list[0] = 0
			if screen_color_list[1] != 0:
				screen_color_list[1] -= 5
				if screen_color_list[1] < 0:
					screen_color_list[1] = 0
			if screen_color_list[2] != 0:
				screen_color_list[2] -= 5
				if screen_color_list[2] < 0:
					screen_color_list[2] = 0
			screen_color_tuple = tuple(screen_color_list)
			if screen_color_tuple == (0,0,0):
				if pygame.Rect.colliderect(player_rect, slime_rect):
					monster_index = 0
				if pygame.Rect.colliderect(player_rect, zombie_rect):
					monster_index = 1
				if pygame.Rect.colliderect(player_rect, zombie_boss_rect):
					monster_index = 2
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
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					moving_right = False
				if event.key == pygame.K_a:
					moving_left = False		
					player_image = pygame.transform.flip(player_image, True, False)
		surf = pygame.transform.scale(display, screen_dimension)
		screen.blit(surf, (0, 0))
		#pygame.draw.rect(screen,(255,0,0),zombie_rect,2) 
		pygame.display.update() # update display
		clock.tick(60)

	if running == False:
		return monster_index