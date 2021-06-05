import math, pygame, random, sys, Character, ctypes

pygame.init()

#set framerate
clock = pygame.time.Clock()
fps = 60

#game window#
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
#-------------------------------------------------------------------------------------#

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
crimson = (254,110,0)
fire_brick = (178,34,34)
white = (255,255,255)

shop_inventory_img = pygame.image.load('Images/Background/ShopBG1.png').convert_alpha()
shop_inventory_img = pygame.transform.scale(shop_inventory_img,(screen_width,screen_height))
inventory_img = pygame.image.load('Images/Background/InventoryBG.png').convert_alpha()
inventory_img = pygame.transform.scale(inventory_img,(screen_width,screen_height)) 
inventory_icon_img = pygame.image.load('Images/Icon/InventoryIcon.png').convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_img,(width(0.035),height(0.035)))
active_skills_hitbox_img = pygame.image.load('Images/Icon/SkillIcons/ActiveButtons.png').convert_alpha()
active_skills_hitbox_img = pygame.transform.scale(active_skills_hitbox_img,(width(0.03),height(0.03)))

banner_image = pygame.image.load('Images/Icon/Banners.png').convert_alpha()

def draw_text_and_box(text, font, text_col, x, y, image):
	font_size = pygame.font.Font.size(font, text)
	text_image = font.render(text, True, text_col)
	image = pygame.transform.scale(image, (font_size[0] + 20, font_size[1] + 20))
	screen.blit(image, (x, y))
	screen.blit(text_image, (x + 10, y + 10))

def draw_text(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_text_middle(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	x = (x / 2) - (font_size[0] / 2)
	img = font.render(text, True, text_col)
	choice_text = screen.blit(img, (x, y))

def draw_text_middle_rect(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	img = font.render(text, True, text_col)
	choice_rect = screen.blit(img, (x, y))

	return choice_rect

def draw_text_middle_no_rect(text, font, text_col, x, y):
	font_size = pygame.font.Font.size(font, text)
	img = font.render(text, True, text_col)
	choice_rect = screen.blit(img, (x, y))

#-------------------------------------------------------------------#
items = {
#combined items
'razor_shield' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics0.png').convert_alpha(), 'description' : 'Return 80% Normal Attack Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -1, 'name' : 'Razor Shield', 'components' : 'Razor Mail + Shield', 'combination_componets' : [6,7]},
'eclipse_capsule' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics1.png').convert_alpha(), 'description' : 'Lightning Turns To Eclipse Beam (Restore 15% MP And HP, 2 Times Damage)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -2, 'name' : 'Eclipse Capsule', 'components' : 'Moon Capsule + Sun Capsule', 'combination_componets' : [36,37]},
'blood_hibiscus' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics2.png').convert_alpha(), 'description' : 'Restores HP From 10% Bleed Damage, Bleed Percentage Changed To 3.5%', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -3, 'name' : 'Blood Hibiscus', 'components' : 'Blood Mosquitop + Jungle Hibiscus', 'combination_componets' : [34,38]},
'yin_and_yang' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics3.png').convert_alpha(), 'description' : 'Rolling Attack Always Deals 50% Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -4, 'name' : 'Yin And Yang', 'components' : 'Yin + Yang', 'combination_componets' : [32,33]},
'dragon_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics4.png').convert_alpha(), 'description' : 'Attack Twice With 25% More Damage Every 2 Attacks (Does Not Proc Special Effects)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -5, 'name' : 'Dragon Claw', 'components' : 'Dragon Eye + Raptor Claw', 'combination_componets' : [1,18]},
'windy_feather' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics5.png').convert_alpha(), 'description' : 'Turn Threshold -100', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -6, 'name' : 'Windy Feather', 'components' : 'Stunted Tornado + Feather', 'combination_componets' : [3,13]},
'black_hole' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics6.png').convert_alpha(), 'description' : 'Each Level Max HP +4', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -7, 'name' : 'Black Hole', 'components' : 'Grey Opal + Dark Matter', 'combination_componets' : [17,22]},
'charged_obsidian' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics7.png').convert_alpha(), 'description' : 'Cast Lightning Every 3 Heavy Attacks', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -8, 'name' : 'Charged Obsidian', 'components' : 'Infernal Obsidian + Lightning Stone', 'combination_componets' : [9,23]},
'dwarfed_phoenix' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics8.png').convert_alpha(), 'description' : 'Moving 100% Screen Width Pixels Triggers Spark', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -9, 'name' : 'Dwarfed Phoenix', 'components' : 'Fire Crow + Phoenix Feather', 'combination_componets' : [35,28]},
'stone_drum' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics9.png').convert_alpha(), 'description' : 'Stomp Decreases Turn Bar By 30% (Half For Boss), END +3 Temporarily', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -10, 'name' : 'Stone Drum', 'components' : 'Stone Bracelet + War Drum', 'combination_componets' : [21,24]},
'hydra_heart' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics10.png').convert_alpha(), 'description' : 'Deals Half Lost HP As Damage (Max 200) Every 4 Seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -11, 'name' : 'Hydra Heart', 'components' : 'Bahamut Heart + Hydro Vortex', 'combination_componets' : [19,27]},
'blue_ruby' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics11.png').convert_alpha(), 'description' : 'Auto HP Regen Every 3 Seconds (Instead Of 5)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -12, 'name' : 'Blue Ruby', 'components' : 'Mist Stone + Ruby', 'combination_componets' : [8,10]},
'ouroboros' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics12.png').convert_alpha(), 'description' : 'Unlocks Serpent Wheel', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -13, 'name' : 'Ouroboros', 'components' : 'Dragon Eye + Crimson Head Snake', 'combination_componets' : [12,18]},
'whip_of_akhlys' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics13.png').convert_alpha(), 'description' : 'Unlocks Venomous Whip', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -14, 'name' : 'Whip Of Akhlys', 'components' : 'Posion Ivy + Glow Fern', 'combination_componets' : [30,25]},
'thunder_kunai' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics14.png').convert_alpha(), 'description' : 'Unlocks Thunder Bolt', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -15, 'name' : 'Thunder Kunai', 'components' : 'Thunder Charge + Kunai', 'combination_componets' : [20,15]},
'condensed_ectoplasm' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics15.png').convert_alpha(), 'description' : 'Ghost Companion Attacks For 10% Hero INT For Some Attacks', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -16, 'name' : 'Condensed Ectoplasm', 'components' : 'Condensed Lightning + Pocket Ghost', 'combination_componets' : [5,29]},
'calamus_draco' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics16.png').convert_alpha(), 'description' : 'Bleeds Every 3 Attacks', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -17, 'name' : 'Calamus Draco', 'components' : 'Dragon Eye + Eye Of Vladimir', 'combination_componets' : [4,18]},
'golden_bean' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics17.png').convert_alpha(), 'description' : 'Moving A Stage Gives 200 More Gold', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -18, 'name' : 'Golden Bean', 'components' : 'Red Bean + Golden Sand', 'combination_componets' : [39,40]},
'zombie_lance' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics18.png').convert_alpha(), 'description' : 'Attack Further By Another 5% Screen Width', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -19, 'name' : 'Zombie Lance', 'components' : 'Zombie Spine + Reaching Lance', 'combination_componets' : [14,41]},
'lightning_eye' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics19.png').convert_alpha(), 'description' : 'Attacks Deal 20% AGI As Physical Damage Calculation', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -20, 'name' : 'Lightning Eye', 'components' : 'Eye Of Vladimir + Condensed Lightning', 'combination_componets' : [5,4]},
'shield_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics20.png').convert_alpha(), 'description' : 'Bat Attacks When Guard, Dealing 10% Hero Max HP Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -21, 'name' : 'Shield Of Vladimir', 'components' : 'Eye Of Vladimir + Shield', 'combination_componets' : [6,4]},
'mail_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics21.png').convert_alpha(), 'description' : 'Bleed End Of Enemy Turn', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -22, 'name' : 'Mail Of Vladimir', 'components' : 'Eye Of Vladimir + Razor Mail', 'combination_componets' : [7,4]},
'bloody_ruby' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics22.png').convert_alpha(), 'description' : 'Regen Hurts Enemies', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -23, 'name' : 'Bloody Ruby', 'components' : 'Eye Of Vladimir + Ruby', 'combination_componets' : [8,4]},
'crimson_obsidian' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics23.png').convert_alpha(), 'description' : 'Fireball Sacrifice 50% Current HP To Deal 3 Times That Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -24, 'name' : 'Crimson Obsidian', 'components' : 'Eye Of Vladimir + Infernal Obsidian', 'combination_componets' : [9,4]},
'alacrity_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics24.png').convert_alpha(), 'description' : 'Attack CD Rate + 0.2/Second', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -25, 'name' : 'Alacrity Claw', 'components' : 'Raptor Claw + Lightning Stone', 'combination_componets' : [1,23]},
'swift_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics25.png').convert_alpha(), 'description' : 'Attack CD Threshold - 5', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -26, 'name' : 'Swift Claw', 'components' : 'Raptor Claw + Stunted Tornado', 'combination_componets' : [1,13]},
'toxic_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics26.png').convert_alpha(), 'description' : '10% Chance To Inflict Posion On Light Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -27, 'name' : 'Toxic Claw', 'components' : 'Raptor Claw + Poison Ivy', 'combination_componets' : [1,30]},
'sticky_claw' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics27.png').convert_alpha(), 'description' : 'Attack Reduce Enemy Turn By 8% (Half For Boss)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -28, 'name' : 'Sticky Claw', 'components' : 'Raptor Claw + Slime Ball', 'combination_componets' : [1,11]},
'mist_vortex' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics28.png').convert_alpha(), 'description' : 'Creates A Mist Vortex That Deletes Projectiles That Touch it, Last 4 Seconds (12 Seconds CD)', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -29, 'name' : 'Mist Vortex', 'components' : 'Mist Stone + Hydro Vortex', 'combination_componets' : [10,19]},
'holy_script' : {'image' : pygame.image.load('Images/Icon/Combined_Relics/Combined_Relics29.png').convert_alpha(), 'description' : 'Restores 20% Hero INT As HP Every Light Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : -30, 'name' : 'Holy Script', 'components' : 'Grimoire + Glow Fern', 'combination_componets' : [25,26]},


#normal items
'ring_of_health' : {'image' : pygame.image.load('Images/Icon/Relics/Relics0.png').convert_alpha(), 'description' : 'Max HP +3', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 0, 'name' : 'Ring Of Health'},
'raptor_claw' : {'image' : pygame.image.load('Images/Icon/Relics/Relics1.png').convert_alpha(), 'description' : 'STR +1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 1, 'name' : 'Raptor Claw'},
'four_leaf_clover' : {'image' : pygame.image.load('Images/Icon/Relics/Relics2.png').convert_alpha(), 'description' : 'LUC +1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 2, 'name' : 'Four Leaf Clover'},
'feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics3.png').convert_alpha(), 'description' : 'SPD +0.25', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 3, 'name' : 'Feather'},
'eye_of_vladimir' : {'image' : pygame.image.load('Images/Icon/Relics/Relics4.png').convert_alpha(), 'description' : 'Non-Skill Attack Lifesteal 1% Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 4, 'name' : 'Eye Of Vladimir', 'cost' : 1250 + random.randint(-250,250)},
'condensed_lightning' : {'image' : pygame.image.load('Images/Icon/Relics/Relics5.png').convert_alpha(), 'description' : 'Fireball Damage * 1.75, INT +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 5, 'name' : 'Condensed Lightning', 'cost' : 1500 + random.randint(-250,250)},
'shield' : {'image' : pygame.image.load('Images/Icon/Relics/Relics6.png').convert_alpha(), 'description' : 'Auto Guard After 8 Seconds, DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 6, 'name' : 'Shield', 'cost' : 1500 + random.randint(-250,250)},
'razor_mail' : {'image' : pygame.image.load('Images/Icon/Relics/Relics7.png').convert_alpha(), 'description' : 'Return 25% DEF + 15% Enemy Normal Attack Damage, DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 7, 'name' : 'Razor Mail', 'cost' : 1500 + random.randint(-250,250)},
'ruby' : {'image' : pygame.image.load('Images/Icon/Relics/Relics8.png').convert_alpha(), 'description' : 'MP Regen Added To HP Regen', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 8, 'name' : 'Ruby', 'cost' : 1250 + random.randint(-250,250)},
'infernal_obsidian' : {'image' : pygame.image.load('Images/Icon/Relics/Relics9.png').convert_alpha(), 'description' : 'Cast Fireball Every 3 Heavy Attacks', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 9, 'name' : 'Infernal Obsidian', 'cost' : 1750 + random.randint(-250,250)},
'mist_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics10.png').convert_alpha(), 'description' : 'Hero MP Regen + 2, Max MP +5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 10, 'name' : 'Mist Stone', 'cost' : 1500 + random.randint(-250,250)},
'slime_ball' : {'image' : pygame.image.load('Images/Icon/Relics/Relics11.png').convert_alpha(), 'description' : 'All Monster SPD -0.5', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 11, 'name' : 'Slime Ball'},
'crimson_head_snake' : {'image' : pygame.image.load('Images/Icon/Relics/Relics12.png').convert_alpha(), 'description' : 'All Monster HP Regen -1', 'hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 12, 'name' : 'Crimson Head Snake'},
'stunted_tornado' : {'image' : pygame.image.load('Images/Icon/Relics/Relics13.png').convert_alpha(), 'description' : 'Hero SPD + 1.5, AGI +1.5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 13, 'name' : 'Stunted Tornado', 'cost' : 1500 + random.randint(-250,250)},
'zombie_spine' : {'image' : pygame.image.load('Images/Icon/Relics/Relics14.png').convert_alpha(), 'description' : 'Unlocks Zombie Stab', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 14, 'name' : 'Zombie Spine'},
'thunder_charge' : {'image' : pygame.image.load('Images/Icon/Relics/Relics15.png').convert_alpha(), 'description' : 'Hero Stamina Recovery +0.5', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 15, 'name' : 'Thunder Charge', 'cost' : 1250 + random.randint(-250,250)},
'fluffy_cloud' : {'image' : pygame.image.load('Images/Icon/Relics/Relics16.png').convert_alpha(), 'description' : 'Hero Stamina Recovery +0.25, SPD +0.25', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 16, 'name' : 'Fluffy Cloud'},
'grey_opal' : {'image' : pygame.image.load('Images/Icon/Relics/Relics17.png').convert_alpha(), 'description' : 'Stamina Threshold -50', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 17, 'name' : 'Grey Opal'},
'dragon_eye' : {'image' : pygame.image.load('Images/Icon/Relics/Relics18.png').convert_alpha(), 'description' : 'Attack Twice With 25% More Damage Every 3 Attacks (Does Not Proc Special Effects)', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 18, 'name' : 'Dragon Eye', 'cost' : 1750 + random.randint(-250,250)},
'hydro_vortex' : {'image' : pygame.image.load('Images/Icon/Relics/Relics19.png').convert_alpha(), 'description' : 'Absorbs 15% Normal Attack Damage As HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 19, 'name' : 'Hydro Vortex', 'cost' : 1250 + random.randint(-250,250)},
'kunai' : {'image' : pygame.image.load('Images/Icon/Relics/Relics20.png').convert_alpha(), 'description' : 'Heavy Attack Deal 25% More Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 20, 'name' : 'Kunai', 'cost' : 1500 + random.randint(-250,250)},
'stone_bracelet' : {'image' : pygame.image.load('Images/Icon/Relics/Relics21.png').convert_alpha(), 'description' : 'All Monster SPD -2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 21, 'name' : 'Stone Bracelet', 'cost' : 1500 + random.randint(-250,250)},
'dark_matter' : {'image' : pygame.image.load('Images/Icon/Relics/Relics22.png').convert_alpha(), 'description' : 'All Monster DEF -2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 22, 'name' : 'Dark Matter'},
'lightning_stone' : {'image' : pygame.image.load('Images/Icon/Relics/Relics23.png').convert_alpha(), 'description' : 'Hero Stamina Recover +2', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 23, 'name' : 'Lightning Stone', 'cost' : 1750 + random.randint(-250,250)},
'war_drum' : {'image' : pygame.image.load('Images/Icon/Relics/Relics24.png').convert_alpha(), 'description' : 'Stomp Every 8 Seconds', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 24, 'name' : 'War Drum', 'cost' : 1750 + random.randint(-250,250)},
'glow_fern' : {'image' : pygame.image.load('Images/Icon/Relics/Relics25.png').convert_alpha(), 'description' : 'Hero HP Regen +10', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 25, 'name' : 'Glow Fern', 'cost' : 1750 + random.randint(-250,250)},
'grimoire' : {'image' : pygame.image.load('Images/Icon/Relics/Relics26.png').convert_alpha(), 'description' : 'All Monster HP -20% Hero INT Every Light Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 26, 'name' : 'Grimoire', 'cost' : 1750 + random.randint(-250,250)},
'bahamut_heart' : {'image' : pygame.image.load('Images/Icon/Relics/Relics27.png').convert_alpha(), 'description' : 'Hero END +5, DEF +3 HP Regen +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 27, 'name' : 'Bahamut Heart', 'cost' : 1750 + random.randint(-250,250)},
'phoenix_feather' : {'image' : pygame.image.load('Images/Icon/Relics/Relics28.png').convert_alpha(), 'description' : 'Hero Revives With 50% HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 28, 'name' : 'Phoenix Feather', 'cost' : 2250 + random.randint(-250,250)},
'pocket_ghost' : {'image' : pygame.image.load('Images/Icon/Relics/Relics29.png').convert_alpha(), 'description' : 'All Monster STR -4', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 29, 'name' : 'Pocket Ghost', 'cost' : 1750 + random.randint(-250,250)},
'poison_ivy' : {'image' : pygame.image.load('Images/Icon/Relics/Relics30.png').convert_alpha(), 'description' : 'All Monster HP Regen -4', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 30, 'name' : 'Poison Ivy', 'cost' : 1750 + random.randint(-250,250)},
'hasai_and_hyo' : {'image' : pygame.image.load('Images/Icon/Relics/Relics31.png').convert_alpha(), 'description' : 'Fireball Turns To Sapphire Flame (Steals 20% Turn), Hero INT +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 31, 'name' : 'Hasai And Hyo', 'cost' : 1750 + random.randint(-250,250)},
'yang' : {'image' : pygame.image.load('Images/Icon/Relics/Relics32.png').convert_alpha(), 'description' : 'Forward Roll On Ground Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 32, 'name' : 'Yang', 'cost' : 1750 + random.randint(-250,250)},
'yin' : {'image' : pygame.image.load('Images/Icon/Relics/Relics33.png').convert_alpha(), 'description' : 'Back Roll On Ground Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 33, 'name' : 'Yin', 'cost' : 1750 + random.randint(-250,250)},
'blood_mosquito' : {'image' : pygame.image.load('Images/Icon/Relics/Relics34.png').convert_alpha(), 'description' : 'Bleeds Enemy When Heavy Attack', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 34, 'name' : 'Blood Mosquito', 'cost' : 1750 + random.randint(-250,250)},
'fire_crow' : {'image' : pygame.image.load('Images/Icon/Relics/Relics35.png').convert_alpha(), 'description' : 'Spark End Of Enemy Turn', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 35, 'name' : 'Fire Crow', 'cost' : 1500 + random.randint(-250,250)},
'moon_capsule' : {'image' : pygame.image.load('Images/Icon/Relics/Relics36.png').convert_alpha(), 'description' : 'Lightning Turns To Lunar Beam (Restore 15% MP)', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 36, 'name' : 'Moon Capsule', 'cost' : 1500 + random.randint(-250,250)},
'sun_capsule' : {'image' : pygame.image.load('Images/Icon/Relics/Relics37.png').convert_alpha(), 'description' : 'Lightning Turns To Solar Beam (Restore 15% HP)', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 37, 'name' : 'Sun Capsule', 'cost' : 1500 + random.randint(-250,250)},
'jungle_hibiscus' : {'image' : pygame.image.load('Images/Icon/Relics/Relics38.png').convert_alpha(), 'description' : 'Moving 80% Screen Width Pixels Recovers 3% Max HP', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 38, 'name' : 'Jungle Hibiscus', 'cost' : 1750 + random.randint(-250,250)},
'red_bean' : {'image' : pygame.image.load('Images/Icon/Relics/Relics39.png').convert_alpha(), 'description' : 'Hero DEF +1', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 39, 'name' : 'Red Bean'},
'golden_sand' : {'image' : pygame.image.load('Images/Icon/Relics/Relics40.png').convert_alpha(), 'description' : 'Hero END +3', 'hitbox' : pygame.rect.Rect(0,0,0,0),'index' : 40, 'name' : 'Golden Sand'},
'reaching_lance' : {'image' : pygame.image.load('Images/Icon/Relics/Relics41.png').convert_alpha(), 'description' : 'Attack Further By 5% Screen Width', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 41, 'name' : 'Reaching Lance', 'cost' : 1500 + random.randint(-250,250)},
'goblin_bomb' : {'image' : pygame.image.load('Images/Icon/Relics/Relics42.png').convert_alpha(), 'description' : 'Throws A Bomb Every 10 Seconds, Dealing 150% PHY Damage', 'hitbox' : pygame.rect.Rect(0,0,0,0),'shop_hitbox' : pygame.rect.Rect(0,0,0,0), 'index' : 42, 'name' : 'Goblin Bomb', 'cost' : 1750 + random.randint(-250,250)}

}

names_list = ['ring_of_health', 'raptor_claw', 'four_leaf_clover', 'feather', 'eye_of_vladimir',
'condensed_lightning', 'shield', 'razor_mail', 'ruby', 'infernal_obsidian', 'mist_stone', 
'slime_ball', 'crimson_head_snake', 'stunted_tornado', 'zombie_spine', 'thunder_charge', 
'fluffy_cloud', 'grey_opal', 'dragon_eye', 'hydro_vortex', 'kunai', 'stone_bracelet', 'dark_matter', 
'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 'phoenix_feather', 'pocket_ghost', 
'poison_ivy', 'hasai_and_hyo', 'yang', 'yin', 'blood_mosquito', 'fire_crow', 'moon_capsule', 'sun_capsule', 
'jungle_hibiscus', 'red_bean', 'golden_sand', 'razor_shield', 'eclipse_capsule', 'blood_hibiscus', 'yin_and_yang',
'dragon_claw', 'windy_feather', 'black_hole', 'charged_obsidian', 'dwarfed_phoenix', 'stone_drum', 'hydra_heart',
'blue_ruby', 'ouroboros', 'whip_of_akhlys', 'thunder_kunai', 'condensed_ectoplasm', 'reaching_lance', 'goblin_bomb',
'calamus_draco', 'golden_bean', 'zombie_lance', 'lightning_eye', 'shield_of_vladimir', 'mail_of_vladimir',
'bloody_ruby', 'crimson_obsidian', 'alacrity_claw', 'swift_claw', 'toxic_claw', 'sticky_claw', 'mist_vortex',
'holy_script']

original_shop_names_list = ['eye_of_vladimir', 'condensed_lightning', 'shield', 'razor_mail', 'ruby', 
'infernal_obsidian', 'mist_stone', 'stunted_tornado', 'thunder_charge', 'dragon_eye', 'hydro_vortex', 
'kunai', 'stone_bracelet', 'lightning_stone', 'war_drum', 'glow_fern', 'grimoire', 'bahamut_heart', 
'phoenix_feather', 'pocket_ghost', 'poison_ivy', 'hasai_and_hyo', 'yang', 'yin', 'blood_mosquito', 
'fire_crow', 'moon_capsule', 'sun_capsule', 'jungle_hibiscus', 'reaching_lance', 'goblin_bomb']

purchased_list = []

shop_names_list = []

def reset_items_in_shop(original_shop_names_list, purchased_list, inventory):
	shop_names_list = []
	if len(inventory) == 0:
		random_shop_item_amount = 10
	else:
		random_shop_item_amount = random.randint(6,8)
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
def inventory_menu(inventory, monster_list, monster_index, hero):

	skills = {
	'guard' : {'name' : 'Guard','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons0.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain Shield Equal To 20% Max HP + 300% DEF Every 10 Seconds', 'calculation' : f'{(hero.max_hp * 0.3) + (hero.defense * 3):.2f}', 'cost' : 'None', 'key_name' : 'guard'},
	'stomp' : {'name' : 'Stomp','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons1.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'All Enemy Turn -20% (Half For Boss) Every 10 Seconds', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'stomp'},
	'start_lightning' : {'name' : 'Start Lightning','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons2.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain 1 Lightning Every 10 Seconds', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'start_lightning'},
	'start_fireball' : {'name' : 'Start Fireball','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons3.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Gain 1 Fireball Every 10 Seconds', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'start_fireball'},
	'cleave' : {'name' : 'Cleave','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons4.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks All Enemies', 'calculation' : f'100% PHY + Random Damage', 'cost' : '7.5MP', 'key_name' : 'cleave'},
	'triple_combo' : {'name' : 'Triple Combo','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons5.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks Head, Body, and Legs 1 time', 'calculation' : f'75% PHY + Random Damage', 'cost' : '10MP', 'key_name' : 'triple_combo'},
	'guard_heal' : {'name' : 'Guard Heal','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons6.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Heals For 5% Max HP + 50% DEF', 'calculation' : f'{(hero.max_hp * 0.05) + (hero.defense * 0.5):.2f}', 'cost' : 'None', 'key_name' : 'guard_heal'},
	'guard_slash' : {'name' : 'Guard Slash','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons7.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Hero Skill Procs Heavy Attacks', 'calculation' : f'50% PHY + Random Damage', 'cost' : 'None', 'key_name' : 'guard_slash'},
	'guard_rush' : {'name' : 'Guard Rush','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons8.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Guard Turn +25%', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'guard_rush'},
	'stomp_buff' : {'name' : 'Stomp Buff','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons9.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Increases STR +2, AGI +2 Temporarily', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'stomp_buff'},
	'stomp_damage' : {'name' : 'Stomp Damage','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons10.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Deals Damage', 'calculation' : f'50% PHY + Random Damage', 'cost' : 'None', 'key_name' : 'stomp_damage'},
	'stomp_rush' : {'name' : 'Stomp Rush','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons11.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Stomp Turn +20% For Each Enemy', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'stomp_rush'},
	'fireball_unconsumed' : {'name' : 'Fireball Unconsumed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons12.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : '10% Not To Consume Fireball Charge', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'fireball_unconsumed'},
	'fireball_agi_damage' : {'name' : 'Fireball Agility','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons13.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Fireball Deals 25% AGI Extra Damage', 'calculation' : f'{hero.agility * 0.25:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'fireball_agi_damage'},
	'lightning_unconsumed' : {'name' : 'Lightning Unconsumed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons14.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' :  '10% Not To Consume Lightning Charge', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'lightning_unconsumed'},
	'lightning_agi_damage' : {'name' : 'Lightning Agility','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons15.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Lightning Deals 25% AGI Extra Damage', 'calculation' : f'{hero.agility * 0.25:.2f} + Random Damage', 'cost' : 'None', 'key_name' : 'lightning_agi_damage'},
	'double_cleave' : {'name' : 'Double Cleave','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons16.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Cleave 2 Times', 'calculation' : f'2 * (100% PHY + Random Damage)', 'cost' : 'None', 'key_name' : 'double_cleave'},
	'cleave_bleed' : {'name' : 'Cleave Bleed','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons17.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Cleave Bleeds Enemy For 1% Current HP 10 Times', 'calculation' : f'None', 'cost' : 'None', 'key_name' : 'cleave_bleed'},
	'triple_head' : {'name' : 'Triple Head','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons18.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Attacks Head 3 Times', 'calculation' : f'75% PHY + Random Damage', 'cost' : 'None', 'key_name' : 'triple_head'},
	'triple_mana_restore' : {'name' : 'Triple Mana Restore','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons19.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Restores 2% Max MP Each Hit', 'calculation' : f'{hero.max_mp * 0.02:.2f}', 'cost' : 'None', 'key_name' : 'triple_mana_restore'},
	'normal_attack' : {'name' : 'Normal Attack','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons20.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Normal Attack', 'calculation' : f'50% PHY + Random Damage', 'cost' : 'None', 'key_name' : 'normal_attack'},
	'zombie_stab' : {'name' : 'Zombie Stab','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons21.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Pierces Enemy DEF and Shield', 'calculation' : f'200% PHY + Random Damage', 'cost' : '10MP', 'key_name' : 'zombie_stab'},
	'serpent_wheel' : {'name' : 'Serpent Wheel','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons24.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 200% PHY Damage + 100% AGI Damage To All Enemies, Causes Bleed', 'calculation' : f'200% PHY + 100% AGI + Random Damage', 'cost' : '20MP', 'key_name' : 'serpent_wheel'},
	'venomous_whip' : {'name' : 'Venomous Whip','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons25.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 200% MAG Damage + 100% STR Damage To All Enemies, Causes Poison ', 'calculation' : f'200% MAG + 100% STR + Random Damage', 'cost' : '20MP', 'key_name' : 'venomous_whip'},
	'thunder_bolt' : {'name' : 'Thunder Bolt','image' : pygame.image.load('Images/Icon/SkillIcons/Buttons26.png').convert_alpha(), 'skill_hitbox' : pygame.rect.Rect(0,0,0,0), 'description' : 'Deal 50% PHY Damage + 50% MAG Damage To All Enemies, Turn +10%, Enemy Turn Usable', 'calculation' : f'50% MAG + 50% PHY + Random Damage', 'cost' : '15MP', 'key_name' : 'thunder_bolt'}

	}

	def draw_items(inventory, monster_list, monster_index, hero, damage_text_group, combination_list, inventory_click):
		image_x = 0
		image_y = height_position(0.1)

		#draw the image
		for names in names_list:
			if items[names]['index'] in inventory:
				image_x += width_position(0.05)
				if image_x > width_position(0.9):
					image_x = width_position(0.05)
					image_y += height_position(0.1)
				items[names]['hitbox'] = pygame.rect.Rect(image_x, image_y, width(0.05), height(0.05))
				image = items[names]['image']
				image = pygame.transform.scale(items[names]['image'],(width(0.05), height(0.05)))
				screen.blit(image, (image_x, image_y))
		
		#if collide with hitbox, show the description
		mousex, mousey = pygame.mouse.get_pos()
		for names in names_list:
			if items[names]['index'] in inventory:
				if items[names]['hitbox'].collidepoint((mousex,mousey)):
					font_size = pygame.font.Font.size(font, items[names]['description'])
					screen.blit(font.render('NAME:' + items[names]['name'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey))
					screen.blit(font.render('DESC:' + items[names]['description'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
					if 'components' in items[names]:
						screen.blit(font.render('COMPONENTS:' + items[names]['components'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))

			if items[names]['hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] in inventory:
				pygame.draw.rect(screen,(255,255,0),items[names]['hitbox'],2)
				if inventory_click == True:
					combination_list.append(items[names]['index'])
					if len(combination_list) == 2 and hero.gold >= hero.combination_cost:
						for relic in items:
							if items[relic]['index'] < 0:
								if sorted(combination_list) == sorted(items[relic]['combination_componets']) and items[relic]['index'] not in inventory:
									
									if items[relic]['index'] == -6:
										hero.turn_threshold -= 100 
									elif items[relic]['index'] == -19:
										hero.attack_length += screen_width * 0.05 
									elif items[relic]['index'] == -26:
										hero.base_attack_time -= 5 
										hero.attack_time -= 5 
									elif items[relic]['index'] == -25:
										hero.attack_cooldown_rate += 0.2 
									elif items[relic]['index'] == -5:
										hero.dragon_item_counter_threshold -= 1
									elif items[relic]['index'] == -13:
										hero.skills_list.append('serpent_wheel')
									elif items[relic]['index'] == -14:
										hero.skills_list.append('venomous_whip')
									elif items[relic]['index'] == -15:
										hero.skills_list.append('thunder_bolt')

									hero.gold -= hero.combination_cost
									hero.combination_cost += 200
									inventory.append(items[relic]['index'])
									combination_text = Character.Damage_Text(mousex, mousey, items[relic]['name'], yellow)	
									damage_text_group.add(combination_text)	
									combination_list.clear()
									break
							else:
								combination_text = Character.Damage_Text(mousex, mousey, 'Failed', yellow)	
								damage_text_group.add(combination_text)	
								combination_list.clear()
								break																		

	def show_skills():
		skill_x = 0
		skill_y = height_position(0.8)
		skill_active_x = 0
		skill_active_y = 0
		for skill_name in hero.skills_list:
			skill_x += width_position(0.03)
			if skill_x > width_position(0.97):
				skill_x = 0
				skill_y += height_position(0.04)
			skill_image = skills[skill_name]['image']
			skill_image = pygame.transform.scale(skill_image,(width(0.03),height(0.03)))
			skills[skill_name]['skill_hitbox'] = pygame.rect.Rect(skill_x, skill_y, width(0.03),height(0.03))	
			screen.blit(skill_image, (skill_x,skill_y))			
			if skill_name in hero.active_skills_list:
				screen.blit(active_skills_hitbox_img, (skill_x,skill_y))
		for active_skill in hero.active_skills_list:
			skill_active_x += width_position(0.035)			
			skill_image = skills[active_skill]['image']
			skill_image = pygame.transform.scale(skill_image,(width(0.035),height(0.035)))
			screen.blit(skill_image, (skill_active_x,skill_active_y))			

		mousex, mousey = pygame.mouse.get_pos()
		for skill_name in hero.skills_list:
			if skills[skill_name]['skill_hitbox'].collidepoint((mousex,mousey)):
				font_size = pygame.font.Font.size(font, skills[skill_name]['description'])
				screen.blit(font.render('NAME:' + skills[skill_name]['name'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey - 20))
				screen.blit(font.render('DESC:' + skills[skill_name]['description'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey))
				screen.blit(font.render('CALC:' + skills[skill_name]['calculation'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
				screen.blit(font.render('COST:' + skills[skill_name]['cost'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
				if inventory_click == True and skills[skill_name]['key_name'] not in hero.active_skills_list and skills[skill_name]['key_name'] in hero.all_active_skills_list and skills[skill_name]['key_name'] != 'normal_attack' and len(hero.active_skills_list) < 5:
					hero.active_skills_list.append(skills[skill_name]['key_name'])
				elif inventory_click == True and skills[skill_name]['key_name'] in hero.active_skills_list and skills[skill_name]['key_name'] in hero.all_active_skills_list and skills[skill_name]['key_name'] != 'normal_attack':
					hero.active_skills_list.remove(skills[skill_name]['key_name'])

	inside_menu = True
	damage_text_group = pygame.sprite.Group()
	combination_list = []
	inventory_click = False

	while inside_menu:
		clock.tick(fps)

		screen.blit(inventory_img, (0,0))
		draw_text_middle(f'INVENTORY', font_heading, white, screen_width, height_position(0.025))
		draw_text(f'GOLD: {hero.gold:.2f}', font, white, width_position(0.03), top_of_bottom_panel)
		draw_items(inventory, monster_list, monster_index, hero, damage_text_group, combination_list, inventory_click)
		draw_text(f'COMBINATION COST: {hero.combination_cost:.2f}', font, white, width_position(0.03), top_of_bottom_panel + text_distance)

		show_skills()

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

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					inside_menu = False

		pygame.display.update()

#-------------------------------------------------------------------#
def shop_menu(inventory, hero, monster_list, monster_index):
	inside_shop = True
	shop_click = False
	image_x = 0
	image_y = height_position(0.1)

	def shop(inventory, hero, shop_click, monster_list, monster_index, image_x, image_y):

		pygame.mouse.set_visible(True)
		mousex, mousey = pygame.mouse.get_pos()

		#resting
		if hero.level >= 5:
			rest_rect = draw_text_middle_rect(f'REST: {100 + (hero.gold * 0.1):.2f}', font, yellow, width_position(0.03), top_of_bottom_panel + text_distance)
			if shop_click == True and hero.gold >= 100 + (hero.gold * 0.1) and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
				hero.gold -= 100 + (hero.gold * 0.1)
				hp_heal_amount = hero.max_hp - hero.hp
				mp_heal_amount = hero.max_mp - hero.mp
				hero.hp += hp_heal_amount
				hero.mp += mp_heal_amount
		else:
			rest_rect = draw_text_middle_rect(f'REST: {100}', font, yellow, width_position(0.03), top_of_bottom_panel + text_distance)
			if shop_click == True and hero.gold >= 100 and rest_rect.collidepoint((mousex,mousey)) and (hero.hp < hero.max_hp or hero.mp < hero.max_mp):
				hero.gold -= 100
				hp_heal_amount = hero.max_hp - hero.hp
				mp_heal_amount = hero.max_mp - hero.mp
				hero.hp += hp_heal_amount
				hero.mp += mp_heal_amount
				
		#buying items
		for names in shop_names_list:
			if names in shop_names_list:
				image_x += width_position(0.05)
				if image_x > width_position(0.95):
					image_x = 0
					image_y += height_position(0.05)
				items[names]['shop_hitbox'] = pygame.rect.Rect(image_x, image_y, width(0.05), height(0.05))
				image = items[names]['image']
				image = pygame.transform.scale(image, (width(0.05), height(0.05)))
				screen.blit(image, (image_x, image_y))

		for names in original_shop_names_list:
			if names not in shop_names_list:
				items[names]['shop_hitbox'] = pygame.rect.Rect(- width_position(0.05), - width_position(0.05), width(0.05), height(0.05))

		for names in shop_names_list:		
			if items[names]['shop_hitbox'].collidepoint((mousex,mousey)) and items[names]['index'] not in inventory:
				font_size = pygame.font.Font.size(font, items[names]['description'])
				screen.blit(font.render('NAME:' + items[names]['name'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey))
				screen.blit(font.render('DESC:' + items[names]['description'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))	
				screen.blit(font.render('COST:' + str(items[names]['cost']), True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
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
				if shop_click == True and hero.gold >= items['reaching_lance']['cost'] and items['reaching_lance']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['reaching_lance']['cost']
					hero.attack_length += screen_width * 0.05		
					inventory.append(41)
					purchased_list.append(41)
					shop_names_list.remove('reaching_lance')
					shop_click = False
				if shop_click == True and hero.gold >= items['goblin_bomb']['cost'] and items['goblin_bomb']['shop_hitbox'].collidepoint((mousex,mousey)):
					hero.gold -= items['goblin_bomb']['cost']	
					inventory.append(42)
					purchased_list.append(42)
					shop_names_list.remove('goblin_bomb')
					shop_click = False

				shop_click = False
				return shop_click

	while inside_shop:
		clock.tick(fps)

		screen.blit(shop_inventory_img, (0,0))
		draw_text_middle(f'SHOP', font_heading, white, screen_width, height_position(0.025))
		draw_text(f'GOLD: {hero.gold:.2f}', font, white, width_position(0.03), top_of_bottom_panel)
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

def option_menu(hero, game_variables):
	inside_option = True
	option_click = False

	while inside_option:
		clock.tick(fps)

		pygame.mouse.set_visible(True)
		mousex, mousey = pygame.mouse.get_pos()

		show_hitbox_rect = draw_text_middle_rect(f'SHOW HITBOX', font, red, width_position(0.03), height_position(0.03))
		if option_click == True and show_hitbox_rect.collidepoint((mousex,mousey)):
			if game_variables.show_hitbox == True:
				game_variables.show_hitbox = False
			elif game_variables.show_hitbox == False:
				game_variables.show_hitbox = True

		quit_rect = draw_text_middle_rect(f'QUIT', font, red, width_position(0.03), height_position(0.06))
		if option_click == True and quit_rect.collidepoint((mousex,mousey)):
			inside_option = False
			sys.exit()

		draw_text_middle_no_rect(f'LVL: {hero.level}', font, yellow, width_position(0.03), height_position(0.09))
		draw_text_middle_no_rect(f'EXP: {hero.experience:.1f}', font, yellow, width_position(0.03), height_position(0.12))
		draw_text_middle_no_rect(f'STAT POINTS: {hero.statpoints}', font, yellow, width_position(0.03), height_position(0.15))
		draw_text_middle_no_rect(f'GOLD: {hero.gold:.2f}', font, yellow, width_position(0.03), height_position(0.18))
		draw_text_middle_no_rect(f'MP REGEN: {hero.mp_regen:.2f}(Base) + {hero.intelligence * 0.1:.2f}(intelligence * 0.1)', font, yellow, width_position(0.03), height_position(0.21))
		draw_text_middle_no_rect(f'HP REGEN: {hero.hp_regen:.2f}(Base) + {hero.endurance * 0.1:.2f}(endurance * 0.1)', font, yellow, width_position(0.03), height_position(0.24))
		draw_text_middle_no_rect(f'DEF: {hero.defense:.2f}(Base) + {hero.endurance * 0.1:.2f}(endurance * 0.1)', font, yellow, width_position(0.03), height_position(0.27))
		draw_text_middle_no_rect(f'SPD/TURN/SKILLCD RATE: {hero.speed:.2f}(Base) + {hero.agility * 0.025:.2f}(agility * 0.025)/SEC', font, yellow, width_position(0.03), height_position(0.3))
		draw_text_middle_no_rect(f'SPD/TURN/SKILLCD THRESHOLD: {hero.turn_threshold:.2f}', font, yellow, width_position(0.03), height_position(0.33))	
		draw_text_middle_no_rect(f'ATKCD RATE: {hero.attack_cooldown_rate:.2f}(Base) + {hero.agility * 0.025:.2f}(agility * 0.025)/SEC', font, yellow, width_position(0.03), height_position(0.36))
		draw_text_middle_no_rect(f'ATKCD THRESHOLD: {hero.base_attack_time:.2f}', font, yellow, width_position(0.03), height_position(0.39))
		draw_text_middle_no_rect(f'ATK LENGTH: {hero.attack_length:.2f}', font, yellow, width_position(0.03), height_position(0.42))
		draw_text_middle_no_rect(f'STA RATE: {hero.stamina_recovery:.2f}(base) + {hero.strength * 0.1:.2f}(strength * 0.1)/SEC', font, yellow, width_position(0.03), height_position(0.45))
		draw_text_middle_no_rect(f'STA THRESHOLD: {hero.stamina_threshold:.2f}', font, yellow, width_position(0.03), height_position(0.48))
		draw_text_middle_no_rect(f'ADDED STR(EVERY 1.5 POINTS STA RATE + 0.5): {hero.added_strength:.2f}', font, yellow, width_position(0.03), height_position(0.51))
		draw_text_middle_no_rect(f'ADDED INT(EVERY 1.5 POINTS MAX MP + 3, MP + 3, MP REGEN + 0.3): {hero.added_intelligence:.2f}', font, yellow, width_position(0.03), height_position(0.54))
		draw_text_middle_no_rect(f'ADDED END(EVERY 1.5 POINTS MAX HP + 3, HP + 3, HP REGEN + 0.3, DEF + 0.1): {hero.added_endurance:.2f}', font, yellow, width_position(0.03), height_position(0.57))
		draw_text_middle_no_rect(f'ADDED LUC: {hero.added_luck:.2f}', font, yellow, width_position(0.03), height_position(0.6))
		draw_text_middle_no_rect(f'ADDED AGI: {hero.added_agility:.2f}', font, yellow, width_position(0.03), height_position(0.63))

		option_click = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inside_option = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				option_click = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					inside_option = False

		pygame.display.update()		