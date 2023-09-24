import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Create Game Window
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hell Loop: Eternal Clash")

# Set Framerate
clock = pygame.time.Clock()
fps = 60

# Define Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
light_blue = (191, 239, 255)
light_coral = (240, 128, 128)

# Define Game Variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] # Player Scores of Player 1 & Player 2
round_over = False
round_over_cooldown = 2000

# Define Fighter Variables
martial_warrior_1_size = 200
martial_warrior_1_scale = 3
martial_warrior_1_offset = [86, 88]
martial_warrior_1_data = [martial_warrior_1_size, martial_warrior_1_scale, martial_warrior_1_offset]

martial_warrior_2_size = 150
martial_warrior_2_scale = 4
martial_warrior_2_offset = [64, 71]
martial_warrior_2_data = [martial_warrior_2_size, martial_warrior_2_scale, martial_warrior_2_offset]

# Load Music and Sounds
pygame.mixer.music.load("assets/audio/M2.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
katana_fx = pygame.mixer.Sound("assets/audio/swordslash.wav")
katana_fx.set_volume(0.75)
spear_fx = pygame.mixer.Sound("assets/audio/spearswing.wav")
spear_fx.set_volume(0.75)

# Load Background Image
bg_image = pygame.image.load("assets/images/stages/balcony.jpg").convert_alpha()

# Load Spritesheets
martial_warrior_1 = pygame.image.load("assets/images/characters/Martial Hero 1/ZMH1.png").convert_alpha()
martial_warrior_2 = pygame.image.load("assets/images/characters/Martial Hero 2/ZMH2.png").convert_alpha()

# Load Victory Screen
victory_icon = pygame.image.load("assets/images/icons/Victory.png").convert_alpha()

# Define Number of Steps in each Animation
martial_warrior_1_animation_steps = [8, 8, 2, 2, 6, 6, 4, 6]
martial_warrior_2_animation_steps = [8, 8, 2, 2, 5, 5, 3, 8]

# Define Font
count_font = pygame.font.Font("assets/fonts/Demonic.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Demonic.ttf", 30)
name_font = pygame.font.Font("assets/fonts/Demonic.ttf", 30)

# Function for Drawing Text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for Generating Background
def gen_bg():
    scaled_bg = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))
    
# Function for Drawing Fighter Health Bars
def fighter_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, white, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, green, (x, y, 400 * ratio, 30))
    
# Create Two Instances of Fighters
fighter_1 = Fighter(1, 200, 455, False, martial_warrior_1_data, martial_warrior_1, martial_warrior_1_animation_steps, katana_fx)
fighter_2 = Fighter(2, 700, 455, True, martial_warrior_2_data, martial_warrior_2, martial_warrior_2_animation_steps, spear_fx)

# Game Loop
run = True
while run:
    
    clock.tick(fps)
    
    # Generate Background
    gen_bg()
    
    # Show Player Health
    fighter_health_bar(fighter_1.health, 20, 20)
    fighter_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: "+ str(score[0]), score_font, yellow, 357, 60)
    draw_text("Tobunaga: The Sekiro", name_font, yellow, 20, 60)
    draw_text("P2: "+ str(score[1]), score_font, yellow, 580, 60)
    draw_text("Vika: The Tarnished", name_font, yellow, 685, 60)
    
    # Update Countdown
    if intro_count <= 0:
        # Move Fighters
        fighter_1.move(screen_width, screen_height, screen, fighter_2, round_over)
        fighter_2.move(screen_width, screen_height, screen, fighter_1, round_over)
    else:
        # Display Count Timer
        draw_text(str(intro_count), count_font, light_coral, screen_width / 2, screen_height / 3)
        # Update Count Timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
    
    
    
    # Update Fighters
    fighter_1.update()
    fighter_2.update()
    
    # Draw Fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    # Check for Player Defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            
    else:
        # Display Victory Screen
        screen.blit(victory_icon, (255, 150))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 455, False, martial_warrior_1_data, martial_warrior_1, martial_warrior_1_animation_steps, katana_fx)
            fighter_2 = Fighter(2, 700, 455, True, martial_warrior_2_data, martial_warrior_2, martial_warrior_2_animation_steps, spear_fx)

        
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    # Update Display
    pygame.display.update()
            
# Exit Pygame
pygame.quit 