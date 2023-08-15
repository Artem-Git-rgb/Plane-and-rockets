import pygame
import random
import time
from pygame.locals import (  # назначаю клавиши
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('jet.png').convert()
        self.image = pygame.transform.scale(self.image, (38, 14))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.up_image = pygame.transform.rotate(self.image, 20)
        self.down_image = pygame.transform.rotate(self.image, -20)
        self.standard_image = pygame.image.load('jet.png').convert()
        self.standard_image.set_colorkey((255, 255, 255))
        self.vertical = 0

    def atack(self, pressed_keys):
        if pressed_keys[K_SPACE]:
            bullet = Bullet(self.rect)

    def update(self, pressed_keys):  # движение
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.vertical = 1
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.vertical = -1
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
            self.vertical = 0
        match self.vertical:
            case 1:
                self.image = self.up_image
            case -1:
                self.image = self.down_image
            case 0:
                self.image = self.standard_image
            case _:
                self.image = self.standard_image
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.vertical == 1:
            if self.rect.top < -10:
                self.rect.top = -10
        else:
            if self.rect.top < 0:
                self.rect.top = 0

        if self.vertical == -1:
            if self.rect.bottom > SCREEN_HEIGHT - 10:
                self.rect.bottom = SCREEN_HEIGHT - 10
        else:
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('bullet.png').convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = rect
        self.speed = 10

    def update(self):  # исчезновение
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):  # класс врага
    velocity = 1

    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image = pygame.transform.scale(self.image, (38, 14))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        if Enemy.velocity > 3:
            Enemy.velocity = 3
        self.speed = random.randint(3, 6) * Enemy.velocity  # (!!!)

    def update(self):  # исчезновение
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            Enemy.velocity += 0.03  # ускорение спауна врагов (!!!)
            self.kill()


class Cloud(pygame.sprite.Sprite):  # класс облаков
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('cloud.png').convert()
        self.image = pygame.transform.scale(self.image, (170, 120))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(90, 130)

    def update(self):  # исчезновение
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Game(object):
    def __init__(self):
        self.speed_game = 1


pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800  # ширина
SCREEN_HEIGHT = 600  # высота
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 600)  # таймер для спавна врага (!!!)
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1500)  # таймер для спавна облака (!)
ADD_BULLET = pygame.USEREVENT + 2
player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# музыка
pygame.mixer.music.load('Apoxode_-_Electric.mp3')
pygame.mixer.music.set_volume(0.10)
pygame.mixer.music.play(loops=-1)
collision_sound = pygame.mixer.Sound('Collision.ogg')
move_up_sound = pygame.mixer.Sound('Rising_putter.ogg')
move_up_sound.set_volume(0.02)  # звук вверх
move_down_sound = pygame.mixer.Sound('Falling_putter.ogg')
move_down_sound.set_volume(0.02)  # звук вниз
# анимация
arr_images = [pygame.image.load(str(i) + '.png') for i in range(1, 6)]
#  счётчик
timer = pygame.font.Font(None, 36)
t = 1
# цикл игры
running = True
while running:  # цикл игры
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADD_ENEMY:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            all_sprites.add(new_cloud)
            clouds.add(new_cloud)
        elif event.type == ADD_BULLET:
            new_bullet = Bullet()
            all_sprites.add(new_cloud)
            bullets.add(new_bullet)
    pressed_keys = pygame.key.get_pressed()
    clouds.update()  # смотрим, где облако и удаляем, если надо
    player.update(pressed_keys)
    enemies.update()
    bullets.update()
    screen.fill((20, 137, 255))  # цвет экрана rgb
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()  # убираем игрока
        move_down_sound.stop()
        move_up_sound.stop()
        for image in arr_images:
            cord = player.rect.center
            image = pygame.transform.scale(image, (70, 70))
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (cord[0] - 35, cord[1] - 35))  # вызываем анимацию взрыва
            pygame.display.flip()
            time.sleep(0.05)
            pygame.display.flip()
        collision_sound.play()
        time.sleep(0.3)
        running = False
    text = timer.render('время: ' + str(t // 90), True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
    pygame.display.flip()
    t += 1
    clock.tick(90)  # кадры в секунду
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
