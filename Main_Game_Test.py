import math,pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events, Speed_Stamina, Consumables, ctypes, time

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 120

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

#define game variables
experiencethreshold = [5]
left_click = False
right_click = False
attack = False
target = None
monster_index = 0 #0 = slime, 1 = zombie, 2 = zombie_boss
game_over = 0
random_stat_list = []
random_stat_list_monsters = []
gold = 0
game_map = 0
#controls player action
action_index = 0 #0 = attack
#turns counter
stage_counter = 0

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
darker_orange = (254,110,0)

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

#load assets#
background_img = pygame.image.load('Images/Background/BackgroundNew.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(screen_width,screen_height))
victory_img = pygame.image.load('Images/Icon/Banners0.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Banners1.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Banners2.png').convert_alpha()
allocate_img = pygame.image.load('Images/Icon/Banners3.png').convert_alpha()
stat_point_img = pygame.image.load('Images/Icon/Banners4.png').convert_alpha()
inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(width(0.035),height(0.035)))
active_skills_hitbox_img = pygame.image.load('Images/Icon/SkillIcons/ActiveButtons.png').convert_alpha()
active_skills_hitbox_img = pygame.transform.scale(active_skills_hitbox_img,(width(0.035),height(0.035)))

#sound_effect = pygame.mixer.Sound('filename') -> add to def in class -> sound_effect.play()

#characters
#----------------------------------------------------------------------------------hero
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, attack_time):

##hero

Character.Random_Stats_Hero(random_stat_list)
hero = Character.Hero(width_position(0.1), bottom_of_bottom_panel, 'Hero', 100, 20, 1, 1, 1, 0, 3000, 0, 0, 25, random_stat_list[0], random_stat_list[1], random_stat_list[2], random_stat_list[3], random_stat_list[4])
random_stat_list.clear()

#----------------------------------------------------------------------------------monster
#(x, y, name, max_hp, max_mp, hp_regen, mp_regen, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance)
##slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(width_position(0.8), bottom_of_bottom_panel, 'Slime', 15, 3, 1, 1, 1, 5, 10, 2, 0, 12 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4])
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime1 = Character.Slime(width_position(0.9), bottom_of_bottom_panel, 'Slime', 15, 3, 1, 1, 1, 5, 10, 2, 0, 12 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4])
random_stat_list_monsters.clear()

slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)

##zombie

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie0 = Character.Zombie(width_position(0.8), top_of_bottom_panel, 'Zombie', 25, 3, 1, 1, 1, 8, 15, 2, 0, 9 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(3,5), random_stat_list_monsters[3] + random.randint(3,5), random_stat_list_monsters[4] + random.randint(3,5))
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie1 = Character.Zombie(width_position(0.9), top_of_bottom_panel, 'Zombie', 25, 3, 1, 1, 1, 8, 15, 2, 0, 9 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(3,5), random_stat_list_monsters[3] + random.randint(3,5), random_stat_list_monsters[4] + random.randint(3,5))
random_stat_list_monsters.clear()

zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)

##zombie boss

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie_boss0 = Character.Zombie_Boss(width_position(0.8), top_of_bottom_panel, 'ZombieBoss', 1000, 10, 3, 3, 1, 1000, 1500, 5, 0, 6 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(10,20), random_stat_list_monsters[1] + random.randint(20,30), random_stat_list_monsters[2] + random.randint(3,5), random_stat_list_monsters[3] + random.randint(3,5), random_stat_list_monsters[4] + random.randint(3,5))

random_stat_list_monsters.clear()

zombie_boss_list = []
zombie_boss_list.append(zombie_boss0)

##zombie and slime

Character.Random_Stats_Monsters(random_stat_list_monsters)
slime2 = Character.Slime(width_position(0.8), top_of_bottom_panel, 'Slime', 15, 3, 1, 1, 1, 5, 10, 2, 0, 12 + random.randint(-3,3), random_stat_list_monsters[0], random_stat_list_monsters[1], random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4])
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
zombie2 = Character.Zombie(width_position(0.9), top_of_bottom_panel, 'Zombie', 25, 3, 1, 1, 1, 8, 15, 2, 0, 9 + random.randint(-3,3), random_stat_list_monsters[0] + random.randint(3,5), random_stat_list_monsters[1] + random.randint(3,5), random_stat_list_monsters[2] + random.randint(3,5), random_stat_list_monsters[3] + random.randint(3,5), random_stat_list_monsters[4] + random.randint(3,5))
random_stat_list_monsters.clear()

zombie_and_slime_list = []
zombie_and_slime_list.append(slime2)
zombie_and_slime_list.append(zombie2)

##swift zombie

Character.Random_Stats_Monsters(random_stat_list_monsters)
swift_zombie0 = Character.Swift_Zombie(width_position(0.8), top_of_bottom_panel, 'SwiftZombie', 20, 3, 1, 1, 1, 20, 25, 2, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + 5, random_stat_list_monsters[1], random_stat_list_monsters[2] + 5, random_stat_list_monsters[3], random_stat_list_monsters[4])
random_stat_list_monsters.clear()

Character.Random_Stats_Monsters(random_stat_list_monsters)
swift_zombie1 = Character.Swift_Zombie(width_position(0.9), top_of_bottom_panel, 'SwiftZombie', 20, 3, 1, 1, 1, 20, 25, 2, 0, 15 + random.randint(-3,3), random_stat_list_monsters[0] + 5, random_stat_list_monsters[1], random_stat_list_monsters[2] + 5, random_stat_list_monsters[3], random_stat_list_monsters[4])
random_stat_list_monsters.clear()

swift_zombie_list = []
swift_zombie_list.append(swift_zombie0)
swift_zombie_list.append(swift_zombie1)

##golem boss

Character.Random_Stats_Monsters(random_stat_list_monsters)
golem_boss0 = Character.Golem_Boss(width_position(0.8), top_of_bottom_panel - height_position(0.135), 'GolemBoss', 3000, 10, 3, 3, 1, 2000, 2500, 10, 0, 5 + random.randint(-1,1), random_stat_list_monsters[0] + random.randint(40,60), random_stat_list_monsters[1] + random.randint(60,80), random_stat_list_monsters[2] + random.randint(3,5), random_stat_list_monsters[3] + random.randint(3,5), random_stat_list_monsters[4] + random.randint(3,5))

random_stat_list_monsters.clear()

golem_boss_list = []
golem_boss_list.append(golem_boss0)

###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)
monster_list.append(zombie_boss_list)
monster_list.append(zombie_and_slime_list)
monster_list.append(golem_boss_list)
monster_list.append(swift_zombie_list)

#bars
##hero
hero_health_bar = Bars.Health_Bar(width_position(0.1), height_position(0.89), hero.hp, hero.max_hp)
hero_shield_bar = Bars.Shield_Bar(width_position(0.1), height_position(0.89))
hero_mana_bar = Bars.Mana_Bar(width_position(0.1), height_position(0.95), hero.mp, hero.max_mp)
hero_experience_bar = Bars.Experience_Bar(0, screen_height - 13)
##slime
slime0_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), slime0.hp, slime0.max_hp)
slime1_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.95), slime1.hp, slime1.max_hp)
slime0_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
slime1_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.95))
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
slime_shield_list = []
slime_shield_list.append(slime0_shield_bar)
slime_shield_list.append(slime1_shield_bar)
##zombie
zombie0_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), zombie0.hp, zombie0.max_hp)
zombie1_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.95), zombie1.hp, zombie1.max_hp)
zombie0_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
zombie1_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.95))
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
zombie_shield_list = []
zombie_shield_list.append(zombie0_shield_bar)
zombie_shield_list.append(zombie1_shield_bar)
##zombie boss
zombie_boss_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), zombie_boss0.hp, zombie_boss0.max_hp)
zombie_boss_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
zombie_boss_health_list = []
zombie_boss_health_list.append(zombie_boss_health_bar)
zombie_boss_shield_list = []
zombie_boss_shield_list.append(zombie_boss_shield_bar)
##swift zombie
swift_zombie0_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), swift_zombie0.hp, swift_zombie0.max_hp)
swift_zombie1_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.95), swift_zombie1.hp, swift_zombie1.max_hp)
swift_zombie0_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
swift_zombie1_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.95))
swift_zombie_health_list = []
swift_zombie_health_list.append(swift_zombie0_health_bar)
swift_zombie_health_list.append(swift_zombie1_health_bar)
swift_zombie_shield_list = []
swift_zombie_shield_list.append(swift_zombie0_shield_bar)
swift_zombie_shield_list.append(swift_zombie1_shield_bar)
##zombie and slime
zombie2_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), zombie2.hp, zombie2.max_hp)
slime2_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.95), slime2.hp, slime2.max_hp)
zombie2_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
slime2_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.95))
zombie_and_slime_health_list = []
zombie_and_slime_health_list.append(zombie2_health_bar)
zombie_and_slime_health_list.append(slime2_health_bar)
zombie_and_slime_shield_list = []
zombie_and_slime_shield_list.append(zombie2_shield_bar)
zombie_and_slime_shield_list.append(slime2_shield_bar)
##golem boss
golem_boss_health_bar = Bars.Health_Bar(width_position(0.6), height_position(0.9), golem_boss0.hp, golem_boss0.max_hp)
golem_boss_shield_bar = Bars.Shield_Bar(width_position(0.6), height_position(0.9))
golem_boss_health_list = []
golem_boss_health_list.append(golem_boss_health_bar)
golem_boss_shield_list = []
golem_boss_shield_list.append(golem_boss_shield_bar)

###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)
monster_health_list.append(zombie_and_slime_health_list)
monster_health_list.append(golem_boss_health_list)
monster_health_list.append(swift_zombie_health_list)
monster_shield_list = []
monster_shield_list.append(slime_shield_list)
monster_shield_list.append(zombie_shield_list)
monster_shield_list.append(zombie_boss_shield_list)
monster_shield_list.append(zombie_and_slime_shield_list)
monster_shield_list.append(golem_boss_shield_list)
monster_shield_list.append(swift_zombie_shield_list)

#button
restart_button = Bars.Button(screen, (screen_width / 2) - 125 , 160, reset_img, 250, 50)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = 0
		monster.action = 0		

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

def collide():
	mousex, mousey = pygame.mouse.get_pos()
	for count, monster in enumerate(monster_list[monster_index]):
		head = monster.head_hitbox
		body = monster.body_hitbox
		leg = monster.leg_hitbox
		limb_list = ['head','body','leg']

		if monster.hitbox.collidepoint((mousex,mousey)) and monster.alive == True:
			screen.blit(font.render('NAME:' + str(monster.name), True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 40))
			screen.blit(font.render(f'STR: {monster.strength:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y - 20))
			screen.blit(font.render(f'INT: {monster.intelligence:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y))
			screen.blit(font.render(f'LUC: {monster.luck:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 20))
			screen.blit(font.render(f'AGI: {monster.agility:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 40))
			screen.blit(font.render(f'END: {monster.endurance:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 60))
			screen.blit(font.render(f'DEF: {monster.defense:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 80))
			screen.blit(font.render(f'SPD: {monster.speed:.2f} + {monster.agility / 5:.2f}', True, blue), (monster.hitbox.x - 100, monster.hitbox.y + 100))

			if left_click == True or right_click == True:				
				target = monster
				target_limb_chance = random.randint(0,100)
				if 0 < target_limb_chance < 25:
					target_limb = 'head'
				elif 25 <= target_limb_chance <= 75:
					target_limb = 'body'
				else:
					target_limb = 'leg'
				hero.hero_to_monster_distance = float(f'{math.hypot((monster.hitbox.y + monster.hitbox.height * 0.5) - (hero.hitbox.y + hero.hitbox.height * 0.5), (monster.hitbox.x + monster.hitbox.width * 0.5) - (hero.hitbox.x + hero.hitbox.width * 0.5)):.2f}')

				return target_limb, target	

def return_scream_debuff(hero):
	#self buff return
	hero.strength -= hero.temp_strength
	hero.intelligence -= hero.temp_intelligence
	hero.agility -= hero.temp_agility
	hero.luck -= hero.temp_luck
	hero.endurance -= hero.temp_endurance

	hero.temp_strength = 0
	hero.temp_intelligence = 0
	hero.temp_agility = 0
	hero.temp_luck = 0
	hero.temp_endurance = 0

def return_stomp_buff(hero):
	hero.strength -= hero.temp_strength_stomp
	hero.agility -= hero.temp_agility_stomp
	hero.endurance -= hero.temp_endurance_stomp

	hero.temp_strength_stomp = 0
	hero.temp_agility_stomp = 0
	hero.temp_endurance_stomp = 0

def return_boss_debuff(hero, monster_list, monster_index):
	#return boss debuff
	hero.strength -= monster_list[monster_index][0].temp_strength
	hero.intelligence -= monster_list[monster_index][0].temp_intelligence
	hero.agility -= monster_list[monster_index][0].temp_agility
	hero.luck -= monster_list[monster_index][0].temp_luck
	hero.endurance -= monster_list[monster_index][0].temp_endurance

	monster_list[monster_index][0].temp_strength = 0
	monster_list[monster_index][0].temp_intelligence = 0
	monster_list[monster_index][0].temp_agility = 0
	monster_list[monster_index][0].temp_luck = 0
	monster_list[monster_index][0].temp_endurance = 0

#inventory and skills
#inventory = [2,3,4,5,25,6,7,8,9,10,11,12,13,14,29,15,16,17,1,18,19,20,35,21,31,22,23,24,26,27,28,30,32,33,34]
inventory = []

active_skills_indexes = {
	'normal_attack' : {'active_index' : 0},
	'cleave' : {'active_index' : 1},
	'triple_combo' : {'active_index' : 2},
	'zombie_stab' : {'active_index' : 3},
	'serpent_wheel' : {'active_index' : 4},
	'venomous_whip' : {'active_index' : 5},
	'thunder_bolt' : {'active_index' : 6}

}

skill_hitbox_active = 0

skill_active_hitbox_indexes = {
	'hitbox' : {0 : (width(0.035),0), 1 : (width(0.07),0), 2 : (width(0.105),0), 3 : (width(0.14),0), 4 : (width(0.175),0)},	

}

#events
event_1 = True
event_2 = True
event_3 = True

#bosses
boss_defeated_list = []

#skill turn counters
fireball_turn_counter = 3
lightning_turn_counter = 3
shield_turn_counter = 0
speed_counter = 0

start_combat_time = 0
level_up_time = 0

boost = False

battle_over = False

boss_turn_amount = 0
monster_special_skill = False

hero.roll_speed_increase_time = 0
player_y_momentum = 0
hero.player_x_momentum = 0
hero.player_x_speed = 4

#sprites
skill_sprite_group = pygame.sprite.Group()
monster_skill_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game variables
game_variables = Character.Game_Option_And_Variables()

#game#
Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)
monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, experiencethreshold, game_variables)
enemy_random_skill_time_list = [350,400,450,500]
enemy_random_skill_time_index = 0
#event 0
Level_Events.lvl_up_event_0(hero, monster_list, monster_index)

music_on = False
battle_theme_list = []
for battle in range(2):
	battle_theme = f'Music/Battle_Theme{battle}.mp3'
	battle_theme_list.append(battle_theme)	

run = True
while run:
	if game_variables.music_on == False:
		pygame.mixer.music.fadeout(500)
		pygame.mixer.music.load(battle_theme_list[random.randint(0,1)])
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)
		game_variables.music_on = True

	#how fast the game runs
	clock.tick(fps)

	#draw background
	Load_Interface.draw_background(background_img)
	#---------------------------#
	#draw panel
	Load_Interface.draw_panel(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen)
	#---------------------------#
	#draw hero bars
	hero_health_bar.draw(hero.hp, hero.max_hp)
	hero_mana_bar.draw(hero.mp, hero.max_mp)
	hero_experience_bar.draw(hero.experience, experiencethreshold)
	hero_shield_bar.draw(hero.shield, hero.max_hp)
	#---------------------------#
	#draw each monster's health bar according to each spawned
	for count, monster_health_bar in enumerate(monster_health_list[monster_index]):
		monster_health_bar.draw(monster_list[monster_index][count].hp, monster_list[monster_index][count].max_hp)
	#draw monster shield bars
	for count, monster_shield_bar in enumerate(monster_shield_list[monster_index]):		
		monster_shield_bar.draw(monster_list[monster_index][count].shield, monster_list[monster_index][count].max_hp)
	#---------------------------#
	skill_sprite_group.update()
	skill_sprite_group.draw(screen)
	monster_skill_sprite_group.update()
	monster_skill_sprite_group.draw(screen)
	damage_text_group.update()
	damage_text_group.draw(screen)
	#---------------------------#
	#if battle is not over shown items
	Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, left_click, battle_over)
	#---------------------------#
	target_limb, target = collide() or (False,None)	
#---------------------------battle effects---------------------------------#
	if battle_over == False and hero.alive == True:

		if hero.lock_target == True:
			pygame.mouse.set_pos(monster_list[monster_index][hero.lock_target_index - 1].hitbox.x + monster_list[monster_index][hero.lock_target_index - 1].hitbox.width * 0.5, monster_list[monster_index][hero.lock_target_index - 1].hitbox.y + monster_list[monster_index][hero.lock_target_index - 1].hitbox.height * 0.5)

		hero.movement_calculation_and_reposition_hitbox(player_y_momentum, hero.player_x_momentum, hero.player_x_speed, hero.roll_speed_increase_time, hero.stand_still_cooldown)

		#reset
		if 'start_fireball' in hero.skills_list:
			if start_combat_time % 1000 == 0 and start_combat_time != 0 and len(hero.consumables_list) < hero.orb_limit:
				hero.consumables_list.append('Fireball')
		if 'start_lightning' in hero.skills_list:
			if start_combat_time % 1000 == 0 and start_combat_time != 0 and len(hero.consumables_list) < hero.orb_limit:
				hero.consumables_list.append('Lightning')

		#pets
		if start_combat_time % 700 == 0:
			hero.pet_active_time = 300
			if len(monster_list[monster_index]) != 1:
				if monster_list[monster_index][0].alive == True:
					pet_random_target = 0
				else:
					pet_random_target = 1
			else:
				pet_random_target = 0
		if hero.pet_active_time > 0:
			hero.pet_active_time -= 1
			pet_target = monster_list[monster_index][pet_random_target]
		else:
			pet_target = hero
		if -16 in inventory:
			hero.ghost_pet_update(monster_list, monster_index, damage_text_group, pet_target)

		#return stats
		if hero.scream_debuff_time > 0:
			hero.scream_debuff_time -= 1
			if hero.scream_debuff_time == 0:
				return_scream_debuff(hero)
		if hero.stomp_buff_time > 0:
			hero.stomp_buff_time -= 1
			if hero.stomp_buff_time == 0:
				return_stomp_buff(hero)

		#balance and checks	
		if hero.hp > hero.max_hp:
			hero.hp = hero.max_hp
		if hero.mp > hero.max_mp:
			hero.mp = hero.max_mp

		#cooldown
		if hero.attack_time > 0:
			hero.attack_time -= float(f'{hero.attack_cooldown_rate + (hero.agility * 0.025):.2f}') #to fix floating point errors devide by 2 ex 1/2, 1/4, 1/8, 1/16 known as newton's method
			if hero.attack_time < 0:
				hero.attack_time = 0
		if hero.jump_cooldown > 0:
			hero.jump_cooldown -= 1
		if hero.stand_still_cooldown > 0:
			hero.stand_still_cooldown -= 1
		if hero.roll_speed_increase_time > 0:
			hero.roll_speed_increase_time -= 1
		if hero.roll_cooldown > 0:
			hero.roll_cooldown -= 1
		if monster_list[monster_index][0] == golem_boss0:
			if monster_list[monster_index][0].special_skill_2_time_counter > 0:
				monster_list[monster_index][0].special_skill_2_time_counter -= 1
		if hero.mist_vortex_time > 0:
			hero.mist_vortex_time -= 1
		if hero.consumable_wait_time > 0:
			hero.consumable_wait_time -= 1

		#monster skill
		for count, monster in enumerate(monster_list[monster_index]):
			if monster.monster_skill_time > 0:
				monster.monster_skill_time -= 1
			#distance to monster
			monster.distance = float(f'{math.hypot((monster.hitbox.y + monster.hitbox.height * 0.5) - (hero.hitbox.y + hero.hitbox.height * 0.5), (monster.hitbox.x + monster.hitbox.width * 0.5) - (hero.hitbox.x + hero.hitbox.width * 0.5)):.2f}')
			monster.collide_damage(hero, damage_text_group, start_combat_time)
			monster.y_momentum_calculation(hero)

		#auto items
		#auto stomp from war drum and stone drum
		if 24 in inventory and start_combat_time % 800 == 0 and start_combat_time != 0:
			hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)
		#auto guard
		if 6 in inventory and start_combat_time % 800 == 0:
			hero.guard(skill_sprite_group, damage_text_group, experiencethreshold, inventory, monster_list, monster_index)

		#hydra heart
		hero.water_blast(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time)
		#auto hp regen
		hero.hp_regen_calculation(start_combat_time, inventory, damage_text_group, monster_list, monster_index)	
		hero.hibiscus_regen_calculation(start_combat_time, inventory, damage_text_group, monster_list, monster_index)		
		#auto mp regen
		hero.mp_regen_calculation(start_combat_time, inventory, damage_text_group, monster_list, monster_index)	
		#goblin bomb
		hero.goblin_bomb(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time)
		#mist vortex
		hero.mist_vortex(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, start_combat_time) 
		#auto phoenix spark
		hero.auto_spark_phoenix(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)

		#combat start time
		start_combat_time += 1			
	else:
		start_combat_time = 0

	#update hero
	hero.update()
	hero.draw(game_variables)

	#draw monsters
	for monster in monster_list[monster_index]:
		monster.update()
		monster.draw(game_variables)

	#turn system
	Speed_Stamina.turn_calculations(boost, hero, monster, monster_list, monster_index, inventory, damage_text_group, skill_sprite_group)
	#current attack picture
	Load_Interface.draw_current_attack(action_index, inventory, hero)
	#show skills icon highlights
	screen.blit(active_skills_hitbox_img,skill_active_hitbox_indexes['hitbox'][skill_hitbox_active])
	
	#consumables
	hero.draw_consumables(start_combat_time)
	#---------------------------#

	#hero guard
	if'guard' in hero.skills_list and start_combat_time % 1000 == 0 and start_combat_time != 0 and hero.shield == 0 and battle_over != True:
		hero.guard(skill_sprite_group, damage_text_group, experiencethreshold, inventory, monster_list, monster_index)

	#hero stomp
	if'stomp' in hero.skills_list and start_combat_time % 1000 == 0 and start_combat_time != 0 and battle_over != True and hero.on_ground == True:
		hero.stomp(damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)

	#out of turn skills
	#thunder bolt
	if action_index == 6 and hero.mp >= 15 and target != None and target.alive == True and hero.turn_amount != hero.turn_threshold:
		hero.thunder_bolt(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group)					
		target = None	

	#attacks
	if target != None and target.alive == True:
		if action_index == 0:
			if hero.attack_time == 0 and hero.on_ground == True and hero.hero_to_monster_distance < hero.attack_length:
				if left_click == True and hero.stamina_amount > hero.stamina_threshold * 0.05:
					hero.light_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
					hero.attack_time = hero.base_attack_time * 0.4
					hero.stamina_amount -= hero.stamina_threshold * 0.05
				elif right_click == True and hero.stamina_amount > hero.stamina_threshold * 0.5:
					hero.heavy_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
					hero.attack_time = hero.base_attack_time
					hero.stand_still_cooldown = 200
					hero.stamina_amount -= hero.stamina_threshold * 0.5		
		elif action_index != 0:
			if hero.turn_amount >= hero.turn_threshold:
				#cleave
				if action_index == 1 and hero.mp >= 7.5 and hero.on_ground == True:
					hero.cleave(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)
					hero.turn_amount = 0
				#triple combo
				elif action_index == 2 and hero.mp >= 10 and hero.on_ground == True:
					hero.triple_combo(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index)
					hero.turn_amount = 0
				#zombie stab
				elif action_index == 3 and hero.mp >= 10:
					hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)
					hero.turn_amount = 0
				#serpent wheel
				elif action_index == 4 and hero.mp >= 20:
					hero.serpent_wheel(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)
					hero.turn_amount = 0
				#venomous whip
				elif action_index == 5 and hero.mp >= 20:
					hero.venomous_whip(target, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group)
					hero.turn_amount = 0
				elif hero.attack_time == 0 and hero.on_ground == True and hero.hero_to_monster_distance < hero.attack_length:
					if left_click == True and hero.stamina_amount > hero.stamina_threshold * 0.05:
						hero.light_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
						hero.attack_time = hero.base_attack_time * 0.4
						hero.stamina_amount -= hero.stamina_threshold * 0.05
					elif right_click == True and hero.stamina_amount > hero.stamina_threshold * 0.5:
						hero.heavy_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
						hero.attack_time = hero.base_attack_time
						hero.stand_still_cooldown = 200
						hero.stamina_amount -= hero.stamina_threshold * 0.5	
			elif hero.attack_time == 0 and hero.on_ground == True and hero.hero_to_monster_distance < hero.attack_length:
				if left_click == True and hero.stamina_amount > hero.stamina_threshold * 0.05:
					hero.light_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
					hero.attack_time = hero.base_attack_time * 0.4
					hero.stamina_amount -= hero.stamina_threshold * 0.05
				elif right_click == True and hero.stamina_amount > hero.stamina_threshold * 0.5:
					hero.heavy_attack(target, experiencethreshold, damage_text_group, inventory, monster_list, monster_index, target_limb, skill_sprite_group)	
					hero.attack_time = hero.base_attack_time
					hero.stand_still_cooldown = 200
					hero.stamina_amount -= hero.stamina_threshold * 0.5		

	#enemy action
	#single enemy
	if len(monster_list[monster_index]) == 1 and hero.alive != False and hero.hp > 0:

		if monster.alive == True:

			monster.movement(hero, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time)

		if monster_index == 2:
			if start_combat_time % 450 == 0 and start_combat_time != 0:
				monster.special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)

			if start_combat_time % 1200 == 0 and start_combat_time != 0:
				monster.special_skill_2(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)

			if monster.monster_turn_amount >= monster.monster_turn_threshold:
				if monster.alive != False:
					if random.randint(0,100) > 80:
						monster.guard(skill_sprite_group, damage_text_group)
					elif monster.distance < monster.attack_length and (hero.hitbox.width != 0 and hero.hitbox.height != 0):
						monster.attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
					else:
						monster.scream(hero, monster_skill_sprite_group, damage_text_group, inventory)
					if 35 in inventory:
						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
					if -22 in inventory:
						hero.bleed(monster, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)

					boss_turn_amount += 1
					monster.shield = 0
					hero.shield = 0 
					monster.monster_turn_amount = 0		

			if monster.alive == False and len(boss_defeated_list) == 0:
				boss_defeated_list.append('zombie_boss')
				Map.stage_major += 1
				Map.stage = 0	
				Map.game_map = 2				
				Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

		if monster_index == 4:

			if monster.hp > monster.max_hp * 0.5:
				if start_combat_time % 800 == 0 and start_combat_time != 0:
					monster.special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
				if start_combat_time % 1200 == 0 and start_combat_time != 0:
					monster.special_skill_2_time_counter = 500
				if monster.special_skill_2_time_counter > 0 and monster.special_skill_2_time_counter % 100 == 0:
					monster.special_skill_2(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
					monster.special_skill_2_counter += 1
			else:
				if start_combat_time % 600 + (200 * math.floor(monster.hp/monster.max_hp)) == 0 and start_combat_time != 0:
					monster.special_skill_1(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)					
				if start_combat_time % 1000 == 0 and start_combat_time != 0:
					monster.special_skill_2_time_counter = 500
				if monster.special_skill_2_time_counter > 0 and monster.special_skill_2_time_counter % 100 == 0:
					monster.special_skill_2(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
					monster.special_skill_2_counter += 1

			if monster.monster_turn_amount >= monster.monster_turn_threshold:

				if monster.alive != False:
					if random.randint(0,100) > 80:
						monster.guard(skill_sprite_group, damage_text_group)
					elif monster.distance < monster.attack_length and (hero.hitbox.width != 0 and hero.hitbox.height != 0):
						monster.attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
					else:
						monster.special_skill_3(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
					if 35 in inventory:
						hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
					if -22 in inventory:
						hero.bleed(monster, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)

					boss_turn_amount += 1
					monster.shield = 0
					hero.shield = 0 
					monster.monster_turn_amount = 0	

			if monster.alive == False and len(boss_defeated_list) == 1:
				boss_defeated_list.append('golem_boss')
				Map.stage_major += 1
				Map.stage = 0	
				Map.game_map = 2
				Screen_Menus.shop_names_list = Screen_Menus.reset_items_in_shop(Screen_Menus.original_shop_names_list, Screen_Menus.purchased_list, inventory)

	#two enemies
	if len(monster_list[monster_index]) == 2 and hero.alive != False and hero.hp > 0: 

		for monster in monster_list[monster_index]:

			if monster.alive == True:

				monster.movement(hero, damage_text_group, monster_skill_sprite_group, inventory, start_combat_time)

			if monster.alive == True and monster.monster_skill_time == 0 and start_combat_time != 0:

				if type(monster) is Character.Slime:
					monster.slime_ball(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
					monster.monster_skill_time = random.randint(600,800)

				if type(monster) is Character.Zombie:
					monster.vomit(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)
					monster.monster_skill_time = random.randint(600,800)

			if monster.alive == True and monster.monster_turn_amount >= monster.monster_turn_threshold:
				#monster guard
				roll_guard_chance = random.randint(0,100)
				if roll_guard_chance > 80:
					monster.guard(skill_sprite_group, damage_text_group)
				elif monster.distance < monster.attack_length and (hero.hitbox.width != 0 and hero.hitbox.height != 0):
					monster.attack(hero, damage_text_group, inventory, experiencethreshold, monster_list, monster_index)
				else:
					if type(monster) is Character.Slime:
						monster.slime_ball(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)

					if type(monster) is Character.Zombie:
						monster.vomit(hero, monster_skill_sprite_group, damage_text_group, inventory, monster)

				if 35 in inventory:
					hero.spark(monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
				if -22 in inventory:
					hero.bleed(monster, hero, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, skill_sprite_group, target_limb)

				hero.shield = 0 
				monster.shield = 0						
				monster.monster_turn_amount = 0	

#--------------------------------------------------------------------------#monster drops
	#check if dead and drop exp, loot, gold
	for monster in monster_list[monster_index]:
		hero.monster_death_drops(monster, experiencethreshold, inventory, monster_list, monster_index)
#--------------------------------------------------------------------------

	#phoenix feather revive
	if 28 in inventory and hero.alive == False:
		hero.hp += hero.max_hp * 0.5
		hero.alive = True
		hero.action = 0
		inventory.remove(28)

	#check alive monsters to change game over condition
	if hero.alive != False and hero.hp > 0:
		alive_monster = 0
		for monster in monster_list[monster_index]:
			if monster.alive == True:
				alive_monster += 1
		if alive_monster == 0:
			game_over = 1
	else:
		game_over = -1

	#if it's a game over -> defeat or victory
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, ((screen_width / 2) - 125, 100))
			battle_over = True

			hero.level_up_hero(inventory, experiencethreshold)

			return_stomp_buff(hero)
			return_scream_debuff(hero)

			hero.pixels_moved_right = 0
			hero.pixels_moved_left = 0
			hero.hibiscus_pixels_moved = 0
			hero.phoenix_spark_moved = 0 
			hero.dragon_item_counter = 0
			hero.attack_bleed_counter = 0
			hero.draw_fire_ball_consumable = False
			hero.heavy_attack_obsidian_counter = 0
			hero.consumable_wait_time = 0
			
			hero.stand_still_cooldown = 0
			hero.shield = 0
			turn_counter = 0
			fireball_turn_counter = 3
			lightning_turn_counter = 3
			shield_turn_counter = 0
			hero.turn_amount = 0
			hero.stamina_amount = 0
			boss_turn_amount = 0

			if monster_index == 4:
				golem_boss0.special_skill_2_counter = 0

			if len(monster_list[monster_index]) != 1:
				monster_list[monster_index][0].monster_turn_amount = 0
				monster_list[monster_index][1].monster_turn_amount = 0
			else:
				monster_list[monster_index][0].monster_turn_amount = 0			

			if hero.statpoints > 0:
				screen.blit(allocate_img, ((screen_width / 2) - 125, 160))
				screen.blit(stat_point_img, ((screen_width / 2) - 125, 220))
			else:
				if restart_button.draw():
					game_variables.music_on = False

					hero.lock_target_index = 0
					hero.lock_target = False

					hero.attack_time = 0

					#trigger level up event	
					if hero.level > 1 and event_1 == True:
						Level_Events.lvl_up_event_1(hero, monster, monster_list, monster_index)
						event_1 = False			

					if hero.level > 3 and event_2 == True:
						if 'guard' in hero.skills_list:
							Level_Events.lvl_up_event_2_guard(hero, monster, monster_list, monster_index)
							event_2 = False
						elif 'stomp' in hero.skills_list:
							Level_Events.lvl_up_event_2_stomp(hero, monster, monster_list, monster_index)
							event_2 = False		
						else:
							Level_Events.lvl_up_event_2(hero, monster, monster_list, monster_index)
							event_2 = False				

					if hero.level > 6 and event_3 == True:
						if 'cleave' in hero.skills_list:
							Level_Events.lvl_up_event_3_cleave(hero, monster, monster_list, monster_index)
							event_3 = False
						elif 'triple_combo' in hero.skills_list:
							Level_Events.lvl_up_event_3_triple_combo(hero, monster, monster_list, monster_index)
							event_3 = False		
					
					hero.consumables_list = hero.active_consumables_list.copy()

					hero.rect.x = width_position(0.1)
					hero.rect.y = height_position(0.52)

					hero.idle()
					
					if len(monster_list[monster_index]) == 2:
						for count, monster in enumerate(monster_list[monster_index]):	
							monster.monster_skill_time = 400					
							monster.rect.x = width_position(0.7 + (0.1 * count))
							monster.hitbox.x = monster.rect.x + monster.hitbox_x_offset
							monster.rect.y = height_position(0.52)
							monster.hitbox.y = monster.rect.y + monster.hitbox_y_offset

					#platformer map menu
					monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list, left_click, boss_defeated_list, experiencethreshold, game_variables)
					#trigger events if move to next map
					if monster_encounter == False:
						random_event_index = random.randint(0,5)
						Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)
					#reset spawns and monsters			
					start_spawn()
					for monster_group in range(len(monster_list)):
						for monster in monster_list[monster_group]:
							monster.level_up_monster(hero)
					battle_over = False
					game_over = 0

		if game_over == -1:
			screen.blit(defeat_img, ((screen_width / 2) - 120, 100))
			battle_over = True
			if restart_button.draw():
				run = False
				sys.exit()

	left_click = False
	right_click = False	

	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN: #left
			if event.button == 1:
				left_click = True
				mousex, mousey = pygame.mouse.get_pos()

			if event.button == 3:
				right_click = True	

			if event.button == 4 and battle_over == False:
				Consumables.swap_consumables(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)

			if event.button == 5 and battle_over == False:
				Consumables.use_consumables(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_e:
				boost = False

				#movement
			if event.key == pygame.K_d:
				hero.running_right = False
				hero.player_x_momentum = 0
				if hero.rect.bottom > bottom_of_bottom_panel:
					hero.short_idle()

			if event.key == pygame.K_a:
				hero.running_left = False
				hero.player_x_momentum = 0
				if hero.rect.bottom > bottom_of_bottom_panel:
					hero.short_idle()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				Screen_Menus.option_menu(hero, game_variables)

				#stamina
			if event.key == pygame.K_e and hero.turn_amount <= hero.turn_threshold:
				boost = True

				#movement
			if event.key == pygame.K_d and battle_over == False:			
				hero.running_right = True
				hero.facing_right = True
				hero.facing_left = False

			if event.key == pygame.K_a and battle_over == False:
				hero.running_left = True
				hero.facing_left = True
				hero.facing_right = False

			if event.key == pygame.K_LSHIFT and battle_over == False and hero.roll_cooldown == 0 and hero.stamina_amount > hero.stamina_threshold * 0.1:
				if hero.running_left == True and hero.hitbox.x > 0:
					hero.player_x_speed = 12
					hero.roll_speed_increase_time = 35
					hero.roll_cooldown = 65
					hero.roll_back(monster_list, monster_index, damage_text_group, experiencethreshold, inventory)	
				if hero.running_right == True and hero.hitbox.x < screen_width - hero.hitbox.width:
					hero.player_x_speed = 12
					hero.roll_speed_increase_time = 35
					hero.roll_cooldown = 65
					hero.roll_forward(monster_list, monster_index, damage_text_group, experiencethreshold, inventory)
				hero.stamina_amount -= hero.stamina_threshold * 0.1

			if event.key == pygame.K_w and hero.jump_counter < 2 and battle_over == False:
				hero.rect.bottom -= screen_height * 0.1
				hero.jump_cooldown = 65
				if hero.jump_counter == 0:
					hero.player_y_momentum -= screen_height * 0.0115
				else:
					hero.player_y_momentum -= screen_height * 0.0085
				hero.jump_counter += 1
				hero.jump()

			if event.key == pygame.K_s and hero.jump_counter > 0 and battle_over == False:
				hero.player_y_momentum += screen_height * 0.0115

			if event.key == pygame.K_z:
				Screen_Menus.inventory_menu(inventory, monster_list, monster_index, hero)

			if event.key == pygame.K_LALT:
				hero.lock_target = True
				hero.lock_target_index += 1
				if len(monster_list[monster_index]) != 1:
					if hero.lock_target_index == 3:
						hero.lock_target_index = 0
						hero.lock_target = False
				else:
					if hero.lock_target_index == 2:
						hero.lock_target_index = 0
						hero.lock_target = False					

				#skills
			if event.key == pygame.K_1:
				action_index = active_skills_indexes[hero.active_skills_list[0]]['active_index']
				skill_hitbox_active = 0

			if event.key == pygame.K_2 and len(hero.active_skills_list) > 1:
				action_index = active_skills_indexes[hero.active_skills_list[1]]['active_index']
				skill_hitbox_active = 1

			if event.key == pygame.K_3 and len(hero.active_skills_list) > 2:
				action_index = active_skills_indexes[hero.active_skills_list[2]]['active_index']
				skill_hitbox_active = 2

			if event.key == pygame.K_4 and len(hero.active_skills_list) > 3:
				action_index = active_skills_indexes[hero.active_skills_list[3]]['active_index']
				skill_hitbox_active = 3

			if event.key == pygame.K_5 and len(hero.active_skills_list) > 4:
				action_index = active_skills_indexes[hero.active_skills_list[4]]['active_index']
				skill_hitbox_active = 4

	pygame.display.update()

pygame.quit()

#drop item in character

#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, mana_potion, level, experience, gold, defense, shield, speed, statpoints, strength, intelligence, agility, luck, endurance, added_strength, added_intelligence, added_agility, added_luck, added_endurance, stamina_recovery, stamina_threshold, fireball_charge, lightning_charge)
#(self, x, y, name, max_hp, max_mp, hp_regen, mp_regen, health_potion, level, experience, gold, defense, shield, speed, strength, intelligence, agility, luck, endurance, monster_turn_amount)

#check type
# print(type(zombie0))
# if type(zombie0) == Character.Zombie:
# 	print('yes')

#https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame/54714144 how to rotate an image at the center