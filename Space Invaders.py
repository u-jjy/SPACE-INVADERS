# Importing and initializing
import pygame
from os import chdir
from random import randint
from random import choice
from math import hypot
from pip._vendor.distlib.compat import raw_input

pygame.init()

# Changing working directory to allow pictures to be loaded - Moved files, making this step a necessity
chdir('Space Game')


difficulty = 'E'

# # Asking for difficulty
# difficulty = raw_input(
#     'Choose your difficulty level:\nEnter E for easy\nEnter I for intermediate\nEnter H for hard\n').upper()
# while difficulty != 'E' and difficulty != 'I' and difficulty != 'H':
#     difficulty = raw_input(
#         'Choose your difficulty level:\nEnter E for easy\nEnter I for intermediate\nEnter H for hard\n').upper()

# Setting screen dimension variables and creating a screen variable
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Creating clock variable for framerate
clock = pygame.time.Clock()

# Changing the title and icon of screen
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo icon.png')  # Must load image into variable as PyGame surface before changing icon
pygame.display.set_icon(icon)

# Loading in audio files as PyGame objects
bullet_fire = pygame.mixer.Sound('bullet_fire.wav')
explosion = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('background_music.wav')  # Loading in music as object, no variable needed
trumpetGameOver = pygame.mixer.Sound('trumpetGameOver.wav')
played_already = False  # Variable to stop multiple playbacks of trumpet sound
# Playing music on loop using -1 as a parameter
pygame.mixer.music.play(-1)


# Player class, attributes and methods
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.image = pygame.image.load('spaceship.png')
        self.vel = 7

    def draw_player(self):
        screen.blit(self.image, (self.x, self.y))

    def move_right(self):
        self.x += self.vel

    def move_left(self):
        self.x -= self.vel

    def check_enemy_collision(self):
        for invader in enemies:
            distance = hypot(self.x - invader.x, self.y - invader.y)
            if distance < 27:
                return True


# Enemy class, attributes and methods
class Enemy:
    def __init__(self, min_score):
        self.x = randint(50, 700)
        self.y = randint(20, 151)
        self.width = 40
        self.height = 40
        self.image = pygame.transform.scale(pygame.image.load('enemy.png'), (40, 40))
        self.x_vel = 6 * choice([-1, 1])  # Randomly makes x velocity negative or positive for the beginning
        if difficulty == 'E':
            self.y_vel = 0.3
        if difficulty == 'I':
            self.y_vel = 0.5
        if difficulty == 'H':
            self.y_vel = 0.7
        self.is_bullet_collision = False
        self.min_score = min_score
        if difficulty == 'E':
            self.lives = 2
        if difficulty == 'I':
            self.lives = 3
        if difficulty == 'H':
            self.lives = 4
        self.lives2 = self.lives

    def draw_enemy(self):
        if score_value >= self.min_score and self.lives > 0:
            screen.blit(self.image, (self.x, self.y))

    def move_enemy(self):
        if score_value >= self.min_score and self.lives > 0:
            # Enemy Movement
            # Constantly adds to x, velocity is made negative if it's on the right, positive if it's on the left
            if self.x <= 0:
                self.x_vel = self.x_vel * - 1
            elif self.x >= 800 - self.width - 5:
                self.x_vel = self.x_vel * - 1

            # Adds to x value using x velocity, which has been altered to negative or positive depending on the value
            self.x += self.x_vel
            # Adds to y value using y velocity, stays constant
            self.y += self.y_vel

    def check_bullet_collision(self):
        if score_value >= self.min_score and self.lives > 0:
            x_centre = self.x + (self.width / 2)
            y_centre = self.y - (self.height / 2)
            bullet_x_centre = bullet.x + (bullet.width / 2)
            bullet_y_centre = bullet.y - (bullet.height / 2)
            distance = hypot(x_centre - bullet_x_centre, y_centre - bullet_y_centre)
            if distance < 33 and self.y < 480:
                self.is_bullet_collision = True

    def respawn(self):
        if score_value >= self.min_score and self.lives > 0:
            self.lives -= 1
            self.x = randint(50, 700)
            self.y = randint(20, 151)
            self.is_bullet_collision = False
        if self.lives == 0:
            self.x = -1000
            self.y = -800
            self.is_bullet_collision = False

    def bullet_collision(self):
        global score_value
        if score_value >= self.min_score and self.lives > 0:
            if self.is_bullet_collision:
                bullet.reset()
                bullet.update_x()
                pygame.mixer.Sound.play(explosion)
                score_value += 1
                self.respawn()


# Bullet class, attributes and methods
class Bullet:
    def __init__(self):
        self.x = spaceship.x + 24
        self.x2 = self.x
        self.y = spaceship.y + 20
        self.y2 = self.y
        self.y_vel = 12
        self.width = 16
        self.height = 16
        self.image = pygame.image.load('bullet2.png')
        self.motion = False

    def draw_bullet(self):
        screen.blit(self.image, (self.x, self.y))

    def fire_bullet(self):
        if not self.motion:
            pygame.mixer.Sound.play(bullet_fire)
        self.motion = True

    def update_x(self):
        self.x = spaceship.x + 24

    def reset(self):
        self.x = self.x2
        self.y = self.y2
        self.motion = False


# Button class, attributes and methods
class Button:
    def __init__(self, x, y, color, text, text_x, text_y):
        self.x = x
        self.y = y
        self.width = len(text) * 9
        self.height = 40
        self.color = color
        if self.color == (0, 255, 0):
            self.color2 = (255, 242, 0)
        if self.color == (255, 0, 0):
            self.color2 = (232, 0, 84)
        self.text = text
        self.font = pygame.font.Font('OpenSans-Bold.ttf', 14)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_x = text_x
        self.text_y = text_y

    def draw_button(self):
        if self.mouse_is_over(mouse_pos):
            pygame.draw.rect(screen, self.color2, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.text_surface, (self.text_x, self.text_y))

    def mouse_is_over(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            return True


# Loading in background image as PyGame surface
bg = pygame.image.load('background2.jpg')

# Instantiating all classes
spaceship = Player(350, 500)
# Enemy objects are given min_score value, this determines the score needed to allow them to activate
space_invader = Enemy(0)
space_invader2 = Enemy(1)
space_invader3 = Enemy(1)
space_invader4 = Enemy(3)
space_invader5 = Enemy(5)
space_invader6 = Enemy(5)
space_invader7 = Enemy(7)
space_invader8 = Enemy(8)
space_invader9 = Enemy(8)
space_invader10 = Enemy(9)
space_invader11 = Enemy(9)
space_invader12 = Enemy(9)
space_invader13 = Enemy(10)
space_invader14 = Enemy(10)
space_invader15 = Enemy(10)
bullet = Bullet()
start_game_button = Button(200, 430, (0, 255, 0), 'Start Game', 206, 440)
quit_button = Button(530, 430, (255, 0, 0), 'Quit Game', 533, 440)
play_again_button = Button(300, 430, (0, 255, 0), 'Play Again', 306, 440)
easy = Button(350, 310, (0, 255, 0), 'Easy', 385, 320)
intermediate = Button(350, 360, (0, 255, 0), 'Intermediate', 356, 370)
hard = Button(350, 410, (0, 255, 0), 'Hard', 385, 420)
easy.width = 108  # Changing button width to equal all three button widths
hard.width = 108

# List of enemies
enemies = [space_invader, space_invader2, space_invader3, space_invader4, space_invader5, space_invader6,
           space_invader7, space_invader8, space_invader9, space_invader10, space_invader11, space_invader12,
           space_invader13, space_invader14, space_invader15]

# Displaying score text on screen
score_value = 0  # Creating variable for value of score to use for displaying
font_for_score = pygame.font.Font('OpenSans-Regular.ttf', 28)  # Creating variable for font and it's size

# Loading in game-over.png as PyGame surface
game_over_image = pygame.image.load('game-over.png')

# Assigning variables for game-over image coordinates
game_over_x = 273
game_over_y = -200
game_over_final_y = 216

# Game Intro
intro_title = pygame.image.load('space_invaders_title.png')
intro_title_x = 150
intro_title_y = 187


def display_score():
    # Creating variable for PyGame surface. Contains text rendered using our loaded font variable
    # Assigning values for text we want used, antialias boolean and color
    score = font_for_score.render("Score: " + str(score_value), True, (255, 255, 255))
    # Drawing score surface onto screen
    screen.blit(score, (10, 10))


# Defining function to see if enemy has been let off screen
def check_position(enemy):
    global game_over
    if enemy.y >= 600:
        game_over = True


already_done = False  # Variable to prevent repeated subtraction from quit_button.x


# Defining function to draw game window
def drawGameWindow():
    global already_done
    if not past_start_screen:
        screen.blit(bg, (0, 0))
        screen.blit(intro_title, (intro_title_x, intro_title_y))
        start_game_button.draw_button()
        quit_button.draw_button()
        pygame.display.update()
    if past_start_screen and not game_begun:
        screen.blit(bg, (0, 0))
        easy.draw_button()
        intermediate.draw_button()
        hard.draw_button()
        pygame.display.update()
    if past_start_screen and game_begun:
        # Bringing game over screen if game_over
        if game_over:
            screen.blit(bg, (0, 0))
            if game_over_y > 210:
                if not already_done:
                    quit_button.x -= 100
                    quit_button.text_x -= 100
                    already_done = True
                quit_button.draw_button()
                play_again_button.draw_button()
            if game_over_y < 210:
                pygame.time.wait(195)
            screen.blit(game_over_image, (game_over_x, game_over_y))
            pygame.display.update()
        else:
            # screen.fill((48, 20, 58))
            screen.blit(bg, (0, 0))
            # Drawing bullet if it has been fired
            if bullet.motion:
                bullet.draw_bullet()
            spaceship.draw_player()  # Drawing player
            # Calling draw enemy method on every enemy, only works if they are activated
            for enemy in enemies:
                enemy.draw_enemy()
            display_score()
            pygame.display.update()


# Main game loop
game_won = False
game_over = False
game_begun = False
played_again = False
past_start_screen = False
already_changed = False
run = True
while run:
    clock.tick(45)  # Using clock to not allow more than 45 iterations a second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_game_button.mouse_is_over(mouse_pos) and not past_start_screen and not game_over:
                past_start_screen = True
            if quit_button.mouse_is_over(mouse_pos) and not game_begun or game_over:
                if not play_again_button.mouse_is_over(mouse_pos):
                    run = False
            if play_again_button.mouse_is_over(mouse_pos) and game_over:
                for enemy in enemies:
                    enemy.lives = enemy.lives2
                    enemy.x = randint(50, 700)
                    enemy.y = randint(20, 151)
                    enemy.is_bullet_collision = False
                score_value = 0
                game_begun = True
                game_over = False
                played_again = True
            if easy.mouse_is_over(mouse_pos) and past_start_screen and not intermediate.mouse_is_over(mouse_pos) and not hard.mouse_is_over(mouse_pos):
                difficulty = 'E'
                game_begun = True

            if intermediate.mouse_is_over(mouse_pos) and past_start_screen and not easy.mouse_is_over(mouse_pos) and not hard.mouse_is_over(mouse_pos):
                difficulty = 'I'
                game_begun = True

            if hard.mouse_is_over(mouse_pos) and past_start_screen and not easy.mouse_is_over(mouse_pos) and not intermediate.mouse_is_over(mouse_pos):
                difficulty = 'H'
                game_begun = True


    for enemy in enemies:
        if not already_changed:
            if difficulty == 'E':
                enemy.y_vel = 0.3
                enemy.lives = 2
            if difficulty == 'I':
                enemy.y_vel = 0.5
                enemy.lives = 3
            if difficulty == 'H':
                enemy.y_vel = 0.7
                enemy.lives = 4
        enemy.lives2 = enemy.lives
        already_changed = True


    if game_over:
        if not played_already:
            pygame.mixer.music.pause()
            trumpetGameOver.play()
            played_already = True
        if game_over_y < game_over_final_y:
            game_over_y += 20

    if game_begun and not game_over:
        if played_again:
            pygame.mixer.music.unpause()
            game_over_y = -200
            played_already = False
            played_again = False

        keys = pygame.key.get_pressed()  # Creating a tuple of all the keys that are pressed, every iteration
        if keys[pygame.K_RIGHT]:  # Checking if right key was pressed
            if spaceship.x < (800 - spaceship.width - 4):
                spaceship.move_right()  # Using method to move spaceship right
        if keys[pygame.K_LEFT]:
            if spaceship.x > 0:
                spaceship.move_left()

        # Bullet Movement
        if bullet.motion:
            # Subtracting from bullet y to make it go up consistently
            bullet.y -= bullet.y_vel
        if bullet.y <= 0 - bullet.height:
            bullet.reset()  # Resetting bullet to original state to allow for re-shooting
        if not bullet.motion:
            bullet.update_x()  # Updating x value of bullet to correspond with ship every iteration
        if keys[pygame.K_SPACE]:
            bullet.fire_bullet()

        # All enemy functions:
        for enemy in enemies:
            # Calling 'move_enemy' method to move invader left to right and down
            enemy.move_enemy()
            # Checking for collision
            enemy.check_bullet_collision()
            #  Respawning enemy and resetting bullet if collision is true using bullet_collision method
            enemy.bullet_collision()

        # Checking if any enemy has collided with ship
        if spaceship.check_enemy_collision():
            game_over = True

        # Checking if any enemy has been let off screen
        for enemy in enemies:
            check_position(enemy)

        # Checking if number of lives for every enemy, adding to dead if lives = 0
        dead = 0  # Assigning dead variable
        for enemy in enemies:
            if enemy.lives == 0:
                dead += 1

        if dead == 15:  # Checking if all enemies are dead
            game_won = True  # Making game won true

    drawGameWindow()

pygame.quit()

print(difficulty)