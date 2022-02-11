import pygame
import os
from pygame import mixer

pygame.mixer.init()
pygame.font.init()

mixer.music.load("Assets/background.wav")
mixer.music.play(-1)

HEIGHT, WIDTH = 500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighter")

BOX_SIZE = (40, 40)
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
FPS = 60
VELOCITY = 5
MAX_BULLETS = 6
BULLET_VELOCITY = 7

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# GIFT_BOX_IMAGE = pygame.image.load(os.path.join("Assets", "giftbox.png"))
# print(GIFT_BOX_IMAGE.get_height(), GIFT_BOX_IMAGE.get_width())
# GIFT_BOX = pygame.transform.scale(
#     GIFT_BOX_IMAGE, BOX_SIZE)
# GIFT_BORDER = pygame.Rect(GIFT_BOX.get_width - 5,0,)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270)

BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, COLOR_BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, COLOR_WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, COLOR_WHITE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width()-10, 10))
    WIN.blit(red_health_text, (10, 10))

    # WIN.blit(GIFT_BOX, (WIDTH/2 - 15, 10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255, 0, 0), bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255, 255, 0), bullet)
    pygame.display.update()


def handel_red_spaceship_movement(key_pressed, ship):
    if key_pressed[pygame.K_a] and ship.x - VELOCITY > 0:
        ship.x -= VELOCITY
    if key_pressed[pygame.K_d] and ship.x + VELOCITY + ship.width < BORDER.x:
        ship.x += VELOCITY
    if key_pressed[pygame.K_w] and ship.y - VELOCITY > 0:
        ship.y -= VELOCITY
    if key_pressed[pygame.K_s] and ship.y + ship.height + VELOCITY < HEIGHT:
        ship.y += VELOCITY


def handel_yellow_spaceship_movement(key_pressed, ship):
    if key_pressed[pygame.K_j] and ship.x - VELOCITY > BORDER.x + BORDER.width:
        ship.x -= VELOCITY
    if key_pressed[pygame.K_l] and ship.x + VELOCITY + ship.width < WIDTH:
        ship.x += VELOCITY
    if key_pressed[pygame.K_i] and ship.y + VELOCITY > 10:
        ship.y -= VELOCITY
    if key_pressed[pygame.K_k] and ship.y + VELOCITY + ship.height < HEIGHT:
        ship.y += VELOCITY


def handel_bullets(red_bullet, yellow_bullet, red, yellow):
    for bullet in red_bullet:
        bullet.x += BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullet.remove(bullet)

    for bullet in yellow_bullet:
        bullet.x -= BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x < 0:
            yellow_bullet.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, COLOR_WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    clock = pygame.time.Clock()
    run = True

    red_health = 20
    yellow_health = 20

    red_bullets, yellow_bullets = [], []

    red = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        handel_red_spaceship_movement(key_pressed, red)
        handel_yellow_spaceship_movement(key_pressed, yellow)
        handel_bullets(red_bullets, yellow_bullets, red, yellow)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)
    main()


if __name__ == "__main__":
    main()
