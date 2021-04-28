import pygame
import random
import math as m
import time
pygame.init()

def main():
    TRANSPARENT = (0,0,0,0)
    OPAQUE = (255,0,0,255)
    RUNNING = True
    TOTAL_SCORE = 0

# SCREEN DISPLAY SIZE, TITLE, AND OTHERS
    class Screen():
        text_font = "freesansbold.ttf"
        screen = pygame.display.set_mode((800,600))
        reload_font = pygame.font.Font(f"{text_font}",50)
        reload_text = reload_font.render("Out of ammo", True, (255,255,255))
        score_font = pygame.font.Font(f"{text_font}",50)
        game_over_font = pygame.font.Font(f"{text_font}",50)
        game_over_text = game_over_font.render("Game Over!",True,(255,255,255))
        restart_font = pygame.font.Font(f"{text_font}",15)
        restart_text = restart_font.render("Press escape to restart",True, (255,255,255))

        def set_screen_caption(self):
            pygame.display.set_caption("My first Pygame")

        def display_reload_text(self, x,y):
            self.screen.blit(self.reload_text, (x,y))

        def display_score(self,x,y):
            score_text = self.reload_font.render(str(TOTAL_SCORE),True,(255,255,255))
            self.screen.blit(score_text,(x,y))
        
        def display_restart(self,x,y):
            self.screen.blit(self.game_over_text,(x,y))
            self.screen.blit(self.restart_text,(x + 60 ,y + 55))
            
    screen_init = Screen()
    screen_init.set_screen_caption

# CHARACTER VARIABLES
    class Character():
        def __init__(self):
            self.character_img = pygame.image.load("assets/xwing50.png")
            self.character_x = 375
            self.character_y = 500
            self.character_x_change = 0
            self.is_character_dead = False

    # TO DISPLAY THE CHARACTER

        def display_character(self,x,y):
            screen_init.screen.blit(self.character_img,(x,y))

    character_init = Character()
    character_init_properties = vars(character_init)

# BULLET VARIABLES
    bullet_count = 10

    class Bullet():
        def __init__(self):
            self.bullet_img = pygame.image.load("assets/bullet30.png")
            
            self.bullet_x = character_init.character_x + 10
            self.bullet_y = character_init.character_y + 10
            self.bullet_x_change = 0
            self.bullet_y_change = 0
            self.rockets_shot = []
            self.out_of_rockets = False
            self.number_of_rockets = 0

    # TO DISPLAY THE BULLET

        def display_bullet(self,x,y):
            screen_init.screen.blit(self.bullet_img, (x,y))

    bullet_init = Bullet()
    bullet_init_properties = vars(bullet_init)

# ENEMY VARIABLES 
    class Enemy():
        def __init__(self,img_path,x,y,x_change,y_change):
            self.enemy_img = pygame.image.load(img_path)
            self.enemy_x = x 
            self.enemy_x_change = x_change
            self.enemy_y = y
            self.enemy_y_change = y_change
            self.explosion_img = pygame.image.load("assets/explosion56.png")
            self.is_enemy_killed = False

    # TO DISPLAY THE ENEMY

        def display_enemy(self,x,y):
            screen_init.screen.blit(self.enemy_img,(x,y))

    # TO DISPLAY THE EXPLOSION

        def display_explosion(self,x,y):
            screen_init.screen.blit(self.explosion_img, (x,y))

    # FOR DISPLAYING THE ENEMIES
    
    enemy_count = 5
    enemy_array = []
    x = random.randrange(20,300)

    for enemy in range(enemy_count):
        img_path = "assets/tiefighter55.png"
        x +=80
        
        y = 150
        x_change = 0
        y_change = 0
        enemy_array.append(Enemy(img_path,x,y,x_change,y_change))
    
# POWERUP VARIABLES

    class PowerUp():
        def __init__(self):
            self.powerup_x = random.randrange(100,700)
            self.powerup_y = 510
            self.powerup_img = pygame.image.load("assets/gunpowerup50.png")
            self.is_powerup = False
        def display_powerup(self,x,y):
            screen_init.screen.blit(self.powerup_img,(x,y))
    powerup_init = PowerUp()

# IN-GAME TIMER
    start_timer = pygame.time.get_ticks()

# BACKGROUND SETTINGS

    def bg_settings():
        bg_color = (0,0,10)
        return bg_color

# COLLISION DETECTION
    def is_collided(enemy_x, enemy_y, bullet_x, bullet_y):
        distance = m.sqrt((m.pow(enemy_x - bullet_x,2)) + (m.pow(enemy_y - bullet_y, 2)))
       
        if distance < 55:
            return True
        else:
            return False

# WHILE LOOP

    while RUNNING == True:
        milliseconds = pygame.time.get_ticks() - start_timer
        seconds = milliseconds / 1000
        
        # print(seconds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
 
# KEYBINDS
            
            if event.type == pygame.KEYDOWN:

    # MOVEMENT KEYS

                if event.key == pygame.K_LEFT:
                    character_init.character_x_change = -2
                    bullet_init.bullet_x_change = -2

                if event.key == pygame.K_RIGHT:
                    character_init.character_x_change = 2
                    bullet_init.bullet_x_change = 2

    # OTHER FUNCTIONS KEYS

                if event.key == pygame.K_SPACE:
                    bullet_init.bullet_y_change = -5
                if event.key == pygame.K_ESCAPE:
                    main()

            if event.type == pygame.KEYUP:

    # MOVEMENT STOPPER KEY FUNCTIONS
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_init.character_x_change = 0
                    bullet_init.bullet_x_change = 0

# BACKGROUND COLOR DISPLAY 
        screen_init.screen.fill(bg_settings())

# COLLISION AND EXPLOSIONS (almost done check note)

        
        for enemy in enemy_array:
            enemy.enemy_y += enemy.enemy_y_change
            collision_detect = is_collided(enemy.enemy_x,enemy.enemy_y,bullet_init.bullet_x,bullet_init.bullet_y)
            enemy.enemy_img.fill(TRANSPARENT)
            if seconds >= 5:
                enemy.enemy_img.fill(OPAQUE)
            if collision_detect == True:
                bullet_init.bullet_x = character_init.character_x + 10
                bullet_init.bullet_y = character_init.character_y + 10
                enemy.enemy_img.fill(TRANSPARENT)
                enemy.display_explosion(enemy.enemy_x,enemy.enemy_y)
                TOTAL_SCORE += 100
                enemy_array.remove(enemy)
                enemy.is_enemy_killed = True

            if seconds >= 7 and seconds <= 8:
                if enemy.is_enemy_killed == False:
                    enemy.enemy_y_change = 5

                
                    if is_collided(enemy.enemy_x,enemy.enemy_y,character_init.character_x,character_init.character_y) == True:
                        enemy.display_explosion(character_init.character_x,character_init.character_y)
                        character_init.character_img.fill(TRANSPARENT)
                        bullet_init.bullet_img.fill(TRANSPARENT)
                        
                        enemy_array.remove(enemy)
                        enemy.enemy_y_change = 0
                        character_init.is_character_dead = True
                        enemy.is_enemy_killed = True
                    if enemy.enemy_y == 650:
                        enemy_array.remove(enemy)
                    

        if character_init.is_character_dead == True:
            screen_init.display_restart(250,300)
                
# VALUES THAT ARE UNDECLARABLE AT THE START 

        character_init.character_x += character_init.character_x_change
      
        bullet_init.bullet_x += bullet_init.bullet_x_change
        bullet_init.bullet_y += bullet_init.bullet_y_change

        if bullet_init.bullet_y == -10:
            bullet_init.bullet_x = character_init.character_x + 10
            bullet_init.bullet_y = character_init.character_y + 10

# BULLET, SHIP, AND ENEMY DISPLAY 

        bullet_init.display_bullet(bullet_init.bullet_x,bullet_init.bullet_y)

        character_init.display_character(character_init.character_x,character_init.character_y)
        for enemy in enemy_array:
            enemy.display_enemy(enemy.enemy_x, enemy.enemy_y)

        screen_init.display_score(55,55)

    # POWERUPS

        if seconds >= 10:
            if character_init.is_character_dead == True:
                pass
            else:
                powerup_init.display_powerup(powerup_init.powerup_x,powerup_init.powerup_y)
            

            if is_collided(character_init.character_x,character_init.character_y,powerup_init.powerup_x,powerup_init.powerup_y):
                powerup_init.is_powerup = True
                powerup_init.powerup_img.fill(TRANSPARENT)
            
        
        if powerup_init.is_powerup == True:
            bullet_init.display_bullet(bullet_init.bullet_x + 15,bullet_init.bullet_y + 10)
            bullet_init.display_bullet(bullet_init.bullet_x - 13,bullet_init.bullet_y +10 )

    # UPDATING THE DISPLAY SCREEN
        pygame.display.update()


main()





# ----------------------------------------------------------------------------------------------------------------------
# note
# when seconds is greater than or equal to 5 then the boxes will appear 
# based on https://nerdparadise.com/programming/pygameblitopacity there will be a box which there is 
# so follow instructions and rename when necessary









# unused settings, just copy paste

    # K_UP and K_DOWN
                # if event.key == pygame.K_UP:
                #     character_init.character_y_change = -2              

                # if event.key == pygame.K_DOWN:
                #     character_init.character_y_change = 2


    # OUT OF AMMO FOR K_SPACE
                    # if len(bullet_init.bullets_shot) == 10:
                    #     bullet_init.out_of_ammo = True

                    # else:
                    #     bullet_init.number_of_bullets += 1
                    #     bullet_init.bullets_shot.append(bullet_init.number_of_bullets)

    # RELOADING FUNCTION FOR K_R
                # if event.key == pygame.K_r:
                    # if bullet_init.out_of_ammo == True:
                    #     bullet_init.bullets_shot = []

                    #     bullet_init.out_of_ammo = False
         
                    # print("Reloading...cover me!")

    # OUT OF AMMO TEXT
        # if bullet_init.out_of_ammo == True:
        #     screen_init.display_reload_text(225 , 300)