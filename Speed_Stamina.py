import math, pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events, ctypes

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
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.35)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
black = (0,0,0)

def turn_calculations(boost, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group):

	class Stamina_Images(pygame.sprite.Sprite):
		def __init__(self, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.animation_list = []
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()	
			for i in range(2,6):
				img = pygame.image.load(f'Images/Icon/Heal/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
				self.animation_list.append(img)
			self.image = self.animation_list[self.frame_index]
			self.rect = self.image.get_rect()
			self.rect.center = (x,y)

		def update(self):
			#animation cooldown in milliseconds
			animation_cooldown = 100
			#handle animation
			#update image
			self.image = self.animation_list[self.frame_index]	
			#check if enough time has passes since last update
			if pygame.time.get_ticks() - self.update_time > animation_cooldown:
				self.update_time = pygame.time.get_ticks()
				self.frame_index += 1
			#if animation runs out reset to the start
			if self.frame_index >= len(self.animation_list):
				self.kill()

	class Speed_Bar():
		def __init__(self, screen, turn, max_bar, x, y, hitbox_width):
			self.x = x
			self.y = y
			self.turn = turn
			self.max_bar = max_bar
			self.hitbox_width = hitbox_width

		def draw(self):
			ratio = self.turn / self.max_bar
			pygame.draw.rect(screen, red, (self.x, self.y, self.hitbox_width, 10))
			pygame.draw.rect(screen, yellow, (self.x, self.y, self.hitbox_width * ratio, 10))			

	class Stamina_Bar():
		def __init__(self, screen, stamina, max_bar, x, y, hitbox_width):
			self.x = x
			self.y = y
			self.stamina = stamina
			self.max_bar = max_bar
			self.hitbox_width = hitbox_width

		def draw(self):
			ratio = self.stamina / self.max_bar
			if hero.stamina_amount == hero.stamina_threshold:
				color = green
			else:
				color = orange	
			pygame.draw.rect(screen, red, (self.x, self.y, self.hitbox_width, 10))
			pygame.draw.rect(screen, color, (self.x, self.y, self.hitbox_width * ratio, 10))	

	#hero speed portion
	hero_turn_amount_bar = Speed_Bar(screen, hero.turn_amount, hero.turn_threshold, hero.hitbox.x, hero.hitbox.y - 10, hero.original_hitbox.width)
	hero_stamina_amount_bar = Stamina_Bar(screen, hero.stamina_amount, hero.stamina_threshold, hero.hitbox.x, hero.hitbox.y - 20, hero.original_hitbox.width)
	hero_turn_amount_bar.draw()
	hero_stamina_amount_bar.draw()

	#monster speed portion
	if len(monster_list[monster_index]) == 1:
			monster0_speed_bar = Speed_Bar(screen, monster_list[monster_index][0].monster_turn_amount, monster_list[monster_index][0].monster_turn_threshold, monster_list[monster_index][0].hitbox.x, monster_list[monster_index][0].hitbox.y, monster_list[monster_index][0].hitbox.width)
			monster0_speed_bar.draw()					
	else:
		monster0_speed_bar = Speed_Bar(screen, monster_list[monster_index][0].monster_turn_amount, monster_list[monster_index][0].monster_turn_threshold, monster_list[monster_index][0].hitbox.x, monster_list[monster_index][0].hitbox.y, monster_list[monster_index][0].hitbox.width)
		monster1_speed_bar = Speed_Bar(screen, monster_list[monster_index][1].monster_turn_amount, monster_list[monster_index][1].monster_turn_threshold, monster_list[monster_index][1].hitbox.x, monster_list[monster_index][1].hitbox.y, monster_list[monster_index][1].hitbox.width)
		monster0_speed_bar.draw()
		monster1_speed_bar.draw()	

	#hero stamina and turn
	if boost == True and hero.turn_amount < hero.turn_threshold and hero.stamina_amount == hero.stamina_threshold:
		hero.stamina_amount -= hero.stamina_threshold
		turn_increase = (hero.turn_threshold - hero.turn_amount) - 0.5
		hero.turn_amount += turn_increase
		stamina_animation = Stamina_Images((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y + (hero.hitbox.height / 2))
		skill_sprite_group.add(stamina_animation)

	if hero.alive == True:
		if hero.turn_amount < hero.turn_threshold:
			hero.turn_amount += hero.speed + (hero.agility * 0.025)
		if hero.turn_amount > hero.turn_threshold:
			hero.turn_amount = hero.turn_threshold
		if hero.stamina_amount < hero.stamina_threshold:
			hero.stamina_amount += hero.stamina_recovery + (hero.strength * 0.1)
		if hero.stamina_amount > hero.stamina_threshold:
			hero.stamina_amount = hero.stamina_threshold

	#single monster
	if len(monster_list[monster_index]) == 1:
		if monster_list[monster_index][0].monster_turn_amount < monster_list[monster_index][0].monster_turn_threshold:
			monster_list[monster_index][0].monster_turn_amount += monster_list[monster_index][0].speed + (monster_list[monster_index][0].agility * 0.025)
		if monster_list[monster_index][0].monster_turn_amount > monster_list[monster_index][0].monster_turn_threshold:
			monster_list[monster_index][0].monster_turn_amount = monster_list[monster_index][0].monster_turn_threshold
			monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
			heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
			damage_text_group.add(heal_text)
			if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
				monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

	else:
		#monster 1
		if monster_list[monster_index][0].alive == False:
			monster_list[monster_index][0].monster_turn_amount = 0
			if monster_list[monster_index][1].monster_turn_amount < monster_list[monster_index][1].monster_turn_threshold:
				monster_list[monster_index][1].monster_turn_amount += monster_list[monster_index][1].speed + (monster_list[monster_index][1].agility * 0.025)
			if monster_list[monster_index][1].monster_turn_amount > monster_list[monster_index][1].monster_turn_threshold:
				monster_list[monster_index][1].monster_turn_amount = monster_list[monster_index][1].monster_turn_threshold
				monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
				heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
				damage_text_group.add(heal_text)
				if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
					monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp

		#monster 2
		if monster_list[monster_index][1].alive == False:
			monster_list[monster_index][1].monster_turn_amount = 0
			if monster_list[monster_index][0].monster_turn_amount < monster_list[monster_index][0].monster_turn_threshold:
				monster_list[monster_index][0].monster_turn_amount += monster_list[monster_index][0].speed + (monster_list[monster_index][0].agility * 0.025)
			if monster_list[monster_index][0].monster_turn_amount > monster_list[monster_index][0].monster_turn_threshold:
				monster_list[monster_index][0].monster_turn_amount = monster_list[monster_index][0].monster_turn_threshold	
				monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
				heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
				damage_text_group.add(heal_text)
				if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
					monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

		if monster_list[monster_index][0].alive == True and monster_list[monster_index][1].alive == True:
			if monster_list[monster_index][0].monster_turn_amount < monster_list[monster_index][0].monster_turn_threshold:
				monster_list[monster_index][0].monster_turn_amount += monster_list[monster_index][0].speed + (monster_list[monster_index][0].agility * 0.025)
			if monster_list[monster_index][0].monster_turn_amount > monster_list[monster_index][0].monster_turn_threshold:
				monster_list[monster_index][0].monster_turn_amount = monster_list[monster_index][0].monster_turn_threshold					
				monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
				heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
				damage_text_group.add(heal_text)
				if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
					monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

			if monster_list[monster_index][1].monster_turn_amount < monster_list[monster_index][1].monster_turn_threshold:
				monster_list[monster_index][1].monster_turn_amount += monster_list[monster_index][1].speed + (monster_list[monster_index][1].agility * 0.025)
			if monster_list[monster_index][1].monster_turn_amount > monster_list[monster_index][1].monster_turn_threshold:
				monster_list[monster_index][1].monster_turn_amount = monster_list[monster_index][1].monster_turn_threshold		
				monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
				heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][1].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
				damage_text_group.add(heal_text)
				if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
					monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp
