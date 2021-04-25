import math, pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 120

#game window#
bottom_panel = 150
screen_width, screen_height = 800, 400 + bottom_panel
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
action_cooldown = 0
action_wait_time = 100
experiencethreshold = [5]
click = False
attack = False
target = None
monster_index = 0 #0 = slime, 1 = zombie, 2 = zombie_boss
game_over = 0
random_stat_list = []
random_stat_list_monsters = []
gold = 0
game_map = 0
#controls player action
action_index = 0 #0 = attack; 1 = fireball; 2 = guard
#turns counter
stage_counter = 0
#fonts
font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 10)

#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
#load assets#
background_img = pygame.image.load('Images/Background/BackgroundNew.png').convert_alpha()
background_img = pygame.transform.scale(background_img,(800,400))
panel_img = pygame.image.load('Images/Icon/Panel.png').convert_alpha()
sword_img = pygame.image.load('Images/Icon/SwordButton.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (50,50))
victory_img = pygame.image.load('Images/Icon/Victory.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icon/Defeat.png').convert_alpha()
reset_img = pygame.image.load('Images/Icon/Reset.png').convert_alpha()

#characters
##hero
Character.Random_Stats_Hero(random_stat_list)
#(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold, speed, hp_regen, mp_regen)
hero = Character.Hero(200, 265, 'Hero', 40, 20, 1, 0, 0, random_stat_list[0], random_stat_list[1], 2, random_stat_list[2], random_stat_list[3], random_stat_list[4], 0, 2, 2, 1500, 6, 1, 1)
##slime
#(x, y, name, max_hp, max_mp, level, experience, strength, intelligence, defense, luck, evasion, accuracy, shield, health_potion, gold, speed, hp_regen, mp_regen)
Character.Random_Stats_Monsters(random_stat_list_monsters)
slime0 = Character.Slime(530, 350, 'Slime', 10, 10, 1, 3, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 20, 3 + random.randint(0,1), 1, 1)
slime1 = Character.Slime(650, 350, 'Slime', 10, 10, 1, 3, random_stat_list_monsters[0], random_stat_list_monsters[1], 2, random_stat_list_monsters[2], random_stat_list_monsters[3], random_stat_list_monsters[4], 0, 1, 20, 3 + random.randint(0,1), 1, 1)
slime_list = []
slime_list = []
slime_list.append(slime0)
slime_list.append(slime1)
##zombie
zombie0 = Character.Zombie(530, 265, 'Zombie', 15, 10, 1, 6, random_stat_list_monsters[0] + random.randint(2,3), random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 30, 2 + random.randint(0,1), 1, 1)
zombie1 = Character.Zombie(650, 265, 'Zombie', 15, 10, 1, 6, random_stat_list_monsters[0] + random.randint(2,3), random_stat_list_monsters[1] + 1, 2, random_stat_list_monsters[2] + 1, random_stat_list_monsters[3] + 1, random_stat_list_monsters[4] + 1, 0, 1, 30, 2 + random.randint(0,1), 1, 1)
zombie_list = []
zombie_list.append(zombie0)
zombie_list.append(zombie1)
##zombie boss
zombie_boss0 = Character.Zombie_Boss(530, 265, 'Zombie Boss', 50, 10, 1, 25, random_stat_list_monsters[0] + random.randint(15,20), random_stat_list_monsters[1] + 10, 2, random_stat_list_monsters[2] + 10, random_stat_list_monsters[3] + 10, random_stat_list_monsters[4] + 10, 0, 1, 200, 1 + random.randint(0,1), 1, 1)
zombie_boss_list = []
zombie_boss_list.append(zombie_boss0)
###append all monsters into list
monster_list = []
monster_list.append(slime_list)
monster_list.append(zombie_list)
monster_list.append(zombie_boss_list)

#bars
##hero
hero_health_bar = Bars.Health_Bar(20, screen_height - bottom_panel + 40, hero.hp, hero.max_hp)
hero_shield_bar = Bars.Shield_Bar(20, screen_height - bottom_panel + 40)
hero_mana_bar = Bars.Mana_Bar(160, screen_height - bottom_panel + 40, hero.mp, hero.max_mp)
hero_experience_bar = Bars.Experience_Bar(0, screen_height - 13)
##slime
slime0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, slime0.hp, slime0.max_hp)
slime1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, slime1.hp, slime1.max_hp)
slime0_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
slime1_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 100)
slime_health_list = []
slime_health_list.append(slime0_health_bar)
slime_health_list.append(slime1_health_bar)
slime_shield_list = []
slime_shield_list.append(slime0_shield_bar)
slime_shield_list.append(slime1_shield_bar)
##zombie
zombie0_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie0.hp, zombie0.max_hp)
zombie1_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 100, zombie1.hp, zombie1.max_hp)
zombie0_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
zombie1_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 100)
zombie_health_list = []
zombie_health_list.append(zombie0_health_bar)
zombie_health_list.append(zombie1_health_bar)
zombie_shield_list = []
zombie_shield_list.append(zombie0_shield_bar)
zombie_shield_list.append(zombie1_shield_bar)
##zombie boss
zombie_boss_health_bar = Bars.Health_Bar(550, screen_height - bottom_panel + 40, zombie_boss0.hp, zombie_boss0.max_hp)
zombie_boss_shield_bar = Bars.Shield_Bar(550, screen_height - bottom_panel + 40)
zombie_boss_health_list = []
zombie_boss_health_list.append(zombie_boss_health_bar)
zombie_boss_shield_list = []
zombie_boss_shield_list.append(zombie_boss_shield_bar)
###append all monster's health bar into list
monster_health_list = []
monster_health_list.append(slime_health_list)
monster_health_list.append(zombie_health_list)
monster_health_list.append(zombie_boss_health_list)
monster_shield_list = []
monster_shield_list.append(slime_shield_list)
monster_shield_list.append(zombie_shield_list)
monster_shield_list.append(zombie_boss_shield_list)

#button
restart_button = Bars.Button(screen, 345, 120, reset_img, 120, 30)

def start_spawn():
	for count, monster in enumerate(monster_list[monster_index]):	
		monster.alive = True
		monster.hp = monster.max_hp
		monster.frame_index = monster.start_frame_index
		monster.action = monster.start_action		

def collide():
	global target
	global attack
	pygame.mouse.set_visible(True)
	mousex, mousey = pygame.mouse.get_pos()
	for count, monster in enumerate(monster_list[monster_index]):
		if monster.hitbox.collidepoint((mousex,mousey)):
			screen.blit(font.render('NAME:' + str(monster.name), True, blue), (mousex - 100, mousey - 40))
			screen.blit(font.render('STR:' + str(monster.strength), True, blue), (mousex - 100, mousey - 20))
			screen.blit(font.render('INT:' + str(monster.intelligence), True, blue), (mousex - 100, mousey))
			screen.blit(font.render('LUC:' + str(monster.luck), True, blue), (mousex - 100, mousey + 20))
			screen.blit(font.render('EVA:' + str(monster.evasion), True, blue), (mousex - 100, mousey + 40))
			screen.blit(font.render('ACC:' + str(monster.accuracy), True, blue), (mousex - 100, mousey + 60))
			screen.blit(font.render('DEF:' + str(monster.defense), True, blue), (mousex - 100, mousey + 80))
			screen.blit(font.render('SPD:' + str(monster.speed), True, blue), (mousex - 100, mousey + 100))
			#hide the mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse
			screen.blit(sword_img, (mousex - 10, mousey - 10))
			if click == True:
				attack = True
				target = monster_list[monster_index][count]

#drop item test
inventory = []
inventory.append(random.randint(4,8))

#skill active
fire_ball_active = False
guard_heal_active = False
cleave_active = False
zombie_stab_active = False

#events
event_1 = True

#skill turn counters
guardheal_turn_counter = 0
ruby_turn_counter = 0
fireball_turn_counter = 0
turn_counter = 0
speed_counter = 0

hero_turn = 0
hero_turn_threshold = 500
monster0_turn = 0
monster1_turn = 0
monster_turn_treshold = 500

battle_over = False

#sprites
fire_ball_sprite_group = pygame.sprite.Group()
guard_sprite_group = pygame.sprite.Group()
cleave_sprite_group = pygame.sprite.Group()
zombie_stab_sprite_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

#game#
monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list)
run = True
while run:
	#how fast the game runs
	clock.tick(fps)

	if monster_index != -1:
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
		#draw hero
		hero.update()
		hero.draw()
		#---------------------------#
		#draw each monster's health bar according to each spawned
		for count, monster_health_bar in enumerate(monster_health_list[monster_index]):
			monster_health_bar.draw(monster_list[monster_index][count].hp, monster_list[monster_index][count].max_hp)
		#draw monster shield bars
		for count, monster_shield_bar in enumerate(monster_shield_list[monster_index]):		
			monster_shield_bar.draw(monster_list[monster_index][count].shield, monster_list[monster_index][count].max_hp)
		#draw monsters
		for monster in monster_list[monster_index]:
			monster.update()
			monster.draw()
		#---------------------------#
		fire_ball_sprite_group.update()
		fire_ball_sprite_group.draw(screen)
		guard_sprite_group.update()
		guard_sprite_group.draw(screen)
		cleave_sprite_group.update()
		cleave_sprite_group.draw(screen)
		zombie_stab_sprite_group.update()
		zombie_stab_sprite_group.draw(screen)
		damage_text_group.update()
		damage_text_group.draw(screen)
		#---------------------------#
		#current attack picture
		Load_Interface.draw_current_attack(action_index, fire_ball_active, cleave_active, zombie_stab_active, inventory)
		#stats
		Load_Interface.stat_up(hero, monster_list, monster_index, font, screen_height, bottom_panel, screen, click, battle_over)
		#---------------------------#
		#default game variables
		attack = False
		target = None
		#---------------------------#
		#clicking on the target returns true value
		#make sure mouse is visible
		collide()
		#---------------------------#
		if monster_index == 2:
			total_turns = 3
		else:
			total_turns = 4
		#---------------------------#
		
		class Speed_Bar():
			def __init__(self, screen, turn, max_bar, x, y):
				self.x = x
				self.y = y
				self.turn = turn
				self.max_bar = max_bar

			def draw(self):
				ratio = self.turn / self.max_bar
				pygame.draw.rect(screen, red, (self.x, self.y, 100, 10))
				pygame.draw.rect(screen, yellow, (self.x, self.y, 100 * ratio, 10))					

		#hero speed portion
		hero_speed_bar = Speed_Bar(screen, hero_turn, hero_turn_threshold, 125, screen_height - bottom_panel)
		hero_speed_bar.draw()

		if hero.alive == True:
			if len(monster_list[monster_index]) == 1:
				if monster0_turn < monster_turn_treshold:
					if hero_turn < hero_turn_threshold:
						hero_turn += hero.speed
					if hero_turn > hero_turn_threshold:
						hero_turn = hero_turn_threshold
						if 8 in inventory:
							hero.hp += hero.hp_regen + hero.mp_regen
							heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen + hero.mp_regen), green)
						else:			
							hero.hp += hero.hp_regen	
							heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen), green)									
						damage_text_group.add(heal_text)
						if hero.hp > hero.max_hp:
							hero.hp = hero.max_hp	

			else:
				if monster_list[monster_index][0].alive == False:
					if monster1_turn < monster_turn_treshold:
						if hero_turn < hero_turn_threshold:
							hero_turn += hero.speed
						if hero_turn > hero_turn_threshold:
							hero_turn = hero_turn_threshold	
							if 8 in inventory:
								hero.hp += hero.hp_regen + hero.mp_regen
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen + hero.mp_regen), green)
							else:			
								hero.hp += hero.hp_regen	
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen), green)									
							damage_text_group.add(heal_text)
							if hero.hp > hero.max_hp:
								hero.hp = hero.max_hp						

				elif monster_list[monster_index][1].alive == False: 			
					if monster0_turn < monster_turn_treshold:
						if hero_turn < hero_turn_threshold:
							hero_turn += hero.speed
						if hero_turn > hero_turn_threshold:
							hero_turn = hero_turn_threshold	
							if 8 in inventory:
								hero.hp += hero.hp_regen + hero.mp_regen
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen + hero.mp_regen), green)
							else:			
								hero.hp += hero.hp_regen	
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen), green)									
							damage_text_group.add(heal_text)
							if hero.hp > hero.max_hp:
								hero.hp = hero.max_hp	

				else:
					if monster0_turn < monster_turn_treshold and monster1_turn < monster_turn_treshold:
						if hero_turn < hero_turn_threshold:
							hero_turn += hero.speed
						if hero_turn > hero_turn_threshold:
							hero_turn = hero_turn_threshold					
							if 8 in inventory:
								hero.hp += hero.hp_regen + hero.mp_regen
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen + hero.mp_regen), green)
							else:			
								hero.hp += hero.hp_regen	
								heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen), green)									
							damage_text_group.add(heal_text)
							if hero.hp > hero.max_hp:
								hero.hp = hero.max_hp	

		#monster speed portion
		if len(monster_list[monster_index]) == 1:
			monster0_speed_bar = Speed_Bar(screen, monster0_turn, monster_turn_treshold, 700 - 250 + 50, screen_height - bottom_panel)
			monster0_speed_bar.draw()					
		else:
			monster0_speed_bar = Speed_Bar(screen, monster0_turn, monster_turn_treshold, 700 - 250 + 25, screen_height - bottom_panel)
			monster1_speed_bar = Speed_Bar(screen, monster1_turn, monster_turn_treshold, 700 - 125 + 25, screen_height - bottom_panel)
			monster0_speed_bar.draw()
			monster1_speed_bar.draw()	

		if len(monster_list[monster_index]) == 1:
			#single monster
			if hero_turn < hero_turn_threshold:
				if monster0_turn < monster_turn_treshold:
					monster0_turn += monster_list[monster_index][0].speed
				if monster0_turn > monster_turn_treshold:
					monster0_turn = monster_turn_treshold
					monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
					heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
					damage_text_group.add(heal_text)
					if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
						monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

		else:
			#monster 1
			if monster_list[monster_index][0].alive == False:
				monster0_turn = 0
				if hero_turn < hero_turn_threshold:
					if monster1_turn < monster_turn_treshold:
						monster1_turn += monster_list[monster_index][1].speed
					if monster1_turn > monster_turn_treshold:
						monster1_turn = monster_turn_treshold
						monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
						heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
						damage_text_group.add(heal_text)
						if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
							monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp

			#monster 2
			if monster_list[monster_index][1].alive == False:
				monster1_turn = 0
				if hero_turn < hero_turn_threshold:
					if monster0_turn < monster_turn_treshold:
						monster0_turn += monster_list[monster_index][0].speed
					if monster0_turn > monster_turn_treshold:
						monster0_turn = monster_turn_treshold	
						monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
						heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
						damage_text_group.add(heal_text)
						if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
							monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

			else:
				if hero_turn < hero_turn_threshold and monster1_turn < monster_turn_treshold:
					if monster0_turn < monster_turn_treshold:
						monster0_turn += monster_list[monster_index][0].speed
					if monster0_turn > monster_turn_treshold:
						monster0_turn = monster_turn_treshold					
						monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
						heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
						damage_text_group.add(heal_text)
						if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
							monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

				if hero_turn < hero_turn_threshold and monster0_turn < monster_turn_treshold:
					if monster1_turn < monster_turn_treshold:
						monster1_turn += monster_list[monster_index][1].speed
					if monster1_turn > monster_turn_treshold:
						monster1_turn = monster_turn_treshold		
						monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
						heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][1].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
						damage_text_group.add(heal_text)
						if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
							monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp

		#enemy action
		#single enemy
		if hero.alive != False and hero.hp > 0 and monster0_turn >= monster_turn_treshold and len(monster_list[monster_index]) == 1:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				roll_guard_chance = random.randint(0,100)
				if monster_list[monster_index][0].alive != False:
					if monster_list[monster_index][0].hp < monster_list[monster_index][0].max_hp * 0.2 or roll_guard_chance > 70:
						monster_list[monster_index][0].guard(guard_sprite_group, damage_text_group, guard_heal_active)
					monster_list[monster_index][0].attack(hero, damage_text_group, inventory)
					action_cooldown = 0
					monster0_turn = 0	
			if monster_list[monster_index][0].alive == False:
				 monster_list[monster_index][0].death()

		#two enemies
		if hero.alive != False and hero.hp > 0 and monster0_turn >= monster_turn_treshold and len(monster_list[monster_index]) == 2 and monster_list[monster_index][0].alive == True:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#monster guard
				roll_guard_chance = random.randint(0,100)
				if monster_list[monster_index][0].hp < monster_list[monster_index][0].max_hp * 0.2 or roll_guard_chance > 50:
					monster_list[monster_index][0].guard(guard_sprite_group, damage_text_group, guard_heal_active)

				#monster skills
				if monster_index == 0 and hero.shield > 0 and random.randint(0,100) > 30:
					monster_list[monster_index][0].armor_corrosion(hero, damage_text_group, inventory)
				elif monster_index == 1 and random.randint(0,100) > 50:
					monster_list[monster_index][0].toxic_bile(hero, damage_text_group, inventory)
				else:
					monster_list[monster_index][0].attack(hero, damage_text_group, inventory)

				action_cooldown = 0
				monster0_turn = 0		
			if monster_list[monster_index][0].alive == False:
				 monster_list[monster_index][0].death()

		if hero.alive != False and hero.hp > 0 and monster1_turn >= monster_turn_treshold and len(monster_list[monster_index]) == 2 and monster_list[monster_index][1].alive == True:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#monster guard
				roll_guard_chance = random.randint(0,100)
				if monster_list[monster_index][1].hp < monster_list[monster_index][1].max_hp * 0.2 or roll_guard_chance > 70:
					monster_list[monster_index][1].guard(guard_sprite_group, damage_text_group, guard_heal_active)

				#monster skills	
				if monster_index == 0 and hero.shield > 0 and random.randint(0,100) > 10:
					monster_list[monster_index][1].armor_corrosion(hero, damage_text_group, inventory)
				elif monster_index == 1 and random.randint(0,100) > 50:
					monster_list[monster_index][1].toxic_bile(hero, damage_text_group, inventory)
				else:
					monster_list[monster_index][1].attack(hero, damage_text_group, inventory)

				action_cooldown = 0
				monster1_turn = 0			
			if monster_list[monster_index][1].alive == False:
				 monster_list[monster_index][1].death()

		#player action
		if game_over == 0 and hero.alive == True and hero_turn >= hero_turn_threshold:
			action_cooldown += 1

			if 6 in inventory and guardheal_turn_counter == 0:
				hero.guard(guard_sprite_group, damage_text_group, guard_heal_active)
				guardheal_turn_counter += 1

			if 9 in inventory and fireball_turn_counter == 0:
				target = monster_list[monster_index][0]
				hero.mini_fire_ball_attack(current_fighter, action_cooldown, target, monster, monster_list, monster_index, experiencethreshold, fire_ball_sprite_group, damage_text_group, inventory)
				Screen_Menus.drop_items(monster, hero, inventory)
				if target.alive == False:
					hero.gold += target.gold
				fireball_turn_counter += 1

			if action_cooldown >= action_wait_time:
				#look for player action

				#attack
				if attack == True and target != None and target.alive and action_index == 0:
					hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group, inventory)
					Screen_Menus.drop_items(monster, hero, inventory, monster_list, monster_index)
					if target.alive == False:
						hero.gold += target.gold
					turn_counter += 1
					hero_turn = 0
					action_cooldown = 0

				#guard
				if click == True and action_index == 1:
					hero.guard(guard_sprite_group, damage_text_group, guard_heal_active)
					turn_counter += 1
					hero_turn = 0
					action_cooldown = 0

				#fireball
				if attack == True and target != None and target.alive and action_index == 2:
					if hero.mp < 5:
						hero.normal_attack(current_fighter, action_cooldown, target, experiencethreshold, damage_text_group, inventory)
						Screen_Menus.drop_items(monster, hero, inventory, monster_list, monster_index)
						if target.alive == False:
							hero.gold += target.gold
					else:
						hero.fire_ball_attack(current_fighter, action_cooldown, target, monster, monster_list, monster_index, experiencethreshold, fire_ball_sprite_group, damage_text_group, inventory)
						Screen_Menus.drop_items(monster, hero, inventory, monster_list, monster_index)
						if target.alive == False:
							hero.gold += target.gold
					turn_counter += 1
					hero_turn = 0
					action_cooldown = 0

				#cleave
				if attack == True and target != None and target.alive and action_index == 3:
					hero.cleave(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, cleave_active, cleave_sprite_group)
					Screen_Menus.drop_items(monster, hero, inventory, monster_list, monster_index)
					for target in monster_list[monster_index]:
						if target.alive == False:
							hero.gold += target.gold
					turn_counter += 1
					hero_turn = 0
					action_cooldown = 0

				#zombie stab
				if attack == True and target != None and target.alive and action_index == 4:
					hero.zombie_stab(target, damage_text_group, inventory, monster_list, monster_index, experiencethreshold, zombie_stab_active, zombie_stab_sprite_group)
					Screen_Menus.drop_items(monster, hero, inventory, monster_list, monster_index)
					for target in monster_list[monster_index]:
						if target.alive == False:
							hero.gold += target.gold
					turn_counter += 1
					hero_turn = 0
					action_cooldown = 0

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
	if game_over != 0 and monster_index != -1:
		if game_over == 1:
			screen.blit(victory_img, ((screen_width / 2) - 120, 50))
			battle_over = True
			if restart_button.draw():
				if hero.mp < hero.max_mp:
					hero.mp += hero.mp_regen
				#reset shield
				hero.shield = 0
				#reset skill counters
				turn_counter = 0
				guardheal_turn_counter = 0
				ruby_turn_counter = 0
				fireball_turn_counter = 0
				hero_turn = 0
				monster0_turn = 0
				monster1_turn = 0
				#trigger level up event	
				if hero.level % 1 == 0 and event_1 == True:
					fire_ball_active, guard_heal_active, cleave_active = Level_Events.lvl_up_event_1(hero, monster, monster_list, monster_index)
					event_1 = False
				#platformer map menu
				monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_list)
				#trigger events if move to next map
				if monster_encounter == False:
					random_event_index = random.randint(0,1)
					roll_event_chance = random.randint(0,100)
					if roll_event_chance > 0:
						Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)
				#reset spawns and monsters			
				start_spawn()
				for i in range(len(monster_list)):
					for monster in monster_list[i]:
						monster.level_up_monster(hero)
				if 14 in inventory:
					zombie_stab_active = True
				battle_over = False
				current_fighter = 1
				action_cooldown = 0
				game_over = 0

		if game_over == -1:
			screen.blit(defeat_img, ((screen_width / 2) - 120, 50))
			if restart_button.draw():
				run = False
				sys.exit()

	elif monster_index == -1:
		monster_index, monster_encounter, game_map = Map.platformer_menu(monster_index, hero, inventory, monster_lists)
		if monster_encounter == False:
			random_event_index = random.randint(0,1)
			roll_event_chance = random.randint(0,100)
			if roll_event_chance > 0:
				Events.game_event_list[random_event_index](hero, monster, monster_list, monster_index)			
		start_spawn()
		current_fighter = 1
		action_cooldown = 0
		game_over = 0

	click = False
	
	#check for events ex. mouse clicks, key down etc.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			click = True
		if event.type == pygame.MOUSEBUTTONUP:
			click = False
		if event.type == pygame.KEYDOWN:
				#stats
			if event.key == pygame.K_KP1:
				if hero.statpoints > 0:
					hero.str_up_button()
			if event.key == pygame.K_KP2:
				if hero.statpoints > 0:
					hero.int_up_button()
			if event.key == pygame.K_KP3:
				if hero.statpoints > 0:				
					hero.luc_up_button()
			if event.key == pygame.K_KP4:
				if hero.statpoints > 0:
					hero.acc_up_button()
			if event.key == pygame.K_KP5:
				if hero.statpoints > 0:				
					hero.eva_up_button()
				#skills
			if event.key == pygame.K_1:
				action_index = 0
			if event.key == pygame.K_2:
				action_index = 1
			if fire_ball_active == True and event.key == pygame.K_3:
				action_index = 2
			if cleave_active == True and event.key == pygame.K_4:
				action_index = 3
			if zombie_stab_active == True and event.key == pygame.K_5:
				action_index = 4

				#inventory
			if event.key == pygame.K_r:
				Screen_Menus.options_menu(inventory, monster_list, monster_index)
				
	pygame.display.update()

pygame.quit()

#print