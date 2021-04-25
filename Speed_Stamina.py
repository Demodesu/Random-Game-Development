import math, pygame, random, sys, csv, Load_Interface, Character, Bars, Screen_Menus, Map, Events, Level_Events

bottom_panel = 150
screen_width, screen_height = 800, 400 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))
#fonts
font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', 10)
#define colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
black = (0,0,0)

def turn_calculations(hero_turn_amount, hero_turn_amount_threshold, hero_stamina_amount, hero_stamina_recover_amount, hero_stamina_amount_threshold, boost, monster0_turn_amount, monster1_turn_amount, monster_turn_amount_threshold, hero, monster, monster_list, monster_index, inventory, damage_text_group, over_usage_amount, over_usage_amount_max):
	
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

	class Stamina_Bar():
		def __init__(self, screen, stamina, max_bar, x, y, over_usage_amount, over_usage_amount_max_bar):
			self.x = x
			self.y = y
			self.stamina = stamina
			self.max_bar = max_bar
			self.over_usage_amount = over_usage_amount
			self.over_usage_amount_max_bar = over_usage_amount_max_bar

		def draw(self):
			ratio = self.stamina / self.max_bar
			over_usage_amount_ratio = self.over_usage_amount / self.over_usage_amount_max_bar
			pygame.draw.rect(screen, red, (self.x, self.y, 100, 10))
			pygame.draw.rect(screen, orange, (self.x, self.y, 100 * ratio, 10))	
			pygame.draw.rect(screen, red, (self.x, self.y - 10, 100, 10))
			pygame.draw.rect(screen, black, (self.x, self.y - 10, 100 * over_usage_amount_ratio, 10))

	#hero speed portion
	hero_turn_amount_bar = Speed_Bar(screen, hero_turn_amount, hero_turn_amount_threshold, 125, screen_height - bottom_panel)
	hero_turn_amount_bar.draw()
	hero_stamina_amount_bar = Stamina_Bar(screen, hero_stamina_amount, hero_stamina_amount_threshold, 125, screen_height - bottom_panel - 10, over_usage_amount, over_usage_amount_max)
	hero_stamina_amount_bar.draw()

	#monster speed portion
	if len(monster_list[monster_index]) == 1:
			monster0_speed_bar = Speed_Bar(screen, monster0_turn_amount, monster_turn_amount_threshold, 700 - 250 + 50, screen_height - bottom_panel)
			monster0_speed_bar.draw()					
	else:
		monster0_speed_bar = Speed_Bar(screen, monster0_turn_amount, monster_turn_amount_threshold, 700 - 250 + 25, screen_height - bottom_panel)
		monster1_speed_bar = Speed_Bar(screen, monster1_turn_amount, monster_turn_amount_threshold, 700 - 125 + 25, screen_height - bottom_panel)
		monster0_speed_bar.draw()
		monster1_speed_bar.draw()	

	#hero stamina and turn
	if boost == True and hero_turn_amount + hero_stamina_recover_amount < hero_turn_amount_threshold and hero_stamina_amount > 0:
		if len(monster_list[monster_index]) == 1:
			if monster0_turn_amount < monster_turn_amount_threshold:
				hero_stamina_amount -= 5
				hero_turn_amount += 5
				over_usage_amount += 5

		else:
			if monster0_turn_amount < monster_turn_amount_threshold and monster1_turn_amount < monster_turn_amount_threshold:
				hero_stamina_amount -= 5
				hero_turn_amount += 5
				over_usage_amount += 5	

		if over_usage_amount > over_usage_amount_max:
			over_usage_amount = 0
			hero.hp -= math.floor(hero.max_hp / 4)	
			if hero.hp < 1:
				hero.hp = 0
				hero.alive = False
				hero.death()	

	if hero_stamina_amount < hero_stamina_amount_threshold and boost == False:
		if len(monster_list[monster_index]) == 1:
			if monster0_turn_amount < monster_turn_amount_threshold and hero_turn_amount < hero_turn_amount_threshold:
				hero_stamina_amount += hero_stamina_recover_amount

		else:
			if monster0_turn_amount < monster_turn_amount_threshold and monster1_turn_amount < monster_turn_amount_threshold and hero_turn_amount < hero_turn_amount_threshold:
				hero_stamina_amount += hero_stamina_recover_amount

		if hero_stamina_amount > hero_stamina_amount_threshold:
			hero_stamina_amount = hero_stamina_amount_threshold

	over_usage_amount -= 0.1
	if over_usage_amount < 0:
		over_usage_amount = 0

	if hero.alive == True:
		if len(monster_list[monster_index]) == 1:
			if monster0_turn_amount < monster_turn_amount_threshold:
				if hero_turn_amount < hero_turn_amount_threshold:
					hero_turn_amount += hero.speed
				if hero_turn_amount > hero_turn_amount_threshold:
					hero_turn_amount = hero_turn_amount_threshold
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
				if monster1_turn_amount < monster_turn_amount_threshold:
					if hero_turn_amount < hero_turn_amount_threshold:
						hero_turn_amount += hero.speed
					if hero_turn_amount > hero_turn_amount_threshold:
						hero_turn_amount = hero_turn_amount_threshold	
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
				if monster0_turn_amount < monster_turn_amount_threshold:
					if hero_turn_amount < hero_turn_amount_threshold:
						hero_turn_amount += hero.speed
					if hero_turn_amount > hero_turn_amount_threshold:
						hero_turn_amount = hero_turn_amount_threshold	
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
				if monster0_turn_amount < monster_turn_amount_threshold and monster1_turn_amount < monster_turn_amount_threshold:
					if hero_turn_amount < hero_turn_amount_threshold:
						hero_turn_amount += hero.speed
					if hero_turn_amount > hero_turn_amount_threshold:
						hero_turn_amount = hero_turn_amount_threshold					
						if 8 in inventory:
							hero.hp += hero.hp_regen + hero.mp_regen
							heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen + hero.mp_regen), green)
						else:			
							hero.hp += hero.hp_regen	
							heal_text = Character.Damage_Text((hero.hitbox.x + hero.hitbox.width / 2), hero.hitbox.y - 60, str(hero.hp_regen), green)									
						damage_text_group.add(heal_text)
						if hero.hp > hero.max_hp:
							hero.hp = hero.max_hp	

	#single monster
	if len(monster_list[monster_index]) == 1:
		if hero_turn_amount < hero_turn_amount_threshold:
			if monster0_turn_amount < monster_turn_amount_threshold:
				monster0_turn_amount += monster_list[monster_index][0].speed
			if monster0_turn_amount > monster_turn_amount_threshold:
				monster0_turn_amount = monster_turn_amount_threshold
				monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
				heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
				damage_text_group.add(heal_text)
				if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
					monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

	else:
		#monster 1
		if monster_list[monster_index][0].alive == False:
			monster0_turn_amount = 0
			if hero_turn_amount < hero_turn_amount_threshold:
				if monster1_turn_amount < monster_turn_amount_threshold:
					monster1_turn_amount += monster_list[monster_index][1].speed
				if monster1_turn_amount > monster_turn_amount_threshold:
					monster1_turn_amount = monster_turn_amount_threshold
					monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
					heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
					damage_text_group.add(heal_text)
					if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
						monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp

		#monster 2
		if monster_list[monster_index][1].alive == False:
			monster1_turn_amount = 0
			if hero_turn_amount < hero_turn_amount_threshold:
				if monster0_turn_amount < monster_turn_amount_threshold:
					monster0_turn_amount += monster_list[monster_index][0].speed
				if monster0_turn_amount > monster_turn_amount_threshold:
					monster0_turn_amount = monster_turn_amount_threshold	
					monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
					heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
					damage_text_group.add(heal_text)
					if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
						monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

		else:
			if hero_turn_amount < hero_turn_amount_threshold and monster1_turn_amount < monster_turn_amount_threshold:
				if monster0_turn_amount < monster_turn_amount_threshold:
					monster0_turn_amount += monster_list[monster_index][0].speed
				if monster0_turn_amount > monster_turn_amount_threshold:
					monster0_turn_amount = monster_turn_amount_threshold					
					monster_list[monster_index][0].hp += monster_list[monster_index][0].hp_regen
					heal_text = Character.Damage_Text((monster_list[monster_index][0].hitbox.x + monster_list[monster_index][0].hitbox.width / 2), monster_list[monster_index][0].hitbox.y - 60, str(monster_list[monster_index][0].hp_regen), green)
					damage_text_group.add(heal_text)
					if monster_list[monster_index][0].hp > monster_list[monster_index][0].max_hp:
						monster_list[monster_index][0].hp = monster_list[monster_index][0].max_hp

			if hero_turn_amount < hero_turn_amount_threshold and monster0_turn_amount < monster_turn_amount_threshold:
				if monster1_turn_amount < monster_turn_amount_threshold:
					monster1_turn_amount += monster_list[monster_index][1].speed
				if monster1_turn_amount > monster_turn_amount_threshold:
					monster1_turn_amount = monster_turn_amount_threshold		
					monster_list[monster_index][1].hp += monster_list[monster_index][1].hp_regen
					heal_text = Character.Damage_Text((monster_list[monster_index][1].hitbox.x + monster_list[monster_index][1].hitbox.width / 2), monster_list[monster_index][1].hitbox.y - 60, str(monster_list[monster_index][1].hp_regen), green)
					damage_text_group.add(heal_text)
					if monster_list[monster_index][1].hp > monster_list[monster_index][1].max_hp:
						monster_list[monster_index][1].hp = monster_list[monster_index][1].max_hp

	return hero_turn_amount, hero_stamina_amount, monster0_turn_amount, monster1_turn_amount, over_usage_amount