import pygame, sys, csv, random, math, Screen_Menus, Consumables, ctypes

clock = pygame.time.Clock()

pygame.init()

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

orange = (255,140,0)
red = (255,0,0)
brown = (48,24,0)
gold = (255,215,0)
darker_orange = (254,110,0)
fire_brick = (178,34,34)
crimson = (220,20,60)
#-------------------------------------------------------------------------------------#
def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

tile_width, tile_height = math.ceil(user32.GetSystemMetrics(0) * 0.03125), math.ceil(user32.GetSystemMetrics(1) * 0.055)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
display = pygame.Surface((screen_width,screen_height))

game_map = 2
monster_encounter = False
current_map_list = []
current_pos_list = []
stage = 0
stage_major = 0

inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(width(0.035),height(0.035)))

#load tiles and map
tile_list = []
for i in range(3):
	img = pygame.image.load(f'Maps/Tiles{i}.png').convert_alpha()
	img = pygame.transform.scale(img, (tile_width,tile_height))
	tile_list.append(img)

ambient_sound_effect = pygame.mixer.Sound(f'Music/Zombie/Zombie_Ambient.mp3')
ambient_sound_effect.set_volume(0.1)

#playformer loop
def platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, experiencethreshold, game_variables):
	all_sounds_to_stop_playing = [hero.running_sound_effect]
	for sounds in all_sounds_to_stop_playing:
		sounds.stop()

	pygame.mixer.music.fadeout(500)
	pygame.mixer.music.load('Music/Forest_Theme.mp3')
	pygame.mixer.music.set_volume(0.3)
	pygame.mixer.music.play(-1)

	global game_map
	global current_map_list
	global current_pos_list
	global stage
	global stage_major
	monster_index = 0
	monster_encounter = False

	game_map_list = []
	if game_map == 0:
		screen_color_tuple = (0,50,0)
		with open('Maps/map0.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))

	if game_map == 1:
		screen_color_tuple = (0,50,0)
		with open('Maps/map1.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))

	if game_map == 2:
		screen_color_tuple = (0,50,0)
		with open('Maps/map2.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))

	if game_map == 3:
		screen_color_tuple = (0,50,0)
		with open('Maps/map3.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))

	if game_map == 4:
		screen_color_tuple = (0,50,0)
		with open('Maps/map4.csv', 'r') as data:
			data = csv.reader(data, delimiter = ',')
			for row in data:
				game_map_list.append(list(row))

	active_stage_list = [1,3,0]

	current_map_list.append(game_map)

	#movement
	moving_right = False
	moving_left = False

	player_y_momentum = 0
	air_timer = 0

	screen_color_list = list(screen_color_tuple)

	#function for drawing tiles on map
	def draw_tiles():
		y = 0
		for row in game_map_list:
		    x = 0
		    for tile in row:
		        if tile == '0':
		            display.blit(tile_list[0], (x * tile_width, y * tile_height))
		        if tile == '1':
		            display.blit(tile_list[1], (x * tile_width, y * tile_height))
		        if tile == '2':
		            display.blit(tile_list[2], (x * tile_width, y * tile_height))
		        if tile != '-1':
		            tile_rects.append(pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height))
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

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - monster_rect.width * 0.5, monster_rect.y - monster_rect.height))

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
			display.blit(self.monster_image, (monster_rect.x - monster_rect.width * 0.5, monster_rect.y - monster_rect.height))

	class Swift_Zombie_Movement(Monster_Movement):
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
				monster_y += 7	
			else:
				if len(hit_list) >= 3:
					monster_y -= tile.height
					monster_x += 0
				else:
					monster_x += dx * 5

			return monster_x, monster_y

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - monster_rect.width * 0.5, monster_rect.y - monster_rect.height))

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
			display.blit(self.monster_image, (monster_rect.x - monster_rect.width * 0.5, monster_rect.y - monster_rect.height))

	class Golem_Boss_Movement(Monster_Movement):
		def __init__(self, monster_image, width, height):
			super().__init__(monster_image, width, height)

		def draw(self, monster_rect, tile_rects):
			display.blit(self.monster_image, (monster_rect.x - monster_rect.width * 0.3, monster_rect.y - monster_rect.height * 0.4))

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
		if random.randint(0,100) > 50 and game_map != 2:
			spawn_list.append('slime')
		if game_map != 2:
			if random.randint(0,100) > 50:
				spawn_list.append('zombie')
			else:
				spawn_list.append('swift_zombie')	
		if game_map == 4:
			spawn_list.append('zombie_boss')
		if game_map == 4:
			spawn_list.append('golem_boss')

		#chest spawn
		roll_spawn = random.randint(0,100) + hero.luck
		if len(current_map_list) > 1 and roll_spawn > 60:
			if current_map_list[-1] != current_map_list[0]:
				spawn_list.append('chest')
		if len(current_map_list) == 2:
			del current_map_list[0]

		if 'chest' not in spawn_list and stage == 4:
			spawn_list.append('chest')

		return spawn_list

	#----------------------load images----------------------#
	#hero
	player_image = pygame.image.load('Maps/Hero.png').convert_alpha()
	player_image = pygame.transform.scale(player_image,(width(0.05),height(0.05)))
	spawn_right = False
	start_pos_dictonary_right = {'0': {'x': screen_width * 0.05, 'y': screen_height * 0.62}, '1': {'x': screen_width * 0.05, 'y': screen_height * 0.58}, '2': {'x': screen_width * 0.05, 'y': screen_height * 0.58}, '3': {'x': screen_width * 0.05, 'y': screen_height * 0.72}, '4': {'x': screen_width * 0.05, 'y': screen_height * 0.6}}
	#slime
	slime_image = pygame.image.load('Maps/Slime.png').convert_alpha()
	slime_image = pygame.transform.scale(slime_image,(width(0.05),height(0.05)))
	#zombie
	zombie_image = pygame.image.load('Maps/Zombie.png').convert_alpha()
	zombie_image = pygame.transform.scale(zombie_image,(width(0.05),height(0.05)))
	#swift zombie
	swift_zombie_image = pygame.image.load('Maps/SwiftZombie.png').convert_alpha()
	swift_zombie_image = pygame.transform.scale(swift_zombie_image,(width(0.05),height(0.05)))	
	#zombie boss
	zombie_boss_image = pygame.image.load('Maps/ZombieBoss.png').convert_alpha()
	zombie_boss_image = pygame.transform.scale(zombie_boss_image,(width(0.0575),height(0.0575)))
	#golem boss
	golem_boss_image = pygame.image.load('Maps/Golem.png').convert_alpha()
	golem_boss_image = pygame.transform.scale(golem_boss_image,(width(0.1),height(0.1)))
	golem_boss_image = pygame.transform.flip(golem_boss_image, True, False)
	#shop
	shop_image = pygame.image.load('Maps/Shop.png').convert_alpha()
	shop_image = pygame.transform.scale(shop_image, (150,100))
	#chest
	chest_image = pygame.image.load('Maps/Chest.png').convert_alpha()
	#--------------------------rects-------------------------#
	#hero
	if len(current_pos_list) != 0:
		player_rect = pygame.Rect(current_pos_list[0], current_pos_list[-1], width(0.025), height(0.0276))
		current_pos_list.clear()
	else:
		player_rect = pygame.Rect(start_pos_dictonary_right[str(game_map)]['x'], start_pos_dictonary_right[str(game_map)]['y'], width(0.025), height(0.0276))
	if game_map != 3:
		#slime
		slime_x, slime_y = random.randint(width_position(0.2), width_position(0.8)), -50
		#zombie
		zombie_x, zombie_y = random.randint(width_position(0.2), width_position(0.8)), -50
		#swift zombie
		swift_zombie_x, swift_zombie_y = random.randint(width_position(0.2), width_position(0.8)), -50
		#zombie boss
		zombie_boss_x, zombie_boss_y = random.randint(width_position(0.2), width_position(0.8)), random.randint(0, 250)
		#golem boss
		golem_boss_x, golem_boss_y = width_position(0.8), height_position(0.51)
	else:
		slime_x, slime_y = random.randint(width_position(0.2), width_position(0.3)), -50
		#zombie
		zombie_x, zombie_y = random.randint(width_position(0.2), width_position(0.3)), -50
		#swift zombie
		swift_zombie_x, swift_zombie_y = random.randint(width_position(0.2), width_position(0.3)), -50
		#zombie boss
		zombie_boss_x, zombie_boss_y = random.randint(width_position(0.2), width_position(0.8)), random.randint(0, 250)
		#golem boss
		golem_boss_x, golem_boss_y = width_position(0.8), height_position(0.51)

	chest_x, chest_y = 	screen_width * 0.7, screen_height * 0.242
	#--------------------------------------------------------#	
	turn_left = False
	spawn_list = spawn_monster()

	ambient_sound_effect_cooldown = random.randint(600,800)

	running = True
	while running:

		if ambient_sound_effect_cooldown > 0:
			ambient_sound_effect_cooldown -= 1
			if ambient_sound_effect_cooldown == 0:
				ambient_sound_effect.play()
				ambient_sound_effect_cooldown = random.randint(600,800)

		display.fill(screen_color_tuple)	

		tile_rects = []
		draw_tiles()

		if player_rect.y > screen_height:
			hero.hp -= hero.max_hp * 0.25
			player_rect.x = start_pos_dictonary_right[str(game_map)]['x']
			player_rect.y = start_pos_dictonary_right[str(game_map)]['y']

		#hero movement
		player_movement = [0, 0]
		if moving_right and player_rect.x < screen_width - player_rect.width:
			player_movement[0] += screen_width * 0.00275
		if moving_left and player_rect.x > 0:
			player_movement[0] -= screen_width * 0.00275
		player_movement[1] += player_y_momentum
		player_y_momentum += screen_height * 0.0005
		if player_y_momentum > screen_height * 0.01:
			player_y_momentum = screen_height * 0.01

		#hero collision
		player_rect, player_collisions = move(player_rect, player_movement, tile_rects)
		if player_collisions['bottom']:
			player_y_momentum = 0
			air_timer = 0
		else:
			air_timer += 1
		if player_collisions['top']:
			player_y_momentum += 1

		if player_rect.x > screen_width - player_rect.width - screen_width * 0.005:
			stage += 1
			if stage % 4 == 0:
				game_map = 2
			elif stage % 5 == 0:
				game_map = 4	
			else:
				random_stage = random.randint(0,2)
				game_map = active_stage_list[random_stage]
			if -18 not in inventory:
				hero.gold += 250
			else:
				hero.gold += 450
			running = False
			while True:
				monster_index_list = [0,1,3,5]
				monster_index = monster_index_list[random.randint(0,3)]
				if monster_index != 2:
					break
			monster_encounter = False
			return monster_index, monster_encounter, game_map

		#monster movement
		if 'slime' in spawn_list and game_map != 5:
			slime = Slime_Movement(slime_image, width(0.025), height(0.025))
			slime_rect = pygame.Rect(slime_x, slime_y, width(0.025), height(0.025))
			slime_x, slime_y = slime.move(slime_x, slime_y, player_rect, tile_rects, slime_rect)
			slime.draw(slime_rect, tile_rects)
		else:
			slime_rect = pygame.Rect(-50, -50, 1, 1)

		if 'zombie' in spawn_list and game_map != 5:
			zombie = Zombie_Movement(zombie_image, width(0.025), height(0.025))
			zombie_rect = pygame.Rect(zombie_x, zombie_y, width(0.025), height(0.025))
			zombie_x, zombie_y = zombie.move(zombie_x, zombie_y, player_rect, tile_rects, zombie_rect)
			zombie.draw(zombie_rect, tile_rects)
		else:
			zombie_rect = pygame.Rect(-50, -50, 0, 0)

		if 'swift_zombie' in spawn_list and game_map != 5:
			swift_zombie = Swift_Zombie_Movement(swift_zombie_image, width(0.025), height(0.025))
			swift_zombie_rect = pygame.Rect(swift_zombie_x, swift_zombie_y, width(0.025), height(0.025))
			swift_zombie_x, swift_zombie_y = swift_zombie.move(swift_zombie_x, swift_zombie_y, player_rect, tile_rects, swift_zombie_rect)
			swift_zombie.draw(swift_zombie_rect, tile_rects)
		else:
			swift_zombie_rect = pygame.Rect(-50, -50, 0, 0)

		if 'zombie_boss' in spawn_list and game_map != 5 and len(boss_defeated_list) == 0:
			zombie_boss = Zombie_Boss_Movement(zombie_boss_image, width(0.025), height(0.025))
			zombie_boss_rect = pygame.Rect(zombie_boss_x, zombie_boss_y, width(0.025), height(0.025))
			zombie_boss_x, zombie_boss_y = zombie_boss.move(zombie_boss_x, zombie_boss_y, player_rect, tile_rects, zombie_boss_rect)
			zombie_boss.draw(zombie_boss_rect, tile_rects)
		else:
			zombie_boss_rect = pygame.Rect(-50, -50, 0, 0)

		if 'golem_boss' in spawn_list and game_map != 5 and len(boss_defeated_list) == 1: 
			golem_boss = Golem_Boss_Movement(golem_boss_image, width(0.07), height(0.07))
			golem_boss_rect = pygame.Rect(golem_boss_x, golem_boss_y, width(0.07), height(0.07))
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
		display.blit(player_image, (player_rect.x - player_rect.width * 0.6, player_rect.y - player_rect.height * 0.8))

		if pygame.Rect.colliderect(player_rect, chest_rect):
			hero.gold += 500 + (hero.level * 2)
			spawn_list.remove('chest')

		#collision encounter fading
		if pygame.Rect.colliderect(player_rect, slime_rect) or pygame.Rect.colliderect(player_rect, zombie_rect) or pygame.Rect.colliderect(player_rect, zombie_boss_rect) or pygame.Rect.colliderect(player_rect, golem_boss_rect) or pygame.Rect.colliderect(player_rect, swift_zombie_rect):
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
				monster_collision_dictionary = {'slime': slime_rect, 'zombie': zombie_rect, 'zombie_boss': zombie_boss_rect, 'golem_boss': golem_boss_rect, 'swift_zombie': swift_zombie_rect}
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
				if pygame.Rect.colliderect(player_rect, monster_collision_dictionary['swift_zombie']):
					monster_index = 5

					current_pos_list.append(swift_zombie_x)
					current_pos_list.append(swift_zombie_y)					

					monster_encounter = True
					running = False											

		#check for events
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				pygame.quit() 
				sys.exit() 
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					Screen_Menus.option_menu(hero, game_variables)

				if event.key == pygame.K_d:
					moving_right = True
					turn_right = True
				if event.key == pygame.K_a:
					moving_left = True
					player_image = pygame.transform.flip(player_image, True, False)
				if event.key == pygame.K_w:
					if air_timer < 6:
						player_y_momentum -= screen_height * 0.015
				if event.key == pygame.K_s:
					player_y_momentum += screen_height * 0.01
				if event.key == pygame.K_c and game_map == 2:
					Screen_Menus.shop_menu(inventory, hero, monster_list, monster_index)	

				if event.key == pygame.K_x:
					Consumables.consumable_menu(hero, inventory, monster_list, monster_index)

				if event.key == pygame.K_z:
					Screen_Menus.inventory_menu(inventory, monster_list, monster_index, hero)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					moving_right = False
				if event.key == pygame.K_a:
					moving_left = False		
					player_image = pygame.transform.flip(player_image, True, False)

			if event.type == pygame.MOUSEBUTTONDOWN:
				inventory_click = True
				mousex, mousey = pygame.mouse.get_pos()

		surf = pygame.transform.scale(display, (screen_width, screen_height))
		screen.blit(surf, (0, 0))
		
		draw_text_middle('STAGE ' + f'{stage}({stage_major})', font, red, screen_width, screen_height * 0.01)

		if game_map == 2:
			screen.blit(shop_image, (screen_width * 0.43, screen_height * 0.242))
		# pygame.draw.rect(screen,(255,0,0),slime_rect,2) 
		# pygame.draw.rect(screen,(255,0,0),zombie_rect,2) 
		# pygame.draw.rect(screen,(255,0,0),golem_boss_rect,2) 
		# pygame.draw.rect(screen,(255,0,0),zombie_boss_rect,2) 
		# pygame.draw.rect(screen,(255,0,0),swift_zombie_rect,2) 		
		pygame.display.update() # update display
		clock.tick(60)

	if running == False:
		return monster_index, monster_encounter, game_map
#print