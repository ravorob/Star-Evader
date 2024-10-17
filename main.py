import sys
import pygame
import random
from settings import load_settings, save_settings
pygame.init()
width = 800
height = 800

#image assets
background = pygame.image.load('gamepics/background1.PNG')
background = pygame.transform.scale(background, (width, height))
astronaut = pygame.image.load('gamepics/astronaut.PNG')
blue_star = pygame.image.load('gamepics/blue_star.PNG')
blue_star = pygame.transform.scale(blue_star, (50, 50))
red_star = pygame.image.load('gamepics/red_star.PNG')
red_star = pygame.transform.scale(red_star, (50, 50))
yellow_star = pygame.image.load('gamepics/yellow_star.PNG')
yellow_star = pygame.transform.scale(yellow_star, (50, 50))
gear = pygame.image.load('gamepics/gear.png')
gear = pygame.transform.scale(gear, (50,50))
#sound files
pygame.mixer.music.load("sounds/Clair de Lune (Studio Version).mp3")
click_sound = pygame.mixer.Sound('sounds/click.mp3')
death_sound = pygame.mixer.Sound('sounds/deathsound.mp3')
#set window name and dimensions
pygame.display.set_caption('Star Dodger')
window = pygame.display.set_mode((width, height))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
main_font = pygame.font.SysFont("cambria", 74)
button_font = pygame.font.Font(None, 48)

clock = pygame.time.Clock()



class Player(object):
    def __init__(self):
        self.img = astronaut
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = width//2
        self.y = height//2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.speed = 5
    def draw(self, window):
        window.blit(self.img, [self.x, self.y, self.w, self.h])
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        #boundary checks below
        if self.x < 0:
            self.x = 0
        if self.x > width - self.w:
            self.x = width - self.w
        if self.y < 0:
            self.y = 0
        if self.y > height - self.h:
            self.y = height - self.h
class Star(object):
    def __init__(self,rank):
        self.rank = rank
        if self.rank == 1:
            self.image = yellow_star
        elif self.rank == 2:
            self.image = blue_star
        else:
            self.image = red_star
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, width-self.w), random.choice([-1*self.h - 5, height+5])), (random.choice([-1*self.w - 5, width + 5]),random.randrange(0, height-self.h))])
        self.x, self.y = self.ranPoint
        if self.x < width//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < height//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1, 3)

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

gameover = False
player = Player()
stars = []
count = 0 #integer gets bigger each time while loop run (used for star creation)
red_bar_length = width




def redraw_game_window():

    window.blit(background, (0,0))
    player.draw(window) # draw player to the window
    for a in stars:
        a.draw(window)

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds

    if game_mode != 'free':
        bar_width = max(width * (1 - elapsed_time / 30), 0)  # Reduces over 30 seconds
        pygame.draw.rect(window, (255, 0, 0), (0, 0, bar_width, 20))
    else:
        stopwatch_text = main_font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
        window.blit(stopwatch_text, (10, 10))

    pygame.display.update() #update the display
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(window, color, (x,y,w,h)) #draw button rectangle

    button_text = button_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(button_text, text_rect)


def settings_menu():
    settings = load_settings()
    running = True

    while running:
        window.fill(BLACK)

        # Display the current difficulty setting
        difficulty_text = main_font.render(f"Game Mode: {settings['game_mode']}", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(center=(width // 2, height // 4))
        window.blit(difficulty_text, difficulty_rect)

        # Draw buttons for selecting game modes
        draw_button("Easy", width // 2 - 100, height // 2 - 100, 200, 50, GREEN)
        draw_button("Medium", width // 2 - 100, height // 2 - 25, 200, 50, BLUE)
        draw_button("Hard", width // 2 - 100, height // 2 + 50, 200, 50, RED)
        draw_button("Free Mode", width // 2 - 100, height // 2 + 125, 200, 50, BLACK)

        # Draw back button to return to main menu
        draw_button("Back", width // 2 - 100, height // 2 + 200, 200, 50, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check for game mode selection and save to settings
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100):
                    if height // 2 - 100 <= mouse_y <= height // 2 - 50:
                        settings['game_mode'] = 'easy'
                    elif height // 2 - 25 <= mouse_y <= height // 2 + 25:
                        settings['game_mode'] = 'medium'
                    elif height // 2 + 50 <= mouse_y <= height // 2 + 100:
                        settings['game_mode'] = 'hard'
                    elif height // 2 + 125 <= mouse_y <= height // 2 + 175:
                        settings['game_mode'] = 'free'

                    # Save settings after any change
                    save_settings(settings)

                # Check for "Back" button to exit settings menu
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 200 <= mouse_y <= height // 2 + 250):
                    running = False
                    main_menu()  # Return to main menu

        pygame.display.flip()


def main_menu():
    running = True
    while running:
        window.fill(BLACK)  # Clear the screen

        # Draw title
        title_text = main_font.render("My Game", True, WHITE)
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        window.blit(title_text, title_rect)

        # Draw buttons
        draw_button("Start", width // 2 - 100, height // 2 - 50, 200, 100, BLUE)
        draw_button("Quit", width // 2 - 100, height // 2 + 50, 200, 100, RED)
        gear_rect = gear.get_rect(center=(width - 60, 60))  # Position at top-right corner
        window.blit(gear, gear_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if the Start button is clicked
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 - 50 <= mouse_y <= height // 2 + 50):
                    click_sound.play()
                    main_game_loop()  # Exit opening screen to start the game

                # Check if the Quit button is clicked
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 50 <= mouse_y <= height // 2 + 150):
                    click_sound.play()
                    sys.exit(0)

                # Check if the settings button (gear icon) is clicked
                if gear_rect.collidepoint(mouse_x, mouse_y):
                    settings_menu()

        pygame.display.flip()  # Update the display
def show_game_over_screen():
    game_over_text = main_font.render("Game Over", True, WHITE)  # actual text
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 4))  # text's position
    window.blit(game_over_text, game_over_rect)

    # draw buttons
    draw_button("Try Again", width // 2 - 100, height // 2 - 50, 200, 100, BLUE)
    draw_button("Quit", width // 2 - 100, height // 2 + 50, 200, 100, RED)
    draw_button("Main Menu", width // 2 - 100, height // 2 + 150, 200, 100, GREEN)
    # update display to show game over
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # IF TRY AGAIN
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 - 50 <= mouse_y <= height // 2 + 50):
                    click_sound.play()
                    reset_game()
                    main_game_loop()
                #IF QUIT
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 50 <= mouse_y <= height // 2 + 150):
                    click_sound.play()
                    sys.exit(0)

                #IF MAIN MENU
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 150 <= mouse_y <= height // 2 + 250):
                    reset_game()
                    waiting = False
                    click_sound.play()
                    main_menu()
def you_win_screen():
    win_text = main_font.render("You Win!", True, WHITE)
    win_text_rect = win_text.get_rect(center = (width//2,height//4))
    window.blit(win_text,win_text_rect)

    # draw buttons
    draw_button("Try Again", width // 2 - 100, height // 2 - 50, 200, 100, BLUE)
    draw_button("Quit", width // 2 - 100, height // 2 + 50, 200, 100, RED)
    draw_button("Main Menu", width // 2 - 100, height // 2 + 150, 200, 100, GREEN)
    # update display to show game over
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # IF TRY AGAIN
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 - 50 <= mouse_y <= height // 2 + 50):
                    click_sound.play()
                    reset_game()
                    main_game_loop()
                # IF QUIT
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 50 <= mouse_y <= height // 2 + 150):
                    click_sound.play()
                    sys.exit(0)

                # IF MAIN MENU
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 150 <= mouse_y <= height // 2 + 250):
                    click_sound.play()
                    reset_game()
                    waiting = False
                    main_menu()



def reset_game():
    # reset the game
    global gameover, stars,count, player, red_bar_length
    gameover = False
    stars = []
    count = 0
    player = Player()
    red_bar_length = width

def main_game_loop():
    global run, count, gameover, stars, player, start_time, game_mode
    settings = load_settings()
    game_mode = settings["game_mode"]
    run = True
    start_time = pygame.time.get_ticks() #starts a time for red bar

    # Update difficulty behavior
    if game_mode == "easy":
        player.speed = 8
        spawn_rate = 70
    elif game_mode == "medium":
        player.speed = 5
        spawn_rate = 50
    elif game_mode == "hard":
        player.speed = 2
        spawn_rate = 20
    elif game_mode == "free":
        player.speed = 5
        spawn_rate = 50
        # Free Mode Logic: no gameover, just a timer


    while run:
        clock.tick(60)
        count += 1
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 # time in seconds
        #red_bar_length = max(0, width - (width*(elapsed_time/30)))

        #spawn new stars
        if not gameover:
            if count % spawn_rate == 0: #make a new star every 'spawn_rate' frames
                ran = random.choice([1, 1, 1, 2, 2, 3]) if game_mode != "free" else random.choice([1, 2, 3]) #changes probability of each star type
                stars.append(Star(ran))
            #move stars and check for collisions
            for star in stars:
                star.x += star.xv
                star.y += star.yv
                star.rect.topleft = (star.x, star.y) #update star rect position

                #check collision between star and player
                if player.rect.colliderect(star.rect):
                    death_sound.play()

                    gameover = True
                    break

        ##########exit the game with x button###########
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        #take input for movement
        keys = pygame.key.get_pressed()
        dx, dy = 0,0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        player.move(dx, dy)
        player.rect.topleft = (player.x,player.y)

        #calls function to draw everything
        redraw_game_window()


        if gameover:
            show_game_over_screen()
        if elapsed_time >= 30 and game_mode != 'free':
            you_win_screen()

    pygame.quit()

#play music in loop
pygame.mixer.music.play(-1)
main_menu()





