import pygame
import random

# Iniializace
pygame.init()

# FPS a hodiny
fps = 60
clock = pygame.time.Clock()

# Obrazovka
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mozkomor")

# Hodnoty hry
player_start_lives = 5
mozkomor_start_speed = 2
mozkomor_acceleration = 0.5
score = 0

player_lives = player_start_lives
mozkomor_speed = mozkomor_start_speed

mozkomor_x = random.choice([-1,1])
mozkomor_y = random.choice([-1,1])

background_image = pygame.image.load("img/hogwarts-castle.jpg")
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0,0)

mozkomor = pygame.image.load("img/mozkomor.png")
mozkomor_rect = mozkomor.get_rect()
mozkomor_rect.center = (width//2,height//2)

# Barvy, fonty, texty
gold = pygame.Color("#938f0c")

harry_font_big = pygame.font.Font("fonts/Harry.ttf", 50)
harry_font_middle = pygame.font.Font("fonts/Harry.ttf", 30)



title_text = harry_font_big.render("HALLOWEEN GAME", True, gold)
title_text_rect = title_text.get_rect()
title_text_rect.center = (500, 40)

game_over_text = harry_font_big.render("KONEC HRY", True, gold)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = harry_font_middle.render("Click to continue...", True, gold)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 40)

# Zvuky a hudba
pygame.mixer.music.load("media/bg-music-hp.wav")
miss_sound = pygame.mixer.Sound("media/miss_click.wav")
miss_sound.set_volume(0.1)
success_sound = pygame.mixer.Sound("media/success_click.wav")
success_sound.set_volume(0.1)


# Hlavní cyklus
lets_continue = True
pygame.mixer.music.play(-1, 0.0)
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]

            # Kolize s mozkomorem
            if mozkomor_rect.collidepoint((click_x, click_y)):
                success_sound.play()
                score +=1
                mozkomor_speed += mozkomor_acceleration

                original_x = mozkomor_x
                original_y = mozkomor_y

                while original_x == mozkomor_x and original_y == mozkomor_y:
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])

            else:
                miss_sound.play()
                player_lives -= 1

    # Pohyb mozkomora
    mozkomor_rect.x += mozkomor_x * mozkomor_speed
    mozkomor_rect.y += mozkomor_y * mozkomor_speed

    # Odraz od stěny
    if mozkomor_rect.left < 0:
        mozkomor_x = 1
    elif mozkomor_rect.right >= width:
        mozkomor_x =-1
    elif mozkomor_rect.top < 0:
        mozkomor_y = 1
    elif mozkomor_rect.bottom >= height:
        mozkomor_y = -1

    # Refresh obrazovky
    pygame.display.update()

    score_text = harry_font_middle.render(f"Skore: {score}", True, gold)
    score_text_rect = score_text.get_rect()
    score_text_rect.topright = (width - 30, 10)

    lives_text = harry_font_middle.render(f"Lives: {player_lives}", True, gold)
    lives_text_rect = score_text.get_rect()
    lives_text_rect.topright = (width - 30, 50)


    screen.blit(background_image, background_image_rect)
    screen.blit(mozkomor, mozkomor_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    screen.blit(title_text, title_text_rect)



    # Zpomalení
    clock.tick(fps)

    # Kontrola Konce hry
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()

        # Pozastavení hry do další klávesy
        pygame.mixer.music.stop()
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = player_start_lives
                    mozkomor_rect.center = (width//2, height//2)
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
                    mozkomor_speed = mozkomor_start_speed
                    pygame.mixer.music.play()
                    pause = False
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

pygame.quit()
