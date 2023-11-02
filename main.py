import pygame
import sys
import random
import math

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
          ball_speed_x *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >=screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >=screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3",False, light_grey)
        screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_number = game_font.render("2",False, light_grey)
        screen.blit(number_number,(screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1",False, light_grey)
        screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('darkblue')
light_grey = (200,200,200)
orange = (255, 165, 0)

ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

#Text variables
player_score = 0 
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf",32)

#Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

#Score Timer
score_time = True

score_limit = 1

game_active = False

while True:
    screen.fill(bg_color)
    start_message = game_font.render("Press SPACE to Start", False, light_grey)
    screen.blit(start_message, (screen_width / 2 - 160, screen_height / 2 - 50))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Start the game when SPACE is pressed
                game_active = True
                break

    if game_active:
        break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_ai()

    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey, player)
    pygame.draw.rect(screen,light_grey, opponent)
    pygame.draw.ellipse(screen,orange, ball)
    pygame.draw.aaline(screen,light_grey, (screen_width/2,0), (screen_width/2,screen_height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}",False,light_grey)
    screen.blit(player_text,(660,470))
   
    opponent_text = game_font.render(f"{opponent_score}",False,light_grey)
    screen.blit(opponent_text,(600,470))

    if player_score >= score_limit:
        winner_text = game_font.render("Player Wins!", False, orange)
        screen.blit(winner_text, (screen_width/2 - 100, screen_height/2 - 50))
        pygame.mixer.Sound("congrats.ogg").play() 
        pygame.display.flip()
        pygame.time.delay(2000)  # Display the winner for 2 seconds
        
        # Play Again option code here
        while True:
            screen.fill(bg_color)
            winner_text = game_font.render("Player Wins!", False, orange)
            screen.blit(winner_text, (screen_width/2 - 100, screen_height/2 - 50))
            play_again_text = game_font.render("Play Again? (Y/N)", False, light_grey)
            screen.blit(play_again_text, (screen_width/2 - 120, screen_height/2 + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # Play again if Y is pressed
                        ball_restart()
                        player_score = 0
                        opponent_score = 0
                        break
                    if event.key == pygame.K_n:  # Quit the game if N is pressed
                        pygame.quit()
                        sys.exit()
        
    elif opponent_score >= score_limit:
        winner_text = game_font.render("Opponent Wins!", False, orange)
        screen.blit(winner_text, (screen_width/2 - 110, screen_height/2 - 50))
        pygame.mixer.Sound("congrats.ogg").play()
        pygame.display.flip()
        pygame.time.delay(2000)  # Display the winner for 2 seconds
        
        # Play Again option code here
        while True:
            screen.fill(bg_color)
            winner_text = game_font.render("Opponent Wins!", False, orange)
            screen.blit(winner_text, (screen_width/2 - 110, screen_height/2 - 50))
            play_again_text = game_font.render("Play Again? (Y/N)", False, light_grey)
            screen.blit(play_again_text, (screen_width/2 - 120, screen_height/2 + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # Play again if Y is pressed
                        ball_restart()
                        player_score = 0
                        opponent_score = 0
                        break
                    if event.key == pygame.K_n:  # Quit the game if N is pressed
                        pygame.quit()
                        sys.exit()

    pygame.display.flip()
    clock.tick(60)





