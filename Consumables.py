import math, pygame, random, sys, Character, ctypes, Map

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
bottom_panel = math.ceil(user32.GetSystemMetrics(1) * 0.25)
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
top_of_bottom_panel = screen_height - bottom_panel
bottom_of_bottom_panel = screen_height * 0.8
text_distance = width(0.012)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Battle')

font = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.008))
font_heading = pygame.font.Font('Kyrou_7_Wide_Bold.ttf', width(0.02))
#-------------------------------------------------------------------------------------#

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
white = (255,255,255)

consumable_inventory_img = pygame.image.load('Images/Background/ShopBG.png').convert_alpha()
consumable_inventory_img = pygame.transform.scale(consumable_inventory_img,(screen_width,screen_height))
fireball_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/FireBallIcon.png').convert_alpha()
fireball_icon_img = pygame.transform.scale(fireball_icon_img,(width(0.035),height(0.035)))
lightning_icon_img = pygame.image.load('Images/Icon/SkillDisplayIcon/LightningIcon.png').convert_alpha()
lightning_icon_img = pygame.transform.scale(lightning_icon_img,(width(0.035),height(0.035)))

def draw_text_middle(text, font, text_col, x, y):
    font_size = pygame.font.Font.size(font, text)
    x = (x / 2) - (font_size[0] / 2)
    img = font.render(text, True, text_col)
    choice_text = screen.blit(img, (x, y))

def draw_text_middle_and_box_consumables(text, font, text_col, rect_col, x, y):
    font_size = pygame.font.Font.size(font, text)
    x = (x / 2) - (font_size[0] / 2)
    img = font.render(text, True, text_col)
    rect = pygame.rect.Rect(x, y, font_size[0] + 10, font_size[1] + 10)
    choice_rect = pygame.draw.rect(screen, rect_col, rect)
    choice_text = screen.blit(img, (x + 5, y + 5))

    return choice_rect

def draw_text_middle_no_box(text, font, text_col, x, y):
    font_size = pygame.font.Font.size(font, text)
    x = (x / 2) - (font_size[0] / 2)
    img = font.render(text, True, text_col)
    choice_text = screen.blit(img, (x + 5, y + 5))

def draw_text_middle_rect(text, font, text_col, x, y):
    font_size = pygame.font.Font.size(font, text)
    img = font.render(text, True, text_col)
    choice_rect = screen.blit(img, (x, y))

    return choice_rect

def draw_text(text, font, text_col, x, y):
    font_size = pygame.font.Font.size(font, text)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def use_consumables(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):
    if len(hero.consumables_list) > 0 and hero.consumable_wait_time == 0:
        if hero.consumables_list[0] == 'Fireball' and hero.mp >= 5:
            hero.fireball(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
            del hero.consumables_list[0]

        elif hero.consumables_list[0] == 'Lightning' and hero.mp >= 5:
            hero.lightning(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
            del hero.consumables_list[0]

        elif hero.consumables_list[0] == 'Frost' and hero.mp >= 5:
            hero.frost(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
            del hero.consumables_list[0]

        elif hero.consumables_list[0] == 'Heal':
            hero.heal(damage_text_group, inventory, skill_sprite_group)
            del hero.consumables_list[0]
            hero.active_consumables_list.remove('Heal')

        elif hero.consumables_list[0] == 'Restore':
            hero.restore(damage_text_group, inventory, skill_sprite_group)
            del hero.consumables_list[0]
            hero.active_consumables_list.remove('Restore')

        elif hero.consumables_list[0] == 'Flameball' and hero.mp >= 10:
            hero.flameball(target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory)
            del hero.consumables_list[0]

        hero.consumable_wait_time = 100

def swap_consumables(hero, target, monster_list, monster_index, experiencethreshold, skill_sprite_group, damage_text_group, inventory):
    if len(hero.consumables_list) > 0:  
        hero.consumables_list.append(hero.consumables_list[0])
        hero.consumables_list.remove(hero.consumables_list[0])

all_consumables = {
#base balls
'Fireball' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons22.png').convert_alpha(), 'description' : 'Deals 125% MAG Damage', 'name' : 'Fireball', 'cost' : '5MP', 'uses' : 'Refresh After Battle'},  
'Lightning' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons23.png').convert_alpha(), 'description' : 'Deals 100% MAG Damage And Increase Hero Turn Bar By 20%', 'name' : 'Lightning', 'cost' : '5MP', 'uses' : 'Refresh After Battle'},  
'Frost' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons28.png').convert_alpha(), 'description' : 'Deals 100% MAG Damage And Decrease Enemy Turn Bar By 20%', 'name' : 'Frost', 'cost' : '5MP', 'uses' : 'Refresh After Battle'},
'Heal' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons29.png').convert_alpha(), 'description' : 'Heal 10% MAX HP Over 1 Seconds', 'name' : 'Heal', 'cost' : 'None', 'uses' : 'Once'},
'Restore' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons30.png').convert_alpha(), 'description' : 'Heal 10% MAX MP Over 1 Seconds', 'name' : 'Restore', 'cost' : 'None', 'uses' : 'Once'},

#combined balls
'Flameball' : {'image' : pygame.image.load('Images/Icon/SkillIcons/Buttons27.png').convert_alpha(), 'description' : 'Deals 225% MAG Damage (2 Times For Boss)', 'name' : 'Flameball', 'cost' : '10MP', 'uses' : 'Refresh After Battle'}

}

all_consumables_in_inventory = {

    
}

all_consumables_in_active = {

    
}

damage_text_group = pygame.sprite.Group()

def consumable_menu(hero, inventory, monster_list, monster_index):  
    left_click = False
    right_click = False
    pygame.mouse.set_visible(True)

    def show_consumables_active(left_click, right_click):
        image_x = 0
        image_y = height_position(0.1)
        #draw the image
        for count, consumables in enumerate(hero.consumables_list):
            image_x += width_position(0.05)
            if image_x > width_position(0.4):
                image_x = width_position(0.05)
                image_y += height_position(0.1)
            image = all_consumables[consumables]['image']
            image = pygame.transform.scale(image,(width(0.05), height(0.05)))
            all_consumables_in_active['image_rect' + f'{count}'] = pygame.rect.Rect(image_x, image_y, width(0.05), height(0.05))            
            screen.blit(image, (image_x, image_y))

            #if collide with hitbox, show the description
            mousex, mousey = pygame.mouse.get_pos()
            if all_consumables_in_active['image_rect' + f'{count}'].collidepoint((mousex,mousey)):
                font_size = pygame.font.Font.size(font, all_consumables[consumables]['description'])
                screen.blit(font.render('NAME:' + all_consumables[consumables]['name'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey))
                screen.blit(font.render('DESC:' + all_consumables[consumables]['description'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
                screen.blit(font.render('COST:' + all_consumables[consumables]['cost'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
                screen.blit(font.render('USES:' + all_consumables[consumables]['uses'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 60))

                if right_click == True:
                    hero.consumables_in_inventory_list.append(all_consumables[consumables]['name'])
                    hero.consumables_list.remove(all_consumables[consumables]['name'])          

    def show_consumables_in_inventory(left_click, right_click):
        image_x = width_position(0.5)
        image_y = height_position(0.1)
        #draw the image
        for count, consumables in enumerate(hero.consumables_in_inventory_list):
            image_x += width_position(0.05)
            if image_x > width_position(0.9):
                image_x = width_position(0.55)
                image_y += height_position(0.1)
            image = all_consumables[consumables]['image']
            image = pygame.transform.scale(image,(width(0.05), height(0.05)))
            all_consumables_in_inventory['image_rect' + f'{count}'] = pygame.rect.Rect(image_x, image_y, width(0.05), height(0.05))
            screen.blit(image, (image_x, image_y))

            #if collide with hitbox, show the description
            mousex, mousey = pygame.mouse.get_pos()
            if all_consumables_in_inventory['image_rect' + f'{count}'].collidepoint((mousex,mousey)):
                font_size = pygame.font.Font.size(font, all_consumables[consumables]['description'])
                screen.blit(font.render('NAME:' + all_consumables[consumables]['name'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey))
                screen.blit(font.render('DESC:' + all_consumables[consumables]['description'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 20))
                screen.blit(font.render('COST:' + all_consumables[consumables]['cost'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 40))
                screen.blit(font.render('USES:' + all_consumables[consumables]['uses'], True, white), ((screen_width / 2) - (font_size[0] / 2), mousey + 60))
                
                if right_click == True and len(hero.consumables_list) < hero.orb_limit:
                    hero.consumables_list.append(all_consumables[consumables]['name'])
                    hero.consumables_in_inventory_list.remove(all_consumables[consumables]['name'])         

    inside_consumable_menu = True
    while inside_consumable_menu:
        clock.tick(fps)
        mousex, mousey = pygame.mouse.get_pos()

        damage_text_group.update()
        damage_text_group.draw(screen)

        screen.blit(consumable_inventory_img, (0,0))
        draw_text_middle(f'CONSUMABLES', font_heading, white, screen_width, 10)
        draw_text(f'GOLD: {hero.gold:.2f}', font, white, width_position(0.03), top_of_bottom_panel)
        draw_text(f'ORB LIMIT: {hero.orb_limit}', font, white, width_position(0.03), top_of_bottom_panel + text_distance)      
                  
        if Map.game_map == 2:
            #consumables
            buy_fireball_rect = draw_text_middle_rect(f'FIREBALL: {hero.consumables_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 2))
            buy_lightning_rect = draw_text_middle_rect(f'LIGHTNING: {hero.consumables_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 3))
            buy_frost_rect = draw_text_middle_rect(f'FROST: {hero.consumables_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 4))    
            buy_heal_rect = draw_text_middle_rect(f'HEAL: {hero.heal_and_restore_consumable_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 5))
            buy_restore_rect = draw_text_middle_rect(f'RESTORE: {hero.heal_and_restore_consumable_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 6))
            buy_orb_limit_rect = draw_text_middle_rect(f'ORB LIMIT: {hero.orb_limit_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 7))          
            buy_combination_rect  = draw_text_middle_rect(f'COMBINE FIRST THREE ITEMS: {hero.consumables_combination_cost}', font, yellow, width_position(0.03), top_of_bottom_panel + (text_distance * 8))

            rect_list = [buy_fireball_rect, buy_lightning_rect, buy_frost_rect, buy_heal_rect, buy_restore_rect, buy_orb_limit_rect, buy_combination_rect]
            for choice in rect_list:
                if choice.collidepoint((mousex,mousey)) and left_click == True:
                    if choice == buy_fireball_rect and hero.gold > hero.consumables_cost:
                        hero.gold -= hero.consumables_cost

                        hero.consumables_in_inventory_list.append('Fireball')
                        hero.consumables_cost += 200

                        left_click = False

                    if choice == buy_lightning_rect and hero.gold > hero.consumables_cost:
                        hero.gold -= hero.consumables_cost  

                        hero.consumables_in_inventory_list.append('Lightning')
                        hero.consumables_cost += 200

                        left_click = False

                    if choice == buy_frost_rect and hero.gold > hero.consumables_cost:
                        hero.gold -= hero.consumables_cost  

                        hero.consumables_in_inventory_list.append('Frost')
                        hero.consumables_cost += 200

                        left_click = False

                    if choice == buy_heal_rect and hero.gold > hero.heal_and_restore_consumable_cost:
                        hero.gold -= hero.heal_and_restore_consumable_cost

                        hero.consumables_in_inventory_list.append('Heal')

                        left_click = False

                    if choice == buy_restore_rect and hero.gold > hero.heal_and_restore_consumable_cost:
                        hero.gold -= hero.heal_and_restore_consumable_cost

                        hero.consumables_in_inventory_list.append('Restore')

                        left_click = False

                    if choice == buy_orb_limit_rect and hero.gold > hero.orb_limit_cost:
                        hero.gold -= hero.orb_limit_cost

                        hero.orb_limit += 1
                        hero.orb_limit_cost += 1000

                        left_click = False

                    if choice == buy_combination_rect and hero.gold > hero.consumables_combination_cost:
                        if hero.consumables_in_inventory_list[0] == 'Fireball' and hero.consumables_in_inventory_list[1] == 'Fireball' and hero.consumables_in_inventory_list[2] == 'Fireball':
                            for i in range(3):
                                del hero.consumables_in_inventory_list[0]
                            hero.gold -= hero.consumables_combination_cost
                            hero.consumables_combination_cost += 200
                            hero.consumables_in_inventory_list.append('Flameball')

                        left_click = False

        show_consumables_active(left_click, right_click)
        show_consumables_in_inventory(left_click, right_click)
            
        right_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inside_consumable_menu = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    hero.active_consumables_list = hero.consumables_list.copy()
                    inside_consumable_menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True   

                if event.button == 3:
                    right_click = True  

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_click = False  

                if event.button == 3:
                    right_click = False 


        pygame.display.update()
