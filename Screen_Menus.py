import math, pygame, random, sys, Character

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
inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(44,44))
active_skills_hitbox_img = pygame.image.load('Images/Icon/SkillIcons/ActiveButtons.png').convert_alpha()
active_skills_hitbox_img = pygame.transform.scale(active_skills_hitbox_img,(30,30))

def draw_text(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
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
items = {
#combined items
'razor_shield' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics0.png').convert_alpha(), 'description' : 'Return 80% Normal Attack Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -1, 'name' : 'Razor Shield', 'components' : 'Razor Mail + Shield'},
'eclipse_capsule' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics1.png').convert_alpha(), 'description' : 'Lightning Turns To Eclipse Beam (Restore 25% MP And HP, 2 Times Damage)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -2, 'name' : 'Eclipse Capsule', 'components' : 'Moon Capsule + Sun Capsule'},
'blood_hibiscus' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics2.png').convert_alpha(), 'description' : 'Restores HP From 10% Bleed Damage, Bleed Percentage Changed To 3.5%', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -3, 'name' : 'Blood Hibiscus', 'components' : 'Blood Mosquitop + Jungle Hibiscus'},
'yin_and_yang' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics3.png').convert_alpha(), 'description' : 'Move Attack Always Deals 150% Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -4, 'name' : 'Yin And Yang', 'components' : 'Yin + Yang'},
'dragon_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics4.png').convert_alpha(), 'description' : 'Attack Twice Every 2 Turns', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -5, 'name' : 'Dragon Claw', 'components' : 'Dragon Eye + Raptor Claw'},
'windy_feather' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics5.png').convert_alpha(), 'description' : 'Turn Threshold -100', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -6, 'name' : 'Windy Feather', 'components' : 'Stunted Tornado + Feather'},
'black_hole' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics6.png').convert_alpha(), 'description' : 'Each Level Max HP +4', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -7, 'name' : 'Black Hole', 'components' : 'Grey Opal + Dark Matter'},
'charged_obsidian' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics7.png').convert_alpha(), 'description' : 'Lightning Start Of Turn, INT +3', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -8, 'name' : 'Charged Obsidian', 'components' : 'Infernal Obsidian + Lightning Stone'},
'dwarfed_phoenix' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics8.png').convert_alpha(), 'description' : 'Move Triggers Spark', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -9, 'name' : 'Dwarfed Phoenix', 'components' : 'Fire Crow + Phoenix Feather'},
'stone_drum' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics9.png').convert_alpha(), 'description' : 'Stomp Decreases Turn Bar By 30% (25% For Boss), END +3 Temporarily', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -10, 'name' : 'Stone Drum', 'components' : 'Stone Bracelet + War Drum'},
'hydra_heart' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics10.png').convert_alpha(), 'description' : 'Deals Lost HP As Damage (Max 200) Every 4 Seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -11, 'name' : 'Hydra Heart', 'components' : 'Bahamut Heart + Hydro Vortex'},
'blue_ruby' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics11.png').convert_alpha(), 'description' : 'Auto Regen Every 3 Seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -12, 'name' : 'Blue Ruby', 'components' : 'Mist Stone + Ruby'},
'ouroboros' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics12.png').convert_alpha(), 'description' : 'Unlocks Serpent Wheel', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -13, 'name' : 'Ouroboros', 'components' : 'Dragon Eye + Crimson Head Snake'},
'whip_of_akhlys' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics13.png').convert_alpha(), 'description' : 'Unlocks Venomous Whip', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -14, 'name' : 'Whip Of Akhlys', 'components' : 'Posion Ivy + Glow Fern'},
'thunder_kunai' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics14.png').convert_alpha(), 'description' : 'Unlocks Thunder Bolt', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -15, 'name' : 'Thunder Kunai', 'components' : 'Thunder Charge + Kunai'},
#'condensed_ectoplasm' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics15.png').convert_alpha(), 'description' : 'Ghost Companion Attacks For 20% Hero STR Every 5 seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -16, 'name' : 'Condensed Ectoplasm', 'components' : 'Condensed Lightning + Pocket Ghost'},

#normal items
'ring_of_health' : {'image' : pygame.image.load('Images/Icon/Relics/Relics0.png').convert_alpha(), 'description' : 'Max HP +3', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 0, 'name' : 'Ring Of Health'},
'raptor_claw' : {'image' : pygame.image.load('Images/Icon/Relics/Relics1.png').convert_alpha(), 'description' : 'STR +1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 1, 'name' : 'Raptor Claw'},
'four_leaf_clover' : {'image' : pygame.image.load('Images/Icon/Relics/Relics2.png').convert_alpha(), 'description' : 'LUC +1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 2, 'name' : 'Four Leaf Clover'},
'feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics3.png').convert_alpha(), 'description' : 'SPD +0.25', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 3, 'name' : 'Feather'},
'eye_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Relics/Relics4.png').convert_alpha(), 'description' : 'Lifesteal 10% Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 4, 'name' : 'Eye Of Vladimir', 'cost' : 1250 + random.randint(-250,250)},
'condensed_lightning' : {'image' : pygame.image.load('Images/Icon/Relics/Relics5.png').convert_alpha(), 'description' : 'Fireball Damage * 1.75, INT +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 5, 'name' : 'Condensed Lightning', 'cost' : 1500 + random.randint(-250,250)},
'shield' : {'image' : pygame.image.load('Images/Icon/Relics/Relics6.png').convert_alpha(), 'description' : 'Auto Guard After Some Turns, DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 6, 'name' : 'Shield', 'cost' : 1500 + random.randint(-250,250)},
'razor_mail' : {'image' : pygame.image.load('Images/Icon/Relics/Relics7.png').convert_alpha(), 'description' : 'Return 25% DEF + 15% Enemy Normal Attack Damage, DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 7, 'name' : 'Razor Mail', 'cost' : 1500 + random.randint(-250,250)},
'ruby' : {'image' : pygame.image.load('Images/Icon/Relics/Relics8.png').convert_alpha(), 'description' : 'MP Regen Added To HP Regen', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 8, 'name' : 'Ruby', 'cost' : 1250 + random.randint(-250,250)},
'infernal_obsidian' : {'image' : pygame.image.load('Images/Icon/Relics/Relics9.png').convert_alpha(), 'description' : 'Fireball Start Of Turn', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 9, 'name' : 'Infernal Obsidian', 'cost' : 1750 + random.randint(-250,250)},
'mist_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics10.png').convert_alpha(), 'description' : 'Hero MP Regen + 2, Max MP +5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 10, 'name' : 'Mist Stone', 'cost' : 1500 + random.randint(-250,250)},
'slime_ball' : {'image' : pygame.image.load('Images/Icon/Relics/Relics11.png').convert_alpha(), 'description' : 'All Monster SPD -0.5', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 11, 'name' : 'Slime Ball'},
'crimson_head_snake' : {'image' : pygame.image.load('Images/Icon/Relics/Relics12.png').convert_alpha(), 'description' : 'All Monster HP Regen -1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 12, 'name' : 'Crimson Head Snake'},
'stunted_tornado' : {'image' : pygame.image.load('Images/Icon/Relics/Relics13.png').convert_alpha(), 'description' : 'Hero SPD + 1.5, AGI +1.5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 13, 'name' : 'Stunted Tornado', 'cost' : 1500 + random.randint(-250,250)},
'zombie_spine' : {'image' : pygame.image.load('Images/Icon/Relics/Relics14.png').convert_alpha(), 'description' : 'Unlocks Zombie Stab', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 14, 'name' : 'Zombie Spine'},
'thunder_charge' : {'image' : pygame.image.load('Images/Icon/Relics/Relics15.png').convert_alpha(), 'description' : 'Hero Stamina Recovery +0.5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 15, 'name' : 'Thunder Charge', 'cost' : 1250 + random.randint(-250,250)},
'fluffy_cloud' : {'image' : pygame.image.load('Images/Icon/Relics/Relics16.png').convert_alpha(), 'description' : 'Hero Stamina Recovery +0.25, SPD +0.25', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 16, 'name' : 'Fluffy Cloud'},
'grey_opal' : {'image' : pygame.image.load('Images/Icon/Relics/Relics17.png').convert_alpha(), 'description' : 'Stamina Threshold -50', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 17, 'name' : 'Grey Opal'},
'dragon_eye' : {'image' : pygame.image.load('Images/Icon/Relics/Relics18.png').convert_alpha(), 'description' : 'Attack Twice Every 3 Turns', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 18, 'name' : 'Dragon Eye', 'cost' : 1750 + random.randint(-250,250)},
'hydro_vortex' : {'image' : pygame.image.load('Images/Icon/Relics/Relics19.png').convert_alpha(), 'description' : 'Absorbs 15% Normal Attack Damage As HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 19, 'name' : 'Hydro Vortex', 'cost' : 1250 + random.randint(-250,250)},
'kunai' : {'image' : pygame.image.load('Images/Icon/Relics/Relics20.png').convert_alpha(), 'description' : 'Counter With Full Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 20, 'name' : 'Kunai', 'cost' : 1500 + random.randint(-250,250)},
'stone_bracelet' : {'image' : pygame.image.load('Images/Icon/Relics/Relics21.png').convert_alpha(), 'description' : 'All Monster SPD -2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 21, 'name' : 'Stone Bracelet', 'cost' : 1500 + random.randint(-250,250)},
'dark_matter' : {'image' : pygame.image.load('Images/Icon/Relics/Relics22.png').convert_alpha(), 'description' : 'All Monster DEF -2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 22, 'name' : 'Dark Matter'},
'lightning_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics23.png').convert_alpha(), 'description' : 'Hero Stamina Recover +2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 23, 'name' : 'Lightning Stone', 'cost' : 1750 + random.randint(-250,250)},
'war_drum' : {'image' : pygame.image.load('Images/Icon/Relics/Relics24.png').convert_alpha(), 'description' : 'Stomp Every 8 Seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 24, 'name' : 'War Drum', 'cost' : 1750 + random.randint(-250,250)},
'glow_fern' : {'image' : pygame.image.load('Images/Icon/Relics/Relics25.png').convert_alpha(), 'description' : 'Hero HP Regen +10', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 25, 'name' : 'Glow Fern', 'cost' : 1750 + random.randint(-250,250)},
'grimoire' : {'image' : pygame.image.load('Images/Icon/Relics/Relics26.png').convert_alpha(), 'description' : 'All Monster HP -20% Hero INT Every End Turn', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 26, 'name' : 'Grimoire', 'cost' : 1750 + random.randint(-250,250)},
'bahamut_heart' : {'image' : pygame.image.load('Images/Icon/Relics/Relics27.png').convert_alpha(), 'description' : 'Hero END +5, DEF +3 HP Regen +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 27, 'name' : 'Bahamut Heart', 'cost' : 1750 + random.randint(-250,250)},
'phoenix_feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics28.png').convert_alpha(), 'description' : 'Hero Revives With 50% HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 28, 'name' : 'Phoenix Feather', 'cost' : 2250 + random.randint(-250,250)},
'pocket_ghost' : {'image' : pygame.image.load('Images/Icon/Relics/Relics29.png').convert_alpha(), 'description' : 'All Monster STR -4', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 29, 'name' : 'Pocket Ghost', 'cost' : 1750 + random.randint(-250,250)},
'poison_ivy' : {'image' : pygame.image.load('Images/Icon/Relics/Relics30.png').convert_alpha(), 'description' : 'All Monster HP Regen -4', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 30, 'name' : 'Poison Ivy', 'cost' : 1750 + random.randint(-250,250)},
'hasai_and_hyo' : {'image' : pygame.image.load('Images/Icon/Relics/Relics31.png').convert_alpha(), 'description' : 'Fireball Turns To Sapphire Flame (Steals 20% Turn), Hero INT +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 31, 'name' : 'Hasai And Hyo', 'cost' : 1750 + random.randint(-250,250)},
'yang' : {'image' : pygame.image.load('Images/Icon/Relics/Relics32.png').convert_alpha(), 'description' : 'Move Forward Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 32, 'name' : 'Yang', 'cost' : 1750 + random.randint(-250,250)},
'yin' : {'image' : pygame.image.load('Images/Icon/Relics/Relics33.png').convert_alpha(), 'description' : 'Move Back Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 33, 'name' : 'Yin', 'cost' : 1750 + random.randint(-250,250)},
'blood_mosquito' : {'image' : pygame.image.load('Images/Icon/Relics/Relics34.png').convert_alpha(), 'description' : 'Bleeds Enemy When Counter', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 34, 'name' : 'Blood Mosquito', 'cost' : 1750 + random.randint(-250,250)},
'fire_crow' : {'image' : pygame.image.load('Images/Icon/Relics/Relics35.png').convert_alpha(), 'description' : 'Spark When Attacked', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 35, 'name' : 'Fire Crow', 'cost' : 1500 + random.randint(-250,250)},
'moon_capsule' : {'image' : pygame.image.load('Images/Icon/Relics/Relics36.png').convert_alpha(), 'description' : 'Lightning Turns To Lunar Beam (Restore 25% MP)', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 36, 'name' : 'Moon Capsule', 'cost' : 1500 + random.randint(-250,250)},
'sun_capsule' : {'image' : pygame.image.load('Images/Icon/Relics/Relics37.png').convert_alpha(), 'description' : 'Lightning Turns To Solar Beam (Restore 25% HP)', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 37, 'name' : 'Sun Capsule', 'cost' : 1500 + random.randint(-250,250)},
'jungle_hibiscus' : {'image' : pygame.image.load('Images/Icon/Relics/Relics38.png').convert_alpha(), 'description' : 'Moving Recovers 1% Max HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 38, 'name' : 'Jungle Hibiscus', 'cost' : 1750 + random.randint(-250,250)},
'red_bean' : {'image' : pygame.image.load('Images/Icon/Relics/Relics39.png').convert_alpha(), 'description' : 'Hero DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 39, 'name' : 'Red Bean'},
'golden_sand' : {'image' : pygame.image.load('Images/Icon/Relics/Relics40.png').convert_alpha(), 'description' : 'Hero END +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 40, 'name' : 'Golden Sand'},

}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather', 'eye_of_vladimir',
'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 
'slime_ball', 'crimson_head_snake', 'stunted_tornado', 'zombie_spine', 'thunder_charge', 
'fluffy_cloud', 'grey_opal', 'dragon_eye', 'hydro_vortex', 'kunai', 'stone_bracelet', 'dark_matter', 
'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 'phoenix_feather', 'pocket_ghost', 
'poison_ivy', 'hasai_and_hyo', 'yang', 'yin', 'blood_mosquito', 'fire_crow', 'moon_capsule', 'sun_capsule', 
'jungle_hibiscus', 'red_bean', 'golden_sand', 'razor_shield', 'eclipse_capsule', 'blood_hibiscus', 'yin_and_yang',
'dragon_claw', 'windy_feather', 'black_hole', 'charged_obsidian', 'dwarfed_phoenix', 'stone_drum', 'hydra_heart',
'blue_ruby', 'ouroboros', 'whip_of_akhlys', 'thunder_kunai']

original_shop_names_list = ['eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 
'infernal_obsidian', 'mist_stone', 'stunted_tornado', 'thunder_charge', 'dragon_eye', 'hydro_vortex', 
'kunai', 'stone_bracelet', 'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 
'phoenix_feather', 'pocket_ghost', 'poison_ivy', 'hasai_and_hyo', 'yang', 'yin', 'blood_mosquito', 
'fire_crow', 'moon_capsule', 'sun_capsule', 'jungle_hibiscus']

purchased_list = []

shop_names_list = []

def reset_items_in_shop(original_shop_names_list, purchased_list, inventory):
	shop_names_list = []
	if len(inventory) == 0:
		random_shop_item_amount = 10
	else:
		random_shop_item_amount = random.randint(7,8)
	#random shop items start of game
	appending = True
	while appending:
		random_append = random.randint(0,len(original_shop_names_list) - 1)
		item = original_shop_names_list[random_append]
		if len(inventory) != len(original_shop_names_list):
			if item not in shop_names_list and items[item]['index'] not in inventory:
				shop_names_list.append(original_shop_names_list[random_append])
				if len(original_shop_names_list) - len(purchased_list) >= random_shop_item_amount:
					if len(shop_names_list) == random_shop_item_amount:
						appending = False
						return shop_names_list
				if len(original_shop_names_list) - len(purchased_list) < random_shop_item_amount:
					if len(shop_names_list) == len(original_shop_names_list) - len(purchased_list):
						appending = False
						return shop_names_list
		else:
			appending = False
			return shop_names_list			

#option loop#
def options_menu(inventory, monster_list, monster_index, hero, skills_list, active_skills_list, all_active_skills_list):

	skills = {
	'guard' : {'name' : 'Guard','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons0.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain Shield Equal To 20% Max HP + 300% DEF Every 5 Seconds', 'calculation' : f'{(hero.max_hp * 0.3) + (hero.defense * 3):.2f}', 'cost' : '50% MAX STA', 'key_name' : 'guard'},
	'stomp' : {'name' : 'Stomp','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons1.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'All Enemy Turn -20% (Boss -15%) Every 5 Seconds', 'calculation' : f'None', 'cost' : '50% MAX STA', 'key_name' : 'stomp'},
	'start_lightning' : {'name' : 'Start Lightning','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons2.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain 1 Lightning End Of Combat If No Charges Are Left', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'start_lightning'},
	'start_fireball' : {'name' : 'Start Fireball','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons3.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain 1 Fireball End Of Combat If No Charges Are Left', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'start_fireball'},
	'cleave' : {'name' : 'Cleave','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons4.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks All Enemies', 'calculation' : f'{hero.strength:.2f} + Random Damage', 'cost' : '7.5MP', 'key_name' : 'cleave'},
	'triple_combo' : {'name' : 'Triple Combo','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons5.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks Head, Body, and Legs 1 time', 'calculation' : f'{hero.strength * 0.75:.2f}', 'cost' : '10MP', 'key_name' : 'triple_combo'},
	'guard_heal' : {'name' : 'Guard Heal','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons6.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Heals For 5% Max HP + 50% DEF', 'calculation' : f'{(hero.max_hp * 0.05) + (hero.defense * 0.5):.2f}', 'cost' : 'None', 'key_name' : 'guard_heal'},
	'guard_slash' : {'name' : 'Guard Slash','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons7.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Also Attacks', 'calculation' : f'{hero.strength:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'guard_slash'},
	'guard_rush' : {'name' : 'Guard Rush','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons8.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Turn +25%', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'guard_rush'},
	'stomp_buff' : {'name' : 'Stomp Buff','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons9.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Increases STR +2, AGI +2 Temporarily', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'stomp_buff'},
	'stomp_damage' : {'name' : 'Stomp Damage','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons10.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Deals 80% Damage', 'calculation' : f'({hero.strength:.2f} + Random Damage) * 0.8', 'cost' : 'None', 'key_name' : 'stomp_damage'},
	'stomp_rush' : {'name' : 'Stomp Rush','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons11.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Turn +20% For Each Enemy', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'stomp_rush'},
	'fireball_unconsumed' : {'name' : 'Fireball Unconsumed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons12.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : '10% Not To Consume Fireball Charge', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'fireball_unconsumed'},
	'fireball_agi_damage' : {'name' : 'Fireball Agility','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons13.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Fireball Deals 25% AGI Extra Damage', 'calculation' : f'{hero.agility * 0.25:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'fireball_agi_damage'},
	'lightning_unconsumed' : {'name' : 'Lightning Unconsumed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons14.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' :  '10% Not To Consume Lightning Charge', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'lightning_unconsumed'},
	'lightning_agi_damage' : {'name' : 'Lightning Agility','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons15.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Lightning Deals 25% AGI Extra Damage', 'calculation' : f'{hero.agility * 0.25:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'lightning_agi_damage'},
	'double_cleave' : {'name' : 'Double Cleave','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons16.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Cleave 2 Times', 'calculation' : f'{hero.strength:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'double_cleave'},
	'cleave_bleed' : {'name' : 'Cleave Bleed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons17.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Cleave Bleeds Enemy For 1% Current HP for 10 Seconds', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'cleave_bleed'},
	'triple_head' : {'name' : 'Triple Head','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons18.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks Head 3 Times', 'calculation' : f'{hero.strength * 0.75:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'triple_head'},
	'triple_mana_restore' : {'name' : 'Triple Mana Restore','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons19.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Restores 2% Max MP Each Hit', 'calculation' : f'{hero.max_mp * 0.02:.2f}', 'cost' : 'None', 'key_name' : 'triple_mana_restore'},
	'normal_attack' : {'name' : 'Normal Attack','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons20.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Normal Attack', 'calculation' : f'{hero.strength:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'normal_attack'},
	'zombie_stab' : {'name' : 'Zombie Stab','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons21.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Pierces Enemy DEF and Shield, Dealing 200% Damage', 'calculation' : f'{hero.strength * 2:.2f} + Random Damage', 'cost' : '10MP', 'key_name' : 'zombie_stab'},
	'fireball' : {'name' : 'Fireball','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons22.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal Hero 125% INT Damage To All Enemies', 'calculation' : f'{hero.intelligence * 1.25:.2f} + Random Damage', 'cost' : '1 Fireball Charge', 'key_name' : 'fireball'},
	'lightning' : {'name' : 'Lightning','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons23.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 100% INT Damage To All Enemies, Turn +25% For Each Enemy', 'calculation' : f'{hero.intelligence:.2f} + Random Damage', 'cost' : '1 Lightning Charge', 'key_name' : 'lightning'},
	'serpent_wheel' : {'name' : 'Serpent Wheel','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons24.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 150% STR Damage And 150% AGI Damage To All Enemies, Causes Bleed', 'calculation' : f'{(hero.strength) * 1.5 + (hero.agility * 1.5):.2f} + Random Damage', 'cost' : '20MP', 'key_name' : 'serpent_wheel'},
	'venomous_whip' : {'name' : 'Venomous Whip','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons25.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 200% INT Damage And 100% STR Damage To All Enemies, Causes Poison ', 'calculation' : f'{(hero.intelligence) * 2 + (hero.strength):.2f} + Random Damage', 'cost' : '20MP', 'key_name' : 'venomous_whip'},
	'thunder_bolt' : {'name' : 'Thunder Bolt','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons26.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 150% AGI Damage To Random Enemy,Turn +25%, Can Be Used On Enemy Turn', 'calculation' : f'{(hero.agility * 1.5):.2f} + Random Damage', 'cost' : '15MP', 'key_name' : 'thunder_bolt'}

	}

	def draw_items(inventory, monster_list, monster_index, hero, damage_text_group, combination_list, inventory_click):
		image_x = -80
		image_y = 75

		#draw the image
		for names in names_list:
			if items[names]['index'] in inventory:
				image_x += 80
				if image_x > 720:
					image_x = 0
					image_y += 75
				items[names]['hitbox'] = pygame.rect.Rect(image_x, image_y, 64, 64)
				screen.blit(items[names]['image'], (image_x, image_y))
		
		#if collide with hitbox, show the description
		mousex, mousey = pygame.mouse.get_pos()
		for names in names_list:
			if items[names]['index'] in inventory:
				if items[names]['hitbox'].collidepoint((mousex,mousey)):
					font_size = pygame.font.Font.size(font, items[names]['description'])
					screen.blit(font.render('NAME:' + items[names]['name'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey))
					screen.blit(font.render('DESC:' + items[names]['description'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
					if 'components' in items[names]:
						screen.blit(font.render('COMPONENTS:' + items[names]['components'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))

			if items[names]['hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] in inventory:
				pygame.draw.rect(screen,(255,255,0),items[names]['hitbox'],2)
				if inventory_click == True:
					combination_list.append(items[names]['index'])
					if len(combination_list) == 2 and hero.gold >= combination_cost:
						if 6 in combination_list and 7 in combination_list and -1 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-1)
							combination_text = Character.Damage_Text(mousex, mousey, 'Razor Shield', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 36 in combination_list and 37 in combination_list and -2 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-2)
							combination_text = Character.Damage_Text(mousex, mousey, 'Eclipse Capsule', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 34 in combination_list and 38 in combination_list and -3 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-3)
							combination_text = Character.Damage_Text(mousex, mousey, 'Blood Hibiscus', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 32 in combination_list and 33 in combination_list and -4 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-4)
							combination_text = Character.Damage_Text(mousex, mousey, 'Yin And Yang', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 1 in combination_list and 18 in combination_list and -5 not in inventory and -13 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-5)
							combination_text = Character.Damage_Text(mousex, mousey, 'Dragon Claw', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 3 in combination_list and 13 in combination_list and -6 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-6)
							combination_text = Character.Damage_Text(mousex, mousey, 'Windy Feather', yellow)
							hero.turn_threshold -= 100	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 17 in combination_list and 22 in combination_list and -7 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-7)
							combination_text = Character.Damage_Text(mousex, mousey, 'Black Hole', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 9 in combination_list and 23 in combination_list and -8 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-8)
							combination_text = Character.Damage_Text(mousex, mousey, 'Charged Obsidian', yellow)
							hero.intelligence += 3	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 35 in combination_list and 28 in combination_list and -9 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-9)
							combination_text = Character.Damage_Text(mousex, mousey, 'Drawfed Phoenix', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 21 in combination_list and 24 in combination_list and -10 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-10)
							combination_text = Character.Damage_Text(mousex, mousey, 'Stone Drum', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 19 in combination_list and 27 in combination_list and -11 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-11)
							combination_text = Character.Damage_Text(mousex, mousey, 'Hydra Heart', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 8 in combination_list and 10 in combination_list and -12 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-12)
							combination_text = Character.Damage_Text(mousex, mousey, 'Blue Ruby', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 12 in combination_list and 18 in combination_list and -13 not in inventory and -5 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-13)
							skills_list.append('serpent_wheel')
							combination_text = Character.Damage_Text(mousex, mousey, 'Ouroboros', yellow)
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 30 in combination_list and 25 in combination_list and -14:
							hero.gold -= combination_cost
							inventory.append(-14)
							skills_list.append('venomous_whip')	
							combination_text = Character.Damage_Text(mousex, mousey, 'Whip Of Akhlys', yellow)
							damage_text_group.add(combination_text)	
							combination_list.clear()
						elif 20 in combination_list and 15 in combination_list and -15 not in inventory:
							hero.gold -= combination_cost
							inventory.append(-15)
							skills_list.append('thunder_bolt')
							combination_text = Character.Damage_Text(mousex, mousey, 'Thunder Kunai', yellow)
							damage_text_group.add(combination_text)	
							combination_list.clear()
						else:
							combination_text = Character.Damage_Text(mousex, mousey, 'Failed', yellow)	
							damage_text_group.add(combination_text)	
							combination_list.clear()

	def show_skills(skills_list):
		skill_x = -10
		skill_y = 460
		skill_active_x = 0
		skill_active_y = 0
		for skill_name in skills_list:
			skill_x += 30
			if skill_x > 720:
				skill_x = 0
				skill_y += 30
			skill_image = skills[skill_name]['image']
			skill_image = pygame.transform.scale(skill_image,(30,30))
			skills[skill_name]['skill_hitbox'] = pygame.rect.Rect(skill_x, skill_y, 30, 30)	
			screen.blit(skill_image, (skill_x,skill_y))			
			if skill_name in active_skills_list:
				screen.blit(active_skills_hitbox_img, (skill_x,skill_y))
		for active_skill in active_skills_list:
			skill_active_x += 44			
			skill_image = skills[active_skill]['image']
			skill_image = pygame.transform.scale(skill_image,(44,44))
			screen.blit(skill_image, (skill_active_x,skill_active_y))			

		mousex, mousey = pygame.mouse.get_pos()
		for skill_name in skills_list:
			if skills[skill_name]['skill_hitbox'].collidepoint((mousex,mousey)):
				font_size = pygame.font.Font.size(font, skills[skill_name]['description'])
				screen.blit(font.render('NAME:' + skills[skill_name]['name'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))
				screen.blit(font.render('DESC:' + skills[skill_name]['description'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey))
				screen.blit(font.render('CALC:' + skills[skill_name]['calculation'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
				screen.blit(font.render('COST:' + skills[skill_name]['cost'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
				if inventory_click == True and skills[skill_name]['key_name'] not in active_skills_list and skills[skill_name]['key_name'] in all_active_skills_list and skills[skill_name]['key_name'] != 'normal_attack' and len(active_skills_list) < 5:
					active_skills_list.append(skills[skill_name]['key_name'])
					print(active_skills_list)
				elif inventory_click == True and skills[skill_name]['key_name'] in active_skills_list and skills[skill_name]['key_name'] in all_active_skills_list and skills[skill_name]['key_name'] != 'normal_attack':
					active_skills_list.remove(skills[skill_name]['key_name'])
					print(active_skills_list)

	inside_menu = True
	damage_text_group = pygame.sprite.Group()
	combination_list = []
	inventory_click = False
	combination_cost = 1000

	while inside_menu:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'INVENTORY', font_heading, red, screen_width, 10)
		draw_text(f'GOLD: {hero.gold:.2f}', font, red, 20, screen_height - bottom_panel + 20)
		draw_items(inventory, monster_list, monster_index, hero, damage_text_group, combination_list, inventory_click)
		draw_text(f'COMBINATION COST: {combination_cost:.2f}', font, red, 20, screen_height - bottom_panel + 40)

		show_skills(skills_list)

		inventory_button = screen.blit(inventory_icon_img, (0,0))

		damage_text_group.update()
		damage_text_group.draw(screen)

		inventory_click = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_menu = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				inventory_click = True
				mousex, mousey = pygame.mouse.get_pos()
				if inventory_button.collidepoint((mousex,mousey)):
					inside_menu = False

		pygame.display.update()

#-------------------------------------------------------------------#

def shop_menu(inventory, hero, monster_list, monster_index):
	inside_shop = True
	shop_click = False
	image_x = -80
	image_y = 75

	def shop(inventory, hero, shop_click, monster_list, monster_index, image_x, image_y):

		pygame.mouse.set_visible(True)
		mousex, mousey = pygame.mouse.get_pos()

		#resting
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

		#consumables
		buy_fireball_rect, buy_fireball_text = draw_text_middle_and_box_consumables(f'FIREBALL: {400 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 60)
		if shop_click == True and hero.gold >= 400 + (hero.level * 20) and buy_fireball_rect.collidepoint((mousex,mousey)) and hero.fireball_charge < 3:
			hero.gold -= 400 + (hero.level * 20)
			hero.fireball_charge += 1

		buy_lightning_rect, buy_lightning_text = draw_text_middle_and_box_consumables(f'LIGHTNING: {400 + (hero.level * 20)}', font, yellow, red, 20, screen_height - bottom_panel + 80)
		if shop_click == True and hero.gold >= 400 + (hero.level * 20) and buy_lightning_rect.collidepoint((mousex,mousey)) and hero.lightning_charge < 3:
			hero.gold -= 400 + (hero.level * 20)
			hero.lightning_charge += 1		

		#buying items
		for names in shop_names_list:
			if names in shop_names_list:
				image_x += 80
				if image_x > 720:
					image_x = 0
					image_y += 75
				items[names]['shop_hitbox'] = pygame.rect.Rect(image_x, image_y, 64, 64)
				image = items[names]['image']
				image = pygame.transform.scale(image, (64, 64))
				screen.blit(image, (image_x, image_y))

		for names in original_shop_names_list:
			if names not in shop_names_list:
				items[names]['shop_hitbox'] = pygame.rect.Rect(-50, -50, 64, 64)

		for names in shop_names_list:		
			if items[names]['shop_hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] not in inventory:
				font_size = pygame.font.Font.size(font, items[names]['description'])
				screen.blit(font.render('NAME:' + items[names]['name'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey))
				screen.blit(font.render('DESC:' + items[names]['description'], True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))	
				screen.blit(font.render('COST:' + str(items[names]['cost']), True, darker_orange), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
				pygame.draw.rect(screen,(255,255,0),items[names]['shop_hitbox'],2)

				if shop_click == True and hero.gold >= items['eye_of_vladimir']['cost'] and items['eye_of_vladimir']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['eye_of_vladimir']['cost']
					inventory.append(4)
					purchased_list.append(4)
					shop_names_list.remove('eye_of_vladimir')
					shop_click = False
				if shop_click == True and hero.gold >= items['condensed_lightning']['cost'] and items['condensed_lightning']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['condensed_lightning']['cost']
					inventory.append(5)
					purchased_list.append(5)
					hero.intelligence += 3
					shop_names_list.remove('condensed_lightning')
					shop_click = False
				if shop_click == True and hero.gold >= items['shield']['cost'] and items['shield']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['shield']['cost']
					hero.defense += 1
					inventory.append(6)
					purchased_list.append(6)
					shop_names_list.remove('shield')
					shop_click = False
				if shop_click == True and hero.gold >= items['razor_mail']['cost'] and items['razor_mail']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['razor_mail']['cost']
					hero.defense += 1
					inventory.append(7)
					purchased_list.append(7)
					shop_names_list.remove('razor_mail')
					shop_click = False
				if shop_click == True and hero.gold >= items['ruby']['cost'] and items['ruby']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['ruby']['cost']
					inventory.append(8)
					purchased_list.append(8)
					shop_names_list.remove('ruby')
					shop_click = False
				if shop_click == True and hero.gold >= items['infernal_obsidian']['cost'] and items['infernal_obsidian']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['infernal_obsidian']['cost']
					inventory.append(9)
					purchased_list.append(9)
					shop_names_list.remove('infernal_obsidian')
					shop_click = False
				if shop_click == True and hero.gold >= items['mist_stone']['cost'] and items['mist_stone']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['mist_stone']['cost']
					hero.max_mp += 5
					hero.mp_regen += 2
					inventory.append(10)
					purchased_list.append(10)
					shop_names_list.remove('mist_stone')
					shop_click = False
				if shop_click == True and hero.gold >= items['stunted_tornado']['cost'] and items['stunted_tornado']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['stunted_tornado']['cost']
					hero.speed += 1.5
					hero.agility += 1.5
					inventory.append(13)
					purchased_list.append(13)
					shop_names_list.remove('stunted_tornado')
					shop_click = False
				if shop_click == True and hero.gold >= items['thunder_charge']['cost'] and items['thunder_charge']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['thunder_charge']['cost']
					hero.stamina_recovery += 0.5
					inventory.append(15)
					purchased_list.append(15)
					shop_names_list.remove('thunder_charge')
					shop_click = False
				if shop_click == True and hero.gold >= items['dragon_eye']['cost'] and items['dragon_eye']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['dragon_eye']['cost']
					inventory.append(18)
					purchased_list.append(18)
					shop_names_list.remove('dragon_eye')
					shop_click = False
				if shop_click == True and hero.gold >= items['hydro_vortex']['cost'] and items['hydro_vortex']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['hydro_vortex']['cost']
					inventory.append(19)
					purchased_list.append(19)
					shop_names_list.remove('hydro_vortex')
					shop_click = False
				if shop_click == True and hero.gold >= items['kunai']['cost'] and items['kunai']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['kunai']['cost']
					inventory.append(20)
					purchased_list.append(20)
					shop_names_list.remove('kunai')
					shop_click = False
				if shop_click == True and hero.gold >= items['stone_bracelet']['cost'] and items['stone_bracelet']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['stone_bracelet']['cost']
					for monster_group in monster_list:
						for monster in monster_group:
							monster.speed -= 2				
					inventory.append(21)
					purchased_list.append(21)
					shop_names_list.remove('stone_bracelet')
					shop_click = False
				if shop_click == True and hero.gold >= items['lightning_stone']['cost'] and items['lightning_stone']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['lightning_stone']['cost']
					hero.stamina_recovery += 2
					inventory.append(23)
					purchased_list.append(23)
					shop_names_list.remove('lightning_stone')
					shop_click = False
				if shop_click == True and hero.gold >= items['war_drum']['cost'] and items['war_drum']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['war_drum']['cost']
					inventory.append(24)
					purchased_list.append(24)
					shop_names_list.remove('war_drum')
					shop_click = False
				if shop_click == True and hero.gold >= items['glow_fern']['cost'] and items['glow_fern']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['glow_fern']['cost']
					hero.hp_regen += 10
					inventory.append(25)
					purchased_list.append(25)
					shop_names_list.remove('glow_fern')
					shop_click = False
				if shop_click == True and hero.gold >= items['grimoire']['cost'] and items['grimoire']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['grimoire']['cost']
					inventory.append(26)
					purchased_list.append(26)
					shop_names_list.remove('grimoire')
					shop_click = False
				if shop_click == True and hero.gold >= items['bahamut_heart']['cost'] and items['bahamut_heart']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['bahamut_heart']['cost']
					hero.endurance += 5
					hero.defense += 3
					hero.hp_regen += 3
					inventory.append(27)
					purchased_list.append(27)
					shop_names_list.remove('bahamut_heart')
					shop_click = False
				if shop_click == True and hero.gold >= items['phoenix_feather']['cost'] and items['phoenix_feather']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['phoenix_feather']['cost']
					inventory.append(28)
					purchased_list.append(28)
					shop_names_list.remove('phoenix_feather')
					shop_click = False
				if shop_click == True and hero.gold >= items['pocket_ghost']['cost'] and items['pocket_ghost']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['pocket_ghost']['cost']
					for monster_group in monster_list:
						for monster in monster_group:
							monster.strength -= 4				
					inventory.append(29)
					purchased_list.append(29)
					shop_names_list.remove('pocket_ghost')
					shop_click = False
				if shop_click == True and hero.gold >= items['poison_ivy']['cost'] and items['poison_ivy']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['poison_ivy']['cost']
					for monster_group in monster_list:
						for monster in monster_group:
							monster.hp_regen -= 4				
					inventory.append(30)
					purchased_list.append(30)
					shop_names_list.remove('poison_ivy')
					shop_click = False
				if shop_click == True and hero.gold >= items['hasai_and_hyo']['cost'] and items['hasai_and_hyo']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['hasai_and_hyo']['cost']	
					hero.intelligence += 3		
					inventory.append(31)
					purchased_list.append(31)
					shop_names_list.remove('hasai_and_hyo')
					shop_click = False
				if shop_click == True and hero.gold >= items['yang']['cost'] and items['yang']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['yang']['cost']		
					inventory.append(32)
					purchased_list.append(32)
					shop_names_list.remove('yang')
					shop_click = False
				if shop_click == True and hero.gold >= items['yin']['cost'] and items['yin']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['yin']['cost']		
					inventory.append(33)
					purchased_list.append(33)
					shop_names_list.remove('yin')
					shop_click = False
				if shop_click == True and hero.gold >= items['blood_mosquito']['cost'] and items['blood_mosquito']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['blood_mosquito']['cost']		
					inventory.append(34)
					purchased_list.append(34)
					shop_names_list.remove('blood_mosquito')
					shop_click = False
				if shop_click == True and hero.gold >= items['fire_crow']['cost'] and items['fire_crow']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['fire_crow']['cost']		
					inventory.append(35)
					purchased_list.append(35)
					shop_names_list.remove('fire_crow')
					shop_click = False
				if shop_click == True and hero.gold >= items['moon_capsule']['cost'] and items['moon_capsule']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['moon_capsule']['cost']		
					inventory.append(36)
					purchased_list.append(36)
					shop_names_list.remove('moon_capsule')
					shop_click = False
				if shop_click == True and hero.gold >= items['sun_capsule']['cost'] and items['sun_capsule']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['sun_capsule']['cost']		
					inventory.append(37)
					purchased_list.append(37)
					shop_names_list.remove('sun_capsule')
					shop_click = False
				if shop_click == True and hero.gold >= items['jungle_hibiscus']['cost'] and items['jungle_hibiscus']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['jungle_hibiscus']['cost']		
					inventory.append(38)
					purchased_list.append(38)
					shop_names_list.remove('jungle_hibiscus')
					shop_click = False

				shop_click = False
				return shop_click

	while inside_shop:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'SHOP', font_heading, red, screen_width, 10)
		draw_text(f'GOLD: {hero.gold:.2f}', font, red, 20, screen_height - bottom_panel + 20)
		shop(inventory, hero, shop_click, monster_list, monster_index, image_x, image_y)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_shop = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				shop_click = True
				shop_click = shop(inventory, hero, shop_click, monster_list, monster_index, image_x, image_y)	

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					inside_shop = False

		pygame.display.update()	
