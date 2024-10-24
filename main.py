import sys
import os
import math
import pygame
import random
from settings import load_settings, save_settings
from volume_settings import load_volume, save_volume
pygame.init()
width = 1300
height = 800


#image assets
jetpack = pygame.image.load('gamepics/jetpack.png')
heart = pygame.image.load("gamepics/heart.PNG")
heart = pygame.transform.scale(heart, (25,25))
background = pygame.image.load('gamepics/background1.PNG')
background = pygame.transform.scale(background, (width, height))
astronaut = pygame.image.load('gamepics/astronaut.PNG')
astronaut2 = pygame.image.load('gamepics/astronaut2old.PNG')
astronaut2 = pygame.transform.scale(astronaut2, (100, 100))
blue_star = pygame.image.load('gamepics/blue_star.PNG')
blue_star = pygame.transform.scale(blue_star, (50, 50))
red_star = pygame.image.load('gamepics/red_star.PNG')
red_star = pygame.transform.scale(red_star, (50, 50))
yellow_star = pygame.image.load('gamepics/yellow_star.PNG')
yellow_star = pygame.transform.scale(yellow_star, (50, 50))
gear = pygame.image.load('gamepics/gear.png')
gear = pygame.transform.scale(gear, (50,50))
astro_icon = pygame.image.load('gamepics/astro_icon.PNG')
astro_icon = pygame.transform.scale(astro_icon, (50,50))




#sound files
pygame.mixer.music.load("sounds/Clair de Lune (Studio Version).mp3")
click_sound = pygame.mixer.Sound('sounds/click.mp3')
death_sound = pygame.mixer.Sound('sounds/deathsound.mp3')
#set window name and dimensions
pygame.display.set_caption('Star Evader')
window = pygame.display.set_mode((width, height))

# Load the volume at the start of the game
volume = load_volume()
pygame.mixer.music.set_volume(volume)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
main_font = pygame.font.SysFont("cambria", 74)
button_font = pygame.font.Font(None, 48)
name_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

######################### SAVE HIGH SCORE ##########################
def load_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            scores = []
            for line in file:
                name, score = line.strip().split(':')
                scores.append((name, float(score)))
            return scores
    except FileNotFoundError:
        return []  # If no file exists, return an empty list

def save_high_score(player_name, new_score):
    try:
        with open("high_scores.txt", "r") as file:
            scores = []
            for line in file:
                name, score = line.strip().split(':')
                scores.append((name, float(score)))
    except FileNotFoundError: #if file don't exist yet
        scores = [] #make empty list of scores

    scores.append((player_name, float(new_score))) #add new score

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5] #sort scores in descending order and keep top 5

    with open("high_scores.txt", "w") as file: #write the update scores back to file
        for name, score in scores:
            file.write(f'{name}:{score}\n')



#####################   SAVE SELECTED SKINS   ##########################
SKIN_FILE = "selected_skin.txt"
def load_selected_skin():
    #load selected skin from file
    if os.path.exists(SKIN_FILE):
        with open(SKIN_FILE, 'r') as file:
            return file.read().strip()
    return 'astronaut' #default skin if no file exists yet
def save_selected_skin(skin_name):
    #save selected skin TO file
    with open(SKIN_FILE, 'w') as file:
        file.write(skin_name)
##display the menu to select astronaut skins
def skin_selection_menu():
    global player

    skins = ['astronaut', 'astronaut2']
    selected_skin = load_selected_skin()

    running = True
    while running:
        clock.tick(60)
        draw_scrolling_background()

        #disply available skins
        for i, skin in enumerate(skins):
            skin_text = button_font.render(skin,True,WHITE)
            skin_text_rect = skin_text.get_rect(center=(width//2, height//4 +i *100))
            window.blit(skin_text, skin_text_rect)
            #check if skin is selected
            if skin == selected_skin:
                pygame.draw.rect(window,GREEN, skin_text_rect.inflate(10,10),3)
        draw_button("Back", width//2-100, height -100, 200, 50, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                for i, skin in enumerate(skins):
                    skin_text_rect = skin_text.get_rect(center=(width // 2, height // 4 + i * 100))
                    if skin_text_rect.collidepoint(mouse_x, mouse_y):
                        click_sound.play()
                        selected_skin = skin  # Update selected skin
                        save_selected_skin(selected_skin)  # Save the selected skin
                        if skin == "astronaut":
                            player.img = astronaut
                        elif skin == "astronaut2":
                            player.img = astronaut2

                    # Check for "Back" button to exit skin selection menu
                    if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                            height - 100 <= mouse_y <= height - 50):
                        click_sound.play()
                        main_menu()

        pygame.display.flip()




# Slider settings
slider_width = 200
slider_height = 20
slider_color = WHITE
slider_x = width - slider_width - 50
slider_y = 700
slider_handle_width = 20
slider_value = volume * slider_width  # Calculate initial slider position based on volume

def draw_slider():
    """Draw the volume slider on the screen."""
    pygame.draw.rect(window, slider_color, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.rect(window, BLUE, (slider_x + slider_value - slider_handle_width // 2, slider_y - 5, slider_handle_width, slider_height + 10))
def handle_slider_event(event):
    """Handle events to adjust the volume slider."""
    global slider_value, volume
    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = event.pos
        if slider_x <= mouse_x <= slider_x + slider_width and slider_y - 10 <= mouse_y <= slider_y + slider_height + 10:
            slider_value = mouse_x - slider_x
            volume = slider_value / slider_width  # Update volume based on slider position
            pygame.mixer.music.set_volume(volume)
            save_volume(volume)  # Save the updated volume



class Player(object):
    def __init__(self):
        selected_skin = load_selected_skin()
        self.img = pygame.image.load(f'gamepics/{selected_skin}.PNG')
        self.w = 75#self.img.get_width()
        self.h = 75#self.img.get_height()
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
        self.x = width
        self.y = random.randint(0, height)
        #self.speed = random.randint(4, 8)
        if self.rank == 1:
            self.image = yellow_star
            self.speed = 5
        elif self.rank == 2:
            self.image = blue_star
            self.speed = 2
        else:
            self.image = red_star
            self.speed = 8
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self):
        # Move the star to the left (assuming horizontal scrolling)
        self.x -= self.speed

    def draw(self, window):
        # Draw the star (you can replace this with an image or a shape)
        window.blit(self.image, (self.x, self.y))

    def off_screen(self):
        # Check if the star has moved off the left side of the screen
        return self.x < -self.w
class Heart:
    def __init__(self, x, y):
        self.image = heart  # Load your heart image
        self.x = x
        self.y = y
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
class Item:
    def __init__(self):
        self.image = pygame.image.load("gamepics/alien.PNG")  # Load item image
        self.x = width
        self.y = random.randint(0, height)
        self.speed = random.randint(3,6)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def move(self):
        self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x < -self.image.get_width()
class Asteroid:
    def __init__(self):
        self.img = pygame.image.load('gamepics/asteroids.png')  # Load your asteroid image
        self.rect = self.img.get_rect()
        self.x = random.randint(0, width - self.rect.width)
        self.y = 0  # Start above the screen
        self.speed = 0.1  # Set a speed for the asteroid
        self.rect.topleft = (self.x, self.y)

    def move(self):
        self.y += self.speed  # Move down the screen
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        window.blit(self.img, self.rect)

    def off_screen(self):
        return self.y > height  # Check if the asteroid is off the screen
class SpeedBoost:
    def __init__(self, x, y):
        self.image = jetpack  # Load your speed boost image
        self.x = x
        self.y = y
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.count = count

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def spawn_item(item_list, spawn_rate):
    if random.randint(0, 1000) < spawn_rate:  # Adjust the spawn rate
        item_list.append(Item())


def spawn_stars(stars, star_spawn_rate):
  # Spawn stars at random intervals based on the spawn rate
  if random.randint(0, 100) < star_spawn_rate:
    rank = random.randint(1, 3)
    stars.append(Star(rank))


def update_stars(stars, window):
  # Move and draw all the stars, and remove stars that go off-screen
  for star in stars[:]:
    star.move()
    star.draw(window)
    if star.off_screen():
      stars.remove(star)

gameover = False
player = Player()
stars = []
count = 0 #integer gets bigger each time while loop run (used for star creation)
red_bar_length = width

################################# SAVE PLAYER NAME ###############################3
# File to save player name
NAME_FILE = "player_name.txt"
def load_player_name():
    """Load the player's name from a file."""
    if os.path.exists(NAME_FILE):
        with open(NAME_FILE, 'r') as file:
            return file.read().strip()
    return None
def save_player_name(name):
    """Save the player's name to a file."""
    with open(NAME_FILE, 'w') as file:
        file.write(name)
def get_player_name():
    """Get the player's name from input, or prompt for it if not available."""
    name = load_player_name()
    if name is None:
        name = input_name()  # Ask for name if not found
    return name
def input_name():
    """Prompt the user to enter their name."""
    name = ""
    input_active = True
    while input_active:
        window.fill(BLACK)
        prompt_text = main_font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 3))
        window.blit(prompt_text, prompt_rect)

        # Render the current input name
        name_text = name_font.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(width // 2, height // 2))
        window.blit(name_text, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    save_player_name(name)
                    input_active = False  # Exit input loop
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Remove last character
                else:
                    name += event.unicode  # Add character to name

        pygame.display.flip()

    return name


def apply_red_tint(image):
    # Create a red surface with the same size as the original image
    tint = pygame.Surface(image.get_size())
    tint.fill((255, 0, 0))  # Fill it with red color
    tint.set_alpha(128)  # Set the transparency level (0 is fully transparent, 255 is fully opaque)

    # Blit the red surface onto the image to create the tinted effect
    tinted_image = image.copy()
    tinted_image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Use alpha blending
    return tinted_image


################################### DRAWING FUNCTIONS #############################
def redraw_game_window(lives, hearts, items, asteroids, speed_boosts):

    draw_scrolling_background()

    if movement_disabled:
        tinted_player_image = apply_red_tint(player.img)
        window.blit(tinted_player_image, player.rect.topleft)
    else:
        player.draw(window) # draw player to the window
    for a in stars:
        a.draw(window)
    for heart in hearts:
        heart.draw(window)
    for item in items:
        item.draw(window)
    for asteroid in asteroids:
        asteroid.draw(window)
    for speed_boost in speed_boosts:
        speed_boost.draw(window)
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds

    if game_mode != 'free':
        bar_width = max(width * (1 - elapsed_time / 30), 0)  # Reduces over 30 seconds
        pygame.draw.rect(window, (255, 0, 0), (0, 0, bar_width, 20))
    else:
        stopwatch_text = main_font.render(f"Time: {int(elapsed_time)}s", True, WHITE)

        window.blit(stopwatch_text, (475, 10))

    pygame.display.flip() #update the display
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(window, color, (x,y,w,h)) #draw button rectangle

    button_text = button_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(button_text, text_rect)

##################################### MENUS AND SCREENS ##############################
def settings_menu():
    settings = load_settings()
    running = True

    while running:
        clock.tick(60)
        draw_scrolling_background()

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
                        click_sound.play()
                        settings['game_mode'] = 'easy'
                    elif height // 2 - 25 <= mouse_y <= height // 2 + 25:
                        click_sound.play()
                        settings['game_mode'] = 'medium'
                    elif height // 2 + 50 <= mouse_y <= height // 2 + 100:
                        click_sound.play()
                        settings['game_mode'] = 'hard'
                    elif height // 2 + 125 <= mouse_y <= height // 2 + 175:
                        click_sound.play()
                        settings['game_mode'] = 'free'

                    # Save settings after any change
                    save_settings(settings)

                # Check for "Back" button to exit settings menu
                if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (
                        height // 2 + 200 <= mouse_y <= height // 2 + 250):
                    click_sound.play()
                    running = False
                    main_menu()  # Return to main menu

        pygame.display.flip()
#load image
bg = pygame.image.load("gamepics/space_bg2.JPG").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

#define game variables
scroll = 0
tiles = math.ceil(width  / bg_width) + 1
def draw_scrolling_background():
  global scroll
  # draw scrolling background
  for i in range(0, tiles):
    window.blit(bg, (i * bg_width + scroll, 0))
    # bg_rect.x = i * bg_width + scroll
    # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

  # scroll background
  scroll -= 2

  # reset scroll
  if abs(scroll) > bg_width:
    scroll = 0
def main_menu():
    running = True
    player_name = get_player_name()
    high_scores = load_high_scores()
    while running:
        clock.tick(60)
        draw_scrolling_background()  # Clear the screen

        # Draw title
        title_text = main_font.render("Star Evader", True, WHITE)
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        window.blit(title_text, title_rect)

        # Draw player name
        name_text = name_font.render(f"Player: {player_name}", True, WHITE)
        name_rect = name_text.get_rect(center=(width // 2, height // 3))
        window.blit(name_text, name_rect)

        # Display High Scores
        score_y_position = height // 2 - 50  # Adjust this as necessary
        for index, (name, score) in enumerate(high_scores):
            score_text = name_font.render(f"{index + 1}. {name}: {score:.2f}s", True, WHITE)
            score_rect = score_text.get_rect(center=(width // 2, score_y_position))
            window.blit(score_text, score_rect)
            score_y_position += 40  # Spacing between scores


        #button dimensions
        button_width = 200
        button_height = 100

        #button positions as rects
        start_button_rect = pygame.Rect(20, 650, button_width, button_height)
        quit_button_rect = pygame.Rect(240, 650, button_width, button_height)

        # Draw buttons
        draw_button("Start", start_button_rect.x, start_button_rect.y, button_width, button_height, BLUE)
        draw_button("Quit", quit_button_rect.x, quit_button_rect.y, button_width, button_height, RED)
        gear_rect = gear.get_rect(center=(width - 60, 60))  # Position at top-right corner
        window.blit(gear, gear_rect)
        astro_icon_rect = astro_icon.get_rect(center=(width-60,110))
        window.blit(astro_icon, astro_icon_rect)

        # Draw volume slider
        draw_slider()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                handle_slider_event(event)



            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if the Start button is clicked
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    main_game_loop()  # Exit opening screen to start the game

                # Check if the Quit button is clicked
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    sys.exit(0)

                # Check if the settings button (gear icon) is clicked
                if gear_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    settings_menu()

                #Check if player_skin button is clicked (astro_icon)
                if astro_icon_rect.collidepoint(mouse_x, mouse_y):
                    pass
                    click_sound.play()
                    skin_selection_menu()


                # Check if the player clicked on the name text
                if name_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    # Input new player name
                    new_name = input_name()
                    if new_name:
                        player_name = new_name
                        save_player_name(player_name)  # Save new name

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
                    player.img = pygame.transform.scale(player.img, (75, 75))
                    player.rect = player.img.get_rect(topleft=(player.x, player.y))
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
    #player = Player()
    red_bar_length = width

def main_game_loop():
    global run, count, gameover, stars, player, start_time, game_mode, movement_disabled
    lives = 3
    hearts = [Heart(10 + i * 40, 20) for i in range(lives)]
    speed_boosts = [SpeedBoost(10 + i * 40, 80) for i in range(3)]  # Create 3 speed boosts
    invincible = False
    invincibility_start = 0
    invincibility_duration = 2000
    items = []
    asteroids = []
    enlarged = False
    enlarged_time = 0
    enlarged_duration = 5
    enlargement_count = 0
    max_enlargements = 1
    movement_disabled = False
    movement_disable_start = 0
    movement_disable_duration = 3000  # 3 seconds
    # Speed boost variables
    available_boosts = 3
    boost_duration = 5  # Duration of the speed boost in seconds
    boost_active = False
    boost_start_time = 0

    # Store the original player image dimensions
    original_width = player.img.get_width()
    original_height = player.img.get_height()


    settings = load_settings()
    game_mode = settings["game_mode"]
    run = True
    start_time = pygame.time.get_ticks() #starts a time for red bar
    player_name = get_player_name()

    # Update difficulty behavior
    if game_mode == "easy":
        player.speed = 8
        spawn_rate = 70
    elif game_mode == "medium":
        player.speed = 5
        spawn_rate = 50
    elif game_mode == "hard":
        player.speed = 3
        spawn_rate = 15
    elif game_mode == "free":
        player.speed = 5
        spawn_rate = 20
        # Free Mode Logic: no gameover, just a timer


    while run:
        clock.tick(60)
        count += 1
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 # time in seconds
        #red_bar_length = max(0, width - (width*(elapsed_time/30)))

        # Check if invincibility should end
        if invincible and pygame.time.get_ticks() - invincibility_start > invincibility_duration:
            invincible = False  # Reset invincibility after 2 seconds


        #spawn new stars and asteroids
        if not gameover:
            if count % spawn_rate == 0: #make a new star every 'spawn_rate' frames
                ran = random.choice([1, 1, 1, 2, 2, 3]) if game_mode != "free" else random.choice([1, 2, 3]) #changes probability of each star type
                stars.append(Star(ran))

                #spawn asteroids only in hard mode
                if game_mode == ('hard') or game_mode == ('medium') or game_mode == ('free'):
                    if count % 150 == 0:
                        asteroids.append(Asteroid())
                    # Handle speed boost spawning (you can adjust the spawn rate as needed)

            #move stars and check for collisions
            for star in stars:
                star.move()
                star.rect.topleft = (star.x, star.y) #update star rect position

                #check collision between star and player
                if not invincible and player.rect.colliderect(star.rect):
                    death_sound.play()
                    lives -= 1
                    hearts.pop()
                    invincible = True
                    invincibility_start = pygame.time.get_ticks()

                    if lives <= 0:
                        gameover = True
                    break
                    # Move asteroids and check for collisions
                for asteroid in asteroids:
                    asteroid.move()
                    if asteroid.off_screen():
                        asteroids.remove(asteroid)

                    # Check collision between asteroid and player
                    if player.rect.colliderect(asteroid.rect):
                        movement_disabled = True
                        movement_disable_start = pygame.time.get_ticks()
                        asteroids.remove(asteroid)  # Remove asteroid upon collision

        # Spawn and handle items
        spawn_item(items, 5)  # Adjust spawn rate for items
        for item in items[:]:
            item.move()
            item.draw(window)
            if item.off_screen():
                items.remove(item)

            # Check for item collision and enlarge player
            if player.rect.colliderect(item.rect):
                if enlargement_count < max_enlargements:
                    enlarged = True
                    enlarged_time = pygame.time.get_ticks()
                    player.img = pygame.transform.scale(player.img,
                                                          (player.img.get_width() * 2, player.img.get_height() * 2))
                    player.rect = player.img.get_rect(topleft=(player.x, player.y))
                    items.remove(item)
                    enlargement_count += 1
        # Reset player size after enlargement duration
        if enlarged:
            elapsed_enlarge_time = (pygame.time.get_ticks() - enlarged_time) / 1000
            if elapsed_enlarge_time > enlarged_duration:
                # Reset player size
                player.img = pygame.transform.scale(player.img, (
                player.img.get_width() // 2, player.img.get_height() // 2))
                player.rect = player.img.get_rect(topleft=(player.x, player.y))
                enlarged = False
                enlargement_count = 0

        #Manage speed boost
        if boost_active:
            elapsed_boost_time = (pygame.time.get_ticks() - boost_start_time) / 1000
            if elapsed_boost_time > boost_duration:
                player.speed /= 2  # Reset speed after boost duration
                boost_active = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and available_boosts > 0 and not boost_active:
            speed_boosts.pop()
            player.speed *= 2  # Increase player speed
            boost_active = True
            boost_start_time = pygame.time.get_ticks()
            available_boosts -= 1


        # Disable player movement for a set duration
        if movement_disabled:

            elapsed_disable_time = (pygame.time.get_ticks() - movement_disable_start)
            if elapsed_disable_time > movement_disable_duration:
                movement_disabled = False

        if gameover or (elapsed_time >= 30 and game_mode != 'free'):
            player.img = pygame.transform.scale(player.img, (original_width, original_height))
            player.rect = player.img.get_rect(topleft=(player.x, player.y))

        ##########exit the game with x button###########
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        #take input for movement
        if not movement_disabled:
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
        redraw_game_window(lives, hearts, items, asteroids, speed_boosts)


        if gameover and game_mode == 'free': #if in free mode
            save_high_score(player_name, float(elapsed_time))
            show_game_over_screen()
        if elapsed_time >= 30 and game_mode != 'free': #if not in free mode and you win
            you_win_screen()
        if gameover: #if not in free mode and you fail
            show_game_over_screen()

    pygame.quit()



#play music in loop
pygame.mixer.music.play(-1)
main_menu()





